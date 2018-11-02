from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import COOKIES
from urllib.parse import quote
import time

cookies = [{'name': cookie.split('=')[0],
            'value': cookie.split('=')[1]}
           for cookie in COOKIES.replace(' ', '').split(';')]

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(chrome_options=chrome_options)

def init_browser():
    """
        initialize browser
    """
    browser.get('https://index.baidu.com/#/')
    browser.set_window_size(1500, 900)
    browser.delete_all_cookies()
    for cookie in cookies:
        browser.add_cookie(cookie)
    browser.refresh()

def get_into_page(keyword):
    """
        get baiduIndex page
    """
    url = 'https://index.baidu.com/v2/main/index.html#/trend?words=%s' % quote(keyword)
    browser.get(url)

def loop_time_range(startdate, enddate):
    """
    max 6 months
    """
    pass

def loop_move(all_days, keyword):
    """
        to get the index by moving mouse
    """
    time.sleep(2)
    chart = browser.find_element_by_xpath('//*[contains(@class, "index-trend-chart")][1]')
    chart_size = chart.size
    move_step = all_days - 1
    step_px = chart_size['width'] / move_step
    cur_offset = {
        'x': 1,
        'y': chart_size['height'] - 50
    }
    for _ in range(all_days):
        time.sleep(0.1)
        webdriver.ActionChains(browser).move_to_element_with_offset(
            chart, int(cur_offset['x']), cur_offset['y']).perform()
        cur_offset['x'] += step_px
        get_index(keyword)

def get_index(keyword):
    """
        get index datas by html
    """
    date = browser.find_element_by_xpath('//*[contains(@class, "index-trend-chart")][1]/div[2]/div[1]').text
    date = date.split(' ')[0]
    index = browser.find_element_by_xpath('//*[contains(@class, "index-trend-chart")][1]/div[2]/div[2]/div[2]').text
    index = index.replace(',', '').strip(' ')
    print(date, index, keyword)

def main(keyword, startdate, enddate):
    init_browser()
    get_into_page(keyword)
    loop_time_range('test', 'test')
    loop_move(30, keyword)
    browser.quit()

if __name__ == '__main__':
    main('张艺兴', '2018-01-01', '2018-09-01')
    time.sleep(20)
