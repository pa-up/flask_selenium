from flask import Flask, render_template, request , send_file , redirect , url_for , session
import threading,webbrowser
import os
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


# flaskアプリの明示
templates_path = 'templates/'
static_path = 'static/'
app = Flask(__name__ , template_folder=templates_path, static_folder=static_path)

# パスの定義
log_txt_path = static_path + "/log/log.txt"
output_csv_path = static_path + "/csv/output.csv"
output_excel_path = static_path + "/excel/output.xlsx"




def browser_setup(browse_visually = "no"):
    """ブラウザを起動する関数"""
    #ブラウザの設定
    options = webdriver.ChromeOptions()
    if browse_visually == "no":
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    #ブラウザの起動
    browser = webdriver.Chrome(options=options , service=ChromeService(ChromeDriverManager().install()))
    browser.implicitly_wait(3)
    return browser


class Scraper:
    def __init__(self , browse_visually = "no"):
        self.driver = browser_setup(browse_visually)
        self.wait_driver = WebDriverWait(self.driver, 10)

    def browser_setup(self , browse_visually = "no"):
        """ブラウザを起動する関数"""
        options = webdriver.ChromeOptions()
        if browse_visually == "no":
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options , service=ChromeService(ChromeDriverManager().install()))
        driver.implicitly_wait(3)
        return driver
    
    def scraping_book_off(self , searched_url):
        """ 任意のスクレイピングを実行する関数 """
        self.driver.get(searched_url)
        # self.driver.implicitly_wait(5)
        time.sleep(4)
        # html要素を取得
        week_recommend_elements = self.driver.find_element(By.CSS_SELECTOR , "section.recommend__inner").find_elements(By.CSS_SELECTOR , "div.recommend__list")
        for loop , element in enumerate(week_recommend_elements):
            if loop == 0:
                week_recommend_text = element.text
            else:
                week_recommend_text = week_recommend_text + "<br>" + element.text
        return week_recommend_text



@app.route('/')
def index():
        return render_template("index.html")



@app.route("/call_from_ajax", methods = ["POST"])
def call_from_ajax():
    if request.method == "POST":
        # ここにPythonの処理を書く
        try:
            # ajax_form_data = request.form["data"]
            # message = f"フン。<b style='border: 2px solid red;'>{ajax_form_data}</b>というのかい。贅沢な名だねぇ。<br>"
            searched_url = "https://shopping.bookoff.co.jp/"
            scraper = Scraper()
            week_recommend_text = scraper.scraping_book_off(searched_url)

        except Exception as e:
            week_recommend_text = str(e)
        dict = {"answer": week_recommend_text}      # 辞書
    return json.dumps(dict)             # 辞書をJSONにして返す



@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        searched_url = "https://shopping.bookoff.co.jp/"
        driver = browser_setup()
        driver.get(searched_url)
        driver.implicitly_wait(5)
        week_recommend_elements = driver.find_element(By.CSS_SELECTOR , "section.recommend__inner").find_elements(By.CSS_SELECTOR , "div.recommend__list")

        week_recommend_text = ""
        for loop , element in enumerate(week_recommend_elements):
            if loop == 0:
                week_recommend_text = element.text
            else:
                week_recommend_text = week_recommend_text + "<br>" + element.text
        

        return render_template(
            "result.html" ,
            week_recommend_text = week_recommend_text ,
        )


@app.route('/page1', methods=['GET', 'POST'])
def page1():
    return render_template("page1.html")




@app.route('/csv_download')
def csv_download():
    directory = os.path.join(app.root_path, 'files') 
    return send_file(os.path.join(directory, output_csv_path), as_attachment=True)

@app.route('/excel_download')
def excel_download():
    directory = os.path.join(app.root_path, 'files') 
    return send_file(os.path.join(directory, output_excel_path), as_attachment=True)



if __name__ == "__main__":
    port_number = 6600
    # threading.Timer(1.0, lambda: webbrowser.open('http://127.0.0.1:' + str(port_number)) ).start()
    app.run(port = port_number , debug=True)

