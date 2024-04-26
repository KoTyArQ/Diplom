import json
import csv
import random
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup



def parse_selenium_data(url):
    options=uc.options.ChromeOptions()
    options.binary_location=r"\Users\Nikita_student.STAR\chrome-win64\chrome.exe"
    driver = uc.Chrome(options=options)
    driver.get(url)
    time.sleep(10)

    with open("index_selenium.html", "w", encoding="utf-8-sig") as file:
        file.write(driver.page_source)

# parse_selenium_data("https://www.ozon.ru/category/termopasta-30799/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=%D1%82%D0%B5%D1%80%D0%BC%D0%BE%D0%BF%D0%B0%D1%81%D1%82%D0%B0")


def data_processing(file_name, json_name):
    with open(file_name,"r",encoding="utf-8-sig")as file:
        src=file.read()
    soup=BeautifulSoup(src,"lxml")
    all_products=soup.find_all("div","i8x xi8")
    all_products_dict={}
    for item in all_products:
        item_link="https://www.ozon.ru"+item.find("a", "ui9").get("href")
        item_name = item.find("span", "tsBody500Medium").text
        # if item_count != None:
        #     item_count=item_count.encode("ascii","ignore").decode()

        all_products_dict[item_name]=item_link

    print(all_products_dict)
    with open(f"{json_name}.json","w",encoding="utf-8-sig") as file:
        json.dump(all_products_dict,file,indent=4,ensure_ascii=False)

#data_processing("index_selenium.html","product_links")


def data_csv_writer(file_name):
    with open(f"{file_name}.json",encoding="utf-8-sig") as file:
        products=json.load(file)
    for product_name,product_data in products.items():
        with open(f"{file_name}.csv","a",encoding="utf-8-sig",newline="") as file:
            writer=csv.writer(file,delimiter=";")
            if product_data[1] != None:
                product_data[1]=product_data[1].replace("Осталось","")
            writer.writerow(
                (
                product_name.strip(),
                product_data[0].replace("Артикул:",""),
                product_data[1],
                )
            )
# data_csv_writer("product_count")


def product_data_parse(file_name):
    products_data_dict={}
    with open(f"{file_name}.json",encoding="utf-8-sig") as file:
        products_links=json.load(file)
    products_data_dict = {}

    for product_name, product_link in products_links.items():

        options = uc.options.ChromeOptions()
        options.binary_location = r"\Users\Nikita_student.STAR\chrome-win64\chrome.exe"
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument("--disable-gpu")
        driver = uc.Chrome(options=options)
        driver.get(f"{product_link}")
        time.sleep(random.randint(5,10))
        src=driver.page_source
        soup = BeautifulSoup(src, "lxml")
        container_info = soup.find_all("div", "container b6")
        for item in container_info:
            title=item.find("h1","x0l tsHeadline550Medium")
            qty = item.find("span", "e601-a4")
            sku = item.find("div", "ga10-a2")
            if qty != None:
                qty=qty.text
            if title != None:
               title=title.text

            if sku != None:
                sku=sku.text

            driver.close()
            products_data_dict[title] = [sku,qty]
            print(title)
            print(qty)
            print(sku)
            print(products_data_dict)
            break

    with open("products_data.json", "w", encoding="utf-8-sig") as file:
        json.dump(products_data_dict, file, indent=4, ensure_ascii=False)
        driver.quit()

product_data_parse("product_links")
