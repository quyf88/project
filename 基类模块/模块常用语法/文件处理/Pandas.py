"""读取excel"""
import pandas as pd
def read_xls(self, filename):
    # 加载数据
    df_read = pd.read_excel(filename)
    df = pd.DataFrame(df_read)
    # 获取指定表头的列数
    phone_num = 0  # 电话列
    name_num = 0  # 企业名称列
    code_num = 0  # 统一社会信用代码列
    type_num = 0  # 企业类型列
    user_num = 0  # 身份证号码
    for i in range(len(df.keys())):
        if df.keys()[i] == '电话':
            phone_num = i
        elif df.keys()[i] == '企业名称':
            name_num = i
        elif df.keys()[i] == '统一社会信用代码':
            code_num = i
        elif df.keys()[i] == '企业类型':
            type_num = i
        elif df.keys()[i] == '身份证号码':
            user_num = i
    # 循环每一行
    for indexs in df.index:
        #  fillna(0)将该列nan值修改为0 方便后续判断
        df.ix[indexs] = df.ix[indexs].fillna(0)
        # 读取指定行列数据 df.ix[行,列]
        data1 = df.ix[indexs, phone_num]
        # 修改指定单元格数据df.iloc[行, 列]
        if data1:
            continue

        # 获取企业信息 查询用
        pre_name = df.ix[indexs, name_num]
        pre_code = df.ix[indexs, code_num]
        pre_type = df.ix[indexs, type_num]
        yield (indexs, pre_name, pre_code, pre_type)
        df.iloc[indexs, phone_num] = self.phone  # 电话
        df.iloc[indexs, user_num] = self.number  # 身份证号
        # 查询一条保存一条 sheet_name工作表名 index是否添加索引 header表头
        df.to_excel(filename, sheet_name='data', index=False, header=True)

"""读取csv"""
def read_csv(self, src):
    # 加载数据
    path = os.getcwd()
    files = os.listdir(path + '\ExportFile')
    if self.filename.split('/')[1] not in files:
        print('没有此文件')
        self.data_save([])
    df_read = pd.read_csv(self.filename)
    df = pd.DataFrame(df_read)
    # 获取指定表头的列数
    phone_num = 0  # 校验码
    for i in range(len(df.keys())):
        if df.keys()[i] == '校验码':
            phone_num = i
    # 循环每一行
    for indexs in df.index:
        # 读取指定行列数据 df.ix[行,列]
        data1 = df.ix[indexs, phone_num]
        # 修改指定单元格数据df.iloc[行, 列]
        if data1 == src:
            df.to_csv(self.filename, index=False, encoding='utf_8_sig')
            return True
    # 读取csv中文乱码 添加encoding='utf_8_sig'
    df.to_csv(self.filename, index=False, encoding='utf_8_sig')
    return False