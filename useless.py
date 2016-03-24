import rous
import requests
from config import (API_KEY,
                    EVENT_ID,
                    MEETUP)
import time


def bot():
    stored_quotes = [quote.lower() for quote in rous.sayings()]
    comments_endpoint = "https://api.meetup.com/{meetup}/events/{event_id}/comments?key={key}".format(meetup=MEETUP,
                                                                                                      event_id=EVENT_ID,
                                                                                                      key=API_KEY)

    while True:
        response = requests.get(comments_endpoint)
        comments = response.json()

        for comment in comments:
            comment_id = comment["id"]
            comment_text = comment["comment"]
            comment_replies = comment.get("replies")

            if comment_replies:
                continue

            for quote in stored_quotes:
                if comment_text.lower() in quote:
                    requests.post(comments_endpoint, data={"comment": quote,
                                                           "in_reply_to": comment_id,
                                                           "notifications": False})
                    time.sleep(3)
                    break
            else:
                requests.post(comments_endpoint, data={"comment": "sorry...",
                                                       "in_reply_to": comment_id,
                                                       "notifications": False})

        print("Waiting for another comment...")
        time.sleep(15)


