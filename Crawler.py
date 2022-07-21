import bs4 
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
class crawl(str): 
    
    def data(self,name):
        from urllib.request import urlopen
        import bs4 
        with urlopen(name) as response:
            data = response.read().decode("utf-8")
            root= bs4.BeautifulSoup(data,'html.parser')
            text = root.find_all("meta",{"itemprop":"description"},"content")[0]["content"]
            url = root.find("a",{"target":"_blank"})["href"]
            result = root.find_all('div',{"class":"point_list"})
            if len(result) == 1:
                traffic = result[0].div.p.text
                address = root.find("a",{"target":"_blank"}).span
                if address ==None:
                    return [text,traffic,url]
                else:
                    address= address.text
                    return [text,address,traffic,url] 
            elif len(result) == 0: 
                address = root.find("div",{"class":"address"})
                if address ==None:
                    return [text]
                else: 
                    address = address.p.span.text
                    return [text,address]
            else:   
                address = root.find("a",{"target":"_blank"}).span.text
                opening_time = result[0].p.text
                fee = result[1].p.text
                return [text,address,opening_time,fee,url]
    def google_search(self,name):
        op = Options()
        op.binary_location =  "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
        op.use_chromium = True
        op.add_argument('--disable-gpu') 
        op.add_argument('--headless')
        driver = webdriver.Chrome(executable_path =r'C:\chromedriver.exe',options=op)
        driver.get(name)
        source = driver.page_source
        root= bs4.BeautifulSoup(source,'html.parser')
        # text = root.find_all("div",{"class":"f4hh3d"},limit=5)
        text = root.find_all("div",{"class":"f4hh3d"})
        img_stars = []
        for i in text:
            src = i.find("div",{"class":"kXlUEb"})
            src = src.find("easy-img",{"class":"dBuxib SCkDmc"})
            # src= src.img['src'] #src: 圖片來源
            try :
                src= src.img['src']
            except:
                src = src.img['data-src']
            # if src.img['src'] == None:
            #     src = src.img['data-src']
            # else:
            #     src= src.img['src'] #src: 圖片來源
            # print(src,sys.stderr)
            fig = i.find("div",{"class":"GwjAi"}) #fig:位置
            comment = fig.find("div",{"class":"nFoFM"}).text
            fig = fig.find("div",{"class":"rbj0Ud AdWm1c"})
            fig = fig.find("div",{"class":"skFvHc YmWhbc"}).text
            stars = i.find("div",{"class":"GwjAi"})
            stars= stars.find("div",{"class":"tP34jb"})
            try : 
                stars = stars.span["aria-label"]
            except :
                stars = None
            # print(fig,sys.stderr)
            # print(stars,sys.stderr)
            # stars = stars.find("span",{"class":"ta47le"})["aria-label"]
            img_stars.append([fig,stars,comment,src])
        return img_stars
    def tour_guide(self,name):
        op = Options()
        op.binary_location =  "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
        op.use_chromium = True
        op.add_argument('--disable-gpu') 
        op.add_argument('--headless')
        driver = webdriver.Chrome(executable_path =r'C:\chromedriver.exe',options=op)
        driver.get('https://www.google.com/search?q='+name)
        source = driver.page_source
        root= bs4.BeautifulSoup(source,'html.parser')
        text = root.find_all("div",{"class":"yuRUbf"},limit=5)
        url_list = []
        for i in text:
            url_list.append(i.a['href'])
        return url_list
   
    def __init__ (self,name):
        self.name = name 

class selenium(str):
    def data(self,name):
        import time 
        # serv = ChromeService(ChromeDriverManager(version='104').install())
        # serv.creationflags = CREATE_NO_WINDOW
        op = Options()
        op.binary_location =  "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
        op.use_chromium = True
        # op.add_argument('--headless') #booking.com不能用
        op.add_argument('--disable-gpu') 
        # driver = webdriver.Chrome(executable_path='C:/chromedriver.exe',options=op)
        driver = webdriver.Chrome(executable_path =r'C:\chromedriver.exe',options=op)
        driver.get('https://www.booking.com/')
        search = driver.find_element(By.ID,"ss")
        search.send_keys(name)
        search.send_keys(Keys.ENTER)
        time.sleep(3)
        source = driver.page_source
        root= bs4.BeautifulSoup(source,'html.parser')
        text = root.find_all("div",{"data-testid":"property-card"},limit=5)
        # print(type(text[0]),sys.stderr)
        # ans = []
        # for i in text:
            # ans.append(bs4.element.Tag(i))
            # print(type(i),sys.stderr)
        # text[0].get_element('')
        return text
    
    def __init__(self,name):
        self.name = name 


class store():
    List = []
    def list_back():
        return store.List
class fig_store():
    fig = [] 
    set = False
    def fig_back():
        return fig_store.fig
    def set_back():
        return fig_store.set