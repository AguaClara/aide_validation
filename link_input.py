from tkinter import *
import validation

root = Tk()

e = Entry(root, width=50)
e.pack()


def urlClick():
    url = 'url: ' + e.get()
    validation.validate(url)
    urlLabel = Label(root, text=url)
    urlLabel.pack()

def exitClick():
    root.destroy()


urlButton = Button(root, text='Validate OnShape Url', command=urlClick)
urlButton.pack()

exitButton = Button(root, text='Exit AIDE Validation', command=exitClick)
exitButton.pack()

root.mainloop()
