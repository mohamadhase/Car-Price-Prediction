# h3 -> jsut one for the company and the model name  ->>done
# h5 -> first two are year and price ->>done
# td -> for the rest of the features -> table counts -> 5 , 7 ,9  ->>done
# ul li -> first ul contains all the additional info discard the rest

from html.parser import HTMLParser
from data_handler import CarFeatures
class MyHTMLParser(HTMLParser):
    """ this class inherits from HTMLParser class and it is responsible for parsing the files and extracting the data from them """
    def __init__(self, *, convert_charrefs: bool = ...) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.obj = CarFeatures()
        self.last_tag = None
        self.h3 = False
        self.h5_count = 0
        self.td_count = 1
        self.table_count = 0
        self.last_att = None
        self.ul_count = 0
    def handle_starttag(self, tag, attrs):
        """ this method is responsible for handling the start tags in the html file
        Args:
            tag (str): the tag name
            attrs (list): the attributes of the tag
        """

        if tag in ['h3', 'h5','td','li'] :
            self.last_tag = tag
        else:
            self.last_tag = None
        if tag == 'table':
            self.table_count+=1
            self.last_att = None
        if tag == 'ul':
            self.ul_count+=1

    def handle_data(self, data):
        """ this method is responsible for handling the data in the html file """
        if self.last_tag == 'h3' and not self.h3:
            #company name and model name separated by space
            self.obj.add_feature('اسم السيارة', data)
            self.h3 = True
        if self.last_tag =='h5' and data.split() and self.h5_count < 2:

            if self.h5_count == 0:
                self.obj.add_feature('السنة', data.split()[2])
                self.h5_count+=1
            elif self.h5_count == 1:
                self.obj.add_feature('السعر', data.split()[0])
                self.h5_count+=1
        if self.last_tag =='td' and data.split() and self.table_count==5 :
                if self.last_att == None:
                    self.last_att = data
                else:
                    self.obj.add_feature(self.last_att, data)
                    self.last_att = None

        if self.last_tag =='td' and data.split() and (self.table_count==7 or self.table_count==6):

            if self.last_att == None:
                self.last_att = data
            else:
                try :
                    self.obj.add_feature(self.last_att, data.split()[-1])
                    self.last_att = None
                except :
                    pass
        if self.last_tag =='td' and data.split() and (self.table_count==9 or self.table_count==8) :
            if self.last_att == None:
                self.last_att = data
            else:
                self.obj.add_feature(self.last_att, data.split()[-1])
                self.last_att = None
        if self.last_tag =='li' and data.split() and self.ul_count==1:
            self.obj.add_feature('ملاحظات', data)