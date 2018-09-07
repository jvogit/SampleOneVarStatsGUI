from tkinter import *
from tkinter import ttk

#Application class
class Application(ttk.Frame):

    someVar = 'Default' #Setting class variables
    
    @classmethod
    def main(cls):
        #Set up your root and initial settings here!
        NoDefaultRoot()
        root = Tk()
        
        app = cls(root)
        root.mainloop()

    def __init__(self, root, **args):
        super().__init__(root, **args)
        print("Initialize Application")
        #Set up applicatiom variables, create widgets, grid widgets onto main frame
        self.root = root
        self.create_widgets()
        self.grid_widgets()
    
    def create_widgets(self):
        pass #means do nothing

    def grid_widgets(self):
        pass #I put this here to prevent compilation errors. Also indicates WIP

    #'self' argument to use class instance. equivalent to 'this' in java
    def create_variables(self):
        self.someVar = 'Hello, World!' #setting class instance variables
        pass

#Allows start
if __name__ == "__main__":
    Application.main()
