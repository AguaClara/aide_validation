from tkinter import *
import validator

root = Tk()

e = Entry(root, width=50)
e.pack()


def urlClick():
    url = e.get()
    validator = Validator()
    message = validator.validate(url)
    urlLabel = Label(root, text=message)
    urlLabel.pack()

def exitClick():
    root.destroy()


urlButton = Button(root, text='Validate OnShape Url', command=urlClick)
urlButton.pack()

exitButton = Button(root, text='Exit AIDE Validation', command=exitClick)
exitButton.pack()

root.mainloop()
