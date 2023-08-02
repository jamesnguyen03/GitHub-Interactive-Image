from flask import Flask, redirect, request
import shutil
import random

FRAMES = ['static/Frame0.png', 'static/Frame1.png', 'static/Frame2.png', 'static/Frame3.png', 'static/Frame4.png',
'static/Frame5.png', 'static/Frame6.png', 'static/Frame7.png', 'static/Frame8.png', 'static/Frame9.png', 'static/Frame10.png',
'static/Frame11.png', 'static/Frame12.png'] #Contains the image paths for each frame
IDX = 0 #IDX is the index of the frame to be displayed
app = Flask(__name__)

#Setting cache to expire immediately
#Forces GitHub to request updated resources
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 

#Increments the FRAMES[IDX] so that the next FRAME can be displayed
def increment():
    global IDX
    UPPERBOUND = 8 #Increment until 8, then go back to start. In this case, I want Frames 9-12 not be visited when clicking next.

    if IDX >= len(FRAMES)-1 or IDX >= UPPERBOUND:
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

@app.route("/")
def home():
    #You can add content here if you want something to appear if someone visits directly
    return '<a href="/next"><img src="' + FRAMES[IDX] + '"></a>'

#Increment FRAMES[] to next FRAME
#Use ?redirect=(githubProfileURL) to redirect back to GitHub Profile
@app.route("/next")
def goNext():
    global IDX, FRAMES
    increment()
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

    if url == None:
        return redirect("/")
    else:
        return redirect(url)

#RANDOM
def rand(lower, upper):
    global IDX
    IDX = random.randint(lower, upper)
#Go to specified FRAMES[IDX]
#Use "?redirect=(githubProfileURL)&idx=(IDX)"
@app.route("/random")
def goRandom():
    global COUNT
    rand(9, 12)
    url = request.args.get('callback')
    if url == None:
        return redirect("/")   
    return redirect(url)
