import os, glob
import src.util as util
from PIL import Image

# Deprecated : from screenshot import Screenshot_Clipping
from Screenshot import Screenshot_Clipping

def canvas_search(driver):
    """Determine to use canvas elements or img elements.
    """
    img_exist = True
    try:
        # Get all canvas elemnets.
        # If canvas element is existed, don't load img elements.
        canvas_data = driver.find_elements_by_tag_name('canvas') 
        canvas_exist = True
    except Exception as e:
        print('Canvas elements are not existed.')
        canvas_exist = False
    
    # If there's not enough canvas elements, don't use canvas elements.
    if len(canvas_data[:-2]) == 0:
        canvas_exist = False

    # If there's enough canvas elements
    else :
        img_exist = False

    return canvas_data, canvas_exist, img_exist


def fullshot_crop(driver, canvas_data, number):
    """Crop image from full size image(capture from monitor).
    Size of each cropped image is size of each canvas elements.
    """

    #screenshot 객체 선언
    screenShotObject = Screenshot_Clipping.Screenshot()

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
        util.createFolder(str(number))

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

def image_merge(number):
    """Merge image and delete cropped image.
    """
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