import sys

import pexpect

PROMPT = ['# ', '>>> ', '> ', '\$ ']


def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before.decode())


def connect(user, host, password):
    ssh_newkey = 'Are you sure you want to continue connecting'
    connStr = f'ssh {user}@{host}'
    child = pexpect.spawn(connStr)
    # this will return an int based on the index of what is returned
    # 0 = timeout, 1 = ssh_newkey, 2 = password
    # pexpect is a non-greedy regex match meaning it will always return the smallest pattern that matches
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    decision(child,ret,password)
    return child

def decision(child, ret, password):
    if ret == 0:
        print("Error Connecting")
    elif ret == 1:
        new_decision(child,password)
    else:
        send_password(child, password)


def new_decision(child,password):
    child.sendline('yes')
    ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
    if ret == 0:
        print("Error Connecting")
    if ret ==1:
        send_password(child,password)


def send_password(child, password):
    child.sendline(password)
    ret = child.expect(PROMPT)
    # Prompt is 4 variables long with an index of 0
    if ret < 4:
        print("Connection Successful")
    else:
        print("Error Connecting")


def main():
    child = connect('lewis', '192.168.x.x', 'password')
    child.sendline('sudo cat /etc/shadow | grep root')
    ret = child.expect([pexpect.TIMEOUT, 'lewis:'])
    if ret == 1:
        send_command(child,'password')
    else:
        child.sendline(exit)
        sys.exit(0)
    try:
        child.sendline(exit)
    except:
        pass

if __name__ == '__main__':
    main()



