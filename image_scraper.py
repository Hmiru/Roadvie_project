import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
from selenium.common.exceptions import TimeoutException, InvalidArgumentException
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import os
import time
import yaml
class roadview_scraper():
    def __init__(self, column_indexes=[], image_number=0, angle=-180):
        with open('scraper_config.yaml', 'r', encoding='utf-8') as stream:
            config = yaml.safe_load(stream)
            
        self.driver = webdriver.Chrome()
        self.driver.execute_script("document.body.style.zoom='50%'")
        self.screenshot_full_path=config['path']['screenshot_full_path']
        self.screenshot_by_angle_path = config['path']['screenshot_by_angle_path']
        self.clusters = pd.read_csv('Cluster_info_labeled.csv',encoding='utf-8')
        self.column_indexes=column_indexes
        self.image_num = image_number-1
        self.start_index = image_number-1
        self.angle=angle

    def set_zoom_level(self, zoom_level):
        zoom_code=f"document.body.style.zoom='{zoom_level}%';"
        self.driver.execute_script(zoom_code)
        
#임의 각도 지정하는 함수
    def angle_changer(self,url,new_value):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        current_value = query_params['p'][0]

        updated_value = current_value.split(",")[:-4]+ new_value.split(",")
        query_params['p'] = [",".join(updated_value)]

        new_query_string = urlencode(query_params, doseq=True)

        # 새 URL 생성
        modified_url = urlunparse(
            (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query_string,
             parsed_url.fragment)
        )
        return modified_url


#로드뷰 창 여는 함수
    def window_opener(self,url):
        try:
            self.driver.get(url)
            self.driver.maximize_window()
            
            try:
                first_element_xpath = '//*[@id="root"]/div/div[2]/div[4]/button'
                wait1 = WebDriverWait(self.driver, 2)
                wait1.until(EC.presence_of_element_located((By.XPATH,first_element_xpath))).click()
            except TimeoutException:
                pass

        except InvalidArgumentException:
            print(f"잘못된 URL: {url}")
            return
        except TimeoutException:
            pass
#연 창에서 캡쳐하는 함수
    def capture_screenshot(self):

        image_name = f"img{self.image_num}.png"
        print(f"{self.screenshot_full_path}/{image_name}")
        self.driver.save_screenshot(f"{self.screenshot_full_path}/{image_name}")

#저장한 사진, 정방형으로 자르는 함수

    def get_folder_path(self,column_index, image_number):
        CLUSTER_MAP = {6: 'a', 9: 'b', 12: 'c', 15: 'd'}
        cluster_name=f"cluster{image_number}"
        group=CLUSTER_MAP.get(column_index,'')
        folder_path=os.path.join(self.screenshot_by_angle_path, cluster_name, group)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path

    def crop(self,angle,column_index):
        img_size=1800 #f나올수 있는 최대의 정사각형의
        image_name = f"img{self.image_num}.png"
        with Image.open(f"{self.screenshot_full_path}/{image_name}") as img:
            width, height = img.size
    # 중앙의 정사각형 영역 계산
            left = (width - img_size) / 2
            top = 0
            right = (width + img_size) / 2
            bottom = img_size
            img_cropped = img.crop((left, top, right, bottom))
            print(column_index)
            folder_path=self.get_folder_path(column_index, self.image_num)
            image_name = f"img{self.image_num}_{angle}.png"

            img_cropped.save(os.path.join(folder_path,image_name))


    def close(self):# 웹드라이버 종료
        self.driver.quit()

    def scrape_by_angle(self,url,column_index):
        for x in range(self.angle,180,  10):#used 10 degree but from now on we will use 30 degree.
            modified_url=self.angle_changer(url,f'{x}.08,10.26,80')
            self.window_opener(modified_url)
            self.capture_screenshot()
            self.crop(x,column_index)

    def scrape(self):
        for column_index in self.column_indexes:  # directly loop through column indexes
            self.image_num = self.start_index
            for index, url in enumerate(self.clusters.iloc[:, column_index]):
                if index < self.start_index:
                    continue
                if pd.isna(url):
                    print("skipp missing URL")
                    self.image_num += 1
                    continue

                self.image_num += 1
                self.scrape_by_angle(url, column_index)

def main():
    scraper = roadview_scraper(column_indexes=[6,9,12,15], image_number=1, angle=-180)
    scraper.scrape()

if __name__ == "__main__":
    main()

