#coding:utf-8
import time
import sqlite3
import json
import sys
from bs4 import BeautifulSoup
from collections import OrderedDict


class Db:
    def __init__(self,path):
        self.db_path = path
        self.connect_db()
        
    # 连接数据库
    # 如果数据库文件不存在就创建
    # 如果数据库中表不存在就创建
    
    def connect_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            sql_string = '''CREATE TABLE diff_table
            (id Integer primary key AUTOINCREMENT ,
            productId CHAR(50),
            diff int NOT NULL);'''
            c.execute(sql_string)
        except BaseException as e:
            print(e)
            print("diff_data table exist!")
        try:
            sql_string = '''CREATE TABLE detail_data
            (id Integer primary key AUTOINCREMENT ,
            name CHAR(50),
            productId CHAR(100),
            price int NOT NULL,
            size_list CHAR(100),
            brand_id  CHAR(100),
            color CHAR(100),
            articleNumber CHAR(100),
            authPrice int NOT NULL,
            sellDate CHAR(100),
            exchangeDesc CHAR(100),
            soldNum int NOT NULL,
            text_string CHAR(2000),
            img_list CHAR(2000),
            size_price CHAR(300));'''
            c.execute(sql_string)
        except BaseException as e:
            print(e)
            print("detail_data table exist!")
        try:
            sql_string = '''CREATE TABLE temp_table
            (id Integer primary key AUTOINCREMENT ,
            name CHAR(50),
            productId CHAR(100),
            price int NOT NULL,
            size_list CHAR(100),
            brand_id  CHAR(100),
            color CHAR(100),
            articleNumber CHAR(100),
            authPrice int NOT NULL,
            sellDate CHAR(100),
            exchangeDesc CHAR(100),
            soldNum int NOT NULL,
            text_string CHAR(2000),
            img_list CHAR(2000),
            size_price CHAR(300));'''
            c.execute(sql_string)
        except BaseException as e:
            print(e)
            print("temp_table table exist!")
        c.close()
        conn.commit()
        conn.close()

    # 获取连接对象 以及游标对象
    def get_conn_c(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        return conn,c


    # 查询
    # 返回 对象 列表
    def query(self,productId = None,is_all = False):
        conn,c = self.get_conn_c()
        if not is_all:
            sql_string = "SELECT productId,data_json from poison_data where productId = {}".format(productId)
        else:
            sql_string = "SELECT productId,data_json from poison_data "
        try:
            c.execute(sql_string)
        except:
            print("error query!")
        data = c.fetchall()
        result = []
        for i in data:
            json_data = i[1]
            try:
                json_data = json.loads(json_data)
            except:
                json_data = json.loads(json_data.replace("###","'"))
            temp = {
                "productId" : i[0],
                "data" : json_data
            }
            result.append(temp)
        c.close()
        conn.commit()
        conn.close()
        return result
    # 删除
    def delete(self,to,timestmap):
        pass
    
    # 更新基本信息
    def update(self,msg):
        conn,c = self.get_conn_c()
        try:
            c.execute('''UPDATE poison_data SET timestamp = ? WHERE productId = ?;''',[str(time.time()),msg['productId']])
            c.execute('''UPDATE poison_data SET data_json = ? WHERE productId = ?;''',[json.dumps(msg['json_data']),msg['productId']])
        except BaseException as e:
            with open("error.txt",'a+',encoding="utf-8") as f:
                f.write("{} {} {}".format("#u",str(msg['productId']),str(e) + "\n"))
        c.close()
        conn.commit()
        conn.close()

    def query_basic_exists(self,msg):
        data = self.query(msg['productId'])
        if not data:
            return False
        else:
            return True

   
    
    def insert_basic_table(self,msg):
        conn,c = self.get_conn_c()
        try:
            sql_string = '''INSERT INTO poison_data (productId,timestamp,data_json)VALUES (?,?,?)'''
            c.execute(sql_string,[str(msg['productId']),str(time.time()),json.dumps(msg['json_data'])])

        except BaseException as e:
            print(e)
            with open("error.txt",'a+',encoding="utf-8") as f:
                f.write("{} {} {}".format("#ib",str(msg['productId']),str(e) + "\n"))
        c.close()
        conn.commit()
        conn.close()

    def query_diff_exists(self,msg):
        conn,c = self.get_conn_c()
        sql_string = "SELECT productId from diff_data where productId = {}".format(msg['productId'])
        c.execute(sql_string)
        data = c.fetchall()
        if not data:
            return False
        else:
            return True
        c.close()
        conn.commit()
        conn.close()

    def query_diff_item_data(self,msg):
        conn,c = self.get_conn_c()
        sql_string = "SELECT diff from diff_data where productId = {}".format(msg['productId'])
        c.execute(sql_string)
        data = c.fetchall()
        try:
            return data[0][0]
        except:
            return 0
        c.close()
        conn.commit()
        conn.close()

    def update_diff_table_item(self,msg):
        try:
            org_diff = self.query_diff_item_data(msg)
            old_data = int(self.query(msg['productId'])[0]['data']['data']['detail']['soldNum'])
            new_data = int(msg['json_data']['data']['detail']['soldNum'])
            new_diff = new_data - old_data
            conn,c = self.get_conn_c()
            diff = org_diff + new_diff
            sql_string = '''UPDATE diff_data SET timestamp = ? where productId = ?;'''
            c.execute(sql_string,[str(time.time()),msg['productId']])
            sql_string = '''UPDATE diff_data SET diff = ? where productId = ?;'''
            c.execute(sql_string,[diff,msg['productId']])
            sql_string = '''UPDATE diff_data SET data_json = ? where productId = ?;'''
            c.execute(sql_string,[json.dumps(msg['json_data']),msg['productId']])
            c.close()
            conn.commit()
            conn.close()
        except BaseException as e:
            with open("error.txt",'a+',encoding="utf-8") as f:
                f.write("{} {} {}".format("#ud",str(msg['productId']),str(e) + "\n"))

    def insert_diff_table(self,msg):
        try:
            if not self.query_diff_item_data(msg):
                conn,c = self.get_conn_c()
                sql_string = '''INSERT INTO diff_data (productId,timestamp,diff,data_json)VALUES (?,?,?,?)'''
                c.execute(sql_string,[str(msg['productId']),str(time.time()),"0",json.dumps(msg['json_data'])])
                c.close()
                conn.commit()
                conn.close()
            else:
                self.update_diff_table_item(msg)
        except BaseException as e:
            pass
            with open("error.txt",'a+',encoding="utf-8") as f:
                f.write("{} {} {}".format("#id",str(msg['productId']),str(e) + "\n"))

    def parse_html(self,html):
        soup = BeautifulSoup(str(html),'lxml')
        text_tag = soup.find_all('p')
        text = ''
        for i in text_tag:
            text += i.get_text(strip=True)
        return text

    def insert_detail(self,msg):
        try:
            data = msg['json_data']['data']
            result = {
                "productId": data['detail']['productId'],
                "brand_id" : data['detail']['brandId'],
                "name": data['detail']['title'],
                "size_list" : ",".join(data['detail']['sizeList']),
                "color" : data['detail']['color'],
                "articleNumber" : data['detail']['articleNumber'],
                "authPrice" : int(data['detail']['authPrice'] / 100),
                "sellDate" : data['detail']["sellDate"],
                "exchangeDesc" : data["exchangeDesc"],
                "text_string" : self.parse_html(data['imageAndText']),
                "soldNum"   : data['detail']['soldNum'],
                "img_list"  : msg['img_list']
            }
            try:
                if type(data['item']['price']) == str:
                    data['item']['price'] = int(data['item']['price'])
                result["price"] = data['item']['price'] / 100
                if result["price"] == 0:
                    result["price"] = "--"
            except:
                result["price"] = "--"
            size_price = []
            for i in data['sizeList']:
                temp = []
                temp.append(i['size'])
                try:
                    if type(i['item']['price']) == str:
                        i['item']['price'] = int(i['item']['price'])
                    price = int(i['item']['price'] / 100)
                except:
                    price = "--"
                temp.append(price)
                size_price.append(temp)
            result['size_price'] = json.dumps(size_price)
            conn,c = self.get_conn_c()
            for i in result:
                if type(result[i]) != int:
                    result[i] = json.dumps(result[i])
            sql_string = '''INSERT INTO detail_data (name,productId,price,size_list,brand_id,color,articleNumber,authPrice,sellDate,exchangeDesc,soldNum,text_string,img_list,size_price) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
            c.execute(sql_string,[result['name'],result['productId'],result['price'],result['size_list'],result['brand_id'],result['color'],result['articleNumber'],result['authPrice'],result['sellDate'],result['exchangeDesc'],result['soldNum'],result['text_string'],result['img_list'],result['size_price']])
            c.close()
            conn.commit()
            conn.close()
        except BaseException as e:
            with open("error.txt",'a+',encoding="utf-8") as f:
                f.write("{} {} {}".format("#ida",str(msg['productId']),str(e) + "\n"))
                f.write(str(msg['json_data']) + "\n")
     

    def query_diff(self):
        conn,c = self.get_conn_c()
        try:
            sql_string = "SELECT productId,diff from diff_data ORDER BY diff DESC LIMIT 10"
            c.execute(sql_string)
        except BaseException as e:
            print(e)
        data = c.fetchall()
        result = []
        for i in data:
            temp = {
                "diff" : i[1]
            }
            sql_string = "SELECT * from detail_data where productId = ?"
            c.execute(sql_string,[i[0]])
            temp['data'] = c.fetchall()[0] 
        c.close()
        conn.commit()
        conn.close()
        return result
        
    def query_detail(self,msg):
        conn,c = self.get_conn_c()
        sql = "SELECT productId from detail_data where productId = ? "
        c.execute(sql,[str(msg['productId'])])
        data = c.fetchall()
        c.close()
        conn.commit()
        conn.close()
        if data:
            return True
        else:
            return False

    def query_all_detail(self):
        conn,c = self.get_conn_c()
        sql = "SELECT * from detail_data;"
        dd = c.execute(sql)     
        data_list = []
        key_list = ["id","name","productId","price","size_list","brand_id","color","articleNumber","authPrice","sellDate","exchangeDesc","soldNum" ,"text_string" ,"img_list" ,"size_price"]
        for row in dd:
            temp = OrderedDict()
            for i in range(len(key_list)):
                try:
                    temp[key_list[i]] = json.loads(row[i])
                except BaseException as e:
                    temp[key_list[i]] = row[i]
            data_list.append(temp)
        c.close()
        conn.commit()
        conn.close()
        return data_list


        

    def insert_temp_table(self,msg):
        conn,c = self.get_conn_c()
        try:
            data = msg['json_data']['data']
            result = {
                "productId": data['detail']['productId'],
                "brand_id" : data['detail']['brandId'],
                "name": data['detail']['title'],
                "size_list" : ",".join(data['detail']['sizeList']),
                "color" : data['detail']['color'],
                "articleNumber" : data['detail']['articleNumber'],
                "authPrice" : int(data['detail']['authPrice'] / 100),
                "sellDate" : data['detail']["sellDate"],
                "exchangeDesc" : data["exchangeDesc"],
                "text_string" : self.parse_html(data['imageAndText']),
                "soldNum"   : data['detail']['soldNum'],
                "img_list"  : msg['img_list']
            }
            try:
                if type(data['item']['price']) == str:
                    data['item']['price'] = int(data['item']['price'])
                result["price"] = data['item']['price'] / 100
                if result["price"] == 0:
                    result["price"] = "--"
            except:
                result["price"] = "--"
            size_price = []
            for i in data['sizeList']:
                temp = []
                temp.append(i['size'])
                try:
                    if type(i['item']['price']) == str:
                        i['item']['price'] = int(i['item']['price'])
                    price = int(i['item']['price'] / 100)
                except:
                    price = "--"
                temp.append(price)
                size_price.append(temp)
            result['size_price'] = json.dumps(size_price)
            conn,c = self.get_conn_c()
            for i in result:
                if type(result[i]) != int:
                    result[i] = json.dumps(result[i])
            sql_string = '''INSERT INTO temp_table (name,productId,price,size_list,brand_id,color,articleNumber,authPrice,sellDate,exchangeDesc,soldNum,text_string,img_list,size_price) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
            c.execute(sql_string,[result['name'],result['productId'],result['price'],result['size_list'],result['brand_id'],result['color'],result['articleNumber'],result['authPrice'],result['sellDate'],result['exchangeDesc'],result['soldNum'],result['text_string'],result['img_list'],result['size_price']])
            conn.commit()
            c.close()
            conn.close()
        except BaseException as e:
            with open("error.txt",'a+',encoding="utf-8") as f:
                f.write("{} {} {}".format("#idt",str(msg['productId']),str(e) + "\n"))


    def change_db_name(self):
        conn,c = self.get_conn_c()
        sql_string = "DROP TABLE detail_data;"
        c.execute(sql_string)
        sql_string = "alter table temp_table rename to detail_data;"
        c.execute(sql_string)
        conn.commit()
        c.close()
        conn.close()


    def delete_same(self):
        conn,c = self.get_conn_c()
        sql_string = "delete from diff_table where rowid not in(select max(rowid) from diff_table group by productId)"
        c.execute(sql_string)
        sql_string = "delete from detail_data where rowid not in(select max(rowid) from detail_data group by productId)"
        c.execute(sql_string)
        conn.commit()
        c.close()
        conn.close()

    def compare_table(self,is_clear = False,is_first = False):
        sql_string = "SELECT productId,soldNum from temp_table"
        conn,c = self.get_conn_c()
        org_data =  c.execute(sql_string)
        for row in org_data.fetchall():
            try:
                productId = row[0]
                soldNum = row[1]
                sql_string = "SELECT soldNum from detail_data where productId = ?"
                new_item_data = c.execute(sql_string,[productId])
                new_soldNum = new_item_data.fetchall()[0][0]
                diff_data =  soldNum - new_soldNum
                try:
                    org_diff_sql = "SELECT diff from diff_table where productId = ?"
                    org_diff = c.execute(org_diff_sql,[productId]).fetchall()
                    if len(org_diff) == 0:
                        sql_string = "INSERT INTO diff_table (productId,diff) VALUES (?,?)"
                        c.execute(sql_string,[productId,0])
                    else:
                        diff_data += org_diff[0][0]
                        change_diff_sql = "UPDATE diff_table SET diff = ? where productId = ?"
                        c.execute(change_diff_sql,[diff_data,productId])
                except BaseException as e:
                # print(e)
                #  print("productID {} is not exists!".format(productId))
                    pass
            except BaseException as e:
                print("* {}".format(row))

        conn.commit()
        c.close()
        conn.close()
        
        
