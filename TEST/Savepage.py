import MyUtils


def fun():
    pass


def main():
    fun()


if __name__ == '__main__':
    page=MyUtils.Edge('https://www.baidu.com/s?ie=UTF-8&wd=edge%E6%8D%95%E8%8E%B7%E6%95%B4%E9%A1%B5%20%E5%BF%AB%E6%8D%B7%E9%94%AE')
    page.save()