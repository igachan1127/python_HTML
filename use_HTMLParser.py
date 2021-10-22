from html import parser
import urllib.request
from html.parser import HTMLParser
import random
import time
from detail_HTML import Parser_detail

class Parser_title(HTMLParser):

    def __init__(self):
        super().__init__()
        self.a=False
        self.td=False
        self.tdday=False
        
        self.headline_title=[]
        self.headline_day=[]
        self.headline_link=[]
              
        self.target_title = ''
        self.target_day = ''
        

    def handle_starttag(self,tag,attr):
        d = dict(attr)
        
        if tag == "td" and self.target_title in d.get('class',''):
            self.td=True

        if tag == "td" and self.target_day in d.get('class',''):
            self.tdday=True

        if tag == "a" :
             self.a = True
        
        if tag == "a" and self.td:
            self.headline_link.append(d["href"])

            
    def handle_endtag(self, tag):
        if tag == "a":
            self.a = False
    

    def handle_data(self,data):
        
        if self.td:
            #print("List item:{}".format(data))
            self.headline_title.append(data)
            if not(self.a):
                self.headline_link.append('***')
            self.td=False

        if self.tdday and not(self.a) and '2021' in data:
            self.headline_day.append(data+'\n')
            self.tdday=False


    def feed(self,content,class_='',class2_=''):
        self.target_title= class_
        self.target_day = class2_    
        super().feed(content)




def wait():
    i=0
    i=int(random.randrange(3,6,2))
    print('please wait' + ' ' + str(i) + 'sec')
    time.sleep(i)
    return

def main():
    res = urllib.request.urlopen("https://www.jpcert.or.jp/at/2021.html")
    html = res.read()
    str = html.decode()
    parser = Parser_title()
    parser.feed(str,class_='at_link',class2_='c')
    #print(parser.headline_texts2[0])
    with open("./title.txt",'w',encoding='utf-8') as file:
        for i,j,k in zip(parser.headline_title,parser.headline_day,parser.headline_link):
            if('***' in k):
                file.write("更新日："+ j + i + '\n' + k + '\n')
                file.write('-----------------------'+'\n')
            
            else:
                file.write("更新日："+ j + i + '\n' + "https://www.jpcert.or.jp"+k + '\n')
                file.write('-----------------------'+'\n')

    for i,k in zip(parser.headline_title,parser.headline_link):
        #wait()
        if('***' in k):
            continue
        
        res = urllib.request.urlopen("https://www.jpcert.or.jp"+k)
        html = res.read()
        str = html.decode()
        parser = Parser_detail()
        parser.feed(str, class_='page_title_area', class2_='at')

        path = './JPCERT/'
        with open(path + i + '.txt' ,'w',encoding='utf-8') as file:
            for j in parser.headline_title:
                file.write(j)
            
            for l in parser.headline_detail:
                file.write(l)

        break


if __name__ == '__main__':
    main()


