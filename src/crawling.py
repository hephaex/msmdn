#!/usr/bin/env python
import re

from selenium import webdriver
from selenium.webdriver.support.ui import Select

title_pattern = re.compile('([\s\S]+)\s+([\d.\-]+)\s*화?')
page_pattern = re.compile('page-(\d+)')
remove_hwa_pattern = re.compile('([\d.\-]+)\s*화?')

def get_title_parsed(string):
    processed =  [[y.strip() for y in x] for x in title_pattern.findall(string)]
    return processed[0] if processed else None

def get_page_parsed(string):
    processed = page_pattern.findall(string)
    return int(processed[0]) if processed else None

def get_remove_hwa(string):
    processed = remove_hwa_pattern.findall(string)
    return processed[0] if processed else None

class Browser:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
        options.add_argument("lang=ko_KR")
        self.driver = webdriver.Chrome('~/manga/chromedriver',
                                       options=options)
        self.driver.implicitly_wait(3)

    def __page_parse(self):
        html_page = self.driver.page_source
        if html_page:
            images_elem = self.driver.find_elements_by_xpath(
                '//*[@id="thema_wrapper"]/div[2]/div/div/div[1]/div[2]/div[3]/img')
            title_elem = self.driver.find_element_by_xpath(
                '//*[@id="thema_wrapper"]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/h1')
            select_elem = self.driver.find_element_by_xpath(
                '//*[@id="thema_wrapper"]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/div/select')
            pages_elem = select_elem.find_elements_by_tag_name('option')
            images_detailed = [
                (get_page_parsed(image.get_attribute('class')), image.get_attribute('src')) for image in images_elem]
            title = title_elem.text
            pages = [(page.get_attribute('value'), get_remove_hwa(page.text.strip())) for page in pages_elem]
            self.select_elem = Select(select_elem)
            return {
                "images": images_detailed,
                "title": get_title_parsed(title),  # ???? ???? ???? \d+화
                "page_info": pages
            }
        raise Exception("Read Problem")

    def readPage(self, page_id='427271'):
        print("requesting ", page_id)
        self.driver.get("https://mangashow.me/bbs/board.php?bo_table=msm_manga&wr_id=" + page_id)
        return self.__page_parse()

    def chooseOption(self, page_id):
        print("requesting ", page_id)
        self.select_elem.select_by_value(page_id)
        return self.__page_parse()

    def __del__(self):
        if self.driver:
            self.driver_close()

    def driver_close(self):
        self.driver.close()
        self.driver = None
