import sys, platform, traceback, json, os

def read_files() -> tuple:
    try:
        with open('website.txt', 'r', encoding='utf-8') as file:
            number = int(file.readline()[:-1])
            url = file.readline()[:-1]
            next_button = file.readline()[:-1]
            comic_name = file.readline()[:-1]
            site_name = file.readline()[:-1]
        
        with open('setting.conf', 'r', encoding='utf-8') as conf_file:
            comic_sites = [comic_site for comic_site in conf_file.readline()[:-1].split('=')[-1].split(',')]
            windows_save_path = conf_file.readline()[:-1].split('=')[-1]
            darwin_save_path = conf_file.readline()[:-1].split('=')[-1]
            linux_save_path = conf_file.readline()[:-1].split('=')[-1]
            thumbnail_link = conf_file.readline()[:-1].split('=')[-1]
            unnecessary_link = conf_file.readline()[:-1].split('=')[-1]

            comic_path = set_comic_path(windows_save_path, darwin_save_path, linux_save_path)

        with open('headers.json', 'r') as json_file:
            headers_json = json.load(json_file)

        return {
            'number': number, 
            'url': url, 
            'next_button': next_button, 
            'comic_name': comic_name, 
            'site_name': site_name, 
            'comic_sites': comic_sites, 
            'comic_path': comic_path,
            'headers' : headers_json,
            'thumbnail_link': thumbnail_link,
            'unnecessary_link': unnecessary_link
        }

    except Exception as e:
        traceback.print_exc()
        sys.exit('Error caused by util.readFile')

def set_comic_path(wp, dp, lp) -> str:
    platform_name = platform.system()
    if platform_name == "Windows":
        comic_path = wp
    elif platform_name == "Darwin":
        comic_path = dp
    elif platform_name == "Linux":
        comic_path = lp

    return comic_path

def create_dir(root, directory):
    try:
        path = os.path.join(root, directory)
        if not os.path.exists(path):
            os.makedirs(path)
        return path
    except OSError:
        print('Error occured with creating', directory)
        traceback.print_exc(file=sys.stdout)
        sys.exit('Error caused by util.createFile')