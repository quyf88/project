import requests
import pandas as pd
import pymysql
for a in range(1,999):
    s = "%03d" % a
    url = 'https://hq.sinajs.cn/etag.php?_=1562677804142&list=sh600{}'.format(s)
    print(url)
    r = requests.get(url)
    dome = r.text.split('=')
    if len(dome[1]) < 5:
        continue

    with open('C:/Users/Administrator/Desktop/text.txt','a+') as f:
        f.write(r.text)
        f.write('                            \n')
for line2 in open("C:/Users/Administrator/Desktop/text.txt"):
    a = line2
    s = a.replace('var hq_str_sh', ' ')
    h = s.replace(',', ' ')
    with open("C:/Users/Administrator/Desktop/ass.txt", 'a+') as fp:
        fp.write(h)

#数据库
file = 'C:/Users/Administrator/Desktop/ass.txt'
data = pd.read_excel(file)

db = pymysql.connect('192.168.1.20', 'xx', 'python')
cursor = db.cursor()
try:
    cursor.execute('create table ass(num int  primary  key,date datetime, sale float )')
except:
    print("数据库已经存在!")
querty = """"insert into ass (num, date, sale) values (%s,%s,%s)"""
for r in range(0,len(data)):
    num = data.ix[r,0]
    data = data.ix[r,1]
    sale = data.ix[r,2]
    values = (int(num), set(data), float(sale))
    cursor.execute(querty, values)
cursor.close()
db.commit()
db.close()

db = pymysql.connect('192.168.1.20', 'xx', 'python')
cursor = db.cursor()
cursor.execute('''select * from  ass''')
results = cursor.fetchall()
for row  in results:
    print(row)
cursor.close()
db.commit()
db.close()