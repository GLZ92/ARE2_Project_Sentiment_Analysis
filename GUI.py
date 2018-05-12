#!/usr/bin/python

#import Tkinter
from Tkinter import *
import ttk
import tkMessageBox

import os
import HTMLParser
import re

#classe tasks
class Task:
    def __init__(self, _titolo, _categorie, _descrizione, _labels, classi):
        self.titolo = _titolo
        self.categorie = _categorie
        self.descrizione = _descrizione
        self.labels = _labels
        self.nClassi = classi

#funzioni
stopwords = []
for line in open('stopwords.txt','r').readlines():
    stopwords.append(line.strip())

def isAStopWord(x):
	if x.lower() in stopwords:
		return True
	return False

def containsDigit(x):
	digit = 0;
	while digit <= 9:
		if x.find(str(digit)) != -1:
			return True
		digit = digit + 1
	return False

def isOK(x):
	# scarto parole troppo corte e parole che rappresentano menzioni tweet o numeri
	if (x.find("@") != -1) or (len(x) < 3) or (x.find("co/") != -1) or (x.find("*") != -1) or (x.find("http:") != -1) or (containsDigit(x)) or (isAStopWord(x)):
		return False
	return True


def fixTweet(x):
    # rimpiazzo alcuni caratteri con spazi
    x = x.replace("\\n", " ")
    x = x.replace("/ht", " ")
    x = x.replace("RT", " ")
    x = x.replace("RT:", " ")
    x = x.replace(",", " , ")
    x = x.replace(".", " . ")
    x = x.replace("..", " ")
    x = x.replace("...", " ")
    x = x.replace("-", " ")
    x = x.replace("'", " ")
    x = x.replace("\"", " ")
    x = x.replace("?", " ")
    x = x.replace("!", " ")
    x = x.replace("+", " ")
    x = x.replace("*", " ")
    x = re.sub("[(]([aA-zZ]+)", "( $1", x)
    x = re.sub("([aA-zZ]+)[)]", " $1 )", x)
    x = re.sub("[<]([aA-zZ]+)", "< $1", x)
    x = re.sub("([aA-zZ]+)[>]", " $1 >", x)
    x = x.replace("  ", " ")

    x = HTMLParser.HTMLParser().unescape(x)
    sentence = x.split()

    fixedSentence = ""
    for word in sentence:
        if (isOK(word)):
            fixedSentence = fixedSentence + " " + word

    fixedSentence = fixedSentence.lstrip()
    fixedSentence = fixedSentence.rstrip()
    return fixedSentence

#creazione window
window = Tk()
window.title("Tweets classification")
window.geometry('1280x720')
window.resizable(width=False, height=False)

#creazione scelte
t1 = Task("EI-oc", ["angry", "fear", "joy", "sadness"], "Given:\n-a tweet\n-an emotion E (anger, fear, joy, or sadness)\nTask: classify the tweet into one of four ordinal classes of intensity of E that best represents the mental state of the tweeter:", "\n0: no E can be inferred\n1: low amount of E can be inferred\n2: moderate amount of E can be inferred\n3: high amount of E can be inferred\nFor each language.", 4)
t2 = Task("V-oc", [], "Given:\n-a tweet\nTask: classify the tweet into one of seven ordinal classes, corresponding to various levels of positive and negative\nsentiment intensity, that best represents the mental state of the tweeter:", "\n3: very positive mental state can be inferred\n2: moderately positive mental state can be inferred\n1: slightly positive mental state can be inferred\n0: neutral or mixed mental state can be inferred\n-1: slightly negative mental state can be inferred\n-2: moderately negative mental state can be inferred\n-3: very negative mental state can be inferred.", 7)
t3 = Task("V-oc-3c", [], "Given:\na tweet\nTask: classify the tweet into one of three ordinal classes:", "\n0: negative\n1: neutral\n2: positive", 3)
tasks = [t1, t2, t3]

#opzioni
limchars = 280

#valori
choosenTask = StringVar(window)
choosenCategory = StringVar(window)
choosenCategory.set(tasks[0].categorie[0]) # default value
choosenTask.set(tasks[0].titolo) # default value

#creazione eventi
def scelgoTask(event):
    if choosenTask.get() == tasks[0].titolo:
        readDescription.config(text=tasks[0].descrizione + tasks[0].labels)
    else:
        if choosenTask.get() == tasks[1].titolo:
            readDescription.config(text=tasks[1].descrizione + tasks[1].labels)
        else:
            readDescription.config(text=tasks[2].descrizione + tasks[2].labels)

    if choosenTask.get() != tasks[0].titolo:
        menuCategory.configure(state="disabled")
    else:
        menuCategory.configure(state="active")

def premoSubmit(event):
    tweet = textTweet.get("1.0",END).strip()
    index = 0

    if len(tweet) == 0:
        tkMessageBox.showerror("ERROR!!!", "Insert tweet")
    else:
        if len(tweet) > 280:
            tkMessageBox.showerror("ERROR!!!", "Tweet text can have at most 280 characters")
        else:
            task_category = choosenTask.get()
            counter = 0
            for t in tasks:
                if t.titolo == task_category:
                    index = counter
                    break
                counter = counter + 1

            hdf5file = choosenTask.get()

            if task_category == "EI-oc":
                task_category = task_category + "/" + choosenCategory.get()
                hdf5file = choosenTask.get() + "-" + choosenCategory.get()

            fileNameRoot = "custom_data/" + task_category

            #creo file con il tweet inserito
            testSet = fileNameRoot + "/En-test.txt"
            record = str(tasks[index].nClassi - 1) + " " + fixTweet(tweet)
            testFile  = open(testSet, "w")
            testFile.write(record)
            testFile.close()

            model = hdf5file + ".t7"
            predictionFile = fileNameRoot + "_predictions.txt"

            cmd1 = "python preprocess0.py custom --test " + testSet + " --custom_name " + hdf5file
            cmd2 = "th main0.lua -data " + hdf5file +  ".hdf5 -debug 0 -warm_start_model results/" + model + " -test_only 1 -preds_file " + predictionFile

            v1 = os.system(cmd1) #eseguo preprocess0
            print cmd1
            if v1 != 0:
                os.exit()
            print cmd2
            v2 = os.system(cmd2) #eseguo main0
            if v2 != 0:
                os.exit()

            #recupero valore predizione
            f = open(predictionFile)
            prediction = f.readlines()[0]

            if task_category == "V-oc":
                prediction = str(int(prediction) - 3)

            predictedClass = ""
            print("Predizione = " + str(prediction))
            for label in tasks[index].labels.split("\n"):
                if label.find(str(prediction).strip()) != -1:
                    predictedClass = label
                    break
            tkMessageBox.showinfo("RESULT", predictedClass)


#creo le due panedwindow
left = PanedWindow(window)
left.pack(side=LEFT, fill="both")
right = PanedWindow(window)
right.pack(side=RIGHT)

#creazione frame
frameTweet = LabelFrame(left, text="Tweet to classify")
frameTweet.pack(side=TOP, expand=YES, fill="both")

frameTask = LabelFrame(left, text="Task")
frameTask.pack(side=TOP, expand=YES, fill="both")

frameCategory = LabelFrame(left, text="Category")
frameCategory.pack(side=TOP, expand=YES, fill="both")

frameButton = LabelFrame(left, text="")
frameButton.pack(side=TOP, expand=YES, fill="both")

frameDescription = LabelFrame(right, text="Description task")
frameDescription.pack(side=TOP, expand=YES, fill="both")

#widget che popolerano frameTweet
labelTweet = Label(frameTweet)
labelTweet["text"] = "Insert tweet: "
labelTweet.pack(side=LEFT)

textTweet = Text(frameTweet, height=3, width=50)
textTweet.pack(side=LEFT)

#widget che popolerano frameTask
labelTask = Label(frameTask)
labelTask["text"] = "Select task: "
labelTask.pack(side=LEFT)

menuTask = OptionMenu(frameTask, choosenTask, *[tasks[0].titolo, tasks[1].titolo, tasks[2].titolo], command=scelgoTask)
menuTask.pack(side=LEFT)

#widget che popolerano frameTask
labelCategory = Label(frameCategory)
labelCategory["text"] = "Select category: "
labelCategory.pack(side=LEFT)

menuCategory = OptionMenu(frameCategory, choosenCategory, *tasks[0].categorie)
menuCategory.pack(side=LEFT)

#frame button
submitButton = Button(frameButton)
submitButton["text"] = "Start classification"
submitButton.place(relx=0.5, rely=0.5, anchor=CENTER)
submitButton.bind("<Button-1>", premoSubmit)

#widget che popoleranno frameDescription
readDescription = Label(frameDescription, height=30, width=300)
readDescription.config(text=tasks[0].descrizione  + "\n" + tasks[0].labels)
readDescription.pack(side=LEFT)


window.mainloop()
