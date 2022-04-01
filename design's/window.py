from tkinter import *


def btn_clicked():
    print("Button Clicked")


window = Tk()

window.geometry("1902x108")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 108,
    width = 1902,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    0.0, 0.0,
    image=background_img)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = -35, y = 19,
    width = 74,
    height = 33)

canvas.create_text(
    24.0, -5.5,
    text = "Cidadao recebeu -1 ponto",
    fill = "#000000",
    font = ("MS-Sans-Serif", int(11.0)))

window.resizable(False, False)
window.mainloop()
