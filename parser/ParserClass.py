#import the constant from /CAR PRICE PREDICTION/src/constants.py
import sys
import pandas as pd
sys.path.insert(1, 'C:/Users/nasser/Desktop/Car-Price-Prediction/src')
from constants import PATH_REGEX
from glob import glob
from MyHTMLParser import MyHTMLParser
from threading import Thread
class Parser():
    """ this class is responsible for parsing the files and extracting the data from them """
    def __init__(self):
        self.path_regex = PATH_REGEX 
        self.files_list = glob(self.path_regex)
        self.parser = None
        self.objects = []
        self.threads = []
        self.parsing_loop()
    def parse(self,file:str):
        """ parse the files and extract the data from them using MyHTMLParser class """
        with open(file, 'r',encoding='utf-8') as f:
            content = f.read()
            self.parser = MyHTMLParser()
            self.parser.feed(content)
            self.objects.append(self.parser.obj)
          
    def parsing_loop(self):
        """ loop over all the files and create a thread for each file """
        for file in self.files_list:

            thread = Thread(target=self.parse,args=(file,)) #            
            thread.start()
            self.threads.append(thread)
            if (self.files_list.index(file) % 10 == 0):
                print(f"Progress Threads: {str(round(self.files_list.index(file) / len(self.files_list) * 100, 2))}%")

            self.threads.append(thread)
        for thread in   self.threads:
            if ( self.threads.index(thread) % 10 == 0):
                print(f"Threads finished: {str(round( self.threads.index(thread) / len(  self.threads) * 100, 2))}%")
            thread.join()
            


        df = pd.DataFrame([obj.__dict__ for obj in self.objects])
        df.to_csv('data.csv', index=False)

