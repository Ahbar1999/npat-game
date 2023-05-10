import socket
import random
import time
import json

if __name__ == "__main__":
    addresses = {
        "name": ("localhost", 9999), 
        "animal": ("localhost", 9998), 
        "place": ("localhost", 9997), 
        "thing": ("localhost", 9996), 
    }

    backup = ("localhost", 9995)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
    while True:
        data = {}
        code = random.randint(ord('a'), ord('z'))  
        for id in addresses:
            HOST, PORT = addresses[id] 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                try:
                    sock.connect((HOST, PORT))
                except:
                    # reassign host, port to backup server
                    (HOST, PORT) = backup 
                    sock.connect((HOST, PORT))
                # Connect to server and send data
                print(code)
                sock.sendall(bytes(str(id) + " " + chr(code), encoding="utf-8"))
                # Receive data from the server and shut down
                received = str(sock.recv(1024), "utf-8")
                
            print("Sent:     {}".format(chr(code)))
            print(f"Received: {format(received)}")
            data[id] = str(received)

        with open('logs', "+a", encoding="utf-8") as f:
            f.write(json.dumps([code, data]) + "\n")

        # send codes after every 2 seconds 
        time.sleep(2)

