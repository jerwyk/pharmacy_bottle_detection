import urllib.request

urls = open('urls.txt')

i = 0

for url in urls:
    #urllib.request.urlr etrieve(url, )
    try:
        f = open('pics\\vitamin\\' + str(i) + r".jpg", 'wb')
        i += 1
        f.write(urllib.request.urlopen(url).read())
        f.close()
        print(i)       
    except:
        print("failed")