import requests
from bs4 import BeautifulSoup
import re
import csv

def cleanhtml(raw_html):
    clean = re.compile('<.*?>')
    cleantext = re.sub(clean, '', raw_html)
    return cleantext

list_of_projects_url=[]
error_file="error_log"
f=open(error_file,"w+")
list_of_projects_csv="gov projects.csv"
rows = []

for i in range(1,152):
    URL = "https://egy-map.com/projects?name=&year=&category=0&location=0&case=0&s=&page=%d" %i
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    list_of_projects=soup.find_all("div", class_="property-title-box")
    for t in list_of_projects:
        for atag in t.find_all('h4'):
            list_of_projects_url.append(atag.a.attrs['href'])

counter=0
for i in list_of_projects_url:
    x=[]
    x.append(i)
    counter=counter+1
    page = requests.get(i)
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        l=cleanhtml(str(soup.select('div.single-listing-title h2')[0])).replace("   ","").split("\n")
        l=[x for x in l if x]
        x.append(str(l[0]).replace("\n",""))
        x.append(str(l[1]).replace("\n",""))
    except:
        f.write("not found %s"%str(i))
        continue
    # location
    try:
        x.append(cleanhtml(str(soup.select('div.inner_location p')[0])).replace("  ","").replace("\n",""))
    except:
        x.append("N/A")
    # category
    try:
        x.append(cleanhtml(str(soup.select('div.inner_category a')[0])).replace("  ","").replace("\n",""))
    except:
        x.append("N/A")
    # Price
    try:
        x.append(cleanhtml((str(soup.select('div.inner_price p')[0])).replace("  ", "").replace("\n","")))
    except:
        x.append("N/A")
    #date, area
    try:
        list_of_sizes = soup.find_all("div", class_="inner_size")
        if len(list_of_sizes)==1:
            x.append("N/A")
            x.append(cleanhtml((str(soup.select('div.inner_size p')[0])).replace("  ", "").replace("\n","")))
        else:
            for t in list_of_sizes:
                for atag in t.find_all('p'):
                    x.append(str(atag.get_text()).replace(" ","").replace("-"," - ").replace("\n",""))
    except:
        x.append("N/A")
        x.append("N/A")

    rows.append(x)

f.close()



with open(list_of_projects_csv, 'w',  encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(rows)

print("the total number of project is %d" %counter)
