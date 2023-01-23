import MyUtils
i='2023年1月22日, 星期日_16.csv'
print(MyUtils.research(r"_\d+\.csv$", i))