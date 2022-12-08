from selenium import webdriver

driver = webdriver.Chrome('./mylib/chromedriver')
driver.get('https://www.hermes.cn/cn/zh/?utm_campaign=Brandzone_Search_CN&utm_source=Shenma&utm_medium=Search&utm_content=MOB_Main_Title')
source = driver.find_element_by_css_selector('#block-hermes-commerce-nav-search')
source.clear()
source.send_keys('包')
button = driver.find_element_by_css_selector('#search')
button.click()
input()
