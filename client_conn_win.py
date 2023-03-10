import tkinter as tk
from tkinter import messagebox
import socket
import websocket
import threading
import json
import rel
import time






window = tk.Tk()
window.title("Battleship Multiplayer Game")
username = ""
Room = ""
 

topFrame = tk.Frame(window)
lblName = tk.Label(topFrame, text = "Name: ").pack(side=tk.LEFT)
entName = tk.Entry(topFrame)
entName.pack(side=tk.LEFT)
lblName = tk.Label(topFrame, text = "Room: ").pack(side=tk.LEFT)
entRoom = tk.Entry(topFrame)
entRoom.pack(side=tk.LEFT)
btnConnect = tk.Button(topFrame, text="Connect", command=lambda : connect())
btnSingleplayer = tk.Button(topFrame, text="Vs AI", command=lambda : AI())
btnSingleplayer.pack(side=tk.RIGHT)
btnConnect.pack(side=tk.LEFT)
#btnConnect.bind('<Button-1>', connect)
topFrame.pack(side=tk.TOP)



displayFrame = tk.Frame(window)
lblLine = tk.Label(displayFrame, text="*********************************************************************").pack()
tkDisplay = tk.Text(displayFrame, height=20, width=67)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
tkDisplay.tag_config("tag_your_message", foreground="blue")
displayFrame.pack(side=tk.TOP)





def AI():
    window.after(1000, window.destroy)



   



def connect():
    global username, Room
    if len(entName.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        username = entName.get()
        Room = entRoom.get()
        connect_to_server(Room, username)




def connect_to_server(Room,name):
    global client
    try:
        ws = websocket.WebSocketApp(f"wss://battleships.lennardwalter.com?room={Room}&name={name}",
                                       on_open=on_open,
                                       on_message=on_message,
                                       on_error=on_error,
                                       on_close=on_close)
        def run():
            ws.run_forever(reconnect=5)

        
        threading.Thread(target=run).start()

        entName.config(state=tk.DISABLED)
        btnConnect.config(state=tk.DISABLED)
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " +  " Server may be Unavailable. Try again later")
        print(e)


def on_message(ws, message):
   print(message)
   msg_json = json.loads(message)
   if msg_json["type"] == "GAME_PHASE_CHANGED":
       if msg_json["data"]["phase"] == "IN_PROGRESS":    
            if msg_json["type"] == "PLAYER_CHANGED":
                if msg_json["data"]["name"] == "Player1":
                    while msg_json["data"]["name"] == "Player1":
                        ShotCoordinatesX = input("Enter X Coordinates")
                        ShotCoordinatesY = input("Enter Y Coordinates")
                        data = {
                            "type": "FIRE_SHOT",
                             "data": {
                                "x": ShotCoordinatesX,
                                "y": ShotCoordinatesY,
                   
                            }
                        }
                        ws.send(json.dumps(data))
                        time.sleep(2.5)


       if msg_json["data"]["phase"] == "SETUP":
           # place ships
           i = 1
           while i < 11:
            ShipCoordinatesX = input("Enter X Coordinates")
            ShipCoordinatesY = input("Enter Y Coordinates")
            ShipDirection = input("Enter Direction with HORINZONTAL or VERTIKAL ")
            Shiplenght = input("Enter Ship lenght")
            data = {
               "type": "PLACE_SHIP",
               "data": {
                   "x": ShipCoordinatesX,
                   "y": ShipCoordinatesY,
                   "length": Shiplenght,
                   "direction": ShipDirection
               }
            }
            ws.send(json.dumps(data))
            i += 1
        

   else:
       print(msg_json)

def on_error(ws, error):
   print(error)
 
 
def on_close(ws, close_status_code, close_msg):
   print("Closed connection")
 
 
def on_open(ws):
   print("Opened connection")

window.mainloop()


