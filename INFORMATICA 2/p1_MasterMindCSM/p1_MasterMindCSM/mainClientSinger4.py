from TCPClient import *
from args import parse_client_args4, check_client_args

if __name__ == '__main__':

    nick, ip, port, frase = parse_client_args4()
    nick_ok, ip_ok, port_ok = check_client_args(nick, ip, port)

    if not nick_ok or not ip_ok or not port_ok:
        print ("Error: La aplicación debe ejecutarse: python3 mainClientPlayer1.py -p puerto -")
        exit(-1)

    socketClient = TCPClient(ip, int(port), nick, frase)
    socketClient.connect()
    socketClient.communication()
    socketClient.diconnectSocket()