import rous
import requests
from config import (API_KEY,
                    EVENT_ID,
                    MEETUP)
import time


def plagiarize():
    reviewed_comments = set([])
    stored_quotes = [quote.lower() for quote in rous.sayings()]

    while True:
        response = requests.get("https://api.meetup.com/{meetup}/events/{event_id}/comments?key={key}"
                                .format(meetup=MEETUP, event_id=EVENT_ID, key=API_KEY))
        comments = response.json()

        for comment in comments:
            comment_id = comment["id"]
            comment_text = comment["comment"]
            comment_likes = comment["like_count"]
            comment_author = comment['member']['name']

            if comment_id in reviewed_comments:
                continue

            if comment_likes:
                for quote in stored_quotes:
                    if comment_text.lower() in quote.lower():
                        print("{quote}\n- {attributed}"
                              .format(quote=quote, attributed=comment_author))
                        reviewed_comments.add(comment_id)
                        time.sleep(3)
                        break
                else:
                    print("No relevant quote found!")

        print("Waiting for another comment...")
        time.sleep(15)


