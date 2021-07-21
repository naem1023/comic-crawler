# Comic Cralwer


## Windows-10-build

- Copy & paste 'website.txt', 'setting.conf', 'header.json' to directory of 'windows-10'.
    - If you want samples of files, contact to me.
- If chromedriver doesn't work, update chrome and download chromedriver matched with your chrome version.
- Run 'main.exe'.

## Other OS build

This program can run in any machine that can install all requirments of this program. So, run with python or build executable file with pyinstaller.

---

## Run with python

### Requirements
- python3
- chrome web driver from https://chromedriver.chromium.org/downloads
- modules in requirements.txt
- headers.json, setting.conf, website.txt
  - If you want samples of files, contact to me.
```
pip3 install -r requirements.txt
```
---
### website.txt

```
1. how many
2. website address
3. next button, prev button(just write 'next', 'prev')
4. comic name
5. comic site
```

### Example of webisite.txt
```
1
www.example.com/1
next
comic_name
haha
```
---
### headers.json

```
{
    "identifier of site ": {
        "User-Agent": "Names of User-Agent"
    },
}
```

### Example of header.json
```
{
    "m": {
        "User-Agent": "Mozilla/5.0"
    },
}
```
---
### setting.conf

```
comic_site=site_names
windows_save_path=path
darwin_save_path=path
linux_save_path=path
thumbnail=address_of_thumbnail
unnecessary_string=address_of_unnecessary_string
```

### Example of setting.conf
```
comic_site=haha,hoho
windows_save_path=C:\\a\\b
darwin_save_path=/home/user/a/b/
linux_save_path=/home/user/a/b/
thumbnail=https://example_thumbnail
unnecessary_string=https://example_unnecessary
```

### Run
```
python main.py
```