#encoding=utf8
import urllib
import socket

socket.setdefaulttimeout(3)
f = open("proxy")
lines = f.readlines()
proxys = []
for i in range(0,len(lines)):
    ip = lines[i].strip("\n").split("\t")
    proxy_host = "http://"+ip[0]+":"+ip[1]
    proxy_temp = {"http":proxy_host}
    proxys.append(proxy_temp)
url = "http://ip.chinaz.com/getip.aspx"
for proxy in proxys:
    try:
        res = urllib.urlopen(url,proxies=proxy).read()
        print res
    except Exception,e:
        print proxy
        print e
        continue