import tkinter as tk
import os
import cv2
import sys
from PIL import Image, ImageTk
import PDFMaker
import shutil
from pathlib import Path

count = 0

directory = "./Images/"

if os.path.exists("Images"):
    shutil.rmtree('Images')
    Path(directory).mkdir(parents=True, exist_ok=True)



fileName = os.environ['ALLUSERSPROFILE'] + "/WebcamCap.txt"
cancel = False

def prompt_ok(event = 0):
    global cancel, button, button1, button2
    cancel = True

    button.place_forget()
    button1 = tk.Button(mainWindow, text="Save Image!", command=saveImage)
    button2 = tk.Button(mainWindow, text="Try Again", command=resume)
    button1.place(anchor=tk.CENTER, relx=0.2, rely=0.9, width=150, height=50)
    button2.place(anchor=tk.CENTER, relx=0.8, rely=0.9, width=150, height=50)
    button1.focus()

def saveImage(event = 0):
    global prevImg, count

    count = count + 1
    print("count: " + str(count))
    if (len(sys.argv) < 2):
        filepath =  directory + str(count) + ".png"
    else:
        filepath = sys.argv[1]

    print ("Output file to: " + filepath)
    prevImg.save(filepath)
    


def resume(event = 0):
    global button1, button2, button, lmain, cancel

    cancel = False

    button1.place_forget()
    button2.place_forget()

    mainWindow.bind('<Return>', prompt_ok)
    button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9, anchor=tk.CENTER, width=300, height=50)
    lmain.after(10, show_frame)

def changeCam(event=0, nextCam=-1):
    global camIndex, cap, fileName

    if nextCam == -1:
        camIndex += 1
    else:
        camIndex = nextCam
    del(cap)
    cap = cv2.VideoCapture(camIndex)

    #try to get a frame, if it returns nothing
    success, frame = cap.read()
    if not success:
        camIndex = 0
        del(cap)
        cap = cv2.VideoCapture(camIndex)

    f = open(fileName, 'w')
    f.write(str(camIndex))
    f.close()

try:
    f = open(fileName, 'r')
    camIndex = int(f.readline())
except:
    camIndex = 0

cap = cv2.VideoCapture(camIndex)
cap.set(3, 1920)
cap.set(4, 1080)


capWidth = cap.get(6)
capHeight = cap.get(8)

success, frame = cap.read()
if not success:
    if camIndex == 0:
        print("Error, No webcam found!")
        sys.exit(1)
    else:
        changeCam(nextCam=0)
        success, frame = cap.read()
        if not success:
            print("Error, No webcam found!")
            sys.exit(1)


mainWindow = tk.Tk(screenName="White Board Recorder")
mainWindow.resizable(width=True, height=True)
#mainWindow.geometry("1000x500")
mainWindow.bind('<Escape>', lambda e: mainWindow.quit())
lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
button = tk.Button(mainWindow, text="Capture", command=prompt_ok)
button_changeCam = tk.Button(mainWindow, text="Switch Camera", command=changeCam)

lmain.pack()
button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9, anchor=tk.CENTER, width=300, height=50)
button.focus()
button_changeCam.place(bordermode=tk.INSIDE, relx=0.85, rely=0.1, anchor=tk.CENTER, width=150, height=50)

def show_frame():
    global cancel, prevImg, button

    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    prevImg = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if not cancel:
        lmain.after(10, show_frame)

show_frame()
mainWindow.mainloop()
print("Video Closed!")
PDFMaker.MakePDF()
