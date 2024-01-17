from scrapy import Spider
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
from typing import Any


# run with scrapy runspider my_spider.py -o output.json


class DynamicContentSpider(Spider):
    name = "dynamic_spider"
    start_urls = ["https://docs.digitalocean.com/reference/api/api-reference/"]

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        load_dotenv()
        PROXY = os.getenv('PROXY')
        options = Options()
        options.add_argument(f'--proxy-server={PROXY}')
        try:
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install(), options=options))
        except ValueError:
            self.driver = webdriver.Chrome(service=ChromeService('/usr/local/bin/chromedriver',
                                                                 options=options))

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.implicitly_wait(3)

        # Assuming 'content_parent' is the CSS selector for the common parent element
        content_parent = self.driver.find_element(By.CSS_SELECTOR, 'content_parent_selector')
        child_elements = content_parent.find_elements(By.XPATH, "./*")

        for child in child_elements:
            tag_name = child.tag_name
            if tag_name == 'p':
                yield {'type': 'paragraph', 'text': child.text}
            elif tag_name == 'code':
                yield {'type': 'code', 'text': child.text}

        self.driver.quit()
