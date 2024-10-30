import os
import re
import base64 #Para codificar en base64 el client id y client secret y mandarlo para que nos den el token
import json #Para manejar los json
import requests #Para manejar las requests a la API
import urllib
from urllib import parse
import random
import string
import webbrowser
import numpy as np

'''
try:
    get_client()
except FileNotFoundError:
    client_txt()
'''

def client_txt():
    client_id = input("\nIngrese su client ID:\n")
    client_secret = input("\nIngrese su client secret:\n")
    client = json.dumps({'client_id': client_id, 'client_secret': client_secret})
    fo = open("client_info.txt", "w")
    fo.write(client)
    fo.close
    return

def get_client():
    with open("client_info.txt", "r") as file:
        for line in file:
            return line

def get_code():
    with open("code.txt", "r") as file:
        for line in file:
            return line

auth_info = json.loads(get_code())
AUTH_CODE = auth_info['code']
AUTH_STATE = auth_info['state']

client_info = json.loads(get_client())
CLIENT_ID = client_info['client_id']
CLIENT_SECRET = client_info['client_secret']

def auth_url():
    url = "https://accounts.spotify.com/authorize"
    state = ''.join(random.choices(string.ascii_letters,
                                 k=16))
    query = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": "http://127.0.0.1:5000",
        "scope": 'user-read-private user-read-email',
        "state": state
    }
    auth_url = f"{url}?{urllib.parse.urlencode(query)}"
    auth_request = requests.get(auth_url)
    url_respuesta = auth_request.url
    return url_respuesta
#print(auth_url())

def auth_user():
    webbrowser.open(auth_url(), new=1, autoraise=True)
auth_user()

def recibir_token():
    '''Función para solicitar el token de acceso necesario para hacer requests a la API de spotify'''
    cadena_auth = CLIENT_ID + ":" + CLIENT_SECRET
    bytes_auth = cadena_auth.encode("utf-8")
    base64_auth = str(base64.b64encode(bytes_auth), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64_auth,
        "Content_Type": "application/x-www-form-urlencoded"
    }
    body = {"grant_type": "authorization_code",
            "code": AUTH_CODE,
            "redirect_uri": "http://127.0.0.1:5000" }
    result = requests.post(url, headers = headers, data = body)
    json_result = json.loads(result.content)
    json_string = json.dumps(json_result)
    fo = open('info_token.txt','w')
    fo.write(json_string)
    fo.close
    return json_string
#print(recibir_token())

def get_info_token():
    with open('info_token.txt', 'r') as file:
        for line in file:
            return line

#print(get_info_token())
info_token = json.loads(get_info_token())
token = info_token['access_token']
refresh_token = info_token["refresh_token"]
#print(info_token)

def auth_header(token): #Función para recibir el header para futuras requests
    return {"Authorization": "Bearer " + token}

#print(recibir_auth_header(token))

def refresh_token():
    cadena_auth = CLIENT_ID + ":" + CLIENT_SECRET
    bytes_auth = cadena_auth.encode("utf-8")
    base64_auth = str(base64.b64encode(bytes_auth), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content_Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + base64_auth
    }
    body = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    respuesta = requests.post(url, headers = headers, data = body)
    respuesta_json = json.loads(respuesta.content)
    json_string = json.dumps(respuesta_json)
    fo = open('info_token.txt', 'w')
    fo.write(json_string)
    fo.close
    return respuesta_json
#info_token = refresh_token()
#print(info_token)



def recibir_perfil():
    url = "https://api.spotify.com/v1/me"
    perfil_respuesta = requests.get(url, headers = auth_header(token))
    perfil = json.loads(perfil_respuesta.content)
    return perfil
perfil = recibir_perfil()
#print(perfil)
USER_ID = perfil['id']
#print(USER_ID)

def recibir_recomendaciones():
    #Función para solicitar y recibir las recomendaciones, asi como guardarlas en una estructura
    url = 'https://api.spotify.com/v1/recommendations?market=ES&seed_artists=4NHQUGzhtTLFvgF5SZesLK&seed_genres=pop%2C+rock&seed_tracks=0c6xIDDpzE81m2q797ordA'
    recomendaciones_respuesta = requests.get(url, headers = recibir_auth_header(token))
    recomendaciones_json = json.loads(recomendaciones_respuesta.content)
    recomendaciones = recomendaciones_json["tracks"]
    return recomendaciones
#recomendencaciones = recibir_recomendaciones()
#print(recomendencaciones)


def recibir_playlists():
    url = 'https://api.spotify.com/v1/users/' + USER_ID + '/playlists'
    playlists_respuesta = requests.get(url, headers = auth_header(token))
    playlists_json = json.loads(playlists_respuesta.content)
    playlists_items = playlists_json['items']
    return playlists_items
playlists = recibir_playlists()
#print(playlists)
#for line in playlists:
#    print(line)

def get_playlists_ids():
    playlists_ids = []
    for item in range(len(playlists)):
        playlists_ids.append(playlists[item]['id'])
    return playlists_ids
playlists_ids = get_playlists_ids()
#print(playlists_ids)


def get_playlists_tracks_ids():
    playlists_tracks_ids = []
    for id in range(len(playlists_ids)):
        url = 'https://api.spotify.com/v1/playlists/' + playlists_ids[id] + '/tracks'
        result = requests.get(url, headers = auth_header(token))
        result_json = json.loads(result.content)
        items = result_json['items']
        tracks = []
        for item in range(len(items)):
            tracks.append(items[item]['track'])
        for track in range(len(tracks)):
            track_id = tracks[track]['id']
            playlists_tracks_ids.append(track_id)
    return playlists_tracks_ids
playlists_tracks_ids = get_playlists_tracks_ids()
#print(len(playlists_tracks_ids))
#for line in playlists_tracks_ids:
#    print(line)
#print(playlists_tracks_ids)


if len(playlists_tracks_ids) <= 100:
    id_chunks = playlists_tracks_ids

if len(playlists_tracks_ids) > 100 and len(playlists_tracks_ids) < 201:
    id_chunks = np.array_split(playlists_tracks_ids, 2)

if len(playlists_tracks_ids) > 200 and len(playlists_tracks_ids) < 301:
    id_chunks = np.array_split(playlists_tracks_ids, 3)

if len(playlists_tracks_ids) > 300 and len(playlists_tracks_ids) < 401:
    id_chunks = np.array_split(playlists_tracks_ids, 4)

if len(playlists_tracks_ids) > 400 and len(playlists_tracks_ids) < 501:
    id_chunks = np.array_split(playlists_tracks_ids, 5)


def get_features():
    features = []
    url = 'https://api.spotify.com/v1/audio-features'
    for chunk in range(len(id_chunks)):
        feature_url = (f'{url}?ids=' + '%2C'.join(id_chunks[chunk]))
        result = requests.get(feature_url, headers = auth_header(token))
        features_json = json.loads(result.content)
        features.append(features_json)
    return features
for line in get_features():
    print(line)
#print(get_features())

'''
def filtro_features():
    audio_features = []
    features_filtradas = []
    for items in get_features():
        for item in items:
            audio_features.append(item['audio_features'])
    return audio_features
#print(filtro_features())
'''
            #audio_features = item['audio_features']
            #danceability = item.get('audio_features', {}).get('danceability', '')
            #energy = item.get('audio_features', {}).get('energy', '')
            #loudness = item.get('audio_features', {}).get('loudness', '')
            #speechiness = item.get('audio_features', {}).get('speechiness', '')
            #acousticness = item.get('audio_features', {}).get('acousticness', '')
            #liveness = item.get('audio_features', {}).get('acousticness', '')
            #features_filtradas.append({})
    #return
#print(filtro_features())



def filtro_enlaces(recomendaciones):
    enlaces_filtrados = []

    pattern = r"https://open\.spotify\.com/track/[a-zA-Z0-9]+"
    for cancion in recomendaciones:
        nombre = cancion.get('name', 'Nombre no disponible')
        url = cancion.get('external_urls', {}).get('spotify', '')

        if re.search(pattern, url):
            enlaces_filtrados.append({'Nombre': nombre, 'url': url})
    return enlaces_filtrados


#canciones = filtro_enlaces(recomendencaciones)

def dump_enlaces(canciones):
    enlaces_str = json.dumps(canciones, indent = "\n", separators = (",",":"))
    fo = open("enlaces.txt", "w")
    fo.write(enlaces_str)
    fo.close()
    return enlaces_str
#dump_enlaces(canciones)










