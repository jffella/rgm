# Python program to create a table 

from tkinter import *
from tkinter.ttk import Treeview

class Theme:
    def __init__(self, theme=None):
        self._theme = theme

    def apply(w):
        if self._theme:
            self._theme.apply(w)
        #apply theme
        if self._color:
            w.color = self._color

class Table:
    def __init__(self,root,an_array): 
        # code for creating table 
        i = 0
        for line in an_array:
            j=0
            for elem in line:
                self.e = Entry(root, width=20, fg='blue', font=('Arial',12,'bold')) 
                self.e.grid(row=i, column=j) 
                self.e.insert(END, elem) 
                j+=1 
            i+=1

# take the data 
lst = [(1,'Raj','Mumbai',19), 
	(2,'Aaryan','Pune',18), 
	(3,'Vaishnavi','Mumbai',20), 
	(4,'Rachna','Mumbai',21), 
	(5,'Shubham','Delhi',21)] 

# create root window 
root = Tk() 
t = Table(root,lst) 
tree = Treeview(root, columns=("ID","Region","Ville","Poids"))
root.mainloop() 
