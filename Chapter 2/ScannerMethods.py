import socket
from socket import *
from threading import *
import nmap

SCREEN_LOCK = Semaphore(value=1)


def nmap_scan(tgtHost, tgtPort):
    nmScan = nmap.PortScanner()
    results = nmScan.scan(tgtHost, tgtPort)
    status = results['scan'][tgtHost]['tcp'][int(tgtPort)]['state']
    print(f'{tgtHost} tcp/{tgtPort} {status}')


def banner_info(socketConnection):
    try:
        setdefaulttimeout(1)
        socketConnection.send(b"ViolentPython\r\n")
        results = socketConnection.recv(100)
        print(results.decode().strip())
        print()
    except:
        print("No information was gathered.")


def conn_scan(tgtHost, tgtPort, bannerInfo):
    try:
        connection = socket(AF_INET, SOCK_STREAM)
        connection.connect((tgtHost, tgtPort))
        SCREEN_LOCK.acquire()
        print(f'\nPort {tgtPort} is open')
        if bannerInfo is True:
            banner_info(connection)
    except:
        SCREEN_LOCK.acquire()
        print(f'\nPort {tgtPort} is closed')
    finally:
        SCREEN_LOCK.release()
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
    threads = thread_conn_scann(tgtHost, tgtPorts, bannerInfo)
    clean_threads(threads)


def thread_conn_scann(tgtHost,tgtPorts, bannerInfo):
    setdefaulttimeout(1)
    threads = []
    for tgtPort in tgtPorts:
        t = Thread(target=conn_scan, args=(tgtHost, int(tgtPort), bannerInfo))
        threads.append(t)
        t.start()
    return threads


def clean_threads(threads):
    for thread in threads:
        thread.join()
