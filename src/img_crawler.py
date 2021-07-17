from urllib.request import urlopen, Request
import os
import src.util as util

def save_image_tag(bs_object, conf):
    # Header for passing header checker
    if conf['site_name'] == conf['comic_sites'][0]:
        headers = conf['headers']['m']
    
    elif conf['site_name'] == conf['comic_sites'][1]:
        headers = conf['headers']['w']

    #이미지 소스 선택
    targetString = 'https://'
    targetlen = len(targetString)

    #썸네일 사진 패스하기
    thumbnailString = conf['thumbnail_link']
    thumbnaillen = len(thumbnailString)

    #그 외 불필요 이미지 파일 패스하기
    otherString = conf['unnecessary_link']
    otherStringlen = len(otherString)

    # 인스턴스의 find_all 이라는 함수에 img 태그가 있으면 img_data에 넣어줌
    img_data = bs_object.find_all("img")

    num_comic_img = 2
    img_idx = 1
    '''
    structure of img tag(prop list)
    1. src
    2. data-....
    3. style
    '''
    for img_tag in img_data:
        # print(list(img_tag.attrs.keys()))
        
        attr_list = list(img_tag.attrs.keys())

        # if lenght of attribute is less than 3
        # it isn't comic image
        if len(attr_list) < 2:
            continue
        # print(attr_list)

        isComicImg = False
        # if it is comic image,
        # attribute list must contain 'data class'
        for attr in attr_list:
            if attr[:4] == 'data':
                isComicImg = True
                data_tag = attr
        
        # some image tag contains 'itemprop' class
        if conf['site_name'] == conf['comic_sites'][0]:
            if 'itemprop' in attr_list:
                isComicImg = True
                data_tag = 'content'

        elif conf['site_name'] == conf['comic_sites'][1]:
            if 'alt' in attr_list:
                isComicImg = True
                data_tag = 'src'

        if not isComicImg:
            continue
        
        print(img_idx, img_tag.attrs[data_tag])

        srcString = img_tag.attrs[data_tag]

        #썸네일은 건너뛰기
        if srcString[:thumbnaillen] == thumbnailString:
            print("pass thumbnail")
            continue

        if 'assets' in srcString:
            print("pass img of assets")
            continue

        #서버 이미지면 저장 그만하기
        #모든 만화 이미지는 외부 서버에 있음
        print("img index=", img_idx)
        if (srcString[:otherStringlen] == otherString):
            print("break othrestring")
            continue

        #구글 드라이브 혹은 타서버에 저장된 만화 이미지 파일 처리
        if srcString[0:targetlen] == targetString:
            #딕셔너리를 순서대로 넣어줌
            imgReq = Request(url=img_tag.attrs[data_tag], headers=headers)
            imageDownload = urlopen(imgReq).read()

            #파일 이름 생성
            filename = "image"+str(img_idx).zfill(2)+'.jpg'

            folder_path = os.path.join(conf['comic_name'], str(conf['number']))

            #폴더 생성
            path = util.create_dir(conf['comic_path'], folder_path)

            #파일 생성 경로
            filepath = os.path.join(path, filename)

            #파일 생성
            with open(filepath,"wb") as f:
                f.write(imageDownload)
            
            print('save => "' + path + "'/" + str(conf['number']) + '"')
            
            img_idx += 1