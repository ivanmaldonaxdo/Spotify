from typing import Dict
from django.shortcuts import render
import requests,base64
from .Spotify import  Spotify
from urllib.parse import urlencode
# Create your views here.
def Home(request):
    client_id,client_secret="7edee5b3e9ab46f2b1ad2c9400fa132d","eb8bf4992eb346d7a5ea6ad3c3118f4c"
    # key u value de client_id y secret_id
    # creds = f"{client_id}:{client_secret}"
    # creds_b64=base64.b64encode(creds.encode()).decode()
    # # print(type(creds_b64),"-credenciales {} " .format(creds_b64),)

    # # print(type(creds),"-credenciales {} " .format(creds),)
    # url='https://accounts.spotify.com/api/token'
    # _data = {
    #     'grant_type':'client_credentials',
    # }
    # _headers = {
    #     'Authorization':f'Basic {creds_b64}',
    # }
    # response = requests.post(url,data=_data, headers=_headers)
    # print(response.json())
    # data=response.json()
    # token=data['access_token']
    # print(token)
    sp=Spotify(client_id,client_secret)
    
    print(sp.Autorizacion())

    print(sp.get_creds_b64())
    print(sp.acces_token)

    acces_token=sp.acces_token
    endpoint='https://api.spotify.com/v1/search'
    _data = urlencode({
        'q':'Eminem',
        'type':'track,album',
        'limit':'20'
    })
    _headers = {
     'Authorization' : f'Bearer {acces_token}',
    }
    url = f"{endpoint}?{_data}"
    # print(_data)
    print(url)

    response = requests.get(url, headers = _headers)
    if response.status_code in range (200,299):
        data = response.json()
        tracks = data['tracks']
        canciones = tracks['items']
        # total = len(canciones)
        i = 0
        # while i<total:
        print(tracks)
        listaCanciones = []
        for c in canciones:
            i += 1
            print("---------------------") 
            print("Item {}" .format(i))
            print("Cancion {}" .format(c['name']))
            print(c['id'])
            print(" Album  {}" .format(c['album']['name']))
            
            listaCanciones.append(dict(
                {'id': c['id'], 
                'Track': c['name'], 
                'Album': c['album']['name']
                }
            ))
            # listaCanciones.append(c['id'])
        print(listaCanciones)
        context = {'songs': listaCanciones}
        for l in listaCanciones:
            print(l['id'])
    # print(response.status_code)
    # print(response.text)
    return render(request,'Spotify/Home.html',context)