# coding=utf-8
# 作者    ： Administrator
# 文件    ：mongodb.py
# IED    ：PyCharm
# 创建时间 ：2019/5/18 18:19


from pymongo import MongoClient


class MongoDB:
    def __init__(self):
        # 连接mongodb
        self.client = MongoClient(host="127.0.0.1", port=27017)
        # 指定数据库,没有则创建
        self.db = self.client["test"]
        # 指定集合,没有则创建
        self.my_set = self.db["student"]

    def add_db(self, data):
        """
        增
        db.student.insert({name:'a',age:20}) # 插入一条数据
        db.student.insert([{name:'a',age:20}, {name:'b',age:10}) # 插入多条数据 放在列表中
        insert_one(data) 添加一条
        insert_many(data) 添加多条
        acknowledged 是否写入成功
        inserted_ids 返回成功写入数据的id
        """
        if isinstance(data, list):
            add = self.my_set.insert_many(data)
            return add.inserted_ids
        elif isinstance(data, dict):
            add = self.my_set.insert_one(data)
            return add.inserted_ids

    def remove_db(self, data, justOne=True):
        """
        删
        db.student.remove({name:'a'})
        db.student.remove({name:'a'},{justOne:true}) # 删除符合条件的一条数据
        db.student.remove({}) # 删除全部数据
        delete_one() 删除一条
        delete_many() 删除多条
        """
        if justOne is False:
            deleted = self.my_set.delete_many(data)
            return deleted.deleted_count
        elif justOne is True:
            deleted = self.my_set.delete_one(data)
            return deleted.deleted_count

    def find_db(self, data=None):
        """
        查
        db.student.find() # 全部查询
        db.student.find({name:'a'}).pretty() # 指定条件查询 格式化显示
        db.student.find({age:{"$gte":10}}) # 查找age大于等于10
        db.student.find({$and:[{条件1},{条件2}]}) # and
        db.student.find({$or:[{条件1},{条件2}]}) # or
        db.student.find({$or:[{$and:[{条件1},{条件2}]},{$and:[{条件1},{条件2}]}]}) # and or 混合查询 噩梦条件
        """

        if data is None:
            return self.my_set.find(data)
        elif isinstance(data, dict):
            return self.my_set.find_one(data)

    def update_db(self, old_data, new_data, multi=False):
        """
        改
        db.stutent.update({需要修改的值},{修改后的值}) # 会重写数据
        db.student.update({{需要修改的值},{$set:{修改后的值}}) # 指定属性修改 只修改第一条数据
        db.student.update({{需要修改的值},{$set:{修改后的值}},{multi:true}) # 修改全部符合条件数据
        update_one(old_data, new_data) 修改一条
        update_many(old_data, new_data) 修改多条
        matched_count 返回成功修改条数
        """
        new_data = {"$set": new_data}
        if multi is True:
            matched = self.my_set.update_many(old_data, new_data)
            return matched.matched_count
        elif multi is False:
            matched = self.my_set.update_one(old_data, new_data)
            return matched.matched_count


a = [{"a": "python", "b": "hello"}, {"c": "haha", "d": 1}]

c = {}
if __name__ == '__main__':
    db = MongoDB()
    print(db.add_db(a))
    # find = db.find_db()
    # update = db.update_db(b, c, multi=True)
    # rem = db.remove_db(c, justOne=False)
    # print(rem)
