from socket import *
from threading import *

SCREENLOCK = Semaphore(value=1)
def banner_info(socketConnection):
    try:
        setdefaulttimeout(1)
        socketConnection.send(b"ViolentPython\r\n")
        results = socketConnection.recv(100)
        print(results.decode())
    except:
        print("No information was gathered.")

def conn_scan(tgtHost, tgtPort, bannerInfo):
    try:
        connection = socket(AF_INET, SOCK_STREAM)
        connection.connect((tgtHost, tgtPort))
        SCREENLOCK.acquire()
        print(f'Port {tgtPort} is open')
        if bannerInfo is True:
            banner_info(connection)
    except:
        SCREENLOCK.acquire()
        print(f'Port {tgtPort} is closed')
    finally:
        SCREENLOCK.release()
        connection.close()

def port_scan(tgtHost, tgtPorts, bannerInfo):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print(f"Can not resolve {tgtHost}")
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
        print(f"Scan Results for: {tgtName[0]}")
    except:
        print(f"Scan Results for: {tgtIP}")

    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t = Thread(target=conn_scan, args =(tgtHost,int(tgtPort),bannerInfo))
        t.start()
