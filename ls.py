import socket
import sys


def check_DNS_table(port, ts1port, ts1Hostname, ts2Port, ts2Hostname):
    try:
        ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('Socket open error at RS: {}\n'.format(err))
        exit()
    server_binding = ('', port)
    ls.bind(server_binding)
    ls.listen(4)

    client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client1.settimeout(1)
    host_addr1 = socket.gethostbyname(ts1Hostname)
    host_binding1 = (host_addr1, ts1port)
    client1.connect(host_binding1)
    client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client2.settimeout(1)
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
            conn.close()
            exit()
        else:
            try:
                client1.send(query.encode('utf-8'))
                data_from_server1 = client1.recv(200)
                received1 = data_from_server1.decode('utf-8')
            except:
                pass

            try:
                client2.send(query.encode('utf-8'))
                data_from_server2 = client2.recv(200)
                received2 = data_from_server2.decode('utf-8')
            except:
                pass

        if len(received1) > 1:
            conn.send(received1.encode('utf-8'))
        elif len(received2) > 1:
            conn.send(received2.encode('utf-8'))
        else:
            err = query+" - Error:HOST NOT FOUND"
            conn.send(err.encode('utf-8'))
    return


check_DNS_table(14007, 14003, 'localhost', 14008, 'localhost')
'''
if __name__ == "__main__":
    if(len(sys.argv) == 2):
        ls_port = int(sys.argv[1])
        check_DNS_table(ls_port, ts1Port, ts1Hostname, ts2Port, ts2Hostname)
    else:
        print("Insufficent arguments")
        exit()
'''
