# Python Selenium automation project
#   Logins to ATPCO
#   Downloads files from Marketview to a directory
#   Logs the Results on a .txt
# by Pedro Araujo - May 2022

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import getpass
import os, fnmatch
import os.path

TODAY = str(date.today())

ATPCO = 'https://faremanager.atpco.net/fmhome/login.jsp'
MARKETVIEW = 'https://faremanager.atpco.net/atpapps/mvui/#/pages/search'

COPA = ['CM - NOVAS ORIGENS']
AEROMEXICO = ['AM_01N', 'AM_02N']
AEROLINEAS = ['CONSULTA_AR_1','CONSULTA_AR_2']
AVIANCA = ['CONSULTA_AV']
AMERICAN = ['AA BR1 ', 'AA BR2 ', 'AA BR3 ', 'AA BR4 ', 'AA BR5 ', 'AA BR6 ', 'AA BR7 ', 'AA BR8 ', 'AA BR9 ', 'AA BR10 ', 'AA BR11 ', 'AA BR12 ', 'AA BR13 ', 'AA BR14 ', 'AA US1 ',  'AA US2 ',  'AA US3 ',  'AA US4 ',  'AA US5 ',  'AA US6 ',  'AA US7 ',  'AA US8 ',  'AA US9 ',  'AA US10 ',  'AA US11 ',  'AA US12 ',  'AA US13 ',  'AA US14 ',  'AA US15 ']

print(''' Welcome message and 

    ============================
    Partner company selector:
    (1) COPA
    (2) AEROMEXICO
    (3) AEROLINEAS
    (4) AVIANCA
    (5) AMERICAN
    ============================
    '''
)

USERNAME = input('Type ATPCO login : ')
PASSWORD = getpass('Type pass: ')

while(True):
    option = int(input(": "))

    match option:
        case 1:
            PARCEIRA = COPA
            dirPath = '\\Path\\to\\Dir'
            break
        case 2:
            PARCEIRA = AEROMEXICO
            dirPath = '\\Path\\to\\Dir'
            break
        case 3:
            PARCEIRA = AEROLINEAS
            dirPath = '\\Path\\to\\Dir'
            break
        case 4:
            PARCEIRA = AVIANCA
            dirPath = '\\Path\\to\\Dir'
            break
        case 5:
            PARCEIRA = AMERICAN
            dirPath = '\\Path\\to\\Dir'
            break
        case _:
            print("Select valid number")

START_TIME = time.time()

chromeOptions = webdriver.ChromeOptions()
preferences = {'download.default_directory' : dirPath}
chromeOptions.add_experimental_option('prefs', preferences)
chrome = webdriver.Chrome(options=chromeOptions)
chrome.get(ATPCO)
chrome.maximize_window()

username = chrome.find_element(By.NAME,'j_username').send_keys(USERNAME)
password = chrome.find_element(By.NAME,'j_password')
password.send_keys(PASSWORD)
password.send_keys(Keys.ENTER)

logDados = open(dirPath + '\logDados.txt', "a")

for busca in PARCEIRA:
    logDados.write('\n' + TODAY + '    pesquisa: ' + busca)

    time.sleep(5)
    chrome.get(MARKETVIEW)

    dropdownMenuClick = WebDriverWait(chrome, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="savedSearchDropdown"]/div/div[3]'))).click()

    fillSearchField = WebDriverWait(chrome, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="savedSearchDropdown"]/div/div[4]/div[1]/input'))).send_keys(busca)
    time.sleep(2)

    searchOptionClick = WebDriverWait(chrome, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="savedSearchDropdown"]/div/div[4]/div[2]/ul/li[2]/div'))).click()
    
    time.sleep(2)

    searchButtonClick = WebDriverWait(chrome, 10).until(EC.element_to_be_clickable((By.ID, 'getData'))).click()

    buttonNotAvailable = True
    while (buttonNotAvailable):
        time.sleep(3)
        downloadButton = chrome.find_elements(By.XPATH, "/html/body/fmis-root/div/fmis-content/div/is-marketview-result/div/div[1]/div[2]/is-download/span[@class='caret is-results-btn is-results-download-btn ng-star-inserted']")

        if (len(downloadButton) > 0):
            downloadButton[0].click()
            buttonNotAvailable = False
    

    numeroDeTarifas = chrome.find_element(By.XPATH, '//*[@id="mv-results-div"]/div[3]/is-result-pagination/div/div[2]/div/button[2]')
    logDados.write(' ' + numeroDeTarifas.text)

numberOfFiles = len(PARCEIRA)
wait = True
while wait:
    time.sleep(1)
    wait = False
    files = fnmatch.filter(os.listdir(dirPath), '*.csv')

    if len(files) != numberOfFiles:
        wait = True
        
END_TIME = time.time()

print('Finishe')
print('Elapsed time: ')
print(END_TIME - START_TIME)

logDados.close()
chrome.close()
os._exit
