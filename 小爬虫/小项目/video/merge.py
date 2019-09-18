import os


class Merge:
    def __init__(self):
        self.path = None

    def run(self):
        """
        合并TS视频文件,输出为MP4
        """
        # 读取当前指定目录下的ts文件
        path_list = os.listdir('.')
        print(path_list)
        path_list = [i for i in path_list if 'ts' in i]
        print(path_list)
        # lambda 剔除
        # 按照文件名顺序排序(数字)
        path_list.sort(key=lambda x: int(x[:-3]))
        # 用+把需要合并的ts文件拼接起来
        files = '+'.join(path_list)
        print(files)
        # 合并ts视频 为MP4
        res = os.popen(f'copy/b {files} {"te.mp4"}')
        print(res.read())
        # 删除ts和m3u8文件
        # os.system('del /Q *.ts')



