import json
import refresh
from secrets import spotify_token, spotify_user_id, discover_weekly_id
from datetime import date



class savediscoverweekly:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.discover_weekly_id = discover_weekly_id
        self.tracks = ""

    def get_discover_songs(self):
        
        print(f'finding songs on discover weekly...')

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(discover_weekly_id)

        response = refresh.get(query,
            headers={"Content-Type": "application/json",
            "Authorization": f'Bearer {spotify_token}'}
        )

        response_json = response.json()

        print(response)

        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"] + ",")
        self.tracks = self.tracks[:-1]

        
        def create_playlist(self):

            print("Trying to create playlist...")
            today = date.today()

            todayformatted = today.strftime("%m%d%y")

            query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)

            request_body = json.dumps({"name": todayformatted + " discover weekly", \
             "description": "Here's your Discovery Weekly you thought you missed out on", "public": True
            })

            response = refresh.post(query, data=request_body, headers={
                "Content-Type": "application/json",
                "Authorization": f'Bearer {spotify_token}'})

            response_json = response.json()
            print(response_json)


a = savediscoverweekly()
a.create_playlist()