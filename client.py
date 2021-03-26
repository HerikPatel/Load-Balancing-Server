import socket
import sys


def sendRequest(port, host):  # Used to search domain in rs server
    resolved_file = open("RESOLVED.txt", "w")
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('Socket open error from Client to RS server: {} \n'.format(err))
        exit()

    if host.lower() == "localhost":
        client.connect(('localhost', port))
    else:
        host_addr = socket.gethostbyname(host)
        host_binding = (host_addr, port)
        client.connect(host_binding)
    f = open("PROJ2-HNS.txt", "r")
    list = [x.rstrip('\r\n') for x in f]
    if(list == []):
        print("PROJ2-HNS.txt is empty, nothing to query")
        print("Closing connection with server")
        client.send("done".encode('utf-8'))
        resolved_file.write("")
        f.close()
        client.close()
        resolved_file.close()
        exit()
    for x in list:

        client.send(x.encode('utf-8'))
        data_from_server = client.recv(200)
        received = data_from_server.decode('utf-8')
        exists = 0
        if "NS" in received:
            tsHost = received
            exists = 1
        else:
            resolved_file.write(received+"\n")
    client.send("done".encode('utf-8'))
    if(exists == 1):
        pass
    f.close()
    client.close()
    resolved_file.close()
    return


sendRequest(14007, 'localhost')
'''
if __name__ == "__main__":
    lsHost = ""
    lsPort = 0
    tsPort = 0
    if(len(sys.argv) == 3):
        lsHost = str(sys.argv[1])
        lsPort = int(sys.argv[2])
    else:
        print("Insufficent arguments")
        exit()
    rs_server(lsPort, lsHost, tsPort)
    print("Done: please check RESOLVED.txt for results")
'''
