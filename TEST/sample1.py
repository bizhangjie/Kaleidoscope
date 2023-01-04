import copy
import time
from openpyxl import Workbook
from lxml import etree
from selenium import webdriver


def main(url, filename):
    # url = r'http://guba.eastmoney.com/list,zg80048752,f_1.html'
    wb = Workbook()  # 定义Excel对象
    sheet = wb.active  # 定义一个sheet页
    sheet.append(['阅读', '评论', '标题', '作者', '发帖时间'])  # 定义sheet页的第一行
    # 以下为加载Chrome的驱动
    dirver = webdriver.Chrome(executable_path=r'D:\standardizedPF\python\310\chromedriver.exe')
    dirver.get(url)  # 加载url
    count = 1  # 执行次数，默认一次
    while True:
        response = dirver.page_source  # 获取网页源码
        html_str = etree.HTML(response)  # HTML格式展示
        for i in range(2, 81):
            # 通过xpath定位需要爬的那一行数据
            odd = html_str.xpath(r'//*[@id="articlelistnew"]/div[{}]//text()'.format(i))
            # 以下方法为删除获取字符串中的空值和"公告"的数据列，可以根据自己的需要进行配置
            odd_remove = get_real_arr(odd)


            del odd_remove[0]
            del odd_remove[1]
            del odd_remove[2]
            del odd_remove[3]
            del odd_remove[4]
            del odd_remove[5]
            sheet.append(odd_remove)  # 添加经过清洗后的数据
        print('******正在下载{}页数据******'.format(count))
        time.sleep(5)
        # 以下方法是点击“下一页”按钮，可以通过xpath定位，也可以通过linktext定位
        # dirver.find_element_by_xpath(r'//*[@id="articlelistnew"]/div[82]/span/span/span[1]/a[12]').click()
        dirver.find_element_by_link_text("下一页").click()
        count += 1  # 循环执行
        time.sleep(5)
        if count == 4:  # 设置爬的数据页数
            break
    wb.save(filename)
    print('****全部数据下载完成****')


def get_real_arr(arr):  # 该功能是清洗数组中的某些值
    """
    返回删除所有空值后的arr
    """
    arr_copy = copy.deepcopy(arr)
    arr_copy = list(filter(None, arr_copy))
    while ' ' in arr_copy:
        arr_copy.remove(' ')
    while '公告' in arr_copy:
        arr_copy.remove('公告')
    return arr_copy


if __name__ == '__main__':
    # 通过定义不同的对象来生成不同的文件， 当然也可以在某个文件中进行配置，然后循环使用
    url = r'http://guba.eastmoney.com/list,zg80048752,f_1.html'
    filename = "东方财富网信息采集_中银基金吧.xlsx"
    main(url, filename)
    url = r'http://guba.eastmoney.com/list,zg80000248,f.html'
    filename = "东方财富网信息采集_广发基金吧.xlsx"
    main(url, filename)

