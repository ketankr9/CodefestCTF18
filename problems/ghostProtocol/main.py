import socket
import threading
from hashlib import md5
import random
import string
from hidemsg import hidemsg

bind_ip = '0.0.0.0'
bind_port = 9092
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(1000)  # max backlog of connections

print('Listening on ' + bind_ip + ":" + str(bind_port))

def generateRand(mLength):
    rand = ''.join([random.choice(string.ascii_letters
            + string.digits) for n in range(mLength)])
    return rand

def send_(client_s, msg):
    #msg=msg+":122:"
    client_s.send(msg.encode('utf-8'))

def receive_(client_s):
    request = client_s.recv(1024)
    print('Received ',request)
    received = request.decode("utf-8").strip()
    print(received)
    return received

def handle_client_connection(client_socket):
    global enc
    send_(client_socket, "Tell me your name and secret\n")
    # Hi I am Alice, R1   -------->>>>>>>
    received = receive_(client_socket)
    try:
        name, nounce = received.split(" ")
        if name == None or nounce == None:
            raise ValueError('Not allowed!')
    except:
        send_(client_socket, "Wrong format!")
        client_socket.close()
        return; 

    val = generateRand(random.randint(5,10))
    # R2 E(R1, K) ------<<<<<<<<<<<<<<<<
    send_(client_socket, val +" " +str(enc.encode(nounce.rstrip())) + "\n")

    # E(R2, K)  ---------->>>>>>>>>>>>>
    received = receive_(client_socket)

    msg = "You aint't authorized!"
    if received == str(enc.encode(val)):
        msg  = "The flag is #muetuAl%authentiKati0n@"
    # Reveal the msg(flag)    
    send_(client_socket,msg)

    client_socket.close()


enc = hidemsg()
while True:
    client_sock, address = server.accept()
    print('Accepted connection from ',address[0], ":", address[1])
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)
    )
    client_handler.start()

