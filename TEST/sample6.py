import MyUtils
import selenium
from selenium import webdriver

def main():
    path1='C:\\Users\\ZX\\AppData\\Local\\Microsoft\\Edge\\User Data'
    path2='C:\\Users\\ZX\\AppData\\Local\\Google\\Chrome\\User Data'
    print(path2)
    print(MyUtils.size(path1),MyUtils.size(path2))
    # options = webdriver.ChromeOptions()
    options = webdriver.EdgeOptions()
    options.add_argument(f"--user-data-dir=C:\\Users\\zx\\AppData\\Local\\Microsoft\\Edge\\User Data")
    # options.add_argument(f"--user-data-dir=C:\\Users\\zx\\AppData\\Local\\Google\\Chrome\\User Data")
    driver = webdriver.Edge(options=options)
    # driver = webdriver.Chrome(options=options)
    MyUtils.sleep(30)
if __name__ == '__main__':
    main()