class Config:
    def __init__(self, is_write_excel=True, go_img=True, isfirst=True):
        # 生成汇总EXCEL
        self.is_write_excel = is_write_excel
        # 下载图片
        self.go_img = go_img
        # 写入数据库
        self.is_first = isfirst
