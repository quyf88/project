#### **MongoDB 库基础命令**

```
mongo # 进入
exit # 退出
show dbs # 查看数据库列表
use 库 # 进入库
db # 查看所在库
db.dropDatabase() # 删除库
```

#### **SET(集合)**

```
# 增
db.createCollection('student') # 创建集合
# 查
show collections # 查看所有集合
# 删
db.student.drop() 
```

#### 文档(数据)

```
# 增
db.student.insert({name:'a',age:20}) # 插入一条数据
db.student.insert([{name:'a',age:20}, {name:'b',age:10}) # 插入多条数据 放在列表中
# 查 
db.student.find() # 全部查询
db.student.find({name:'a'}).pretty() # 指定条件查询 格式化显示
db.student.find({age:{"$gte":10}}) # 查找age大于等于10
db.student.find({$and:[{条件1},{条件2}]}) # and 
db.student.find({$or:[{条件1},{条件2}]}) # or
db.student.find({$or:[{$and:[{条件1},{条件2}]},{$and:[{条件1},{条件2}]}]}) # and or 混合查询 噩梦条件
# 改
db.stutent.update({需要修改的值},{修改后的值}) # 会重写数据
db.student.update({{需要修改的值},{$set:{修改后的值}}) # 指定属性修改 只修改第一条数据
db.student.update({{需要修改的值},{$set:{修改后的值}},{multi:true}) # 修改全部符合条件数据
# 删     默认删除全部符合条件数据
db.student.remove({name:'a'}) 
db.student.remove({name:'a'},{justOne:true}) # 删除符合条件的一条数据
db.student.remove({}) # 删除全部数据
# 条件
$ne  不等于
$gt  大于
$lt  小于
$gte 大于等于
$lte 小于等于
```

