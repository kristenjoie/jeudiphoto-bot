# jeudiphoto-bot

An app to tweet your favorites photos from your Google Photo library.

This app will choose random photo from your favorites photos, then tweet it.

## 🚥 Pre-requisites
### For Google Photo
- Create Oauth Client ID and an API KEY
You must on [Google Cloud Console](https://console.cloud.google.com) create an OAuth 2.0 Client ID and an API_KEY.  
You can follow this tutorial --> https://gilesknap.github.io/gphotos-sync/main/tutorials/oauth2.html#client-id
- Set Environment variable GOOGLE_CLIENT_SECRET and GOOGLE_CLIENT_ID, GOOGLE_API_KEY.

### For Twitter
- Set Environment variable TWITTER_API_KEY, TWITTER_API_KEY_SECRET, TWITTER_ACCESS_TOKEN and TWITTER_ACCESS_SECRET.  
Follow this doc to generate token --> https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api

## 🏗️ Install
Install pip packages:
```
pip3 install -r requirements.txt
```

## 🚀 Run

### For the Main scritp:

The main script will:
- get date of the last tweet of the user.  
--> if the date is the same as today, nothing will be done
- download a random photo from your favorites of your Google Photo library.  
If you use `--exclude_album` it will reduce the favorite list
- tweet the photo with the text you set and tag an user you option `user_tag`

Run command:
```
python3 main.py "Tweet text" [--exclude_album 'private'] [--user_tag nasa] [--photo_path photo.jpg]
```
With arguments:
- `--exclude_album`: name of the album to exclude
- `--user_tag`: name of the user to tag in the tweet
- `--photo_path`: path of the photo. By default "photo.jpg"

---

### For Google Photo part **Only**
```
python3 download_gphoto.py
```

At the first launch, a new browser windows will be displayed on the authentifcation flow to authorize an app to get access to your private data. (if not the link will be displayed in the console).  
- Accept these Google Authorization.
- In the console, the message `Your refresh token is: "..."`, add this to the environment variable GOOGLE_REFRESH_TOKEN

### For Twitter part **Only**
```
python3 twitter.py "My tweet text" <username>
```
This will send a tweet with the photo file `'photo.jpg'` and the text you choose. You can add an username of the twitter user you want to tag to the photo.

## 🔗 Link

Doc [Google Photo API](https://developers.google.com/photos/library/reference/rest)
Doc python package [tweepy](https://docs.tweepy.org/en/stable/index.html)