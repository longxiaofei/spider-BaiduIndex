"""
    author: libra
    date: 2018-09-26
"""
from urllib.parse import urlencode, unquote
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from PIL import Image, ImageOps
from config import COOKIES
import pytesseract
import datetime
import requests
import random
import base64
import json
import time
import re
import os
import io

headers = {
    'Cookie': COOKIES,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}
base_dir = os.path.abspath(os.path.dirname(__file__))

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get('file://%s/template.html' % base_dir)

with open('%s/Raphael.js' % base_dir, 'r') as f:
    driver.execute_script(f.read())

js_template = """
document.getElementsByClassName('view-value')[0].innerHTML = '%s'
"""

def get_res1(html):
    """
        get res1, parse html to get res1.
    """
    res = re.search(r'.*PPval\.ppt = \'(.*?)\'', html)
    res = unquote(res[1]) if res else None
    return res


def get_res2(html):
    """
        get res2, parse and get js code in the html,
        then run this js code in the browser, need Raphael.js
    """
    res_script = re.search(r'<script type="text/javascript">\n(T\(function[\d\D]*?)</script>', html)
    res_script = res_script[1] if res_script else None
    res_script_list = res_script.split('\n')
    first_var = re.search(r'(.{15}) = \'.{50}\';', res_script)[1].lstrip(' ')
    all_var = []
    all_var.append(first_var)
    final_script_list = []
    res_var = None
    for line in res_script_list:
        if res_var:
            break
        for var in all_var:
            if var in line:
                temp_var = re.search(r'(.*?) = .*?', line)
                if temp_var:
                    temp_var = temp_var[1].lstrip(' ')
                    all_var.append(temp_var)
                    final_script_list.append(line.strip(' '))
                else:
                    res_var = line.lstrip(' ').rstrip(');').replace('BID.res2(', '')
                break
    final_script = '\n'.join(final_script_list)
    res_script = """
    function %s_func () {
        %s
        return %s
    }
    return %s_func()
    """ % (res_var, final_script, res_var, res_var)
    result = driver.execute_script(res_script)
    return result


def get_res3_datas(res1, res2, startdate, enddate):
    """
        get res3, 
    """
    url_args = {
        'res': res1,
        'res2': res2,
        'startdate': startdate,
        'enddate': enddate,
    }
    url = 'http://index.baidu.com/Interface/Search/getSubIndex/?' + urlencode(url_args)
    html = request(url)
    datas = json.loads(html)
    res3_list = datas['data']['all'][0]['userIndexes_enc'].split(',')
    res3_datas = []
    cur_date = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    for res3 in res3_list:
        res3_datas.append({
            'res3': res3,
            'date': cur_date.strftime('%Y-%m-%d')
        })
        cur_date += datetime.timedelta(days=1)
    return res3_datas


def get_background(url):
    """
        get backgroud-img
    """
    response = requests.get(url, headers=headers)
    img_base64 = base64.b64encode(response.content).decode()
    return img_base64


def get_the_index_html(res1, res2, res3):
    """
        get the BaiduIndex of html
    """
    url_args = {
        'res': res1,
        'res2': res2,
        'res3[]': res3,
    }
    url = 'http://index.baidu.com/Interface/IndexShow/show/?' + urlencode(url_args)
    html = request(url)
    if html:
        datas = json.loads(html)
        html_code = datas['data']['code'][0]
        img_url = re.search(r'url\((".*?")\)}', html_code)[1]
        img_base64 = get_background('http://index.baidu.com' + img_url.replace('"', ''))
        html_code = html_code.replace(img_url, 'data:image/png;base64,%s' % img_base64)
        return html_code


def request(url):
    """
        a simple function of use http/get
    """
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response.encoding = 'gbk'
        result = response.text.replace('\r', '')
    else:
        print('request fail!')
        result = None

    return result


def get_the_index(html):
    """
        get reuslt about index of baidu
        ps: use js to change html and crop image about index of baidu
    """
    js_code = js_template % html
    driver.execute_script(js_code)
    width_list = re.findall(r'style="width:(\d*?)px;"', html)
    screen_hot = driver.get_screenshot_as_base64()
    img_byte = base64.b64decode(screen_hot)
    the_index = parse_index_img(img_byte, width_list)
    return the_index


def parse_index_img(img_byte, width_list):
    """
        get index by tesseract to parse image
    """
    all_width = 0
    for width in width_list:
        all_width += int(width)
    im = Image.open(io.BytesIO(img_byte)).convert('RGB')
    im = im.crop((0,8,all_width*2,32))
    im = im.resize((im.size[0]*6, im.size[1]*6))
    # im.save('test.png')
    result = pytesseract.image_to_string(im, config='digits')
    result = result.replace(' ', '').replace('.', '')
    return result


def sleep_fuc():
    time.sleep(random.randint(1100, 2100)*0.001)


def main(keyword, startdate, enddate):
    """
        main
    """
    url_args = {
        'tpl': 'trend',
        'word': keyword.encode('gbk')
    }
    url = 'http://index.baidu.com/?' + urlencode(url_args)
    html = request(url)
    if html:
        res1 = get_res1(html)
        res2 = get_res2(html)
        res3_datas = get_res3_datas(res1, res2, startdate, enddate)
        for res3_data in res3_datas[]:
            sleep_fuc()
            res3 = res3_data['res3']
            date = res3_data['date']
            html = get_the_index_html(res1, res2, res3)
            the_index = get_the_index(html)
            result = {
                'keyword': keyword,
                'date': date,
                'the_index': the_index,
            }
            yield result

    driver.quit()

if __name__ == "__main__":
    pass
