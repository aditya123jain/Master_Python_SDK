import requests
import base64

'''DIRECT FUNCTION AVAILABLE ON  https://codeshare.io/dwZx0B'''

class decoder():
    def __init__(self,mastertrust_app_id, mastertrust_secret_key):
           self.mastertrust_app_id = mastertrust_app_id,
           self.mastertrust_secret_key = mastertrust_secret_key,
           self.code  = None,
           self.access_token = None



    def decode(self,code):

            usrPass = f"{self.mastertrust_app_id}:{self.mastertrust_secret_key}"
            b64Val = base64.b64encode(usrPass.encode()).decode()

            MASTERTRUST_ACCESS_TOKEN_URL = 'https://masterswift-beta.mastertrust.co.in/oauth2/token'

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                "Authorization": f"Basic {b64Val}",
            }

            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': 'http://127.0.0.1'
            }
            response = requests.post(MASTERTRUST_ACCESS_TOKEN_URL, headers=headers, data=data)
            print(response.json())


            if 'access_token' in response.json():
                access_token = response.json()['access_token']
                print(f'code decoded successfully with access_token\n{access_token}')
            return self.access_token