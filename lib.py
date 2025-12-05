import requests
import uuid
import json

def getrand(keyword, plrsunder, excluisons=[]):
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
                        if game.get("playerCount", 0) <= plrsunder and game.get("rootPlaceId") not in excluisons:
                            imageurljson = requests.get(f"https://thumbnails.roblox.com/v1/games/icons?universeIds={game.get('universeId')}&size=150x150&format=Png&isCircular=false").json()
                            image_url = imageurljson["data"][0]["imageUrl"]
                            return {
                                'placeid': game.get("rootPlaceId"),
                                'universeid': game.get("universeId"),
                                'name': game.get("name"),
                                'description': game.get("description"),
                                'plrs': game.get("playerCount", 0),
                                'thumbnail': image_url,
                                'votes': {
                                    'totalUpVotes': game.get("totalUpVotes"),
                                    'totalDownVotes': game.get("totalDownVotes"),
                                    'totalVotes': game.get("totalUpVotes") - game.get("totalDownVotes"),
                                }
                            }

        token = res.get("nextPageToken")
        if not token:
            return None

if __name__ == "__main__":
    res = getrand('\\n', 5, excluisons=json.loads(open('exclude.json', 'r').read()))

    exclusions = json.load(open('exclude.json', 'r'))

    with open('exclude.json', 'w') as outfile:
        exclusions.append(res['placeid'])
        json.dump(exclusions, outfile, indent=4)