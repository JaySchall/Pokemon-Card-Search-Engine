from PIL import ImageTk,Image 
import tkinter as tk
import requests
from io import BytesIO
import re
import Stemmer
import math
stem = Stemmer.Stemmer("english")
# Top level window
frame = tk.Tk()
frame.title("Pokemon Card Search")
#frame.geometry('400x200')
# Function for getting Input
# from textbox and printing it 
# at label widget
cards = []
displayNum = 3
totalDocs = 13140.0
def searchCards():
    
    inp = inputtxt.get(1.0, "end-1c")
    allScores = {}
    querywords = inp.split()
    for word in querywords:
        word = stem.stemWord(word.lower())
        doc = 0
        docsfile = open("docs.txt", "r")
        for line in docsfile:
            if word <= line:
                break
            else:
                doc+=1
        invertedTuples = []
        inverted = open("inverted/inverted" + str(doc) + ".txt", "r")
        
        
        for line in inverted:
                if line.split()[1] == word:
                    print(word)
                    docs = float(line.split()[2])
                    for lineWord in line.split(" (")[1:]:
                        lineWord = re.sub("[()']", "", lineWord)
                        key,val = lineWord.strip('()').rstrip('\n').split(', ')
                        score = float(val)
                        score = score * math.log((math.log10((totalDocs+1)/docs))+1)
                        #print(key)
                        invertedTuples.append((key, score))
                        if key not in allScores:
                            allScores[key] = score
                        else:
                            allScores[key] += score

        #print("done scoring this 1")            

        inverted.close()
    sortedScores = sorted(allScores.items(), key=lambda x:x[1], reverse=True)
    w = frame.winfo_width()/displayNum
    h = frame.winfo_height()/2

    for i in range(0,displayNum):
        datafile = open("train.csv", "r")
        for line in datafile:
            split = line.split(',')
             #print(split[0])
            try:
                if sortedScores[i][0] == split[0]:
                    #print("testing")
                    response = requests.get(split[1])
                    img_data = response.content
                    imageTemp = Image.open(BytesIO(img_data))
                    scale = w/imageTemp.width
                    h = scale * imageTemp.height
                    resize_image = imageTemp.resize((int(w), int(h)))
                    img = ImageTk.PhotoImage(resize_image)  
                    #img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
                    cards[i].configure(image=img)
                    cards[i].image = img
                    #cards[i].place_forget()
                    #print(split[1])
                    break
            except:
                response = requests.get("https://cdn.shopify.com/s/files/1/0443/2366/8118/products/darkgrey_600x.png")
                img_data = response.content
                imageTemp = Image.open(BytesIO(img_data))
                resize_image = imageTemp.resize((int(w), int(h)))
                img = ImageTk.PhotoImage(resize_image)  
                #img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
                cards[i].configure(image=img)
                cards[i].image = img
                #cards[i].place_forget()
                break
        #print(sortedScores[i])
    #print(allScores)

    lbl.config(text = "Provided Input: "+inp)
  
# TextBox Creation
inputtxt = tk.Text(frame,
                   height = 1,
                   font=("Arial Bold", 20),
                   width = 50)
  
inputtxt.pack()
  
# Button Creation
printButton = tk.Button(frame,
                        text = "Search",
                        font=("Arial Bold", 20),
                        command = searchCards)
printButton.pack()
  
# Label Creation
lbl = tk.Label(frame, text = "")
lbl.pack()
response = requests.get("https://cdn.shopify.com/s/files/1/0443/2366/8118/products/darkgrey_600x.png")
img_data = response.content
imageTemp = Image.open(BytesIO(img_data))
resize_image = imageTemp.resize((100, 100))
img = ImageTk.PhotoImage(resize_image)
cardOne = tk.Label(frame, image=img)
cardOne.pack(side="left", fill="both", expand="yes")
cardTwo = tk.Label(frame, image=img)
cardTwo.pack(side="left", fill="both", expand="yes")
cardThree = tk.Label(frame, image=img)
cardThree.pack(side="right", fill="both", expand="yes")
cards.append(cardOne)
cards.append(cardTwo)
cards.append(cardThree)
frame.mainloop()