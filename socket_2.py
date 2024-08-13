from struct import pack_into
import ctypes, struct
from packetDecoder import decodeDetailedMarketData, decodeCompactMarketData, decodeSnapquoteData, decodeOrderUpdate
import websocket
import _thread
import time
import rel
import json
import threading
global nos


access_token = "bX3ZHHkPs0zKtzDFfWY1anvxkvmxzfKR2ijE5kP0D-w.BO0SgUOtodqnNaSkjXdJNiTsEJBa974J5TArSGaE4qw"
def on_message(ws, message):
    mode = struct.unpack('>b', message[0:1])[0]

    if mode == 1:
        global nos
        nos = decodeDetailedMarketData(message)
        # print("detailed market data")
        # print(res)

    elif mode == 2:
        res = decodeCompactMarketData(message)
        print(res)

    elif mode == 4:
        res = decodeSnapquoteData(message)
        print("snap quote data")
        print(res)




def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")


    sub_packet = '{"a": "subscribe", "v": [[4, 250060],[1,22]], "m": "marketdata"}'

    ws.send(sub_packet)

    hbThread = threading.Thread(target=heartbeat_thread, args=(ws,))
    hbThread.start()



def heartbeat_thread(clientSocket):
    while clientSocket:
        send_data = '{"a": "h", "v": [], "m": ""}'
        try:
            clientSocket.send(send_data)
        except Exception as e:
            print(e)
            print("HEARTBEAT [ERROR]: [BLITZ_HYDRA_STREAM] Connection closed.")
            break

        time.sleep(8)




#    websocket.enableTrace(True)
ws = websocket.WebSocketApp(f"wss://masterswift-beta.mastertrust.co.in/ws/v1/feeds?login_id=TEST25&token=bX3ZHHkPs0zKtzDFfWY1anvxkvmxzfKR2ijE5kP0D-w.BO0SgUOtodqnNaSkjXdJNiTsEJBa974J5TArSGaE4qw",

                          on_message=on_message,
                          on_error=on_error,
                          on_close=on_close)


ws.on_open = on_open ## sending request through this function

ws.run_forever()

