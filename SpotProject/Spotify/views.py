from typing import Dict
from django.shortcuts import render
import requests,base64
from .Spotify import  Spotify
from urllib.parse import urlencode
import json
# from Query import Q
# Create your views here.
def Home(request):
    client_id,client_secret="7edee5b3e9ab46f2b1ad2c9400fa132d","eb8bf4992eb346d7a5ea6ad3c3118f4c"
    sp=Spotify(client_id,client_secret)
    print(sp.Autorizacion())
    # print(sp.get_creds_b64())
    # print(sp.acces_token)
    limit = 5
    limit = 20 if limit is None else limit
    # canciones = sp.get_all_tracks('licor','track',limit)
    # print(canciones)
    busqueda = request.GET.get('busqueda')
    if busqueda:
        print("Cancion a buscar: {}".format(busqueda)) 
    # context = {'songs':canciones}

    listAlbumes = sp.get_all_albums('Toto','album',limit)
    listAlbumes = sorted(listAlbumes, key = lambda i: (i['album_type'],i['Fecha']))
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