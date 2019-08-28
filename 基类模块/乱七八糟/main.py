"""主程序"""
from com.baiduwords.get_data_dao import GetData


def admin():
    """主函数"""

    get_data = GetData()
    get_data.retrieve_data()


if __name__ == '__main__':
    admin()
