import socket
import sys
try :
    connection1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("connection established ")
except socket.error as error:
    print ("socket creation failed with error %s" %(error))

prot = 8001

try:
    host_ip = socket.gethostbyname('www.google.com')
    print(host_ip)

except socket.gaierror:
    # this means could not resolve the host
    print("there was an error resolving the host")
    sys.exit()

connection1.connect((host_ip, 80))
print ("the socket has successfully connected to google")
