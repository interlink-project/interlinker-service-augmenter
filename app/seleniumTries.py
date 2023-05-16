from selenium.webdriver.chrome.options import Options
from selenium import webdriver

# ---------------------------------------------------------------------------------
# With a Viewer
# ---------------------------------------------------------------------------------
# DRIVER_PATH = "C:\\Users\\Daniel\\Downloads\\chromedriver_win32\\chromedriver.exe"
# driver = webdriver.Chrome(executable_path=DRIVER_PATH)
# driver.delete_all_cookies()
# driver.implicitly_wait(15)
# driver.maximize_window()

# url = 'https://dev.interlink-project.eu/'

# driver.get(url)
# driver.refresh()

# content = driver.find_element_by_name('html').text

# print(content)

# ---------------------------------------------------------------------------------
# Without a Viewer
# ---------------------------------------------------------------------------------
DRIVER_PATH = "C:\\Users\\Daniel\\Downloads\\chromedriver_win32\\chromedriver.exe"
options = Options()
options.headless = True

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

driver.delete_all_cookies()
driver.implicitly_wait(15)
driver.maximize_window()

url = 'https://dev.interlink-project.eu/'

driver.get(url)

pageSource = driver.find_element_by_xpath("//*").get_attribute("outerHTML")

print(pageSource)
# print(driver.page_source)

driver.quit()
