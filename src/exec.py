import argparse
import os
import pathlib
from pprint import pprint

import requests

from crawling import Browser

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="parameters")
    parser.add_argument('dn_dir', type=str, help="target directory")
    parser.add_argument('page_num', type=str, help="page number to download")
    args = parser.parse_args()

    print(args.dn_dir)
    print(args.page_num)
    pathlib.Path(args.dn_dir).mkdir(parents=True, exist_ok=True)
    baseNumber = args.page_num
    browser = None

    try:
        browser = Browser()
        readen = browser.readPage(baseNumber)
        # {'images': [(0, 'https://img3.mangashow.me/upload/5061041a2ca98b3a796bea74ba7822aa.jpg'), (1, 'https://img3.mangashow.me/upload/172581b92cd07038b080bc649a4a8e05.jpg'), (2, 'https://img3.mangashow.me/upload/bdffe07fd1afc7ff71d87ecc3b5c37f5.jpg'), (3, 'https://img3.mangashow.me/upload/8a178036ebd5d3b88730eb0944ab8570.jpg'), (4, 'https://img3.mangashow.me/upload/366b7863bfdf3edaff02f8ffbdce634c.jpg'), (5, 'https://img3.mangashow.me/upload/d8dc31d97a7585a2ffff34f84e51a2fc.jpg'), (6, 'https://img3.mangashow.me/upload/d549e5562d6e3130b6d7a0076f06de51.jpg'), (7, 'https://img3.mangashow.me/upload/889076b19a700fa35ea116a3f93637fd.jpg'), (8, 'https://img3.mangashow.me/upload/5b10be1f495bc325f903a29c00d497d0.jpg'), (9, 'https://img3.mangashow.me/upload/4284f1ef7a98d73d287921a3849e215f.jpg'), (10, 'https://img3.mangashow.me/upload/41f4ec653294e30faaafd335cacbfc52.jpg'), (11, 'https://img3.mangashow.me/upload/0a7a1f3b87cb94f4e7eb7beb43f5e26e.jpg'), (12, 'https://img3.mangashow.me/upload/395ed62fb4ff4a5af0e5aac5fb68575c.jpg'), (13, 'https://img3.mangashow.me/upload/87119e064afa7a5a108e6c6ba8c6c5af.jpg'), (14, 'https://img3.mangashow.me/upload/e365b20678d34148efe1f22de8aa053a.jpg'), (15, 'https://img3.mangashow.me/upload/41e1a454e75e0d05b8ef00c219d3cd8a.jpg'), (16, 'https://img3.mangashow.me/upload/9a3f96f05261fb609dda084afc02f616.jpg'), (17, 'https://img3.mangashow.me/upload/74c7847131d7f6c7e16ff005592e2152.jpg'), (18, 'https://img3.mangashow.me/upload/f908d467831e4dd7062da8b14247d597.jpg'), (19, 'https://img3.mangashow.me/upload/6f716a26cbad1f66d778c9c40497d181.jpg'), (20, 'https://img3.mangashow.me/upload/14dc66d0c7c605ccda3a6d3cac0cb74c.jpg'), (21, 'https://img3.mangashow.me/upload/9aa3b1bd04a3fb723a52b47f29ef5034.jpg'), (22, 'https://img3.mangashow.me/upload/96e8020453c1b9ee1b849946923b1165.jpg'), (23, 'https://img3.mangashow.me/upload/2930792fdb76aef960c3ce90bb12db63.jpg'), (24, 'https://img3.mangashow.me/upload/563b1ad58e8b802953bbed0f3c66b91d.jpg'), (25, 'https://img3.mangashow.me/upload/9412198c909b45eca23f2cdac7f0e813.jpg'), (26, 'https://img3.mangashow.me/upload/f371f1db49bcf997fed23196b1390860.jpg'), (27, 'https://img3.mangashow.me/upload/82ea5ef7e0b0b3f1a61eb97b5a29b9e2.jpg'), (28, 'https://img3.mangashow.me/upload/bf2f24b73adb789bcbb78e6beefaf9c5.jpg'), (29, 'https://img3.mangashow.me/upload/bd637d9c5e302a54ec1d8c6dfa31dfeb.jpg'), (30, 'https://img3.mangashow.me/upload/9f6683a5b9771005e72b0a9c44097ec9.jpg'), (31, 'https://img3.mangashow.me/upload/a6111899560b424c8eb0d63e91f71c15.jpg'), (32, 'https://img3.mangashow.me/upload/e87a2eae54c6357583d8770883c08bfd.jpg'), (33, 'https://img3.mangashow.me/upload/8d4432a7baf2f923dec2b58d3d6ff86b.jpg'), (34, 'https://img3.mangashow.me/upload/0d876915dac4545497735897a9ca8296.jpg')], 'title': ['마왕님의 갑작스런 던전 시찰', '2'], 'page_info': [('427271', '2'), ('113523', '1')]}

        infos = dict((page_num, {}) for page_num, _ in readen['page_info'])
        infos[baseNumber]['title'] = readen['title']
        infos[baseNumber]['images'] = readen['images']

        for page_num, info_dict in infos.items():
            if not info_dict:
                readen = browser.chooseOption(page_num)
                info_dict['title'] = readen['title']
                info_dict['images'] = readen['images']
        pprint(infos)
        for one_issue in infos.values():
            # dir check
            target_dir = os.path.join(args.dn_dir,*(one_issue['title']))
            print(one_issue['title'])
            pathlib.Path(target_dir).mkdir(parents=True, exist_ok=True)
            for img_num, img_link in one_issue['images']:
                target_file = os.path.join(target_dir, "%03d.jpg" % img_num)
                print(target_file)
                if not os.path.exists(target_file):
                    req = requests.get(img_link)
                    if req.status_code < 300 and req.status_code >=200:
                        with open(target_file, 'wb') as fw:
                            fw.write(req.content)
                    else:
                        raise Exception(str(req))
    except Exception as e:
        if browser:
            Browser.driver_close()
        raise e


