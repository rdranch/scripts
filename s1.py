import socket, urllib.parse, ssl
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
    s.connect((url, port))

    request = "GET %s HTTP/1.1\r\nHost: %s\r\nAccept: text/html\r\nConnection: close\r\n" % (name, url)
    request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n"
    request += "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36\r\n\r\n"
    #print(request)
    s.sendall(request.encode())
    page = b""

    while True:
        data = s.recv(2048)
        if not data:
            break
        page += data
    #print(page)
    return page

def getName(link):
    if link[0] == "/":
        return "www.rit.edu"
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


lnks = ["https://www.rit.edu"]
emails = []


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
    #print(l)

    return l[2] in ["wwww.rit.edu", "library.rit.edu", "join.rit.edu", "rit.edu"]

'''
Determines if the link uses https
'''
def isSSL(link):
    return link[0:5] == "https"

'''
www remover
Not used
'''
def wwwRemover(link):
    if len(link) >= 11:
        if link[7:10] == "www":
            return "http://"+link[11:]
        if link[8:11] == "www":
            return "https://"+link[12:]
        return link
    return link

'''
Create a list with links to visit
'''
def linkList(request):
    l2v = []

    for links in request:
        #now = wwwRemover(links['href'])
        now = links['href']
        #print(now)
        if now[0:7] == "mailto:" and now[7:] not in emails:
            emails.append(now[7:])
        elif now not in l2v and len(now) >= 1 and (now[0] == 'h' or now[0] == '/') and domainInLink(now):
            if now[0] == "/":
                l2v.append(lnks[0]+now)
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
        #print(l)
        page = req(getName(l), getPath(l), port)
        #print(getName(l)+getPath(l)+":"+str(port))
        #print("start:"+page.decode())
        #page = page.decode()
        #print(page)
        #if page[0:15] != "HTTP/1.1 200 OK":
        #    continue
        soup = BeautifulSoup(page, "html.parser")
    
        txt = soup.findAll("a", href=True)
        #print(txt)

        for link in linkList(txt):
            if link[-1] == "/":
                link = link[:-1]
            if depthLevel(link) == depth and link not in lnks:
                lnks.append(link)
                #print(lnks)

'''
Creates two files for emails links
'''
def fileCreator(depth):
    with open("links_depth"+str(depth)+".txt", "w") as l:
            for line in lnks:
                l.write(line+"\n")
    with open("emails_depth"+str(depth)+".txt", "w") as e:
        for lin in emails:
            e.write(lin+"\n")
    print("> Files created.")
                
'''
Creates threads that run linkExtension to a certain depth
'''
def thread_manager(depth):
    p = Pool(10)
    p.map(linkExtension, [0, depth])
    p.close()
    p.join()

    fileCreator(depth)


def main():
    if len(argv) != 2 or int(argv[1]) not in range(0, 5):
        print("Wrong args given.\n> python3 act2D.py [depth of 0-4]")
        exit(0)
    depth = argv[1]

    start = datetime.now()
    print("Started at " + str(start))

    thread_manager(int(depth))
    print("It took: " + str(datetime.now() - start)[0:7])

if __name__ == '__main__':
    main()