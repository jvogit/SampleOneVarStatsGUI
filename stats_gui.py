from tkinter import *
from tkinter import ttk
import threading

#Application class
class Application(ttk.Frame):
    
    @classmethod
    def main(cls):
        NoDefaultRoot()
        root = Tk()
        app = cls(root)
        app.grid(column=1, row=1)
        root.resizable(True, True)
        root.mainloop()

    def __init__(self, root, **args):
        super().__init__(root, **args)
        print("Initialize Application")
        self.root = root
        self.create_variables()
        self.create_widgets()
        self.grid_widgets()
        self.center_frame()
        self.updateThread = LiveUpdateThread(self)
        self.updateThread.start()
    
    def create_widgets(self):
        self.data_set_title = Label(self, text="Enter sample here")
        self.data_set_entry = Text(self)
        self.meanText = Label(self, text='mean: ')
        self.meanLabel = Label(self, textvariable = self.meanVar, relief='groove')
        self.medianText = Label(self, text='median: ')
        self.medianLabel = Label(self, textvariable = self.medianVar, relief='groove')
        self.standardDevText = Label(self, text='Sx')
        self.standardLabel = Label(self, textvariable = self.standardDevVar, relief='groove')
        pass

    def grid_widgets(self):
        self.data_set_title.grid(column=0,row=0, columnspan=6)
        self.data_set_entry.grid(column=0, row=1, columnspan=6)
        self.meanText.grid(column=0, row=2)
        self.meanLabel.grid(column=1, row=2)
        self.medianText.grid(column=2, row=2)
        self.medianLabel.grid(column=3, row=2)
        self.standardDevText.grid(column=4, row=2)
        self.standardLabel.grid(column=5, row=2)
        pass

    def create_variables(self):
        self.meanVar = StringVar(self)
        self.medianVar = StringVar(self)
        self.standardDevVar = StringVar(self)
        pass

    def center_frame(self):
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i, weight=1)

class LiveUpdateThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app
        self.exitFlag = False

    def run(self):
        while True and not self.exitFlag:
            app = self.app

            unparsed_numbers = app.data_set_entry.get(1.0, END).split(",")
            PARSED_NUMBERS = list()
            
            for unparsed_number in unparsed_numbers:
                try:
                    PARSED_NUMBERS.append(int(unparsed_number))
                except ValueError:
                    continue
            PARSED_NUMBERS.sort()
            
            if(len(PARSED_NUMBERS) > 1):
                mean = self.calculateMean(PARSED_NUMBERS)
                app.meanVar.set(str(mean))
                median = self.calculateMedian(PARSED_NUMBERS)
                app.medianVar.set(str(median))
                sx = self.calculateStandardDeviation(PARSED_NUMBERS)
                app.standardDevVar.set(str(sx))
            else:
                app.meanVar.set("")
                app.medianVar.set("")
                app.standardDevVar.set("")
                
            pass

    def calculateMean(self, array):
        summation = 0
        for number in array:
            summation += number
        return summation/len(array)

    def calculateMedian(self, array):
        if(len(array) % 2 == 0):
            halfway = int(len(array)/2)-1
            one = array[halfway]
            two = array[halfway+1]
            return self.calculateMean([one, two])
        else:
            halfway = int(len(array)/2)
            return array[halfway]
        pass

    def calculateStandardDeviation(self, array):
        mean = self.calculateMean(array)
        summation = 0
        for number in array:
            summation += pow(number - mean, 2)
        variance = summation/(len(array)-1)
        return pow(variance, 0.5)
        pass

    def exitFlag():
        self.exitFlag = True

#Allows start
if __name__ == "__main__":
    Application.main()
