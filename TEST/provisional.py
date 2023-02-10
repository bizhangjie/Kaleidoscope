import MyUtils
page=MyUtils.Chrome('https://www.douyin.com/user/MS4wLjABAAAA3F65iJhX1o-tDuuIMaaaXW7Ojmk-ynj78wq2mEmlKVA0kQpflL80FD7LtnmFg-6e')
el=page.element('//*[@id="douyin-right-container"]/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/ul/li[67]/a/div/div[3]/div')
page.look(el)
e=page.element('.//@text',root=el)