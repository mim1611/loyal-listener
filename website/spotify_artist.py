from requests import post, get
import json


def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist"
    
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        return None

    return sorted(json_result, key=lambda x: x["popularity"], reverse=True)

def artist_name(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    name = json.loads(result.content)["name"]
    return name

def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?limit=50&include_groups=album,single"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return sorted(json_result, key=lambda x: x["release_date"])

def get_songs_from_album(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result

def create_playlist(token, user_id, playlist_name):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = json.dumps({
        "name": f"{playlist_name} enthusiast",
        "description": f"{playlist_name} playlist made by Loyal Listener",
    })
    result = post(url, data=data, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def populate_playlist(token, playlist_id, uri_list):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token)
    batch = []
    while uri_list:
        if len(batch) == 100:
            data = json.dumps({
                "uris": batch
            })
            post(url, data=data, headers=headers)
            batch = []
        batch.append(uri_list[0])
        uri_list.pop(0)
    if batch:
        data = json.dumps({
            "uris": batch
        })
        post(url, data=data, headers=headers)
    return 