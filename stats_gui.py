from tkinter import *
from tkinter import ttk
import threading

#Application class
class Application(ttk.Frame):

    @classmethod
    def main(cls):
        #defaults set
        NoDefaultRoot()
        root = Tk()
        app = cls(root) #Creates Application and initlialize it! see Application#__init__
        app.grid(column=1, row=1) #center the frame
        root.resizable(True, True) #allow resizeablility!!
        root.mainloop() #actually start and show the GUI

    def __init__(self, root, **args):
        super().__init__(root, **args) #Init the Frame. Application is a 'subclass' of Frame
        print("Initialize Application")
        self.root = root #Variables
        self.create_variables()
        self.create_widgets()
        self.grid_widgets()
        self.center_frame()
        self.updateThread = LiveUpdateThread(self) #Create the update thread process
        self.updateThread.start() #acually start it
        self.data_set_entry.insert(END, "1,2,3") #Fill in defaults
    
    def create_widgets(self):
        #widgets individual elements
        self.data_set_title = Label(self, text="Enter sample here Delimitter comma (,)")
        self.data_set_entry = Text(self)
        self.meanText = Label(self, text='mean: ')
        self.meanLabel = Label(self, textvariable = self.meanVar, relief='groove') #I use textvariable See create_variables this is so i can dynmically update them later!!
        self.medianText = Label(self, text='median: ')
        self.medianLabel = Label(self, textvariable = self.medianVar, relief='groove')
        self.standardDevText = Label(self, text='Sx')
        self.standardLabel = Label(self, textvariable = self.standardDevVar, relief='groove')
        pass

    def grid_widgets(self):
        #grid the widgets using the concept of columns and rows
        #this GUI has 3 rows and 6 columns !!
        self.data_set_title.grid(column=0,row=0, columnspan=6) #columnspan allows the single widget to take up 6 columns
        self.data_set_entry.grid(column=0, row=1, columnspan=6) 
        self.meanText.grid(column=0, row=2)
        self.meanLabel.grid(column=1, row=2)
        self.medianText.grid(column=2, row=2)
        self.medianLabel.grid(column=3, row=2)
        self.standardDevText.grid(column=4, row=2)
        self.standardLabel.grid(column=5, row=2)
        pass

    def create_variables(self):
        self.meanVar = StringVar(self) #These are variables in Python that I can dynmically change
        self.medianVar = StringVar(self)
        self.standardDevVar = StringVar(self)
        pass

    def center_frame(self):
        #This is copy paste so it looks neat lol it just makes the widgets take up the space in their respective column row
        for i in range(6):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i, weight=1)

#Entirely separate class this is my Thread
#You see it is a subclass of Thread. it is like in Java LiveUpdateThread extends Thread so it can inherit the properties of the class Thread
class LiveUpdateThread(threading.Thread):
    #__init__ basically constructor in Java
    def __init__(self, app):
        #B/c it is subclass thread i want to make sure it initializes the parent class Thread right. It's like 'super' in Java
        threading.Thread.__init__(self)
        #Some variables
        self.app = app
        #Not used lol
        self.exitFlag = False

    '''This will run forever in its thread. It's basically a separate process. I want the main thread to control necessary things for the program like the GUI. I dont want to block its operations.
        if you look in your task manager you might see two processes for your programs when this thing runs :OO
        It is better to locate the Updating in a separate process'''
    '''it is better to have this in a different thread. Because these operations take time and it will BLOCK the main thread.
       blocking main thread will freeze the entire program until the operations are done
       tho i dont think its entirely necessary in this simple program however it is good practice!!
       u wanna learn more learn about multithreading its very hard topic hehe'''
    def run(self):
        while True and not self.exitFlag:
            #convenience so i dont have to call self.app lol
            app = self.app

            #This parses out the Text Entry separated by commas. It returns an Array
            #So string '1,2,3,a' becomes Array of Strings [1, 2, 3, a]
            unparsed_numbers = app.data_set_entry.get(1.0, END).split(",")

            #I want this list to be all the ints i can find in the text entry. Array of ints
            PARSED_NUMBERS = list()

            #This loop loops through the splitted Array of strings unparsed_numbers
            for unparsed_number in unparsed_numbers:
                #This will check to see if the string can be an int then adds it
                try:
                    #Attempts to parse the string and add it
                    #the int function will throw a ValueError if it is not a number which we check for in this try catch thing
                    PARSED_NUMBERS.append(int(unparsed_number))
                except ValueError:
                    #This means it is not a number the int func threw an error
                    #continue means continue on the loop
                    #break means break out of the loop :O
                    continue
                    #on wards!!!
                
                #E.g. Array [1,2,3,a] this loop will successfully convert the string array into an int array
                #The PARED_NUMBERS will contain ints [1, 2, 3] and the loop filters out Strings 'a' that cannot be converted to ints
                
            PARSED_NUMBERS.sort()
            #Sort the list in ascending order

            #I want to have at least 2 numbers entered
            if(len(PARSED_NUMBERS) > 1):
                #good theres at least two numbers i want to know calculate and set the variables
                mean = self.calculateMean(PARSED_NUMBERS)
                #Dynamically setting the variable which updates the Label widget automatically :O
                app.meanVar.set(str(mean))
                median = self.calculateMedian(PARSED_NUMBERS)
                app.medianVar.set(str(median))
                sx = self.calculateStandardDeviation(PARSED_NUMBERS)
                app.standardDevVar.set(str(sx))
            else:
                #If there is no numbers i want to reset the fields
                app.meanVar.set("")
                app.medianVar.set("")
                app.standardDevVar.set("")

            pass

    #this is math angelina!!
    def calculateMean(self, array):
        #Mean calcuation
        #len function returns the length
        summation = 0
        for number in array:
            summation += number
        return summation/len(array)

    def calculateMedian(self, array):
        #Even calc of median
        if(len(array) % 2 == 0):
            halfway = int(len(array)/2)-1
            one = array[halfway]
            two = array[halfway+1]
            return self.calculateMean([one, two])
        else:
            #odd calc of median
            halfway = int(len(array)/2)
            return array[halfway]
        pass

    def calculateStandardDeviation(self, array):
        #pow function equivalant to Math.pow
        mean = self.calculateMean(array)
        summation = 0
        for number in array:
            summation += pow(number - mean, 2)
        variance = summation/(len(array)-1)
        #honestly i don't know if python had a squareroot so i can pow 0.5 hehe
        return pow(variance, 0.5)
        pass

    #not used you can ignore this
    #tho its suppose to allow the thread to 'exit gracefully' :3
    #but i was lazy
    def exitFlag():
        self.exitFlag = True

#Allows start basically the public static void main(String[] args) but shorter ;)
if __name__ == "__main__":
    Application.main()
