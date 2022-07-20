from urllib.request import urlopen

url = "https://www.travelking.com.tw/tourguide/hualien/scenery105505.html"
from urllib.request import urlopen
import bs4 
with urlopen(url) as response:
    data = response.read().decode("utf-8")
root= bs4.BeautifulSoup(data,'html.parser')
text = root.find_all("meta",{"itemprop":"description"},"content")
address = root.find("a",{"target":"_blank"})
result = root.find_all('div',{"class":"point_list"})
if result == None:
    result = root.find_all('div',{"class":"text"}).p.text
opening_time = root.find('div',{"class":"point_list"}).p.text
fee = root.find('div',{"class":"point_list"}).p.text
