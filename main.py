from fastapi import FastAPI
from starlette.responses import RedirectResponse
from facebook_scraper import get_posts
from mongo_serv import *

app = FastAPI()


@app.get("/",include_in_schema=False)
async def redirect_to_swagger():
    return RedirectResponse(url='/docs')


@app.get("/scrap/{page_name}",summary="Scraps posts from facebook by page name")
async def scrap_posts(page_name):
    posts = []
    try:
        posts = list(get_posts(page_name, pages=1))
        posts = [delete_none(post) for post in posts]
        insert_posts(posts)
    except:
        pass
    return posts



@app.get("/read",summary="find all stored posts in database")
async def find_all():
    response = dict()
    posts = find_posts()
    response["total"] = len(posts)
    response["posts"] = posts
    return response


@app.get("/read/{page_name}",summary="find stored posts by page name in database")
async def find_by_name(page_name):
    response = dict()
    posts = find_posts(page_name)
    response["total"] = len(posts)
    response["posts"] = posts
    return response


def delete_none(d):
    new_dict = dict()
    for k, v in d.items():
        if v:
            new_dict[k] = v
    new_dict["_id"] = new_dict["post_id"]
    return new_dict