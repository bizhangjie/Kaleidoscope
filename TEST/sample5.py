import MyUtils
import selenium
from selenium import webdriver

def main():

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir=C:\\Users\\ZX\\AppData\\Local\\Microsoft\\Edge\\User Data")
    driver = webdriver.Edge(options=options)
    MyUtils.sleep(30)
if __name__ == '__main__':
    main()
