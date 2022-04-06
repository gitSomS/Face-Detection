from tkinter import*
import tkinter as tk, threading
import imageio
from PIL import Image,ImageTk
import cv2 #opencv
import face_recognition #opencv

root = Tk()
root.geometry("1000x600")
main = Frame(root)
f1 = ("Arial", 20)
#video_path = cv2.VideoCapture(0) #paste your video path here

def main_f():

    #video
    vid = LabelFrame(root,relief=SOLID)
    vid.place(relx=0.25,rely=0.1, anchor="nw", relwidth=0.45,relheight=0.6)
    root.update()
    width = vid.winfo_width()
    height = vid.winfo_height()
    video = cv2.VideoCapture(0)

    print("Carregando...") 


    def display_video(label):
    # iterate through video data
        for image in video.iter_data():
            # convert array into image
            img = Image.fromarray(image)
            img2 = img.resize(((width,height)))
            # Convert image to PhotoImage
            image_frame = ImageTk.PhotoImage(image = img2)
            
            # configure video to the lable
            label.config(image=image_frame)
            label.image = image_frame
    # create and start thread
    my_vid = Label(vid)
    my_vid.pack()
    thread = threading.Thread(target=display_video, args=(my_vid,))
    thread.start()

   
main_f()
root.mainloop()