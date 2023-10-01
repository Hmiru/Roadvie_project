import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
from selenium.common.exceptions import TimeoutException, InvalidArgumentException
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class roadview_scraper():
    def __init__(self, column_indexes=[], image_number=0, angle=-180):
        self.driver = webdriver.Chrome()
        #self.screenshot_full_path="C:\\Users\\mirun\\PycharmProjects\\roadview_project\\screenshot_full"
        #self.screenshot_cropped_path="C:\\Users\\mirun\\PycharmProjects\\roadview_project\\screenshot_cropped"
        #self.screenshot_by_angle_path="C:\\Users\\mirun\\PycharmProjects\\roadview_project\\test_by_angle"
        #self.clusters = pd.read_csv("C:\\Users\\mirun\\PycharmProjects\\roadview_project\\Cluster_info_labeled.csv",encoding='cp949')

        self.screenshot_full_path="C:\\Users\\mirun\\roadview_dataset\\screenshot_full"
        self.screenshot_by_angle_path = "C:\\Users\\mirun\\roadview_dataset\\test_by_angle"
        self.clusters = pd.read_csv("C:\\Users\\mirun\\roadview_dataset\\roadview_coordinates.csv",encoding='cp949')
        self.column_we_want =[self.clusters.iloc[:, i] for i in column_indexes]
        self.image_num = image_number-1
        self.start_index = image_number-1
        self.angle=angle

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
           # wait = WebDriverWait(self.driver, 10)  # 10초 동안 최대로 기다림
            element_xpath = '//*[@id="root"]/div/div[2]/div[4]/button'
        except InvalidArgumentException:
            print(f"잘못된 URL: {url}")
            return
        try:
            wait = WebDriverWait(self.driver, 1)
            wait.until(EC.presence_of_element_located((By.XPATH, element_xpath))).click()
        except TimeoutException:
            pass
            # self.driver.refresh()

#연 창에서 캡쳐하는 함수
    def capture_screenshot(self):

        image_name = f"img{self.image_num}.png"
        print(f"{self.screenshot_full_path}\\{image_name}")
        self.driver.save_screenshot(f"{self.screenshot_full_path}\\{image_name}")

#저장한 사진, 정방형으로 자르는 함수
    def crop(self,angle):
        image_name = f"img{self.image_num}.png"
        with Image.open(f"{self.screenshot_full_path}\\{image_name}") as img:
            width, height = img.size
    # 중앙의 정사각형 영역 계산
            left = (width - 1140) / 2
            top = 0
            right = (width + 1140) / 2
            bottom = 1140 #사진만 나올수 있는 최대의 정사각형의 길이
            img_cropped = img.crop((left, top, right, bottom))
            image_name = f"img{self.image_num}_{angle}.png"
            img_cropped.save(f"{self.screenshot_by_angle_path}\\{image_name}")


    def close(self):# 웹드라이버 종료
        self.driver.quit()

    def scrape_by_angle(self,url):
        for x in range(self.angle,181, 10):
            modified_url=self.angle_changer(url,f'{x}.08,10.26,80')
            print(modified_url)
            self.window_opener(modified_url)
            self.capture_screenshot()
            self.crop(x)
#위 함수들을 합친 함수
    def scrape(self):
        for column in self.column_we_want: #4개의 클러스터 열 중 인덱스 설정(6,9,12,15)
            for index, url in enumerate(column):
                if index < self.start_index:
                    continue
                self.image_num += 1
                self.driver.refresh()
                self.scrape_by_angle(url)



def main():
    scraper = roadview_scraper(column_indexes=[0], image_number=1, angle=-180)
    scraper.scrape()


if __name__ == "__main__":
    main()