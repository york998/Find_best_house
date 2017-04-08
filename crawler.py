#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urlparse import urljoin
import requests
import csv
import os.path

if not os.path.exists(file_path):
    csv_file = open("rent.csv","wb") 
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow([house_title, house_location, house_money, house_url])
    csv_file.close()


url = "https://www.zillow.com/homes/for_rent/Austin-TX/condo,apartment_duplex_type/10221_rid/30.620778,-97.272263,29.963858,-98.300858_rect/9_zm/{page}_p/"


#search all the page of the result
page = 0

csv_file = open("rent.csv","wb") 
csv_writer = csv.writer(csv_file, delimiter=',')

while True:
    page += 1
    print "fetch: ", url.format(page=page)
    response = requests.get(url.format(page=page))
    html = BeautifulSoup(response.text)
    house_list = html.select(".zsg-photo-card-spec > p")

    # end the loop untile can't find new results
    if not house_list:
        break

    for house in house_list:
        house_title = house.select("h4")[0].string.encode("utf8")
        house_url = urljoin("www.zillow.com", house.select("a")[0]["href"])
        house_location = house.select(".zsg-photo-card-address")[0].string.encode("utf8")
        house_money = house.select("zsg-photo-card-info")[0].select(".zsg-photo-card-unit")[0].string.encode("utf8")
            csv_writer.writerow([house_title, house_location, house_money, house_url])

csv_file.close()