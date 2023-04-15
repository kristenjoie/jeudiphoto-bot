import sys
import os
import argparse
import time
import random

from download_gphoto import GoogleAPI
from twitter import TwitterAPI


# args parse
parser = argparse.ArgumentParser()
parser.add_argument("tweet_text", type=str,
                    help="Text to tweet"),
parser.add_argument("--check_date", action='store_true'),
parser.add_argument("--exclude_album", type=str,
                    help="Name of the albums to exclude photo seletion")
parser.add_argument("--user_tag", type=str,
                    help="the user tag in the tweet. For example: nasa to tag @nasa")
parser.add_argument("--photo_path", type=str, default="photo.jpg",
                    help="Path to the photo file")
args = parser.parse_args()


GOOGLE_REFRESH_TOKEN = os.getenv('GOOGLE_REFRESH_TOKEN')
GOOGLE_CLIENT_ID =  os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = os.getenv("TWITTER_API_KEY_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

if GOOGLE_REFRESH_TOKEN is None or GOOGLE_REFRESH_TOKEN == "" \
        or GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_ID == "" \
        or GOOGLE_CLIENT_SECRET is None or GOOGLE_CLIENT_SECRET == "" \
        or GOOGLE_API_KEY is None or GOOGLE_API_KEY == "" \
        or TWITTER_API_KEY is None or TWITTER_API_KEY == "" \
        or TWITTER_API_KEY_SECRET is None or TWITTER_API_KEY_SECRET == "" \
        or TWITTER_ACCESS_TOKEN is None or TWITTER_ACCESS_TOKEN == "" \
        or TWITTER_ACCESS_SECRET is None or TWITTER_ACCESS_SECRET == "" :
    print("Error missing Environment Variable, please check it!")
    exit(1)


# authenticate to Twitter and Google
twitter = TwitterAPI(TWITTER_API_KEY, TWITTER_API_KEY_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
googleapi = GoogleAPI(GOOGLE_REFRESH_TOKEN, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_API_KEY)

# get list photo
print("Getting List Photo...")
favorties_list = googleapi.get_all_items(googleapi.get_favorites)
if args.exclude_album:
    print("Getting Excluded List Photo...")
    base_album_id = googleapi.find_album_by_title(args.exclude_album)["id"]
    base_list = googleapi.get_all_items(googleapi.get_album_photos_by_id, albumId = base_album_id)
    # exclued photo
    list_to_use = favorties_list.copy()
    for x in base_list :
        for y in favorties_list :
            if x["id"] == y["id"]:
                list_to_use.remove(y)
                break
else:
    list_to_use = favorties_list

if list_to_use == []:
    print('Not anymore photo to share')
    exit()
photo_to_download = random.choice(list_to_use)

# download random photo
print("Downloading Photo...")
googleapi.download_photo(args.photo_path, photo_to_download)

# upload  part
tagged_user = None
if args.user_tag:
    print("Getting User Tag...")
    tagged_user = twitter.get_user_id(args.user_tag)
if os.path.exists(args.photo_path):
    print("Tweeting Photo...")
    twitter.tweet_photo(args.tweet_text, args.photo_path, tagged_user, alt_text="{}".format(photo_to_download["filename"]))
else :
    print("File '{}' does not exits".format(args.photo_path))
    exit(1)
