import os


class Merge:
    def __init__(self):
        self.path = None

    def run(self):
        """
        合并TS视频文件,输出为MP4
        """
        # 读取指定目录下的ts文件
        p = r'D:\project\小爬虫\小项目\video\video\MIAA-155'
        path_list = os.listdir(p)
        print(path_list)
        # 获取ts文件列表
        path_list = [i for i in path_list if 'ts' in i]
        print(path_list)
        # lambda 剔除
        # 按照文件名顺序排序(数字)
        path_list.sort(key=lambda x: int(x[:-3]))
        # 文件路径拼接,os.sep自适应文件拼接符
        path_list = [p + os.sep + i for i in path_list]
        # 用+把需要合并的ts文件拼接起来
        files = '+'.join(path_list)
        print(p + os.sep + files)
        # 合并ts视频 为MP4
        res = os.popen(f'copy/b {files} {"te.mp4"}')
        print(res.read())
        # 删除ts和m3u8文件
        # os.system('del /Q *.ts')


if __name__ == '__main__':
    merge = Merge()
    merge.run()


