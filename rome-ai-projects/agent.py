import os
import json
import urllib.request
from openai import OpenAI

# 1. Initialize our free OpenRouter client
# We tell OpenRouter which app is calling (required for ranking/identification)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

# We will use openrouter/free which dynamically routes to the best free model
MODEL_NAME = "openrouter/free"

# 2. Define our Tavily Search Tool (Traditional programmatic request)
def tavily_search(query: str) -> str:
    """Run a free search query using Tavily API."""
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return "Error: Tavily API Key is missing."
    
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    data = json.dumps({
        "api_key": api_key,
        "query": query,
        "search_depth": "basic"  # Keeps it at 1 credit per search!
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            # Pull only snippet summaries to keep context window tiny (saves memory/tokens)
            results = [f"Source: {r['url']}\nSnippet: {r['content']}\n" for r in res_data.get("results", [])]
            return "\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Failed to perform search: {str(e)}"

# 3. Define tool schemas so the LLM understands what it has access to
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "tavily_search",
            "description": "Searches the web for up-to-date information, news, and facts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to lookup on the web."
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# 4. Core Agent Orchestration Loop (Perceive -> Reason -> Act)
messages = [
    {
        "role": "system", 
        "content": "You are a smart AI agent. Use the 'tavily_search' tool whenever you need real-time info or facts you do not know."
    }
]

print("--- Free-Tier Agent Active (Type 'exit' to quit) ---")

while True:
    user_prompt = input("\nYou: ")
    if user_prompt.lower() == "exit":
        break
        
    messages.append({"role": "user", "content": user_prompt})
    
    # Send request to OpenRouter
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=tools_schema,
        tool_choice="auto"
    )
    
    response_message = response.choices[0].message
    
    # Check if the model wants to call a tool (Act Phase)
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            if tool_call.function.name == "tavily_search":
                arguments = json.loads(tool_call.function.arguments)
                print(f"\n[Agent decided to search for: '{arguments['query']}']")
                
                # Run the search
                search_result = tavily_search(arguments["query"])
                
                # Append tool call and result to message stream
                messages.append(response_message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": "tavily_search",
                    "content": search_result
                })
                
                # Let the model process the tool data and speak to you
                second_response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages
                )
                final_reply = second_response.choices[0].message.content
                print(f"\nAgent: {final_reply}")
                messages.append({"role": "assistant", "content": final_reply})
    else:
        # If no tools were needed
        reply = response_message.content
        print(f"\nAgent: {reply}")
        messages.append({"role": "assistant", "content": reply})