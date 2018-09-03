import socket
import threading
from web3 import Web3, HTTPProvider
import sqlite3

dd=dict()

bind_ip = '0.0.0.0'
bind_port = 9091
http1 = "https://ropsten.infura.io"
http2 = "http://localhost:8545"
infura_provider = HTTPProvider(http1)
web3 = Web3([infura_provider])
TEST_ACC = '0xC41a1508B50E7F956168788188DA0b61365413C2'
CODE = "0x608060405260043610603f576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063ed88c68e146044575b600080fd5b604a604c565b005b426001819055506101f460005460015403118015606a575060053411155b801560755750600034115b1515607f57600080fd5b6001546000819055505600a165627a7a723058200e626a96bafe30796e2f608d8ac86c6cf8a5afe091556f51f1d01351bfe671ba0029"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(1000)  # max backlog of connections

def getCode(acc):
    return web3.eth.getCode(Web3.toChecksumAddress(acc)).hex()

# print('Listening on ' + bind_ip + ":" + str(bind_port))

def handle_client_connection(client_socket):
    client_socket.send(("Enter contract address(Spiritual box): ").encode('utf-8'))
    request = client_socket.recv(1024)
    # print('Received ',request)
    client_input = request.decode("utf-8").strip()
    try:
        cAddr = web3.toChecksumAddress(client_input)
        bal = int(web3.eth.getBalance(cAddr))
    except:
        client_socket.send(("Is that even a valid contract address!").encode('utf-8'))
        client_socket.close()
        return;
    
    cCode = getCode(cAddr)
    if cCode == "0x00":
        client_socket.send(("Contract doesn't exists on Ropsten Testnet!").encode('utf-8'))
        client_socket.close()
        return;
    # print(bal, cCode)
    # print(cCode == CODE)

    if cCode == CODE and bal == 69:
        if dd.get(cAddr,0) == 1:
            client_socket.send("You can't use an address twice to get the flag, start again from beginning.".encode('utf-8'))
            client_socket.close()
            return;   
        client_socket.send("The flag is @self%DesTruct$".encode('utf-8'))
        dd[cAddr] = 1
    else:
        client_socket.send(("Requirements not satisfied!").encode('utf-8'))

    client_socket.close()

while True:
    client_sock, address = server.accept()
    # print('Accepted connection from ',address[0], ":", address[1])
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()
