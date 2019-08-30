import os
import psutil


class Monitor:
    def write(self):
        """
        将主程序进程号写入文件
        :return:
        """
        # 获取当前进程号
        pid = os.getpid()
        print('当前进程号：{}'.format(pid))
        with open('pid.txt', 'w') as f:
            f.write(str(pid))

    def read(self):
        """
        读取进程中的数据
        :return:
        """
        if os.path.exists('pid.txt'):
            with open('pid.txt', 'r') as f:
                pid = f.read()
                return pid
        else:
            return '0'

    def run(self):
        """
        读取配置文件中的进程号判断当前程序是否在运行
        :return:
        """
        pid = int(self.read())
        print('读取进程号：{}'.format(pid))
        if pid:
            # 获取所有进程pid
            running_pids = psutil.pids()
            if pid in running_pids:
                print('程序正在运行中!')
                return True
            else:
                self.write()
                print('程序没有运行，启动中!')
                return False
        else:
            self.write()
            print('程序没有运行，启动中!')
            return False

    def kill(self):
        """
        杀死进程
        :return:
        """
        command = 'taskkill /F /IM python.exe'
        os.system(command)

