from typing import Dict
from django.shortcuts import render
import requests,base64
from .Spotify import  Spotify
from urllib.parse import urlencode
import json
# Create your views here.
def Home(request):
    client_id,client_secret="7edee5b3e9ab46f2b1ad2c9400fa132d","eb8bf4992eb346d7a5ea6ad3c3118f4c"
    sp=Spotify(client_id,client_secret)
    print(sp.Autorizacion())
    # print(sp.get_creds_b64())
    # print(sp.acces_token)
    limit = 4
    limit = 20 if limit is None else limit
    # canciones = sp.get_all_tracks('licor','track',limit)
    # print(canciones)

    # context = {'songs':canciones}
    acces_token = sp.acces_token
    endpoint='https://api.spotify.com/v1/search'
    _data = urlencode({
        'q':'Green Day',
        'type':'album',
        'limit':limit
    })
    _headers = {
    'Authorization' : f'Bearer {acces_token}',
    }
    url = f"{endpoint}?{_data}"
    # print(_data)
    print(url)
    response = requests.get(url, headers = _headers)

    print(response.status_code)
    data = response.json()
    print("llaves {} " .format(data.keys()))
    # print("Que tiene data>albums {}"  .format(data['albums']))
    print("llaves del data>albums {} " .format(data['albums'].keys()))
    albumes = data['albums']['items']
    listAlbumes = []
    i = 0
    for a in albumes:
        # print("Nombre album " .format(a.keys()))
        print(a['name'])
        print(a['id'])
        print(a['release_date'])
        listAlbumes.append(dict(
            {'Id':a['id'],'Nombre':a['name'].replace('\xad', ''),'Fecha': a['release_date'] }
    ))
    # listAlbumes = sorted(listAlbumes, key = lambda i: i['Fecha'])
    # print("Items de data Albums {}" .format(albumes))


        #ELIMINAR DUPLICAS DE DICCIONARIOS EN LISTA
        #list_dupl = [dict(t) for t in {tuple(d.items()) for d in listAlbum}]   
       # print(list_dupl)

        #ORDENAR LISTA DE DICCIONARIOS
        # print(sorted(listaCanciones, key = lambda i: i['Fecha']))
        # print(listAlbum)
        #context = {'songs': sorted(listaCanciones, key = lambda i: i['Track'])}
    # print(response.status_code)
    # print(response.text)

    context = {'Albumes' : listAlbumes}

    return render(request,'Spotify/Home.html',context)