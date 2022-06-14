import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import AuthorizedSession
import os
import random

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

class GoogleAPI:
    def __init__(self, refresh_token, client_id, client_secret, api_key):
        credentials = google.oauth2.credentials.Credentials(None,
                                                            refresh_token=refresh_token,
                                                            token_uri="https://oauth2.googleapis.com/token",
                                                            client_id=client_id,
                                                            client_secret=client_secret)
        self.authed_session = AuthorizedSession(credentials)
        self.api_key = api_key

    def _request(self, method, url, data=None):
        url = "{}&key={}".format(url, self.api_key)
        if method == 'GET':
            return self.authed_session.get(url)
        elif method == 'POST':
            return self.authed_session.post(url, str(data))
        else:
            pass
    
    def get_albums(self, pageToken = None):
        url = 'https://photoslibrary.googleapis.com/v1/albums?pageSize=50'
        if pageToken is not None:
            url = 'https://photoslibrary.googleapis.com/v1/albums?pageSize=50&pageToken={}'.format(pageToken)
        return self._request('GET', url)
    
    def find_album_by_title(self, title):
        list_albums = self.get_all_items(self.get_albums)
        for i in list_albums:
            if i['title'] == title:
                return i
        return None

    def get_album_photos_by_id(self, albumId = "", pageToken = None):
        data= {"albumId": albumId}
        if pageToken is not None:
            data["pageToken"] = pageToken
        url = 'https://photoslibrary.googleapis.com/v1/mediaItems:search?pageSize=100'
        return self._request('POST', url, data)

    def get_favorites(self, pageToken=None):
        data= {"filters":{"featureFilter":{"includedFeatures":["FAVORITES"]}}}
        if pageToken is not None:
            data["pageToken"] = pageToken
        url = 'https://photoslibrary.googleapis.com/v1/mediaItems:search?pageSize=100'
        return self._request('POST', url, data)
    
    def get_all_items(self, ftn, **kwargs):
        list = []
        nextPageToken = None
        while True:
            kwargs["pageToken"] = nextPageToken
            response = ftn(**kwargs).json()
            key = "mediaItems" if "mediaItems" in response else "albums" 
            for item in response[key]:
                list.append(item)
            if 'nextPageToken' in response :
                nextPageToken = response["nextPageToken"]
            else:
                break
        return list
    
    def download_photo(self, path, photoItem):
        url = photoItem["baseUrl"] + '=d'
        r = self.authed_session.get(url) # not using _request() because we must not add API_KEY 
        with open(path, 'wb') as f:
            f.write(r.content)
            f.close()
        return path

if __name__ == '__main__':
    GOOGLE_REFRESH_TOKEN = os.getenv('GOOGLE_REFRESH_TOKEN')
    GOOGLE_CLIENT_ID =  os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

    if GOOGLE_CLIENT_SECRET is None or GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET == "" or GOOGLE_CLIENT_ID == "":
        print("Create Oauth Client ID --> https://gilesknap.github.io/gphotos-sync/main/tutorials/oauth2.html#client-id\nAnd  set the environment variable CLIENT_SECRET & CLIENT_ID")
        exit(1)

    if GOOGLE_REFRESH_TOKEN is None or GOOGLE_REFRESH_TOKEN == "":
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        cred = flow.run_local_server()
        print("----\nYour refresh token is: \"{}\"\nAnd set the environment variable REFFREH_TOKEN\n----".format(cred.refresh_token))
        exit(1)

    if GOOGLE_API_KEY is None or GOOGLE_API_KEY == "":
        print("Set the environment variable API_KEY")
        exit(1)

    googleapi = GoogleAPI(GOOGLE_REFRESH_TOKEN, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_API_KEY)
    
    # get all favorites photos
    favorties_list = googleapi.get_all_items(googleapi.get_favorites)

    # get random photo and download it
    photo_to_download = random.choice(favorties_list)

    googleapi.download_photo("photo.jpg", photo_to_download)

