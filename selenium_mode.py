from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import psutil
import threading
import time
import requests
import json
import re
from lxml import etree

# Parse the data
def get_info_list(json_data):
    info_dict = {}
    info_list = []
    date_time_list = []
    for data in json_data:
        if data['fields'] == "date_separator,date_text,displayType,all_results_hidden,":
            date_time_list.append(data['p1'])
            continue
        # p1 = id
        # p3 = title
        # p4 = date, time
        if data['p1'] != '':
            info_dict['id'] = data['p1']
            info_dict['title'] = data['p3']
            re_obj = re.compile(r"<p style='margin:0;'>(.*?)</p><p style='margin:0;'>(.*?) &ndash; (.*?)</p>", (re.S))
            result = re_obj.findall(data['p4'])
            info_dict['time'] = result[0]
            print(info_dict)
            info_list.append(info_dict)
            info_dict = {}
    return date_time_list, info_list

# Execute JavaScript operation to scroll
def move_scroll_by(web_driver):
    step_length = 2000
    stop_length = 30000
    while True:
        if stop_length - step_length <= 0:
            break
        # Use JavaScript code to scroll down
        web_driver.execute_script(f'window.scrollBy(0, {step_length})')
        stop_length -= step_length
        time.sleep(0.5)

# Click using JavaScript
def click_by_js(web_driver, xpath):
    for i in range(1, 6):
        more = web_driver.find_element(By.XPATH, xpath)
        web_driver.execute_script('arguments[0].click();', more)
        print(f'Clicked {i} times')

# Check if an element is loaded in the DOM
def find_element_by_xpath(web_driver, xpath):
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.wait import WebDriverWait
    WebDriverWait(web_driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    print(f'{xpath} is loaded')

# Set Chrome path
def set_chrome_path():
    chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application'
    obj = os.popen('path')
    path = obj.read()
    if chrome_path not in path:
        os.popen(f'setx /M PATH "%PATH%;{chrome_path}')
        print('Environment variable configured successfully')
    else:
        print('Environment variable already exists')

# Run Chrome browser
def run_chrome():
    os.popen('chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\selenum\\AutomationProfile"')

# Get Chrome WebDriver
def get_web_driver(debug=False):
    chrome_options = Options()
    # Headless browser
    if debug:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=4000,1600")
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Select Chrome process
def select_chrome_process():
    while True:
        list_of_processes = psutil.pids()
        for i in range(0, len(list_of_processes)):
            try:
                process = psutil.Process(list_of_processes[i])
                if process.cmdline()[0].find("chrome.exe") != -1:
                    return 1
            except:
                pass

# Start the automation process
def start(event_id):
    # Set environment variable
    set_chrome_path()
    # Open browser
    t = threading.Thread(target=run_chrome)
    t.setDaemon(True)
    t.start()
    # Find the process
    while True:
        result = select_chrome_process()
        if result:
            print('Found the process')
            break
    # Get device environment
    web = get_web_driver()
    web.implicitly_wait(30)
    url = 'https://whattodu.campusgroups.com/home_login'
    web.get(url)
    login_btn = web.find_element(By.XPATH, r'//*[@id="topbar"]/div[2]/nav/ul/li[7]/a')
    login_btn.click()
    what_to_du_btn = web.find_element(By.XPATH, r'//*[@id="page-cont"]/div[2]/div/div/div/p[2]/a')
    what_to_du_btn.click()
    username_input = web.find_element(By.XPATH, r'//*[@id="usernameUserInput"]')
    username_input.send_keys('???')
    pwd_input = web.find_element(By.XPATH, r'//*[@id="password"]')
    pwd_input.send_keys('???')
    cont_btn = web.find_element(By.XPATH, r'//*[@id="loginForm"]/div[9]/div[2]/button')
    cont_btn.click()
    # Check if the element is loaded
    find_element_by_xpath(web, '//*[@id="header__btn-cont--events"]/a')
    web.get(f'https://whattodu.campusgroups.com/rsvp?id={event_id}')
    # Register
    register_btn = web.find_element(By.XPATH, r'//*[@id="more_tickets"]/div/div[4]/a')
    register_btn.click()
    return True



    # time_list,info_list = get_infoList(json_data)



    #address
    #https://whattodu.campusgroups.com/rsvp?id=1964683

    #https://whattodu.campusgroups.com/BRE/rsvp_boot?id=1964683
