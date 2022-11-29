import MyUtils
f=MyUtils.txt(MyUtils.projectpath('./browser/Spectrum.txt'))
f1=MyUtils.txt(MyUtils.desktop('ee.txt'))
l=f.l
for i in l:
    if 'youtube'in i:
        f1.l.append(i)
        f.delete(i)
f1.save()
