from tkinter import*
import tkinter as tk, threading
import imageio
from PIL import Image,ImageTk

root = Tk()
root.geometry("1000x600")
main = Frame(root)
f1 = ("Arial", 20)
video_path = "5.mp4" #paste your video path here
def main_f():
    main.pack(fill="both", expand=1)
    #title
    Label(main, text="CCTV Control", font=f1, relief=SOLID).place(relx=0.25, rely=0, anchor="nw", relwidth=0.45, relheight=0.1)
    #listbox
    listbox = Text(root, relief=SOLID)
    listbox.place(relx=0, rely=0, anchor="nw", relwidth=0.25, relheight=0.7)
    listbox.configure(state=DISABLED)
    #video
    vid = LabelFrame(root,relief=SOLID)
    vid.place(relx=0.25,rely=0.1, anchor="nw", relwidth=0.45,relheight=0.6)
    root.update()
    width = vid.winfo_width()
    height = vid.winfo_height()
    video = imageio.get_reader(video_path)
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

    #text
    text = Text(root, relief=SOLID)
    text.place(relx=0.7, rely=0, anchor="nw", relwidth=0.3, relheight=0.5)
    #Button Area DataBase
    #Button(main,text="Button",font=f1, relief=SOLID).place(relx=0, rely=0.7, anchor="nw", relwidth=0.25, relheight=0.3)
    Button(main, text="submit",relief=SOLID).place(relx=0.5,rely=0.55, anchor="center")

    #Button2
    Button(main,text="Button2",font=f1, relief=SOLID).place(relx=0.25, rely=0.7, anchor="nw", relwidth=0.45, relheight=0.3)
    #input field
    inf = LabelFrame(root,relief=SOLID)
    inf.place(relx=0.7,rely=0.5, anchor="nw", relwidth=0.3,relheight=0.5)
    Label(inf, text="Name").place(relx=0.2,rely=0.1, anchor="nw")
    entry_name = Entry(inf)
    entry_name.place(relx=0.4,rely=0.1, anchor="nw")

    Label(inf, text="Apelido").place(relx=0.2,rely=0.2, anchor="nw")
    entry_apelido = Entry(inf)
    entry_apelido.place(relx=0.4,rely=0.2, anchor="nw")

    Label(inf, text="Pontos").place(relx=0.2,rely=0.3, anchor="nw")
    entry_pontos = Entry(inf)
    entry_pontos.place(relx=0.4,rely=0.3, anchor="nw")

    Label(inf, text="Crime").place(relx=0.2,rely=0.4, anchor="nw")
    entry_crime = Entry(inf)
    entry_crime.place(relx=0.4,rely=0.4, anchor="nw")
    def submit():
        listbox.configure(state=NORMAL)
        info = "{},{},{},{}\n".format(entry_name.get(),entry_apelido.get(),entry_pontos.get(),entry_crime.get())
        listbox.insert(END,info)
        listbox.configure(state=DISABLED)
    Button(inf, text="submit", command=submit).place(relx=0.5,rely=0.55, anchor="center")
main_f()
root.mainloop()