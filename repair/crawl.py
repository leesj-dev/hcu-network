from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time

load_dotenv()
login_id = os.getenv("id")
login_pw = os.getenv("pw")


link = "https://hcuhs.kr/login.php"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(link)

driver.find_element(By.ID, "st").click()
driver.find_element(By.XPATH, "/html/body/form/div/input[1]").send_keys(login_id)
driver.find_element(By.ID, "password").send_keys(login_pw)
driver.find_element(By.XPATH, "/html/body/form/div/input[3]").click()
time.sleep(1)

for i in range(1, 34):
    driver.get("https://hcuhs.kr/repair/student.php?page=" + str(i) + "&text1=&choice=")
    page_html = driver.page_source
    page_html = page_html.replace(' style=";"', '')
    page_html = page_html.replace('1.jpg', '../1.jpg')
    page_html = page_html.replace('../student.php', '../student.html')
    page_html = page_html.replace('student.php?page=' + str(i) + '&amp;choice=&amp;text1=', './student_' + str(i) + '.html')
    page_html = page_html.replace('write_s.php', './write_s.html')
    page_html = page_html.replace('new.gif', '../new.gif')

    j = 2
    while True:
        try:
            href = driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr[" + str(j) + "]/td[2]/a").get_attribute("href")
            uid = href[href.find("qUID=") + 5 : href.find("&page=")]
            page_html = page_html.replace('view_s.php?qUID=' + uid + '&amp;page=' + str(i) + '&amp;choice=&amp;text1=', 'view_s_' + str(i) + '_'+ uid + '.html')

            driver.get(href)
            page_html_n = driver.page_source
            page_html_n = page_html_n.replace(' style=";"', '')
            page_html_n = page_html_n.replace('1.jpg', '../1.jpg')
            page_html_n = page_html_n.replace('../student.php', '../student.html')
            page_html_n = page_html_n.replace('student.php?page=' + str(i) + '&amp;choice=&amp;text1=', './student_' + str(i) + '.html')
            page_html_n = page_html_n.replace('write_s.php', './write_s.html')
            page_html_n = page_html_n.replace('default_icon.gif', '../default_icon.gif')

            with open('./repair/view_s_' + str(i) + '_'+ uid + '.html', "w") as f:
                f.write(page_html_n)

            driver.get("https://hcuhs.kr/repair/student.php?page=" + str(i) + "&text1=&choice=")
            j += 1

        except:
            break



    page_html = page_html.replace('/repair/student.php?page=', './student_')
    page_html = page_html.replace('&amp;text1=&amp;choice=', '.html')

    with open('./repair/student_' + str(i) + '.html', "w") as f:
        f.write(page_html)