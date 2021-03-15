# https://www.youtube.com/watch?v=gy_YlibMW6Q&list=PLqGS6O1-DZLprgEaEeKn9BWKZBvzVi_la&index=4
# 21-50


import requests
from bs4 import BeautifulSoup

def get_data(url):
    headers = {
        "user-agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }

    # req = requests.get(url, headers)
    #
    # with open("project_dyn.html", "w", encoding="utf-8") as file:
    #     file.write(req.text)
    with open("project_dyn.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    articles = soup.find_all("article", class_="ib19")
 #   print(articles)

    project_urls = []
    for article in articles:
        project_url = "http://www.edutainme.ru" + article.find("div", class_="txtBlock").find("a").get("href")
        project_urls.append(project_url)

    for project_url in project_urls[:1]:    #срез для тестирования
        req = requests.get(project_url,headers)
        project_name = project_url.split("/")[-2]

        with open(f"data_dyn/{project_name}.html", "w", encoding="utf-8") as file:
            file.write(req.text)
        with open(f"data_dyn/{project_name}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        project_data =  soup.find("div", class_="inside")

        try:
            project_logo = "http://www.edutainme.ru" + project_data.find("div", class_="Img logo").find("img").get("src")
            print(project_logo)
        except Exception:
            print("No project logo")

        try:
            project_name = project_data.find("div", class_="txt").find("h1").text
            print(project_name)
        except Exception:
            print("No project name")

get_data("http://www.edutainme.ru/edindex/")
