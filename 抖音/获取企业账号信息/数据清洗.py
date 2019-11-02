import re
import io
#  需要被提取的文件地址
path = "demo.txt"
con = open(path, 'r', encoding='utf-8')
#  提取后的文件地址
f=open('tes2t2.txt','w')
tt1 = set()
for line in con.readlines():
    result = re.findall('([a-zA-Z0-9_\-]{8,})', line)
    if result:
        for itme in result:
            if len(itme) <= 20 and 'QQ' not in itme and '_' not in itme:
                pattern = re.compile('[0-9]+')
                match = pattern.findall(itme)
                if match:
                    tt=itme.lstrip('V')
                    tt=tt.lstrip('v')
                    tt=tt.lstrip('X')
                    tt=tt.lstrip('__')
                    tt1.add(tt)

# 数据去重
for i in tt1:
    f.write(i)
    f.write('\n')
print(tt1)
