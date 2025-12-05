import requests
import uuid
import json

def getrand(keyword: str, plrsunder: int, plrsover: int, excluisons=[]):
    url = 'https://apis.roblox.com/search-api/omni-search'
    session = str(uuid.uuid4())
    token = None

    while True:
        params = {
            "searchQuery": keyword,
            "sessionId": session,
            "pageType": "games",
            "maxRows": 50
        }
        if token:
            params["pageToken"] = token

        res = requests.get(url, params=params).json()

        if "searchResults" in res:
            for group in res["searchResults"]:
                if "contents" in group:
                    for game in group["contents"]:
                        if game.get("playerCount", 0) <= plrsunder and game.get("playerCount", 0) >= plrsover and game.get("rootPlaceId") not in excluisons:
                            imageurljson = requests.get(f"https://thumbnails.roblox.com/v1/games/icons?universeIds={game.get('universeId')}&size=150x150&format=Png&isCircular=false").json()
                            image_url = imageurljson["data"][0]["imageUrl"]

                            detailsjson = requests.get(f'https://games.roblox.com/v1/games?universeIds={game.get("universeId")}&languageCode=en_us').json()['data'][0]

                            return {
                                'placeid': game.get("rootPlaceId"),
                                'universeid': game.get("universeId"),
                                'name': game.get("name"),
                                'description': detailsjson["description"],
                                'plrs': game.get("playerCount", 0),
                                'thumbnail': image_url,
                                'votes': {
                                    'totalUpVotes': game.get("totalUpVotes"),
                                    'totalDownVotes': game.get("totalDownVotes"),
                                    'totalVotes': game.get("totalUpVotes") - game.get("totalDownVotes"),
                                },
                                'url': f"https://www.roblox.com/games/{game.get('rootPlaceId')}",
                                'creator': detailsjson["creator"]["name"],
                                'made': detailsjson["created"].split("T")[0],
                                'updated': detailsjson["updated"].split("T")[0],
                                'visits': detailsjson["visits"],
                                'maxplrs': detailsjson["maxPlayers"],
                                'avatar': detailsjson["universeAvatarType"],
                                'genre': f"{detailsjson['genre_l1']} {detailsjson['genre_l2']}",
                                'favourites': detailsjson["favoritedCount"],
                            }

        token = res.get("nextPageToken")
        if not token:
            return {
                    'placeid': 1,
                    'universeid': 1,
                    'name': 'non',
                    'description': 'non',
                    'plrs': 1,
                    'thumbnail': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbTO_sW0Q8frkEEz9JkqF3MVTswsLUxCIgYw&s',
                    'votes': {
                        'totalUpVotes': 1,
                        'totalDownVotes': 1,
                        'totalVotes': 1,
                    },
                    'url': "https://www.roblox.com/games/nan",
                    'creator': 'non',
                    'made': "9999-99-99",
                    'updated': "9999-99-99",
                    'visits': 1,
                    'maxplrs': 1,
                    'avatar': 'non',
                    'genre': "non",
                    'favourites': 1,
                }
