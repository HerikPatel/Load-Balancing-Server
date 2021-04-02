import socket
import sys


def lsServer(port, ts1Hostname, ts1port, ts2Hostname, ts2Port):
    try:
        ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('Socket open error at LS: {}\n'.format(err))
        exit()
    server_binding = ('', port)
    ls.bind(server_binding)
    ls.listen(5)

    client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client1.settimeout(2.5)
    host_addr1 = socket.gethostbyname(ts1Hostname)
    host_binding1 = (host_addr1, ts1port)
    client1.connect(host_binding1)
    client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client2.settimeout(2.5)
    host_addr2 = socket.gethostbyname(ts2Hostname)
    host_binding2 = (host_addr2, ts2Port)
    client2.connect(host_binding2)
    conn = None
    print("Waiting for connection")
    conn, addr = ls.accept()
    while True:
        received1 = ""
        received2 = ""
        data_from_client = conn.recv(200)
        query = data_from_client.decode('utf-8')
        if(query == "done"):
            print("Donewith client: Closing connection")
            client1.send("done".encode('utf-8'))
            client2.send("done".encode('utf-8'))
            conn.close()
            exit()

        else:
            client1.send(query.encode('utf-8'))
            client2.send(query.encode('utf-8'))
            received=""
            try:
                data_from_server1 = client1.recv(200)
                received = data_from_server1.decode('utf-8')
            except:
                pass

            try:
                data_from_server2 = client2.recv(200)
                received = data_from_server2.decode('utf-8')
            except:
                pass

        if len(received) > 1:
            conn.send(received.encode('utf-8'))
        else:
            err = query+" - Error:HOST NOT FOUND"
            conn.send(err.encode('utf-8'))
    return


#lsServer(14007, 14003, 'localhost', 14008, 'localhost')
if __name__ == "__main__":
    if(len(sys.argv) == 6):
        ls_port = int(sys.argv[1])
        ts1_host = str(sys.argv[2])
        ts1_port = int(sys.argv[3])
        ts2_host = str(sys.argv[4])
        ts2_port = int(sys.argv[5])
        lsServer(ls_port, ts1_host, ts1_port, ts2_host, ts2_port)
    else:
        print("Insufficent arguments")
        exit()
