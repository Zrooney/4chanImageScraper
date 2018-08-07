from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import filedialog
import shutil
import time
import os
#from PIL import Image

def set_rootdir():
    root = Tk()
    root.filename = filedialog.askdirectory(initialdir = "")
    rootdir = (root.filename)
    root.destroy()
    return rootdir

# def duplicateRemover (list):
#     listFinal = []
#     for i in range(len(list)):
#         try:
#             if list[i] != list[i + 1]:
#                 listFinal.append(list[i])
#         except:
#             print("")
#     return listFinal;

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

def imageDownloader(imageURL, fileLocation = ""):
    for i in imageURL:
        try:
            link = "http:" + i
            # f = urlopen(link)
            # myfile = Image.open(f)
            tempIndex = i.rfind('/')
            name = i[tempIndex + 1:]
            print(name)
            if fileLocation =="":
                out_file = saveDest + os.sep  + name
            else:
                out_file = saveDest + os.sep + fileLocation + os.sep + name
            response = requests.get(link, stream=True)
            with open(out_file, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            # myfile.save(saveDest+"\\"+name)
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

rawThreadList = list(set(rawThreadList))


# input("Do you want to download all images into single file, or multiple folders? yes / no")
if (downloadDecision == "yes"):
    for i in range(len(rawThreadList)):
        threadDict = (rawThreadList[i].rsplit("/",1))
        threadFile = saveDest + os.sep + threadDict[1]
        os.mkdir(threadFile)
        print(threadDict[0])
        print(threadDict[1])
        imageLink = imageURLGetter(threadDict[0])
        imageDownloader(imageLink, threadDict[1])
        imageURL.append(threadDict)
else:
    for thread in threadList:
        thread = "http://boards.4chan.org"+thread
        threadPage = requests.get(thread)
        threadSoup = BeautifulSoup(threadPage.content, 'html.parser')
        for a in threadSoup.find_all('a', href=True):
            tempURL = a['href']
            if tempURL[-4:] in fileEndings:
                print(tempURL)
                rawImageURL.append((tempURL))
        imageURL = list(set(rawImageURL))

        print(threadList)
        print("")
        print(imageURL)
        print(len(imageURL))

        slashType = os.sep

        for i in imageURL:
            try:
                link = "http:" + i
                #f = urlopen(link)
                #myfile = Image.open(f)
                tempIndex = i.rfind('/')
                name = i[tempIndex + 1:]
                out_file = saveDest+slashType+name
                response = requests.get(link, stream=True)
                with open(out_file, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                #myfile.save(saveDest+"\\"+name)
                print("Downloaded " + name)
            except:
                print("Error Encountered")

print("--- %s seconds ---" % (time.time() - start_time))
