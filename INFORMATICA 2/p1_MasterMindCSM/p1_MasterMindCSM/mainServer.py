import TCPS
from args import check_server_args, parse_server_args

if __name__ == '__main__':

    ip, port = parse_server_args()
    ip_ok, port_ok = check_server_args(ip, port)
    if not port_ok or not ip_ok:
        print ("Error: La aplicación debe ejecutarse: python3 mainServer.py -i ip -p puerto")
        exit(-1)

    socketServer = TCPS.TCPServer(ip, int(port))
    socketServer.connect()
    socketServer.communication()