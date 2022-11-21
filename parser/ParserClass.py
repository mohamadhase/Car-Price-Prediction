#import the constant from /CAR PRICE PREDICTION/src/constants.py
import sys
import pandas as pd
sys.path.insert(1, 'C:/Users/moham/Desktop/CAR/src')
from  constants import PATH_REGEX
from glob import glob
from MyHTMLParser import MyHTMLParser
class Parser():
    """ this class is responsible for parsing the files and extracting the data from them """
    def __init__(self):
        self.path_regex = PATH_REGEX 
        self.files_list = glob(self.path_regex)
        self.parser = None
        self.objects = []
        self.parse()
    def parse(self):
        """ parse the files and extract the data from them using MyHTMLParser class """
        for file in self.files_list:
            with open(file, 'r',encoding='utf-8') as f:
                content = f.read()
                self.parser = MyHTMLParser()
                self.parser.feed(content)
                self.objects.append(self.parser.obj)
                self.parser.reset()
        df = pd.DataFrame([obj.__dict__ for obj in self.objects])
        df.to_csv('data.csv', index=False)


