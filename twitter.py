from tweepy import Client, API, OAuthHandler
import os
import sys

class TwitterAPI:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.client = Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
        
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = API(auth)

    def get_current_user_id(self):
        r = self.client.get_me()
        return r.data.id 

    def get_user_id(self, usename):
        r = self.client.get_users(usernames=["kr1s1o"], user_auth=True)
        return r.data[0].id

    def get_user_last_tweet_date(self, user_id):
        r = self.client.get_users_tweets(id=user_id, max_results=5, user_auth=True)
        r = self.client.get_tweet(r.meta["newest_id"], tweet_fields=["created_at"], user_auth=True)
        return r.data.created_at
    
    def tweet_photo(self, text, filepath, media_tagged_user_ids=None, alt_text=None):
        r = self.api.simple_upload(filepath)
        media_id = r.media_id
        if alt_text is not None:
            r = self.api.create_media_metadata(media_id, alt_text)
        media_tagged_user_ids = None if media_tagged_user_ids is None else [media_tagged_user_ids]
        r = self.client.create_tweet(media_ids=[media_id], text=text, media_tagged_user_ids=media_tagged_user_ids)
        return r

if __name__ == "__main__":
    consumer_key = os.getenv("TWITTER_API_KEY")
    consumer_secret = os.getenv("TWITTER_API_KEY_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_SECRET")

    if consumer_key is None or consumer_key == "" \
        or consumer_secret is None or consumer_secret == "" \
        or access_token is None or access_token == "" \
        or access_token_secret is None or access_token_secret == "" :
        print("Error Missing Environment Variable TWITTER_API_KEY, TWITTER_API_KEY_SECRET, TWITTER_ACCESS_TOKEN or TWITTER_ACCESS_SECRET")
        exit(1)

    if len(sys.argv) < 2:
        print('You must add to the command the tweet text, you can add an user to tag.\nFor example: python3 twitter.py "My tweet text" friend_tag')
        exit(1)

    twitter = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

    current_id = twitter.get_current_user_id()
    last_tweet_date = twitter.get_user_last_tweet_date(current_id)
    print("last tweet date : {}".format(last_tweet_date))

    # upload  part
    tagged_user = None
    if len(sys.argv) > 2:
        tagged_user = twitter.get_user_id(sys.argv[2])
    if os.path.exists('photo.jpg'):
        twitter.tweet_photo(sys.argv[1], 'photo.jpg', tagged_user)
    else :
        print('File "photo.jpg" does not exits')
        exit(1)