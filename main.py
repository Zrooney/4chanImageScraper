import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import filedialog
import shutil
import time
import os

def set_rootdir():
    root = Tk()
    root.filename = filedialog.askdirectory(initialdir = "")
    rootdir = (root.filename)
    root.destroy()
    return rootdir

def imageURLGetter(threadURL):

    thread = "http://boards.4chan.org/" + userInput + "/" + threadURL
    print(thread)
    threadPage = requests.get(thread)
    threadSoup = BeautifulSoup(threadPage.content, 'html.parser')
    for a in threadSoup.find_all('a', href=True):
        tempURL = a['href']
        if tempURL[-4:] in fileEndings:
            print(tempURL)
            rawImageURL.append((tempURL))
    imageURL = list(set(rawImageURL))
    print(imageURL)
    return(imageURL)

def imageDownloader(imageURL, recursiveFile = "", saveDest = ""):
    for i in imageURL:
        try:
            link = "http:" + i
            # f = urlopen(link)
            # myfile = Image.open(f)
            tempIndex = i.rfind('/')
            name = i[tempIndex + 1:]
            if recursiveFile =="":
                out_file = saveDest + os.sep + name
            else:
                out_file = saveDest + os.sep + recursiveFile + os.sep + name
            if name in out_file:
                print(name + " already exists")
            else:
                response = requests.get(link, stream=True)
                with open(out_file, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                    print("Downloaded " + name)
        except:
            print("Error Encountered")

rawImageURL = []
imageURL = []
rawThreadList = []
threadList = []
fileEndings = [".jpg",".png",".gif","webm"]
start_time = time.time()
downloadDecision = ""

userInput = input("Enter what board you wish to go to, enter just the letter and nothing else: ")
downloadDecision = input("Do you want to download all images into single file, or multiple folders? yes / no")
saveDest = set_rootdir()
#page = requests.get("http://boards.4chan.org/"+userInput+"/")

for i in range(1,11):
    if i ==1:
        page = requests.get("http://boards.4chan.org/" + userInput + "/")
        soup = BeautifulSoup(page.content, 'html.parser')
    else:
        page = requests.get("http://boards.4chan.org/" + userInput + "/" + str(i))
        soup = BeautifulSoup(page.content, 'html.parser')
    #following gets replylinks, and adds only those with link information added
    for a in soup.find_all('a', class_="replylink"):
        tempURL = a['href']
        if (tempURL[-1:].islower() == True):
            rawThreadList.append(tempURL)

threadList = list(set(rawThreadList))
print(len(threadList))

# input("Do you want to download all images into single file, or multiple folders? yes / no")
if (downloadDecision == "yes"):
    for i in range(len(threadList)):
        threadDict = (threadList[i].rsplit("/",1))
        threadFile = saveDest + os.sep + threadDict[1]
        if (os.path.exists(threadFile) != TRUE):
            os.mkdir(threadFile)
        else:
            print("File already exists.")
        #print(os.getcwd())
        #print(threadDict[0])
        #print(threadDict[1])
        rawImageURL = imageURLGetter(threadDict[0])
        imageURL = list(set(rawImageURL))
        #imageURL = imageURLGetter(threadDict[0]) // commented out to see if i can make a list and remove dupes for faster downloads, this line  does work!
        imageDownloader(imageURL, threadDict[1],saveDest)
        imageURL.append(threadDict)
else:
    for thread in threadList:
        tempIndex = thread.rfind('/')
        massThread = thread[:tempIndex]
        rawImageURL = imageURLGetter(massThread)
        imageURL = list(set(rawImageURL))
        #print(threadList)
        #print("")
        #print(imageURL)
        #print(len(imageURL))
        imageDownloader(imageURL,"",saveDest)
print("--- %s seconds ---" % (time.time() - start_time))

# if you change the set_rootdir to be hard coded, putting this true around the main will have it run indefinitley with a cooldown period of the sleep time
# keep in mind the sleep time is in seconds. Good for having a bot making a 1:1 backup of the chan.
# while True:
#     (main)
#     time.sleep(7200)
