import requests
import json


NSE = 1
NFO = 2
CDS = 3
MCX = 4
BSE = 6
BFO = 7


class Connect:
    def __init__(self, client_id, client_secret, base_url, access_token):
        self.headers = {'Content-type': 'application/json'}
        self.access_token = access_token
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.Master_contracts = {}
        if "https" in base_url:
            url = base_url.replace("https", "wss")
        else:
            url = base_url.replace("http", "ws")
        self.websocket_url = url

    def ex_code(self, exchange):
        if exchange == 'NSE':
            return str(NSE)
        elif exchange == 'NFO':
            return str(NFO)
        elif exchange == 'CDS':
            return str(CDS)
        elif exchange == 'MCX':
            return str(MCX)
        elif exchange == 'BSE':
            return str(BSE)
        elif exchange == 'BFO':
            return str(BFO)

    def master_list(self, exchanges):  # exchanges in type List

        for exchange in exchanges:

            dict1 = {}
            URL = f"https://masterswift.mastertrust.co.in/api/v2/contracts.json?exchanges={exchange}"
            response = requests.request("GET", URL)


            Master_List = response.json()

            for exch in Master_List:

                for data in Master_List[exch]:
                    dict1[data['symbol']] = data
            self.Master_contracts.update(dict1)
        return self.Master_contracts

    # def get_access_token(self):
    #	url = f"{self.base_url}/api/v1/user/login?login_id={self.user_id}&password={self.password}"
    #	payload={}
    #	headers = {}
    #	response = requests.request("POST", url, headers=headers, data=payload)
    #	twofa_token = response.json()['data']['twofa_token'] #['twofa']

    #	url = f"{self.base_url}/api/v1/user/twofa?login_id={self.user_id}&twofa_token={twofa_token}&type=GENERAL_QUESTIONS&password={self.password}"
    #	payload = json.dumps({
    #	  "login_id": self.user_id,
    #	  "twofa": [
    #		{
    #		  "question_id": 1,
    #		  "answer": self.twofa,
    #		  "type": "GENERAL_QUESTIONS"
    #		}
    #	  ],
    #	  "twofa_token": twofa_token
    #	})
    #	headers = {
    #	  'login_id': self.user_id,
    #	  'Content-Type': 'application/json'
    #	}

    #	response = requests.request("POST", url, headers=headers, data=payload)
    #	access_token = response.json()['data']['auth_token']
    #	Connect.set_access_token(self, access_token)
    #	Connect.print_access_token(self)
    #	return access_token

    # def set_access_token(self, access_token):
    #	self.access_token = access_token

    # def print_access_token(self):
    #	print(f'access_token: {self.access_token}')

    def get_request(self, url, params):
        headers = self.headers
        headers['Authorization'] = f'Bearer {self.access_token}'
        res = requests.get(f'{self.base_url}{url}', params=params, headers=headers)
        return res.json()

    def post_request(self, url, data):
        headers = self.headers
        headers['Authorization'] = f'Bearer {self.access_token}'
        res = requests.post(f'{self.base_url}{url}', headers=headers, data=json.dumps(data))
        print(res)
        return res.json()

    def put_request(self, url, data):
        headers = self.headers
        headers['Authorization'] = f'Bearer {self.access_token}'
        res = requests.put(f'{self.base_url}{url}', headers=headers, data=json.dumps(data))
        print(res)
        return res.json()

    def delete_request(self, url, params):
        headers = self.headers
        headers['Authorization'] = f'Bearer {self.access_token}'
        res = requests.delete(f'{self.base_url}{url}', params=params, headers=headers)
        return res.json()

    def _send_request(self, method='get', endpoint='', params={}):
        r = requests.request(
            method=method,
            headers={
                'Accept': 'application/json',
                'x-authorization-token': f'{self.access_token}'
            },
            url=f'{self.base_url}{endpoint}',
            params=params)

        if r.status_code == 200:
            r_json = r.json()
            try:
                return r_json['data']
            except KeyError as e:
                print(e)
                return r_json

        print(r)
        print(r.json())

    # def fetch_profile(self, user_id):
    #	endpoint = f'/api/v1/user/profile?client_id={user_id}'
    #	data = self._send_request(endpoint=endpoint)
    #	return data


    def fetch_profile(self, user_id):
        params = None
        endpoint = f'/api/v1/user/profile?client_id={user_id}'
        data = self.get_request(endpoint,params)
        return data


    def place_order(self, payload):
        data = {
            "exchange": payload['exchange'],
            "order_type": payload['order_type'],
            "instrument_token": payload['instrument_token'],
            "quantity": payload['quantity'],
            "disclosed_quantity": payload['disclosed_quantity'],
            "price": payload['price'],
            "order_side": payload['order_side'],
            "trigger_price": payload['trigger_price'],
            "validity": payload['validity'],
            "product": payload['product'],
            "client_id": payload['client_id'],
            "user_order_id": payload['user_order_id'],
            "market_protection_percentage": 0,  # added
            "device": "api",
        }
        # "execution_type": payload['execution_type']
        # "amo": payload['amo'],
        res = self.post_request(f'/api/v1/orders', data)
        return res


    def modify_order(self, payload):
        data = {
            "exchange": payload['exchange'],
            "instrument_token": payload['instrument_token'],
            "client_id": payload['client_id'],
            "order_type": payload['order_type'],
            "price": payload['price'],
            "quantity": payload['quantity'],
            "disclosed_quantity": payload['disclosed_quantity'],
            "validity": payload['validity'],
            "product": payload['product'],
            "oms_order_id": payload['oms_order_id'],
            "trigger_price": payload['trigger_price']
            # "execution_type": payload['execution_type']
        }
        res = self.put_request("/api/v1/orders", data)
        return res


    def cancel_order(self, payload):
        params = {
            'client_id': payload['client_id']
            #'execution_type': payload['execution_type']
        }
        oms_order_id = payload['oms_order_id']
        res = self.delete_request(f'/api/v1/orders/{oms_order_id}', params)
        return res


    def fetch_scripinfo(self, payload):
        params = {
            'info': 'scrip',
            'token': payload['token']
        }
        exchange = payload["exchange"]
        res = self.get_request(f'/api/v1/contract/{exchange}', params)
        return res


    def search_scrip(self, payload):
        params = {
            'key': payload['key']
        }
        res = self.get_request(f'/api/v1/search', params)
        return res


    def fetch_scrip_price(self, payload):
        params = {}
        exchange = payload['exchange']
        token = payload['token']
        if exchange == 'NSE':
            ltp_res = self.get_request(f'/api/v1/marketdata/NSE/Capital?token={token}&key=last_trade_price', params)
            close_price_res = self.get_request(f'/api/v1/marketdata/NSE/Capital?token={token}&key=close_price', params)
        elif exchange == 'BSE':
            ltp_res = self.get_request(f'/api/v1/marketdata/BSE/Capital?token={token}&key=last_trade_price', params)
            close_price_res = self.get_request(f'/api/v1/marketdata/BSE/Capital?token={token}&key=close_price', params)
        elif exchange == 'NFO':
            ltp_res = self.get_request(f'/api/v1/marketdata/NSE/FutOpt?token={token}&key=last_trade_price', params)
            close_price_res = self.get_request(f'/api/v1/marketdata/NSE/FutOpt?token={token}&key=close_price', params)
        elif exchange == 'CDS':
            ltp_res = self.get_request(f'/api/v1/marketdata/NSE/Currency?token={token}&key=last_trade_price', params)
            close_price_res = self.get_request(f'/api/v1/marketdata/NSE/Currency?token={token}&key=close_price', params)
        elif exchange == 'MCX':
            ltp_res = self.get_request(f'/api/v1/marketdata/MCX/FutOpt?token={token}&key=last_trade_price', params)
            close_price_res = self.get_request(f'/api/v1/marketdata/MCX/FutOpt?token={token}&key=close_price', params)
        else:
            ltp_res = {"data": 0, "message": "Exchange is ---- invalid", "status": "error"}
            close_price_res = {"data": 0, "message": "Exchange is invalid", "status": "error"}
        if (ltp_res["status"] == "error" or close_price_res["status"] == "error"):
            res = {"last_traded_price": 0, "close_price": 0, "status": "error", "message": ltp_res['message']}
        else:
            res = {"last_traded_price": ltp_res['data'], "close_price": close_price_res['data'], "status": "success",
                   "message": ""}
      #  print(res)
        return res


    def fetch_pending_orders(self, payload):
        params = {
            'type': 'pending',
            'client_id': payload['client_id']
        }
        res = self.get_request(f'/api/v1/orders', params)
        return res


    def fetch_completed_orders(self, payload):
        params = {
            'type': 'completed',
            'client_id': payload['client_id']
        }
        res = self.get_request(f'/api/v1/orders', params)
        return res


    def fetch_trades(self, payload):
        params = {
            'client_id': payload['client_id']
        }
        res = self.get_request(f'/api/v1/trades', params)
        return res


    def fetch_order_history(self, payload):
        params = {
            'client_id': payload['client_id']
        }
        oms_order_id = payload['oms_order_id']
        res = self.get_request(f'/api/v1/order/{oms_order_id}/history', params)
        return res


    def fetch_live_positions(self, payload):
        params = {
            'client_id': payload['client_id'],
            'type': 'live'
        }
        res = self.get_request(f'/api/v1/positions', params)
        return res


    def fetch_netwise_positions(self, payload):
        params = {
            'client_id': payload['client_id'],
            'type': 'historical'
        }
        res = self.get_request(f'/api/v1/positions', params)
        return res


    def fetch_holdings(self, payload):
        params = {
            'client_id': payload['client_id']
        }
        res = self.get_request(f'/api/v1/holdings', params)
        return res


    def fetch_funds_v2(self, payload):
        params = {
            'client_id': payload['client_id'],
            'type': 'all'
        }
        res = self.get_request(f'/api/v2/funds/view', params)
        return res


    def fetch_funds_v1(self, payload):
        params = {
            'client_id': payload['client_id'],
            'type': 'all'
        }
        res = self.get_request(f'/api/v1/funds/view', params)
        return res

