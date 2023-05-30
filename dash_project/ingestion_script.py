import os
import time
import hashlib

import praw
import pymongo

from dash_project.mongo_conn import get_mongo_conn


REDDIT_SOURCE = praw.Reddit(
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET"),
    username=os.environ.get("REDDIT_USERNAME"),
    password=os.environ.get("REDDIT_PASSWORD"),
    user_agent="sujaysstuff"
)

SUBS = (
    "Bangalore", "Mumbai", "Pune", "Hyderabad", "Chennai", "Ahmedabad"
)

MONGO_CLIENT = get_mongo_conn()
CITIES_DB = MONGO_CLIENT.cities
CITIES_REDDIT_COLLECTION = CITIES_DB.cities_reddit


def get_hash(post_dict: dict) -> str:
    hash_str = str(post_dict["karma"]) + "_" + post_dict[
        "title"] + "_" + post_dict["subreddit"]
    return hashlib.md5(hash_str.encode("utf-8")).hexdigest()


def get_top_hots(sub_reddit: str) -> dict:
    sub = REDDIT_SOURCE.subreddit(sub_reddit)
    hot_sub = sub.hot(limit=1000)

    posts_dict_list = []

    for post in hot_sub:
        post_dict = {}
        post_dict['subreddit'] = sub_reddit
        post_dict['title'] = post.title
        post_dict['text'] = post.selftext
        post_dict['karma'] = post.score
        post_dict['_id'] = get_hash(post_dict)
        posts_dict_list.append(post_dict)

    return posts_dict_list


def insert_to_mongo(posts_list: list, city: str) -> None:
    CITIES_REDDIT_COLLECTION.insert_many(posts_list, ordered=False)
    print(f"""
        Done with inserting {len(posts_list)} documents
        for city {city}
    """)


def main() -> int:
    for city in SUBS:
        posts_list = get_top_hots(city)

        try:
            insert_to_mongo(posts_list, city)
        except pymongo.errors.BulkWriteError:
            time.sleep(2)
    
    return 0


if __name__ == '__main__':
    main()
