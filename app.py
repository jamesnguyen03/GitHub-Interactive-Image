from flask import Flask, redirect, request
import shutil
import random

FRAMES = ['static/Frame0.png', 'static/Frame1.png', 'static/Frame2.png', '...'] #Contains the image paths for each frame
IDX = 0 #IDX is the index of the frame to be displayed
app = Flask(__name__)

#Setting cache to expire immediately
#Forces GitHub to request updated resources
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 

#Increments the FRAMES[IDX] so that the next FRAME can be displayed
#If IDX is incremented out of range, IDX = 0
def increment():
    global IDX
    if IDX >= len(FRAMES)-1:
        print(len(FRAMES))
        IDX = 0
    else:
        IDX = IDX + 1

#If 'i' is out of range, IDX = 0
def setIdx(i):
    global IDX
    if IDX >= len(FRAMES):
        IDX = 0
    else:
        IDX = i

#Copies the FRAMES[IDX] image and makes it "DISPLAY.png"
def copyFile(filePath):
    #Specify path of image to be updated and displayed on GitHub
    #Example: <img src="(public ip)/pathTo/DISPLAY.png">
    #When deploying, Users will need to be given WRITE access to DISPLAY.png
    shutil.copyfile(filePath, "static/DISPLAY.png")

@app.route("/")
def home():
    #You can add content here if you want something to appear if someone visits directly
    return '<a href="/next"><img src="/static/DISPLAY.png"></a>'

#Increment FRAMES[] to next FRAME
#Use ?redirect=(githubProfileURL) to redirect back to GitHub Profile
@app.route("/next")
def goNext():
    global IDX, FRAMES
    increment()
    copyFile(FRAMES[IDX])

    url = request.args.get('redirect')
    if url == None:
        return redirect("/")
    else:
        return redirect(url)

#Go to specified FRAMES[IDX]
#Use "?redirect=(githubProfileURL)&idx=(IDX)"
@app.route("/jump")
def jumpTo():
    global IDX, FRAMES
    url = request.args.get('redirect')
    idx = request.args.get('idx')

    if idx == None:
        setIdx(0)
    else:
        setIdx(int(idx))
    copyFile(FRAMES[IDX])

    if url == None:
        return redirect("/")
    else:
        return redirect(url)

