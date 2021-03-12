# pip install bs4 requests lxml
from bs4 import BeautifulSoup
import requests
import csv

START_URL = 'https://www.wildberries.ru/catalog/detyam/odezhda/dlya-devochek/bele'
#https://www.wildberries.ru/catalog/detyam/odezhda/dlya-devochek/bele
CSV_FILE = 'C:\\Users\\KSvitochev\\Desktop\\WB.csv'

def get_content(url, class_):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    }
    response = requests.get(url, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')
    return soup.findAll('div', class_)

def parse():
    results =[]
    brandname = ''
    composition = ''
    description = ''
    price = ''
    for item in get_content(START_URL, 'dtList-inner'):
        title =  item.find('div', class_ = 'dtlist-inner-brand-name').text.strip()
        link = 'https://www.wildberries.ru'+item.find('a', class_ = 'ref_goods_n_p j-open-full-product-card').get('href').strip()
        for item2 in get_content(link, 'product-content-v1'):
            brandname = item2.find('div', class_='brand-and-name j-product-title').text.strip()
            composition = item2.find('div', class_='i-composition-v1 i-collapsable-v1').find('span').text.strip()
            description = item2.find('div', class_='j-description collapsable-content description-text').find('p').text.strip()
            price = item2.find('div', class_='inner-price').find('span').text.strip()
        results.append({
            'title' : title.replace('\n', ''),
            'brandname' : brandname,
            'composition' : composition,
            'description': description,
            'price' : price[:-2],
            'link' : link
        })
    with open(CSV_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["title", "brandname", "composition", "description", "price", "link"])
        for res in results:
            #print(f'{res["title"]} -> brandname: {res["brandname"]}-> composition: {res["composition"]}-> description: {res["description"]}-> Price: {res["price"]}-> link: {res["link"]}')
            writer.writerow([res["title"], res["brandname"], res["composition"], res["description"], res["price"], res["link"]])  #res["price"]
            #writer.writerow(res)
            #print(type(res["title"]))
            print(res["price"])


def save_to_csv():
    pass

parse()

# for item2 in get_content('https://www.wildberries.ru/catalog/detyam/odezhda/dlya-devochek/bele', 'product-content-v1'):
#     brandname = item2.find('div', class_='j-description collapsable-content description-text').find('p').text.strip()
#     print(brandname)