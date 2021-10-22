from html import parser
import urllib.request
from html.parser import HTMLParser
import random
import time

class Parser_detail(HTMLParser):
    
     def __init__(self):
        super().__init__()
        self.div_detail = False
        self.div_title = False
        self.h4 = False
        
        self.headline_title=[]
        self.headline_detail=[]
              
        self.target_title = ''
        self.target_detail = ''
        
     def handle_starttag(self, tag ,attr):
        d = dict(attr)
        
        if tag == "div" and self.target_detail in d.get('class',''):
            self.div_detail = True

        if tag == "div" and self.target_title in d.get('class',''):
            self.div_title = True

        if tag  == "h4":
            self.h4 = True


     def handle_endtag(self, tag):
         if tag == "div":
            self.div_detail = False
            self.div_title = False
        
         if tag == "h4":
             self.h4 = False
            
        
        
     def handle_data(self, data):
        if self.div_title:
            #print("List item:{}".format(data))
            self.headline_title.append(data)
           
        if self.div_detail and self.h4:
            self.headline_detail.append(data+'\n')
        
        if self.div_detail and not(self.h4):
            self.headline_detail.append(data)
            

     def feed(self,content,class_='',class2_=''):
        self.target_title = class_
        self.target_detail = class2_
        super().feed(content)


