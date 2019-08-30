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