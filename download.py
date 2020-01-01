# 내장함수
from urllib.request import urlopen, Request
# 명령행 파싱 모듈 argparse 모듈 사용
import argparse
# request => 요청하는거를 웹에 요청한 결과값을 얻어올수 있는 모듈
import requests as req
# 웹에 요청한 결과를 보내주는 모듈
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys

import os
import sys

from Screenshot import Screenshot_Clipping

import glob

#image module
from PIL import Image


def canvasSearch(driver, canvasExist, imgExist):
    try:
        #canvas 인스턴스들 모두 가져오기
        canvas_data = driver.find_elements_by_tag_name('canvas')

        #canvas 인스턴스가 존재하면 img 태그는 로드안함
    except Exception as e:
        print('canvas 태그 존재하지 않음')
        canvasExist = False
    
    #canvas 태그가 없다면
    if len(canvas_data[:-2]) == 0:
        canvasExist = False
    #canvas 태그가 있다면
    else :
        imgExist = False

    return canvas_data, canvasExist, imgExist

def deleteNaviBar(driver):
    #내비 바 요소 제거 자바 스크립트
    js_string = """
    function f() {
   var x = document.getElementsByClassName("manga-bottom-navi");
        for(var i = x.length - 1; i >= 0; i--) {
        x[i].parentNode.removeChild(x[i]);
        }
    }

    f();
    """

    #자바 스크립트 구문 실행
    driver.execute_script(js_string)

def deleteThumbnailList(driver):
    #내비 바 요소 제거 자바 스크립트
    js_string = """
    function f() {
   var x = document.getElementsByClassName("list-container");
        for(var i = x.length - 1; i >= 0; i--) {
        x[i].parentNode.removeChild(x[i]);
        }
    }

    f();
    """

    #자바 스크립트 구문 실행
    driver.execute_script(js_string)
#폴더 생성 함수
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('폴더 생성 에러 ' + directory)


def fullshotCrop(driver, screenShotObject, canvas_data, number):
    #전체 화면 스샷 이름
    fullshotName = "fullshot" + str(number) + '.png'

    #전체화면 스샷 후 저장
    #전체화면 스샷이 존재하지 않을 때만 스샷 진행
    #if not os.path.isfile(os.path.join(fullshotName)):
    image = screenShotObject.full_Screenshot(driver, save_path=r'.', image_name=fullshotName)

    print('\nFull Shot Crop 시작...\n')
    #print('canvas tag 개수 : ', len(canvas_data[:-2]))

    for i in enumerate(canvas_data[:-2]):
        print(i[0], i[1])

        
        filename = "image"+str(i[0]+1).zfill(2)+'.png'

        #폴더 생성
        createFolder(str(number))

        #파일 생성 경로(파일 이름 포함)
        filepath = os.path.join(str(number), filename)

        
        #전체 화면 중 엘레멘트 위치 계산
        location = i[1].location
        size = i[1].size
        x = location['x']
        y = location['y']
        w = size['width']
        h = size['height']
        width = x + w
        height = y + h

        #전체화면 스샷 로드
        image_object = Image.open(image)

        #전체화면 크롭
        image_object = image_object.crop((int(x), int(y), int(width), int(height)))
        

        #경로 구하기
        img_url = os.path.abspath(filepath)

        #저장
        image_object.save(img_url)

        print(str(i[0]+1) + ' -> ' + '저장 폴더 ' + str(number))


#이미지 합치기
def imageMerge(number):
    filepath =  os.path.join(str(number) + "\\")

    target_dir = os.path.abspath(filepath)

    files = sorted(glob.glob(target_dir + "\*.*"))
    
    for i in range(0, len(files), 2):
        firstImage = Image.open(files[i])
        secondImage = Image.open(files[i+1])

        x = firstImage.size[0]
        y = firstImage.size[1] + secondImage.size[1]
        
        #새로운 이미지 생성
        new_image = Image.new('RGB', (x, y))
        print(x, y)
        

        #이미지가 new_image에 들어갈 시작를 box로 설정
        new_image.paste(firstImage, box=(0,0))
        new_image.paste(secondImage, box=(0, firstImage.size[1]))

        #이미지 이름, 경로 게산
        fileName = "merge" + str(int((i+2)/2)) + ".png"
        filepath = os.path.join(target_dir, fileName)

        #이미지 저장
        new_image.save(filepath)

        print(fileName + ' save completely!!..\n')

        os.remove(os.path.join(target_dir, 'image' + str(i+1).zfill(2) + '.png'  ))
        os.remove(os.path.join(target_dir, 'image' + str(i+2).zfill(2) + '.png'  ))

#txt 파일 읽어서 몇 화, 무슨 링크인지 확인
def readTxtFile():
    file = open("website.txt", 'r')

    number = int(file.readline())
    url = file.readline()
    button = file.readline()

    return number, url, button

def saveImageTag(bs_object, driver, number):
    #크롤링 접근 방지 웹사이트용 헤더
    headers = {'User-Agent': 'Mozilla/5.0'}

    #이미지 소스 선택
    targetString = 'https://'
    targetlen = len(targetString)

    #썸네일 사진 패스하기
    subnailString = 'https://chickencdn'
    subnaillen = len(subnailString)

    #그 외 불필요 이미지 파일 패스하기
    otherString = 'https://manamoa'
    otherStringlen = len(otherString)



    print('\n Img 인스턴스로 저장 중')
    #인스턴스의 find_all 이라는 함수에 img 태그가 있으면 img_data에 넣어줌
    img_data = bs_object.find_all("img")

    for i in enumerate(img_data[1:]):
        print(i[0], i[1].attrs['src'])

        srcString = i[1].attrs['src']

        #썸네일은 건너뛰기
        if srcString[0:subnaillen] == subnailString:
            continue

        #마나모아 서버 이미지면 저장 그만하기
        #모든 만화 이미지는 외부 서버에 있음
        if (srcString[0:otherStringlen] == otherString) and i[0] >= 4:
            break

        #구글 드라이브 혹은 타서버에 저장된 만화 이미지 파일 처리
        if srcString[0:targetlen] == targetString:
            #딕셔너리를 순서대로 넣어줌
            imgReq = Request(url=i[1].attrs['src'], headers=headers)
            imageDownload = urlopen(imgReq).read()

            #파일 이름 생성
            filename = "image"+str(i[0]+1).zfill(2)+'.jpg'

            #폴더 생성
            createFolder(str(number))

            #파일 생성 경로
            filepath = os.path.join(str(number), filename)

            #파일 생성
            with open(filepath,"wb") as f:
                f.write(imageDownload)
            
            print('저장 폴더 ' + str(number) + ' 에 저장완료')

def clickNextButton(driver, number, button):
    #다음 페이지 버튼 감별
    if button == 'next':
        #다음 페이지 버튼 요소 가져오기
        nextButton = driver.find_element_by_xpath("""//a[@class="chapter_next"]""")    

        #다음 페이지 버튼 클릭
        nextButton.click()
    elif button == 'prev':
        #다음 페이지 버튼 요소 가져오기
        prevButton = driver.find_element_by_xpath("""//a[@class="chapter_prev"]""")

        #다음 페이지 버튼 클릭
        prevButton.click()
    #텍스트 파일에 버튼 입력 잘못함
    else :
        print('-' * 20)
        print('website.txt에서 버튼 입력이 잘못됐습니다. 확인해 주세요.')
        print('-' * 20)

        sys.exit()
    
    #페이지 url 저장
    url_info = str(driver.current_url)

    number+=1

    print('\n-----' + str(number) + '번째 페이지로 이동 중' + '-----')   

    return number, url_info

def imageCrawl():
    #타겟 사이트 정보 확인
    number, url_info, button = readTxtFile()

    #몇 화인지
    #number = 2

    #screenshot 객체 선언
    screenShotObject = Screenshot_Clipping.Screenshot()

    #크롬 드라이버 로드
    driver = webdriver.Chrome('chromedriver.exe')

    canvasExist = True
    imgExist = True


    while 1:
        try :
            while 1:
                print('\n' + '-' * 20)
                print(str(number) + '번째 만화 페이지 로딩 시작')
                
                #페이지 로드, 전부 될 때까지 대기
                driver.get(url_info)
                print(str(number) + '페이지 로딩 완료...')

                #페이지 엘리먼트들 모두 저장
                req = driver.page_source

                #인스턴스 생성
                bs_object = BeautifulSoup(req)
                
                canvas_data, canvasExist, imgExist = canvasSearch(driver, canvasExist, imgExist)
                    
                #canvas 인스턴스가 존재할 때
                if canvasExist :
                    #내비 바 요소 제거
                    #이래야 전체 스샷해도 내비바가 스샤이 안됨
                    deleteNaviBar(driver)

                    #풀 스샷에서 canvas 태그 크기별로 크롭 실행
                    fullshotCrop(driver, screenShotObject, canvas_data, number)

                    #이미지 합치기 및 잘린 이미지 제거
                    imageMerge(number)

                #canvas 인스턴스가 없어서 img 인스턴스를 로드해야 할 때
                if imgExist :
                    #썸네일 리스트 삭제
                    deleteThumbnailList(driver)

                    #썸네일 리스트 삭제했으니 다시 페이지 요소 저장
                    #페이지 엘리먼트들 모두 저장
                    req = driver.page_source

                    #인스턴스 생성
                    bs_object = BeautifulSoup(req)    

                    #img 태그 저장 함수 호출
                    saveImageTag(bs_object, driver, number)

                number, url_info = clickNextButton(driver, number, button)



        #다음 버튼을 누를 수 없을 때 1
        except NoSuchElementException :
            print('-' * 20)
            _, _ , tb = sys.exc_info() # tb -> traceback object 
            print ('file name = ', __file__)
            print ('error line No = {}'.format(tb.tb_lineno))
            print('만화가 더 이상 없습니다')
            break

        #다음 버튼을 누를 수 없을 때 2
        except ElementNotVisibleException :
            print('-' * 20)
            _, _ , tb = sys.exc_info() # tb -> traceback object 
            print ('file name = ', __file__)
            print ('error line No = {}'.format(tb.tb_lineno))
            print('만화가 더 이상 없습니다')
            break

        #다음 버튼을 누를 수 없을 때 3
        except ElementNotInteractableException :
            print('-' * 20)
            _, _ , tb = sys.exc_info() # tb -> traceback object 
            print ('file name = ', __file__)
            print ('error line No = {}'.format(tb.tb_lineno))
            print('만화가 더 이상 없습니다')
            break

        #이미지 서버 상태가 안 좋아서 이미지 다운이 안될 때
        except FileNotFoundError :
            print('-' * 20)
            print('이미지 로딩에 실패했습니다.')
            print('다시 페이지를 로딩합니다.')
            driver.navigate().refresh()
            numer-=1
            continue

        #그 외 에러 처리
        except Exception as e :
            print('-' * 20)
            print('에러가 발생했습니다', e)
            _, _ , tb = sys.exc_info() # tb -> traceback object 
            print ('file name = ', __file__)
            print ('error line No = {}'.format(tb.tb_lineno))


def main():
    imageCrawl()

if __name__=="__main__":
    main()