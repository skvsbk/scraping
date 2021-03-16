 # https://www.youtube.com/watch?v=gy_YlibMW6Q&list=PLqGS6O1-DZLprgEaEeKn9BWKZBvzVi_la&index=4
# 21-50


import requests
from bs4 import BeautifulSoup
import json
import os
import time
import random

def get_data(url):
    headers = {
        "user-agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    project_data_list = []
    iteration_count = 23
    print(f"Total iteration: #{iteration_count}")

    for item in range(1, 24):

        req = requests.get(url + f"PAGEN_1={item}&PAGEN_2={item}", headers)

        folder_name = f"data_dyn/data_{item}"
        if os.path.exists(folder_name):
            print("Folder is exist")
        else:
            os.mkdir(folder_name)

        with open(f"{folder_name}/projects_{item}.html", "w", encoding="utf-8") as file:
            file.write(req.text)

        with open(f"{folder_name}/projects_{item}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        articles = soup.find_all("article", class_="ib19")

        project_urls = []
        for article in articles:
            project_url = "http://www.edutainme.ru" + article.find("div", class_="txtBlock").find("a").get("href")
            project_urls.append(project_url)


        for project_url in project_urls:    #[:1] - срез для тестирования
            req = requests.get(project_url,headers)
            project_name = project_url.split("/")[-2]

            with open(f"{folder_name}/{project_name}.html", "w", encoding="utf-8") as file:
                file.write(req.text)
            with open(f"{folder_name}/{project_name}.html", encoding="utf-8") as file:
                src = file.read()

            soup = BeautifulSoup(src, "lxml")
            project_data =  soup.find("div", class_="inside")

            try:
                project_logo = "http://www.edutainme.ru" + project_data.find("div", class_="Img logo").find("img").get("src")
                #print(project_logo)
            except Exception:
                project_logo = "No project logo"

            try:
                project_name = project_data.find("div", class_="txt").find("h1").text
               # print(project_name)
            except Exception:
                project_name = "No project name"

            try:
                project_short_description = project_data.find("div", class_="txt").find("h4", class_="head").text
                #print(project_short_description)
            except Exception:
                project_short_description = "No short description"

            try:
                project_website = project_data.find("div", class_="txt").find("p").find("a").text
                #print(project_website)
            except Exception:
                project_website = "No website"

            try:
                project_full_description = project_data.find("div", class_="textWrap").find("div", class_="rBlock").text
                #print(project_full_description)
            except Exception:
                project_full_description = "No full description"

            for s in ["<p>", "</p>"]:
                project_full_description = project_full_description.replace(s, "") if s in project_full_description else project_full_description

            project_data_list.append(
                {
                    "Имя проекта": project_name,
                    "URL логотипа проекта": project_logo,
                    "Краткое описание проекта": project_short_description,
                    "Сайт проекта": project_website,
                    "Полное описание проекта" : project_full_description.strip()
                }
            )

        iteration_count -=1
        print(f"Iteration #{item} was done. Remind #{iteration_count} of iterations")
        if iteration_count == 0:
            print("Data collect is complete")
        time.sleep(random.randrange(2, 4))

    with open("data_dyn/projects_data.json", "a", encoding="utf-8") as file:
        json.dump(project_data_list, file, indent=4, ensure_ascii=False)


get_data("http://www.edutainme.ru/edindex/ajax.php?params=%7B%22LETTER%22%3Anull%2C%22RESTART%22%3A%22N%22%2C%22CHECK_DATES%22%3Afalse%2C%22arrWHERE%22%3A%5B%22iblock_startaps%22%5D%2C%22arrFILTER%22%3A%5B%22iblock_startaps%22%5D%2C%22startups%22%3A%22Y%22%2C%22SHOW_WHERE%22%3Atrue%2C%22PAGE_RESULT_COUNT%22%3A9%2C%22CACHE_TYPE%22%3A%22A%22%2C%22CACHE_TIME%22%3A0%2C%22TAGS_SORT%22%3A%22NAME%22%2C%22TAGS_PAGE_ELEMENTS%22%3A%22999999999999999999%22%2C%22TAGS_PERIOD%22%3A%22%22%2C%22TAGS_URL_SEARCH%22%3A%22%22%2C%22TAGS_INHERIT%22%3A%22Y%22%2C%22SHOW_RATING%22%3A%22Y%22%2C%22FONT_MAX%22%3A%2214%22%2C%22FONT_MIN%22%3A%2214%22%2C%22COLOR_NEW%22%3A%22000000%22%2C%22COLOR_OLD%22%3A%22C8C8C8%22%2C%22PERIOD_NEW_TAGS%22%3A%22%22%2C%22DISPLAY_TOP_PAGER%22%3A%22N%22%2C%22DISPLAY_BOTTOM_PAGER%22%3A%22N%22%2C%22SHOW_CHAIN%22%3A%22Y%22%2C%22COLOR_TYPE%22%3A%22Y%22%2C%22WIDTH%22%3A%22100%25%22%2C%22USE_LANGUAGE_GUESS%22%3A%22N%22%2C%22PATH_TO_USER_PROFILE%22%3A%22%23SITE_DIR%23people%5C%2Fuser%5C%2F%23USER_ID%23%5C%2F%22%2C%22SHOW_WHEN%22%3Afalse%2C%22PAGER_TITLE%22%3A%22%5Cu0420%5Cu0435%5Cu0437%5Cu0443%5Cu043b%5Cu044c%5Cu0442%5Cu0430%5Cu0442%5Cu044b+%5Cu043f%5Cu043e%5Cu0438%5Cu0441%5Cu043a%5Cu0430%22%2C%22PAGER_SHOW_ALWAYS%22%3Atrue%2C%22USE_TITLE_RANK%22%3Afalse%2C%22PAGER_TEMPLATE%22%3A%22%22%2C%22DEFAULT_SORT%22%3A%22rank%22%2C%22noTitle%22%3A%22Y%22%7D&")
