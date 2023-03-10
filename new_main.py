from client_conn_win import window
from client_conn_win import connect_to_server
from client_conn_win import AI
import main
from main import *
import multiplayer
from multiplayer import *


window.mainloop()

while window.mainloop():
    if connect_to_server():
        multiplayer
        while multiplayer():
            window.after(3000, window.destroy)
    if AI():
        main