import re
import string
import time


print('123456'in'1234456')
s1=''
s2=''
for i in range(len(s1)):
    if not s1[i]==s2[i]:
        print(i,s1[i],s2[i])
        break