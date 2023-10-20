# Spotify-Genres

# Spotify Playlist Generator

This Python script interacts with the Spotify API to create playlists based on specific genres. It also fetches genre information for artists and associates tracks with appropriate genres.

## Prerequisites

Before you can use this script, you need to:

1. Create a Spotify Developer App to obtain your `client_id` and `client_secret`.
2. Set up the appropriate scope for your Spotify App.
3. Ensure you have the necessary Python libraries installed (e.g., requests, pandas).

## Usage

1. Modify the following variables in the script with your credentials:
   - `client_id` and `client_secret` with your Spotify Developer App credentials.
   - `redirect_uri` with your preferred redirect URI.
   - `scope` with the required scope for your application.

2. Run the script to perform the following tasks:
   - Authorization: Obtain an access token for your Spotify account.
   - Retrieve and process data from your Spotify listening history.
   - Create playlists based on genres.
   - Save data to a CSV file.

3. View the generated playlists on your Spotify account.

## Acknowledgments

- This script is for educational and personal use and may require further modifications for production use.
- Please ensure you have proper permissions and follow Spotify's terms of service when using the Spotify API.

