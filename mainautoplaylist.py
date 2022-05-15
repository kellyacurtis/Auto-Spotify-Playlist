import json
import requests
from secrets import spotify_user_id,  discover_weekly_id
from datetime import date
from refresh import Refresh


class savediscoversongs:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.discover_weekly_id = discover_weekly_id
        self.tracks = ""
        self.new_playlist_id = ""

    
    
    #find discovery weekly songs and save to track list
    def find_discover_songs(self):

        print("Finding songs in discover weekly...")
        

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            discover_weekly_id)

        response = requests.get(query,
                    headers={"Content-Type": "application/json",
                    "Authorization": f'Bearer {self.spotify_token}'})

        response_json = response.json()

        print(response)

        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"] + ",")
        self.tracks = self.tracks[:-1]

        self.add_to_playlist()

    
    
    # Create a new playlist
    def create_playlist(self):
        
        print("Trying to create playlist...")
        today = date.today()

        todayFormatted = today.strftime("%m/%d/%Y")

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)

        request_body = json.dumps({
            "name": todayFormatted + " discover weekly", \
                "description": "You thought you missed out on your Discover Weekly, here it is!", "public": True
        })

        response = requests.post(query, data=request_body, headers={
            "Content-Type": "application/json",
            "Authorization": f'Bearer {self.spotify_token}'
        })

        response_json = response.json()
        print(response_json)

        return response_json["id"]

     
     
    #add songs from track to new playlist
    def add_to_playlist(self):
        # add all songs to new playlist
        print("Adding songs...")

        self.new_playlist_id = self.create_playlist()

        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.new_playlist_id, self.tracks
            )

        response = requests.post(query, headers={"Content-Type": "application/json",
            "Authorization": f'Bearer {self.spotify_token}'})

        print(response.json)
        
    #access refresh token so this can be repeated
    def call_refresh(self):
    
        print("Refreshing token...")

        refreshCaller = Refresh()

        self.spotify_token = refreshCaller.refresh()

        self.find_discover_songs()

    

    

a = savediscoversongs()
a.call_refresh()
