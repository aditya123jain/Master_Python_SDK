from connect import Connect
from code_decorder import decoder


######################################################## USER DETAILS ###########################################
App_ID = '5B5sp6DhtD'    ###USER NEED TO ADD App_ID here(SAME AS mastertrust_app_id)

mastertrust_app_id = '5B5sp6DhtD'
mastertrust_secret_key =  'PanpYtZLRKXYzQM8Qm6F5SFkFVWaMOhx2OacXfChbBw6qDemHy74RSKtUdZhwI9l'
redirect_uri = 'http://127.0.0.1'
client_id  = 'TEST25'
access_token = "bX3ZHHkPs0zKtzDFfWY1anvxkvmxzfKR2ijE5kP0D-w.BO0SgUOtodqnNaSkjXdJNiTsEJBa974J5TArSGaE4qw"
base_url = 'https://masterswift-beta.mastertrust.co.in/'


###############################################Create an instance from  Connect class #######################################

ms  = Connect(mastertrust_app_id,mastertrust_secret_key, base_url, access_token)

ms.master_list(['NSE'])




data = {
"exchange": 'NSE',
"order_type": 'LIMIT',
"instrument_token": 22,
"order_side": 'BUY',
"product": "MIS",
"quantity": 25,
"disclosed_quantity": 0,
"price": 2500,
"trigger_price": 0,
"validity": 'DAY',
"client_id":  'TEST25',
"user_order_id": 1000,
"market_protection_percentage": 0
}

place_order = ms.place_order(data)
print(place_order)
oms_order_id = place_order['data']['oms_order_id']

data = { 'info': 'scrip',
            'token': 22,
         "exchange": 'NSE'}

print(ms.fetch_scripinfo(data))

data = {'exchange' : 'NSE',
        'token' : 22}
print(ms.fetch_scrip_price(data))

