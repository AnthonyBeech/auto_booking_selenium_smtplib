from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import datetime

import smtplib
from email.mime.text import MIMEText


def finder(xpath):
    return WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '{}'.format(xpath))))


EMAIL = **
PASSWORD = **
SPORT = "Sq"
DATE = "07042023"
TIME = 17
FREE = 0
ITER_TIME = 30*60

service = Service(executable_path="/usr/bin/chromedriver")
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--headless")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
options.add_argument("--window-size=1920,1080")
options.add_argument('--start-maximized')

while FREE == 0:
    browser=webdriver.Chrome(service=service, options=options) 
    browser.get("https://account.everyoneactive.com/login/?redirect=/")
    print("enetered site...")

    finder('//*[@id="emailAddress"]').send_keys(EMAIL)
    finder('//*[@id="password"]').send_keys(PASSWORD)
    finder('//*[@id="__next"]/div/div/div/main/div/div/div/div/form/button').click()
    finder('//*[@id="__next"]/div/div/div/aside/div/div/div[2]/ul/li[3]/a').click()

    print("logged in")

    try:
        finder('//*[@id="cookie-accept"]').click()
    except:
        print("no cookie popup")

    browser.switch_to.frame(finder('//*[@id="bookingFrame"]'))
    finder('//*[@id="search-panels"]/div[2]/div[1]/h3').click()
    finder('//*[@id="ctl00_MainContent__advanceSearchUserControl_ActivityGroups"]').send_keys(SPORT)
    finder('//*[@id="ctl00_MainContent__advanceSearchUserControl_startDate"]').send_keys(DATE)
    finder('//*[@id="ctl00_MainContent__advanceSearchUserControl__searchBtn"]').click()

    print("choosing sport...")


    sleep(2)
    finder('//*[@id="ctl00_MainContent__advanceSearchResultsUserControl_Activities_ctrl0_lnkActivitySelect_lg"]').click()
    browser.switch_to.default_content()
    browser.switch_to.frame(finder('//*[@id="bookingFrame"]'))
    sleep(2)

    print("checking for bookings...")

    for t in range(TIME,22):
        for i in range(1, 6):
            try:
                browser.find_element("xpath", '//*[@id="ctl00_MainContent_grdResourceView"]/tbody/tr[{}]/td[{}]/input'.format(t, i))
                court = i
                tcourt = t
                break
            except:
                print("no slot in time {}, court {}".format(t, i))
                court = 0
                tcourt = 0

        if court != 0:
            break

    if court == 0:
        print("no courts")
        browser.close()
        sleep(ITER_TIME)
    else:
        print("courts found!")
        FREE = 1
    print(datetime.datetime.now())
    

print("booking court {}".format(court))
finder('//*[@id="ctl00_MainContent_grdResourceView"]/tbody/tr[{}]/td[{}]/input'.format(tcourt, court)).click()
browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.CONTROL + Keys.HOME)
finder('//*[@id="ctl00_MainContent_btnBasket"]').click()
link = browser.current_url
print("sending booking email...")


fr = "beechhceebtest@gmail.com"
to = "abeech123@virginmedia.com"

MSG = MIMEText(link)
MSG['Subject'] = 'link to booking'
MSG['From'] = fr
MSG['To'] = to

s = smtplib.SMTP('smtp.gmail.com')
s.starttls()
s.login(fr, "ksoaikuvscklnrhd")
s.sendmail(fr, to, MSG.as_string())
s.quit()
