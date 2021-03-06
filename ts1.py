import socket
import sys


def get_DNS_values():  # Gets values of dns table and stores in dictonary
    rs_DNS = {}
    f = open("PROJ2-DNSTS1.txt", "r")
    list = [x.rstrip('\r\n') for x in f]
    for x in list:
        temparr = x.split()
        rs_DNS[temparr[0].lower()] = x
    return rs_DNS


# Connects with client and recives and sends data to the client
def check_DNS_table(port, rs_dns):
    try:
        rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('Socket open error at RS: {}\n'.format(err))
        exit()
    server_binding = ('', port)
    rs.bind(server_binding)
    rs.listen(1)
    conn = None
    print("Waiting for connection")
    conn, addr = rs.accept()
    while True:
        data_from_client = conn.recv(200)
        query = data_from_client.decode('utf-8')
        if(query == "done"):
            print("Donewith client: Closing connection")
            conn.close()
            exit()
        reply = ""
        if (rs_dns == {}):
            pass
        elif query.lower() in rs_dns:
            reply = rs_dns[query.lower()]
            conn.send(reply.encode('utf-8'))
    return


if __name__ == "__main__":
    if(len(sys.argv) == 2):
        rs_port = int(sys.argv[1])
        rs_dns = get_DNS_values()
        check_DNS_table(rs_port, rs_dns)
    else:
        print("Insufficent arguments")
        exit()
