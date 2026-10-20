from openai import OpenAI
client = OpenAI(api_key="")

response =  client.chat.completions.create(
    model= "gpt-4o",
    messages=[{"role" : "user",
               "content":"What is a API"}],
    temperature= 0
)