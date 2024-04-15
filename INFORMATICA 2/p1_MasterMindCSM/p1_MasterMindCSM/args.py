import sys
import getopt

# Crooners
# Tony Bennett.
# Nat 'King' Cole.
# Perry Como.
# Don Cornell.
# Bing Crosby.
# Vic Damone.
# Bobby Darin.
# Sammy Davis Jr.


def parse_client_args1():
    ip = "127.0.0.1"
    port = 1234
    nick = "Tony Bennett"
    frase = "Frère Jacques"

    opts, args = getopt.getopt(sys.argv[1:], "n:i:p:", ["nick=", "ip=", "port="])
    for o, a in opts:
        if o in ("-i", "--ip"):
            ip = a
        elif o in ("-p", "--port"):
            port = a
        elif o in ("-n", "--nick"):
            nick = a

    return nick, ip, port, frase

def parse_client_args2():
    ip = "127.0.0.1"
    port = 1234
    nick = "Nat 'King' Cole"
    frase = "Dormez vous?"

    opts, args = getopt.getopt(sys.argv[1:], "n:i:p:", ["nick=", "ip=", "port="])
    for o, a in opts:
        if o in ("-i", "--ip"):
            ip = a
        elif o in ("-p", "--port"):
            port = a
        elif o in ("-n", "--nick"):
            nick = a

    return nick, ip, port, frase

def parse_client_args3():
    ip = "127.0.0.1"
    port = 1234
    nick = "Bing Crosby"
    frase = "Sonnez les matines"

    opts, args = getopt.getopt(sys.argv[1:], "n:i:p:", ["nick=", "ip=", "port="])
    for o, a in opts:
        if o in ("-i", "--ip"):
            ip = a
        elif o in ("-p", "--port"):
            port = a
        elif o in ("-n", "--nick"):
            nick = a

    return nick, ip, port, frase

def parse_client_args4():
    ip = "127.0.0.1"
    port = 1234
    nick = "Sammy Davis Jr"
    frase = "Ding ding dong"

    opts, args = getopt.getopt(sys.argv[1:], "n:i:p:", ["nick=", "ip=", "port="])
    for o, a in opts:
        if o in ("-i", "--ip"):
            ip = a
        elif o in ("-p", "--port"):
            port = a
        elif o in ("-n", "--nick"):
            nick = a

    return nick, ip, port, frase


def check_client_args(nick, ip, port):
    ip_ok = True
    port_ok = True
    nick_ok = True

    if len(ip)==0:
        ip_ok = False

    try:
        port = int(port)
        port_ok = True
    except ValueError:
        port_ok = False

    if len(nick) == 0:
        nick_ok = False

    return nick_ok, ip_ok, port_ok


def parse_server_args():
    ip = "127.0.0.1"
    port = 1234

    opts, args = getopt.getopt(sys.argv[1:], "i:p:", ["ip=", "port="])
    for o, a in opts:
        if o in ("-i", "--ip"):
            ip = a
        elif o in ("-p", "--port"):
            port = a

    return ip, port


def check_server_args(ip, port):
    port_ok = True
    ip_ok = True
    try:
        port = int(port)
        port_ok = True
    except ValueError:
        port_ok = False

    if len(ip)==0:
        ip_ok = False
    return ip_ok, port_ok