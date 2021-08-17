from urllib.parse import urlencode
import requests,base64
import datetime
from urllib.parse import urlencode
import json
from requests import api
class Spotify():
    client_id = None
    client_secret = None
    time_expire_tk = datetime.datetime.now()
    tk_expired = True
    token_url = 'https://accounts.spotify.com/api/token'
    acces_token = None

    def __init__(self,client_id,client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id=client_id
        self.client_secret=client_secret

    def get_creds_b64(self):
        creds= f"{self.client_id}:{self.client_secret}"
        creds_b64=base64.b64encode(creds.encode()).decode()
        return creds_b64

    def get_tk_headers(self):
        return {'Authorization':f'Basic {self.get_creds_b64()}'}

    def get_tk_data(self):
        return {'grant_type':'client_credentials'}

    def Autorizacion(self):
        url = self.token_url
        _data = self.get_tk_data()
        _headers = self.get_tk_headers()
        response = requests.post(url,data=_data, headers=_headers)
        if response.status_code in range(200,299):
            now = datetime.datetime.now()
            data = response.json()
            acces_token = data['access_token']
            expires_in = data['expires_in']#segundos
            tiempo_expiracion= now + datetime.timedelta(seconds=expires_in)
            self.time_expire_tk = tiempo_expiracion
            self.tk_expired = tiempo_expiracion < now
            self.acces_token = acces_token
            return True
        else:
            # token=data['access_token']
            return False

    def get_acces_token(self):
        token = self.acces_token
        expires = self.time_expire_tk
        now = datetime.datetime.now()
        if expires < now or token == None:
            self.Autorizacion()
            return self.get_acces_token()
        return token
    def get_url_encode(self,data,endpoint):
        _data = urlencode(data)
        url = f"{endpoint}?{_data}"
        return url

    def get_search_base(self):
        return 'https://api.spotify.com/v1/search'

    def get_search_response(self,_data):
        url = self.get_url_encode(_data,self.get_search_base())
        print(url)
        _headers = {
            'Authorization' : f'Bearer {self.get_acces_token()}',
        }
        response = requests.get(url, headers = _headers)
        return response
    
    def get_all_tracks(self,query,type,_limit):
        _data = {
            'q': query,
            'type': type,
            'limit': _limit
        }
        response = self.get_search_response(_data) 
        print(self.acces_token)
        if response.status_code in range (200,299):
            data = response.json()
            canciones = data['tracks']['items']
            i = 0
            listaCanciones = []
            for c in canciones:
                i += 1
                print("Item {}" .format(i))
                album=c['album']
                print("Año de Publicacion  {}" .format(album['release_date']))
                listaCanciones.append(dict(
                    {'id': c['id'], 
                    'Track': c['name'], 
                    'Album': album['name'].replace('\xad', ''),
                    'Fecha': album['release_date']
                    }
                ))
            return listaCanciones
        else:
            return []
    
    def get_all_albums(self,query,type,_limit):
        _data = {
            'q': query,
            'type': type,
            'limit': _limit
        }
        response = self.get_search_response(_data) 
        if response.status_code in range (200,299):
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
                print(a['album_type'])
                listAlbumes.append(dict(
                    {'Id':a['id'],'Nombre':a['name'].replace('\xad', ''),
                    'Fecha': a['release_date'],'album_type': a['album_type']}
            ))            
            return listAlbumes
        else:
            return []        

    def get_track(self):
        pass
