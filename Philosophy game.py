import urllib
from bs4 import BeautifulSoup as bs
import re
import time

class Philosophy_Game(object):
    
    def __init__(self,url_page):
        self.page = url_page    # Wikipedia Page
        self.counter = 0        # no. of cycles to get to philosophy
        self.flag = False       # flag when stucking in a loop
        self.max_steps = 100    # max no. of cycles
        self.prev_urls = [url_page[24:]]    # all the urls we visiten including the first one
        
    def get_page(self):
        self.req = urllib.request.Request(self.page)    
        self.content = urllib.request.urlopen(self.req).read()  # get the page

        self.soup = bs(self.content,"html.parser")  # parse it
  
        self.title = self.soup.findAll("h1", {"class" : "firstHeading"})[0].contents[0] # get the title of the page
    
        if isinstance(self.title, str):     # if the title is inside another tag e.g. <b>title</b>
            print("Article:",self.title)
        else:
            print("Article:",self.title.contents[0])
                

        self.maincontent = self.soup.findAll("div", { "class" : "mw-parser-output" })[0]    # get main body
        self.paragraphs = self.maincontent.findAll("p")  # get paragraphs inside the body
        
    def get_link(self):
        self.links = [] # all the links availible in the paragphs

        for p in self.paragraphs:
            if len(p.findAll("a")) > 1:
                for i in p.findAll("a"): # extracting only "Normal" links
                    if re.match(r'\/wiki\/[^"]+',str(i.get("href"))) and "/wiki/Help:IPA" not in str(i.get("href")):
                        if "[" not in i.contents[0] and "]" not in i.contents[0] and i.contents[0] != "listen" and isinstance(i.contents[0],str):
                            
                            self.links.append((i.contents[0],i.get("href")))                               

    def Initiate(self):
        while self.counter <= self.max_steps and not self.flag: # the loop ends if we stuck in a loop or the cycles reaches 100
            
            self.get_page()
            self.get_link()
            
            if self.title == "Philosophy": # break the loop when Philosophy is reached
                break 
            
            self.num = 0
            for link,url in self.links:     # subing the first "Valid" link with self.page and start other loop
                if url not in self.prev_urls:
                    self.prev_urls.append(url)  # adding the "valid" link to our "visited links" list
                    self.page = "https://en.wikipedia.org"+url
                    self.num += 1 
                    break
                if url[self.num] == self.prev_urls[-2]:
                    print("Stuck in a Loop!!")
                    self.flag = True
                    break  
            self.counter += 1  
            time.sleep(0.5) # 0.5 second timeout between queries to avoid heavy load on Wikipedia
            
if __name__ == "__main__":
    
    phil = Philosophy_Game(input("Enter a wikipedia page: "))
    phil.Initiate()   
    print("\n\nIt took",phil.counter,"cycles to get to Philosophy!")                  