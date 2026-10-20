from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI() #Creates the FastAPI application instance

templates = Jinja2Templates(directory="templates")#Sets up Jinja2 templates from a templates folder (where home.html should live)

#mock data-A list of dictionaries representing blog posts
posts: list[dict]=[
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "Fastapi is Awsome",
        "content": "This fr4amework is really easy to use and super fast",
        "date_posted":"April 20, 2026",
    },
    {
        "id": 2,
        "author":"Jane doe",
        "title":"pyton is good",
        "content":"python is a good programming language beginner frirndly",
        "date_posted":"April 29, 2026",
    },
]
@app.get("/", include_in_schema=False)
@app.get("/posts", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "posts": posts, "title":"Home"})
    #return templates.TemplateResponse(request, "home.html")
    #templates.TemplateResponse renders the HTML template
@app.get("/api/posts")
def get_posts():# returns the posts data as json at /api/docs
    return posts
    #this is a rest api endpoint 