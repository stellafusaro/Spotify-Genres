#!/usr/bin/env python
# coding: utf-8

# In[42]:


import requests
import json
import random
import string
from urllib.parse import urlencode
import base64
import webbrowser
client_id = '8f739181617c4055be70e61f0975752e'
client_secret = '0137655ca07e4b189bd956705ef37ec4'



scope = "playlist-modify-private"


request_url = "https://accounts.spotify.com/authorize?"
redirect_uri = 'http://localhost:3000';
scope = 'playlist-modify-private';

data = {
    'client_id' : client_id,
    'response_type': 'code',
    'redirect_uri': redirect_uri,
    'scope': scope
}

webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(data))

#print(user_response)


# In[43]:


code = 'AQAABxD54guA25khFRWNytOLurgndsYAPS1aMx6E2c8oMYMm0JLgd1SgkF06d9a4EtGAXTN_mAc4qZZbgS8katuVfvbPhxOPhN_638ExENYCXiZ4VFsQGF1T-qCKAKUNp4ni3pFFlL0tCkLbo8SzN2_3dnCgWcIOxWDueosUrcduv7WoOHMEjYm6kWyvjyhWdyM'


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

auth_response = requests.post(url = auth_url, data=data)
access_token = auth_response.json().get('access_token')
print(auth_response.json())


# In[4]:


user_id = "vasearcy"
endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
request_body = json.dumps({
          "name": "Top Tree",
          "description": "Top three songs by each artist listened to.",
          "public": False # let's keep it between us - for now
        })
response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json", 
                        "Authorization": f"Bearer {access_token}"})
playlist_id = response.json()['id']
print(response.json())


# In[34]:


import requests

# Replace with your Spotify artist ID and access token
artist_id = "15kQGEy89K8deJcZVFEn0N"
#access_token = "BQBZ9TJRa84D2QI2gBnAD0glcL1qSm343ZWwEbJ8TD6iPz_KHQFJKKb5VRsBl7mG2VNJE1UqAB1K-pMRfaiWzEag5BZ9SoBjxtZ54GVKgqUSGy70s9gSS68pRUhCZ9kfQbGd863o9Zd9izj9RrfWC7OsAG-Xiy7QKJvAAC-TKm_3-IJdKybO5MjU03yz-ASP9lRIWrb9UEEHwYw"

# Define the endpoint URL for the Spotify API
endpoint_url = f"https://api.spotify.com/v1/artists/{artist_id}"

# Set up headers with the authorization token
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Make a GET request to retrieve artist information
response = requests.get(url=endpoint_url, headers=headers)

# Check if the request was successful (status code 200)
#if response.status_code == 200:
artist_info = response.json()
    
    # Print the artist information
print("Artist Name:", artist_info['name'])
print("Followers:", artist_info['followers']['total'])
print("Genres:", ", ".join(artist_info['genres']))
print("Popularity:", artist_info['popularity'])
    # Add more fields as needed
#else:
   # print("Error:", response.status_code)


# In[35]:


import requests
from requests import get



def search_for_genres(token,artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = {
    "Authorization": f"Bearer {token}"
    }
    query = f"q={artist_name}&type=artist&limit=1"
    
    query_url = url + "?" + query
    result = get(query_url,headers=headers)
    json_result = result.json()
    artists = json_result.get("artists", {}).get("items", [])
    for artist in artists:
        genres = artist.get("genres", [])
        print("Genres:", ", ".join(genres))
    
search_for_generes(access_token, "ACDC")


# In[36]:


"https://api.spotify.com/v1/me/top/tracks?limit=10&offset=0"


# In[37]:


import json
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import pandas as pd
import os

folder_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'Computer Science and Math', 'Spotify Project','MyData')
#folder_path = '/home/Stella Fusaro/Documents/path/to/Computer Science and Math/Spotify Project/MyData'

json_files =[f for f in os.listdir(folder_path)if f.endswith('.json')]

all_data = pd.DataFrame()

for json_file in json_files:
    with open(os.path.join(folder_path,json_file), 'r')as file:
        data = json.load(file)
        temporary = pd.DataFrame(data)
        all_data = pd.concat([all_data, temporary],ignore_index = True)

all_data.drop(['username','platform','user_agent_decrypted','episode_name','episode_show_name','spotify_episode_uri','shuffle','offline','offline_timestamp','incognito_mode'],axis=1,inplace = True)
#print(all_data)

print("Shape of the DataFrame:", all_data.shape)
n = 20
test_data = all_data.head(n)

songs = {}

for index,row in all_data.iterrows():
    song = row['master_metadata_track_name']
    artist = row['master_metadata_album_artist_name']
    uri = row['spotify_track_uri']
    
    if song and artist:
        if(song,artist) not in songs.items():
            songs[song] = {'artist': artist, "uri": uri}
        
print(songs)
print('hi')

keyList = ["pop", "rap", "rock", "classical","country", "soul", "techno", "italian", "soundtrack", "alternative", "latin", "french"]

the_genres = {key: [] for key in keyList}
artists_processed = set()

def genre_contains_keyword(genre, keyword):
    return keyword.lower() in genre.lower()

def search_for_genres(token, artist_name,uri):
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
    search_for_genres(access_token, artist,uri)


print("here they are")
print(the_genres)


# In[47]:


for genre, uris in the_genres.items(): 
    user_id = "vasearcy"
    
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
    
   #chunk_uris = value_list[-numberuris%chunk_size:]

    # Add the list of track URIs to the playlist
   # url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    #request_body = json.dumps({
      #  "uris": chunk_uris  # Pass the list of track URIs here
   # })

    #response = requests.post(url=url, data=request_body, headers={
                 #        "Content-Type": "application/json", "Authorization": f"Bearer {access_token}"})
                         
    if response.status_code == 200:
        try:
            response_data = response.json()
            print(f"Added songs to playlist: {genre} - Response: {response_data}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
    else:
        print(f"Error: {response.status_code} - {response.text}")


# In[11]:





# In[36]:


import json
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import pandas as pd
import os

folder_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'Computer Science and Math', 'Spotify Project','MyData')
#folder_path = '/home/Stella Fusaro/Documents/path/to/Computer Science and Math/Spotify Project/MyData'

json_files =[f for f in os.listdir(folder_path)if f.endswith('.json')]

all_data = pd.DataFrame()

for json_file in json_files:
    with open(os.path.join(folder_path,json_file), 'r')as file:
        data = json.load(file)
        temporary = pd.DataFrame(data)
        all_data = pd.concat([all_data, temporary],ignore_index = True)

all_data.drop(['username','platform','user_agent_decrypted','episode_name','episode_show_name','spotify_episode_uri','shuffle','offline','offline_timestamp','incognito_mode'],axis=1,inplace = True)
#print(all_data)

print("Shape of the DataFrame:", all_data.shape)
n = 20
test_data = all_data.head(n)

songs = {}

for index,row in test_data.iterrows():
    song = row['master_metadata_track_name']
    artist = row['master_metadata_album_artist_name']
    uri = row['spotify_track_uri']
    ts = [ts]
    
    if song and artist:
        if(song,artist) not in songs.items():
            songs[song] = {'artist': artist, "uri": uri, "ts": ts}
        
print(songs)
print('hi')

the_genres = {}
artists_processed = set()

def search_for_genres(token, artist_name,ts):
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
                    if genre in the_genres:
                        print("always entered loop 1")
                        the_genres[genre].append(ts)
                    else:
                        print("entered loop 2")
                        the_genres[genre] = [ts]
                    
    # ...

for song, details in songs.items():
    artist = details['artist']
    ts = details['ts']
    search_for_genres(access_token, artist,ts)


print("here they are")
print(the_genres)

data_frame = pd.DataFrame(data)
print (data_frame)

data_frame['ts'] = pd.to_datetime(df['ts'])

df.set_index('ts', inplace = true)


genre_counts = df.groupby('genre').resample('1H').count()['ts'].unstack().fillna(0)
# Plot a stacked bar chart
genre_counts.plot(kind='bar', stacked=True, figsize=(12, 6))

# Customize the plot
plt.title('Music Genre Distribution Over Time (1-hour intervals)')
plt.xlabel('Time (1-hour intervals)')
plt.ylabel('Number of Songs')
plt.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)

# Show the plot
plt.tight_layout()
plt.show()




# In[50]:


data = []

# Iterate through the_genres and create a list of dictionaries
for genre, uris in the_genres.items():
    for uri in uris:
        data.append({'genre': genre, 'uri': uri})

# Create a DataFrame from the list of dictionaries
dataframe = pd.DataFrame(data)
dataframe.to_csv('the_genres.csv', index=False)


# In[ ]:



