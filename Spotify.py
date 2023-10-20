import requests
import json
import random
import string
from urllib.parse import urlencode
import base64
import webbrowser

# Your Spotify API credentials
client_id = 'your client id'
client_secret = 'your client secret'

scope = "playlist-modify-private"
redirect_uri = 'http://localhost:3000'
scope = 'playlist-modify-private'

data = {
    'client_id': client_id,
    'response_type': 'code',
    'redirect_uri': redirect_uri,
    'scope': scope
}

webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(data))

# Code retrieval and authorization

# In[43]:
code = 'your code'

# In[44]:
auth_url = 'https://accounts.spotify.com/api/token'

data = {
    'grant_type': 'authorization_code',
    'client_id': client_id,
    'client_secret': client_secret,
    'code': code,
    'scope': scope,
    'redirect_uri': 'http://localhost:3000',
    'content-type': 'application/x-www-form-urlencoded',
}

auth_response = requests.post(url=auth_url, data=data)
access_token = auth_response.json().get('access_token')
print(auth_response.json())

# Functions for genre searching

# In[34]:

import requests
from requests import get


def search_for_genres(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    query = f"q={artist_name}&type=artist&limit=1"

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = result.json()
    artists = json_result.get("artists", {}).get("items", [])
    for artist in artists:
        genres = artist.get("genres", [])
        print("Genres:", ", ".join(genres)


search_for_genres(access_token, "ACDC")

# Process data and create playlists

# In[37]:
import json
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import pandas as pd
import os

folder_path = os.path.join(os.path.expanduser('~'), 'your folder')
json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]

all_data = pd.DataFrame()

for json_file in json_files:
    with open(os.path.join(folder_path, json_file), 'r') as file:
        data = json.load(file)
        temporary = pd.DataFrame(data)
        all_data = pd.concat([all_data, temporary], ignore_index=True)

all_data.drop(['username', 'platform', 'user_agent_decrypted', 'episode_name', 'episode_show_name', 'spotify_episode_uri', 'shuffle', 'offline', 'offline_timestamp', 'incognito_mode'], axis=1, inplace=True)
print("Shape of the DataFrame:", all_data.shape)
n = 20
test_data = all_data.head(n)

songs = {}

for index, row in all_data.iterrows():
    song = row['master_metadata_track_name']
    artist = row['master_metadata_album_artist_name']
    uri = row['spotify_track_uri']

    if song and artist:
        if (song, artist) not in songs.items():
            songs[song] = {'artist': artist, "uri": uri}

print(songs)
print('hi')

keyList = ["pop", "rap", "rock", "classical", "country", "soul", "techno", "italian", "soundtrack", "alternative", "latin", "french"]

the_genres = {key: [] for key in keyList}
artists_processed = set()


def genre_contains_keyword(genre, keyword):
    return keyword.lower() in genre.lower()


def search_for_genres(token, artist_name, uri):
    print(f"Searching for genres for {artist_name}")
    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    query = f"q={artist_name}&type=artist&limit=1"

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = result.json()
    print(json_result)
    artists = json_result.get("artists", {}).get("items", [])
    for artist in artists:
        if artist_name not in artists_processed:
            genres = artist.get("genres", [])
            if genres:
                for genre in genres:
                    for keyword in keyList:
                        if genre_contains_keyword(genre, keyword):
                            if uri not in the_genres[keyword]:
                                print("always entered loop 1")
                                the_genres[keyword].append(uri)
                                print(f"Added genre: {genre} for {artist_name}")
                            break

    # ...


for song, details in songs.items():
    artist = details['artist']
    uri = details['uri']
    search_for_genres(access_token, artist, uri)

print("here they are")
print(the_genres)

# Create playlists for genres

# In[47]:
for genre, uris in the_genres.items():
    user_id = "your user id"

    # Create a playlist for the genre
    endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    request_body = json.dumps({
        "name": genre,
        "description": genre + " playlist",
        "public": False
    })

    response = requests.post(url=endpoint_url, data=request_body, headers={
        "Content-Type": "application/json", "Authorization": f"Bearer {access_token}"})
    playlist_id = response.json()['id']
    print(f"Created playlist: {genre} - ID: {playlist_id}")

    value_list = the_genres[genre]
    numberuris = len(value_list)

    chunk_size = 99
    for i in range(0, numberuris, chunk_size):
        chunk_uris = value_list[i:i + chunk_size]

        # Add the list of track URIs to the playlist
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        request_body = json.dumps({
            "uris": chunk_uris  # Pass the list of track URIs here
        })

        response = requests.post(url=url, data=request_body, headers={
            "Content-Type": "application/json", "Authorization": f"Bearer {access_token}"})

    if response.status_code == 200:
        try:
            response_data = response.json()
            print(f"Added songs to playlist: {genre} - Response: {response_data}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Save data to a CSV file

# In[50]:
data = []

# Iterate through the_genres and create a list of dictionaries
for genre, uris in the_genres.items():
    for uri in uris:
        data.append({'genre': genre, 'uri': uri})

# Create a DataFrame from the list of dictionaries
dataframe = pd.DataFrame(data)
dataframe.to_csv('the_genres.csv', index=False)
