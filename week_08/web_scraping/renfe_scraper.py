########################################################################################################################
# IMPORTS

import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

########################################################################################################################
# PARAMETERS

# renfe
ORIGIN = 'MADRID'
DESTINATION = 'PONFERRADA'
DAYS_TILL_TRIP = 5

# selenium
HEADLESS = True

# scraping
SCRAPING_DICT = {
    'id': {
        'cookies_button': 'onetrust-accept-btn-handler',
        'train_table': 'listaTrenesTBodyIda',
    },
    'class': {
        'round_trip_menu_button': 'menu-button',
        'start_date_menu': 'rf-search__dates',
        'start_date_apply_button': 'lightpick__apply-action-sub',
        'query_trips_button': 'mdc-button__touch',
    },
    'css_selector': {
        'origin': '#origin > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)',
        'destination': '#destination > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)',
        'one_way_ticket_button': '#tripType > div > div > ul > li:nth-child(1) > span',
        'start_date_right_arrow': 'i.icon-arrow_right:nth-child(1)',

    }
}

########################################################################################################################
# SCRIPT

os.environ['PATH'] = f'{os.environ["PATH"]}:{os.getcwd()}/drivers'

options = Options()
options.headless = HEADLESS

print('launching browser...')

try:
    driver = webdriver.Firefox(options=options)
    driver.get('https://www.renfe.com/')

    # wait till html is finally rendered
    time.sleep(1)
    
    print('filling form...')
    
    # close cookies
    cookies_button = driver.find_element_by_id(SCRAPING_DICT['id']['cookies_button'])
    cookies_button.click()

    # set origin
    origin = driver.find_element_by_css_selector(SCRAPING_DICT['css_selector']['origin'])
    origin.send_keys(ORIGIN)
    origin.send_keys(Keys.ARROW_DOWN)
    origin.send_keys(Keys.ENTER)

    # set destination
    destination = driver.find_element_by_css_selector(SCRAPING_DICT['css_selector']['destination'])
    destination.send_keys(DESTINATION)
    destination.send_keys(Keys.ARROW_DOWN)
    destination.send_keys(Keys.ENTER)

    # open round trip menu
    round_trip_menu_button = driver.find_element_by_class_name(SCRAPING_DICT['class']['round_trip_menu_button'])
    round_trip_menu_button.click()

    # choose one-way ticket
    driver.find_element_by_css_selector(SCRAPING_DICT['css_selector']['one_way_ticket_button']).click()

    # open start date menu
    driver.find_element_by_class_name(SCRAPING_DICT['class']['start_date_menu']).click()

    # increase DAYS_TILL_TRIP days today's date
    for i in range(DAYS_TILL_TRIP):
        driver.find_element_by_css_selector(SCRAPING_DICT['css_selector']['start_date_right_arrow']).click()

    # select date
    driver.find_element_by_class_name(SCRAPING_DICT['class']['start_date_apply_button']).click()

    print('querying trips...')
    
    # query trips
    driver.find_element_by_class_name(SCRAPING_DICT['class']['query_trips_button']).click()

    # parse trips
    trips = driver.find_element_by_id(SCRAPING_DICT['id']['train_table'])
    print(f'available trips:\n{trips.text}')

    # get cookies
    cookies_raw = driver.get_cookies()

    cookies = {}
    for cookie in cookies_raw:
        cookies[cookie['name']] = cookie['value']

    if 'DWRSESSIONID' not in cookies:
        raise KeyError('DWRSESSIONID not in cookies file!')

    print(f'cookies:\n{cookies}')
    
except Exception as ex:
    print(ex)
    
finally:

    driver.close()

