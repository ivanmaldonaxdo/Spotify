import requests,base64
import datetime

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
            totalTimeExpire = now + datetime.timedelta(seconds=expires_in)
            self.time_expire_tk = totalTimeExpire
            self.tk_expired = totalTimeExpire < now
            self.acces_token = acces_token
            return True
        else:
            # token=data['access_token']
            return False

        def get_all_tracks(self):
            pass
        
        def get_track(self):
            pass
