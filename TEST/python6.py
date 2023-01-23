import MyUtils
import selenium
from selenium import webdriver
from selenium.webdriver.edge.options import Options

def main():
    mode='edge'
    if mode=='edge':
        options = Options()
        options.add_argument(f"--user-data-dir=F:\\User Data")
        driver = webdriver.Edge(options=options)
    elif mode=='chrome':
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir=C:\\Users\\17371\\AppData\\Local\\Google\\Chrome\\User Data")
        driver = webdriver.Chrome(options=options)
    MyUtils.sleep(30)
if __name__ == '__main__':
    main()