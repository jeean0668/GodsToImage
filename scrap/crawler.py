import pandas as pd 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import options

from time import sleep
import re
import math
import os

class Crawler:
    
    def __init__(self, opt):
        
        self.click_time = opt.click_time
        self.send_time = opt.click_time
        self.date_time = opt.date_time
        self.wait_time = opt.wait_time
        self.driver_path = opt.driver_path
        
        self.crawling_news = dict({"Date":[], "Title":[], "Content":[]})
        
        try:
            self.driver = webdriver.Chrome(self.driver_path)
            sleep(self.date_time)
        except:
            sleep(self.wait_time)
            self.driver = webdriver.Chrome(self.driver_path)
            sleep(self.date_time)
        self.driver.implicitly_wait(self.wait_time)
        self.driver.maximize_window()

        try:
            self.driver.get(opt.url);sleep(self.date_time)
        except:
            sleep(self.wait_time)
            self.driver.get(opt.url);sleep(self.date_time)
    def Search(self, keyword, opt):
        
        self.keyword = keyword
        self.start_day = opt.start_day
        self.end_day = opt.end_day
        
        # keyword
        try:
            self.driver.find_element(By.CLASS_NAME, 'search-key').send_keys(keyword);sleep(self.send_time)
        except:
            sleep(self.wait_time)
            self.driver.find_element(By.CLASS_NAME, 'search-key').send_keys(keyword);sleep(self.send_time)
         
         # 상세 검색
        try:
            self.driver.find_element(By.CLASS_NAME, 'btn-srchDetail.btn-srchDetail-search').click();sleep(self.click_time)
        except:
            sleep(self.wait_time)
            self.driver.find_element(By.CLASS_NAME, 'btn-srchDetail.btn-srchDetail-search').click();sleep(self.click_time)
        
        # 기간 메뉴
        try:
            self.driver.find_element(By.CLASS_NAME, 'tab-btn.search-tab_group').click();sleep(self.click_time)
        except:
            sleep(self.wait_time)
            self.driver.find_element(By.CLASS_NAME, 'tab-btn.search-tab_group').click();sleep(self.click_time)
        
        # 시작 기간
        try:
            self.driver.find_element(By.ID, 'search-begin-date').send_keys("\b\b\b\b\b\b\b\b\b\b{}".format(self.start_day));sleep(self.send_time)
        except:
            sleep(self.wait_time)
            self.driver.find_element(By.ID, 'search-begin-date').send_keys("\b\b\b\b\b\b\b\b\b\b{}".format(self.start_day));sleep(self.send_time)
            
        # 끝 기간
        try:
            self.driver.find_element(By.ID, 'search-end-date').send_keys("\b\b\b\b\b\b\b\b\b\b{}".format(self.end_day));sleep(self.send_time)
        except:
            sleep(self.wait_time)
            self.driver.find_element(By.ID, 'search-end-date').send_keys("\b\b\b\b\b\b\b\b\b\b{}".format(self.end_day));sleep(self.send_time)
        
        self.driver.find_element(By.CLASS_NAME, 'btn-srch.input-group-btn.news-search-btn').click();sleep(self.click_time)
    def pages(self):
        lastPage = self.driver.find_element(By.CLASS_NAME, 'lastNum').text
        isLastPage = False
        curPage = 1
        while not isLastPage:
        
            self.page_crawling_news()
            if curPage == int(lastPage):
                isLastPage = True
            else:
                self.driver.find_element(By.CLASS_NAME, 'page-next.page-link').send_keys(Keys.ENTER)
                sleep(self.click_time)
                curPage+=1
        self.Save()
        
    
    def page_crawling_news(self):
        articles = self.driver.find_element(By.ID, 'news-results')

        for i in range(1,len(articles.find_elements(By.CLASS_NAME, 'news-item'))+1):
            try:
                self.driver.find_element(By.XPATH, f'//*[@id="news-results"]/div[{i}]/div/div[2]/a/div/strong/span').click();sleep(self.click_time)
            except:
                sleep(self.wait_time)
                self.driver.find_element(By.XPATH, f'//*[@id="news-results"]/div[{i}]/div/div[2]/a/div/strong/span').click();sleep(self.click_time)            

            try:
                date = self.driver.find_element(By.XPATH, f'//*[@id="news-detail-modal"]/div/div/div[1]/div/div[1]/div[1]/ul').text;sleep(self.click_time)
            except:
                sleep(self.click_time)
                date = self.driver.find_element(By.XPATH, f'//*[@id="news-detail-modal"]/div/div/div[1]/div/div[1]/div[1]/ul').text;sleep(self.click_time)
            
            try:
                title = self.driver.find_element(By.XPATH, f'//*[@id="news-detail-modal"]/div/div/div[1]/div/div[1]/h1').text;sleep(self.click_time)
            except:
                sleep(self.click_time)
                title = self.driver.find_element(By.XPATH, f'//*[@id="news-detail-modal"]/div/div/div[1]/div/div[1]/h1').text;sleep(self.click_time)
                
            try:
                content = self.driver.find_element(By.XPATH, f'//*[@id="news-detail-modal"]/div/div/div[1]/div/div[2]').text;sleep(self.click_time)
            except:
                sleep(self.click_time)
                content = self.driver.find_element(By.XPATH, f'//*[@id="news-detail-modal"]/div/div/div[1]/div/div[2]').text;sleep(self.click_time)
            self.crawling_news["Date"].append(date)
            self.crawling_news["Title"].append(title)
            self.crawling_news["Content"].append(content)
        
            try:
                self.driver.find_element(By.XPATH, '//*[@id="news-detail-modal"]/div/div/button').click();sleep(self.click_time)
            except:
                sleep(self.wait_time)
                self.driver.find_element(By.XPATH, '//*[@id="news-detail-modal"]/div/div/button').click();sleep(self.click_time)
    def Save(self):
        s_d = self.start_day[:4] + self.start_day[5:7] + self.start_day[-2:]
        e_d = self.end_day[:4] + self.end_day[5:7] + self.end_day[-2:]
        pd.DataFrame(self.crawling_news).to_csv(f"/빅카인즈/{self.keyword}_{s_d}_{e_d}", index=False)
        