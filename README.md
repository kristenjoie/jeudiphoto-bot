# jeudiphoto-bot

An app to tweet your favorites photos from your Google Photo library.

This app will choose randomly from your favorites photos minus photos already in the album called 'Twitter'.  
The downloaded photo will be file `'photo.jpg'`.

## 🚥 Pre-requisites
- Create Oauth Client ID and an API KEY
You must on [Google Cloud Console](https://console.cloud.google.com) create an OAuth 2.0 Client ID and an API_KEY.  
You can follow this tutorial --> https://gilesknap.github.io/gphotos-sync/main/tutorials/oauth2.html#client-id
- Set Environment variable GOOGLE_CLIENT_SECRET and GOOGLE_CLIENT_ID, GOOGLE_API_KEY.

## 🏗️ Install
Install pip packages:
```
pip3 install -r requirements.txt
```

## 🚀 Run

```
python3 download_gphoto.py
```

At the first launch, a new browser windows will be displayed on the authentifcation flow to authorize an app to get access to your private data. (if not the link will be displayed in the console).  
- Accept these Google Authorization.
- In the console, the message `Your refresh token is: "..."`, add this to the environment variable GOOGLE_REFRESH_TOKEN

