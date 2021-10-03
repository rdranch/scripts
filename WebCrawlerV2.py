'''
Web Crawler
webcrawl.py
Designed by: Russell Dranch
'''

import socket, urllib.parse, ssl, csv
from sys import argv
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
from multiprocessing import Process, Manager
from datetime import datetime

start = datetime.now()

def req(url, name, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if port == 443:
        s = ssl.wrap_socket(s)
    s.settimeout(3)

    if url[0:4] == "http":
        url = url[7:]
        port = 80
    if url[0:5] == "https":
        url = url[8:]
        port = 443
        s = ssl.wrap_socket(s)

    #print(url + ":" + str(port))

    try:
        s.connect((url, port))
    except:
        return None

    if len(name) >= 3 and name[-1] == "/":
        name = name[:-1]

    request = "GET %s HTTP/1.1\r\nHost: %s\r\nAccept: text/html\r\nConnection: close\r\n" % (name, url)
    request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n"
    request += "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36\r\n\r\n"
    #print(request)
    s.sendall(request.encode())
    page = b""

    while True:
        try:
            data = s.recv(2048)
            if not data:
                break
            page += data
        except:
            break
    #print(page)
    return page

'''
Puts all links to the companies in a list
'''
def companyList():
    companies = set()
    with open('companies.csv', newline='') as excel:
        data = csv.DictReader(excel)
        for row in data:
            if len(companies) > 25:
                break
            link = row['Link']
            companies.add(link)
    return companies


def getName(link):
    if link[0] == "/":
        return lnks[0]
    link = link.split("/")

    name = link[2]
    return name

def getPath(link):
    link = link.split("/")
    if link[-1] == "":
        link.pop()

    l = 3
    s = "/"
    if len(link) <= 3:
        return s
    while l < len(link):
        s += link[l] + "/"
        l += 1
    return s


lnks = []
dm = []
dirs = []


'''
Ensure that the link is from the domain.
Often a site references other links such as YouTube or Twitter
'''
def domainInLink(link):
    if link[0] == "/":
        return True
    if len(link) < 13:
        return False

    l = link.split("/")
    return l[2] in dm       

'''
Determines if the link uses https
'''
def isSSL(link):
    return link[0:5] == "https"

'''
Create a list with links to visit
'''
def linkList(request, domain):
    l2v = []

    for links in request:
        #now = wwwRemover(links['href'])
        now = links['href']
        if now not in l2v and now not in dirs and len(now) >= 1 and (now[0] == 'h' or now[0] == '/') and domainInLink(now):
            if now.find("?") != -1:
                now = now[0:now.find("?")]
            if now[0] == "/":
                dirs.append(now)
                l2v.append(domain+now)
            else:
                l2v.append(now)
    return l2v

'''
Returns the depth of a certain link
'''
def depthLevel(link):
    l = link.split("/")
    if l[-1] == "":
        l.pop()
    #print (link + " " + str(len(l)-3))
    return len(l) - 3

'''
Finds all links in a page to a certain depth
'''
def linkExtension(depth):
    depth = int(depth)
    for l in lnks:
        if isSSL(l):
            port = 443
        else:
            port = 80
        
        if l.find("?") != -1:
            #print(l + " " + str(l.find("?")))
            l = l[0:l.find("?")]
        
        page = req(getName(l), getPath(l), port)

        if page == None:
            continue
        
        try:
            if page.decode()[0:12] == "HTTP/1.1 301" or page.decode()[0:12] == "HTTP/1.1 302":
                try:
                    lnks.remove(l)
                except:
                    pass
                find = page.decode().find("Location")
                if find != -1:
                    find = page.decode().split("Location: ")
                    l = find[1].partition("\r")[0]
                    lnks.append(l)
                    page = req(getName(l), getPath(l), port)
                else:
                    continue
        except:
            continue


        #print(page.decode())
        try:
            soup = BeautifulSoup(page, "html.parser")
        except:
            continue
    
        txt = soup.findAll("a", href=True)
        #print(txt)

        for link in linkList(txt, getName(l)):
            if link[-1] == "/":
                link = link[:-1]
            if link[0:3] == "www":
                link = "https://"+link
            if depthLevel(link) == depth and link not in lnks:
                lnks.append(link)
                print(len(lnks))

'''
Creates two files for emails links
'''
def fileCreator(depth):
    with open("links_depth"+str(depth)+".txt", "w") as l:
            for line in lnks:
                l.write(line+"\n")
    print("> Files created.")
                
'''
Creates threads that run linkExtension to a certain depth
'''
def thread_manager(depth):
    p = Pool(10)
    p.map(linkExtension, list(range(depth+1)))
    p.close()
    p.join()

    fileCreator(depth)


def main():
    if len(argv) != 2 or int(argv[1]) not in range(0, 5):
        print("Wrong args given.\n> python3 webcrawl.py [depth of 0-4]\nNote: a companies.csv file is required.")
        exit(0)
    depth = argv[1]

    start = datetime.now()
    print("Started at " + str(start))

    companies = companyList()
    for l in range(len(companyList())):
        if len(lnks) >= 50:
            break
        lnks.append(companies.pop())


    thread_manager(int(depth))
    print("It took: " + str(datetime.now() - start)[0:7])

if __name__ == '__main__':
    main()
