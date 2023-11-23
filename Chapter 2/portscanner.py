import optparse
import sys
import ScannerMethods

# Creating options for command line
# Create the file
parser = optparse.OptionParser('portscanner.py' +
                               ' -H <target host> -p <target-port>')
# Adds the -H header to give it a string argument
parser.add_option('-H', dest='tgtHost', type='string',
                  help="Specify target host")
# Adds the -p to take an int argument
parser.add_option('-p', dest='tgtPort', type='str',
                  help="Specify target ports by , seperated values")
parser.add_option('-v', dest='bannerInfo', default=False,
                  action="store_true", help="Grab banner information from the port")
# returns a dictionary like object from optparse.Values into options and a list of leftover arguments
options, args = parser.parse_args()
target = options.tgtHost
ports = options.tgtPort.split(",")
bannerInfo = options.bannerInfo

if (target is None) | (ports is None):
    print("Invalid arguments")
    sys.exit(0)


def main():
    ScannerMethods.port_scan(target, ports, bannerInfo)
    for port in ports:
        ScannerMethods.nmap_scan(target, port)


if __name__ == "__main__":
    main()