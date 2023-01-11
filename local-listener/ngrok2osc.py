import sys, os
from threading import Thread
from pythonosc import udp_client
from flask import Flask, make_response
import subprocess, socket

def osc_forward():
  
  osc_server = udp_client.SimpleUDPClient(address="127.0.0.1", port=8066)
  osc_server.send_message("/locally_connected", True)
  
  HOST, PORT = "127.0.0.1", 8055
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Listening to the port: {PORT}")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            osc_server.send_message("/message", data)
            

def init_ngrok():
  # output = subprocess.run(["C:\\bin\\ngrok","http", "8051"], capture_output=True)
  # print(output.stdout)
  # No output as you can NOT connect to the same port that you are listening too
  
  from pyngrok import process, conf, ngrok
  # _conf = conf.PyngrokConfig(ngrok_path=os.path.join(os.path.dirname(__file__), "ngrok.exe"))
  # process.installer.get_ngrok_bin()
  # ngrok.get_ngrok_process(_conf)
  # ngrok.get_default_config()
  ngrok_url = ""
  print("🌐 Downloading required libraries ...")
  with suppress_stdout():
    ngrok_url = ngrok.connect(5000).public_url
  print("✔️ Connected to the remote server")
  print(ngrok_url)
  return ngrok_url
  
from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

if __name__ == "__main__":
  # th1 = Thread(target=init_pagekit)
  th1 = Thread(target=init_ngrok)
  th2 = Thread(target=osc_forward)
  th1.start()
  th2.start()
  
