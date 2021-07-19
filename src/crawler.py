# 웹에 요청한 결과를 보내주는 모듈
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, ElementNotInteractableException, UnexpectedAlertPresentException

import os, sys, traceback, platform

from selenium.webdriver.firefox.webdriver import WebDriver

import src.img_util as img_util, src.util as util
import src.canvas_crawler as canvas_crawler, src.img_crawler as img_crawler

def clickNextButton(driver, conf) -> None:
    if conf['site_name'] == conf['comic_sites'][0]:
        #다음 페이지 버튼 감별
        if conf['next_button'] == 'next':
            #다음 페이지 버튼 요소 가져오기
            nextButton = driver.find_element_by_xpath("""//a[@id="goNextBtn"]""")    
            
            #다음 페이지 버튼 클릭
            nextButton.click()
        elif conf['next_button'] == 'prev':
            #다음 페이지 버튼 요소 가져오기
            prevButton = driver.find_element_by_xpath("""//a[@id="goPrevBtn"]""")

            #다음 페이지 버튼 클릭
            prevButton.click()
    elif conf['site_name'] == conf['comic_sites'][1]:
        #다음 페이지 버튼 감별
        if conf['next_button'] == 'next':
            #다음 페이지 버튼 요소 가져오기
            nextButton = driver.find_element_by_xpath("""//div[@class="nextpage"]""")    
            
            #다음 페이지 버튼 클릭
            nextButton.click()
        elif conf['next_button'] == 'prev':
            #다음 페이지 버튼 요소 가져오기
            prevButton = driver.find_element_by_xpath("""//div[@class="prepage"]""")    

            #다음 페이지 버튼 클릭
            prevButton.click()
    #텍스트 파일에 버튼 입력 잘못함
    else :
        print('-' * 20)
        print('website.txt에서 버튼 입력이 잘못됐습니다. 확인해 주세요.')
        print('-' * 20)

        sys.exit()
    
    #페이지 url 저장
    conf['url'] = str(driver.current_url)

    conf['number'] += 1

    print('\n-----' + str(conf['number']) + '번째 페이지로 이동 중' + '-----')   


class Crawler:
    """Manage method of crawling and set environments.
    """
    def __init__(self) -> None:
        self.conf = util.read_files()
        self.driver = self.load_chrome_driver()
        # util.create_dir(self.conf['comic_name'], '')

        self.crawl()

    def print_summary(self) -> None:
        print('='*5, "Sumamry", '='*5)
        print("Starting number of comic=", self.conf['number'])
        print("Url=",self.conf['url'])
        print("Next button type = ", self.conf['next_button'])
        print("Comic name = ", self.conf['comic_name'])

    def load_chrome_driver(self) -> WebDriver:
        platform_name = platform.system()
        if platform_name == "Windows":
            driver = webdriver.Chrome(os.path.join('src', 'chromedriver.exe'))
        elif platform_name == "Darwin":
            driver = webdriver.Chrome(os.path.join('src', 'chromedriver'))
        elif platform_name == "Linux":
            driver = webdriver.Chrome(os.path.join('src', 'chromedriver_linux64'))
        
        return driver

    def crawl(self) -> None:
        """Run cralwer
        """        
        while True:
            try :
                print('\n' + '-' * 20)
                print(f"Load {self.conf['number']} comic.")
                
                # Load synchronized page.
                self.driver.get(self.conf['url'])

                print(f"Completely load {self.conf['number']} comic.")

                # Save all elements of web page.
                req = self.driver.page_source

                # Craete bs4 instance.
                bs_object = BeautifulSoup(req)
                
                # Determine to use canvas or img.
                canvas_data, canvas_exist, img_exist = canvas_crawler.canvas_search(self.driver)
                    
                if canvas_exist and not img_exist :
                    print("\nRead via canvas elements")
                    
                    img_util.delete_navi_bar(self.driver)

                    canvas_crawler.fullshot_crop(self.driver, canvas_data, self.conf['number'])

                    canvas_crawler.image_merge(self.conf['number'])

                elif not canvas_exist and img_exist :
                    print("\nRead via img tag")
                    
                    img_util.delete_thumbnail_list(self.driver)
                    
                    # Save all elements of web page removed thumbnail list.
                    req = self.driver.page_source

                    # Craete bs4 instance for edited page source.
                    bs_object = BeautifulSoup(req)

                    img_crawler.save_image_tag(bs_object, self.conf)

                # Update number and url.
                clickNextButton(self.driver, self.conf)

            #다음 버튼을 누를 수 없을 때 1
            except NoSuchElementException :
                print('-' * 20)
                _, _ , tb = sys.exc_info() # tb -> traceback object 
                print ('file name = ', __file__)
                print ('error line No = {}'.format(tb.tb_lineno))
                print('만화가 더 이상 없습니다')
                traceback.print_exc()
                break

            #다음 버튼을 누를 수 없을 때 2
            except ElementNotVisibleException :
                print('-' * 20)
                _, _ , tb = sys.exc_info() # tb -> traceback object 
                print ('file name = ', __file__)
                print ('error line No = {}'.format(tb.tb_lineno))
                print('만화가 더 이상 없습니다')
                traceback.print_exc()
                break

            #다음 버튼을 누를 수 없을 때 3
            except ElementNotInteractableException :
                print('-' * 20)
                _, _ , tb = sys.exc_info() # tb -> traceback object 
                print ('file name = ', __file__)
                print ('error line No = {}'.format(tb.tb_lineno))
                print('만화가 더 이상 없습니다')
                traceback.print_exc()
                break

            #이미지 서버 상태가 안 좋아서 이미지 다운이 안될 때
            except FileNotFoundError :
                print('-' * 20)
                print('이미지 로딩에 실패했습니다.')
                print('다시 페이지를 로딩합니다.')
                self.driver.navigate().refresh()
                self.conf['number'] -= 1
                traceback.print_exc()
                continue

            except UnexpectedAlertPresentException :
                print("마지막화입니다.")
                traceback.print_exc()
                break
            #그 외 에러 처리
            except Exception as e :
                print('-' * 20)
                print('에러가 발생했습니다', e)
                _, _ , tb = sys.exc_info() # tb -> traceback object 
                print ('file name = ', __file__)
                print ('error line No = {}'.format(tb.tb_lineno))
                traceback.print_exc()

