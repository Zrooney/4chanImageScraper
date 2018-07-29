from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import filedialog
import shutil
import time
from PIL import Image
def set_rootdir():
    root = Tk()
    root.filename = filedialog.askdirectory(initialdir = "")
    rootdir = (root.filename)
    root.destroy()
    return rootdir

def duplicateRemover (list):
    listFinal = []
    for i in range(len(list)):
        try:
            if list[i] != list[i + 1]:
                listFinal.append(list[i])
        except:
            print("")
    return listFinal;

rawImageURL = []
imageURL = []
rawThreadList = []
threadList = []
fileEndings = [".jpg",".png",".gif","webm"]
start_time = time.time()


userInput = input("Enter what board you wish to go to, enter just the letter and nothing else: ")
saveDest = set_rootdir()
#page = requests.get("http://boards.4chan.org/"+userInput+"/")

for  i in range(1,11):
    if i ==1:
        page = requests.get("http://boards.4chan.org/" + userInput + "/")
        soup = BeautifulSoup(page.content, 'html.parser')
    else:
        page = requests.get("http://boards.4chan.org/" + userInput + "/" + str(i))
        soup = BeautifulSoup(page.content, 'html.parser')
    for a in soup.find_all('a', href=True):
        print("Found the URL:", a['href'])
        tempURL = a['href']
        if ('/thread' in tempURL):
            tempIndex = tempURL.find('#')
            tempURL = tempURL[0:tempIndex]
            rawThreadList.append(tempURL)

threadList = duplicateRemover(rawThreadList)

for thread in threadList:
    thread = "http://boards.4chan.org"+thread
    threadPage = requests.get(thread)
    threadSoup = BeautifulSoup(threadPage.content, 'html.parser')
    for a in threadSoup.find_all('a', href=True):
        tempURL = a['href']
        if tempURL[-4:] in fileEndings:
            print(tempURL)
            rawImageURL.append((tempURL))
    imageURL = duplicateRemover(rawImageURL)

print(threadList)
print("")
print(imageURL)
print(len(imageURL))

for i in imageURL:
    try:
        link = "http:" + i
        #f = urlopen(link)
        #myfile = Image.open(f)
        tempIndex = i.rfind('/')
        name = i[tempIndex + 1:]
        out_file = saveDest+"\\"+name
        response = requests.get(link, stream=True)
        with open(out_file, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        #myfile.save(saveDest+"\\"+name)
        print("Downloaded " + name)
    except:
        print("Error Encountered")

print("--- %s seconds ---" % (time.time() - start_time))
