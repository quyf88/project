from openpyxl import load_workbook
import pandas as pd
import os
PATH = os.getcwd()
file = f'{PATH}/test.xlsx'
print(file)
excelWriter = pd.ExcelWriter(file, engine='openpyxl')
DataFrame = pd.DataFrame(pd.read_excel('test.xlsx'))


def _excelAddSheet(dataframe, excelWriter, sheet_name):
    """
    excel新建sheet
    :param dataframe: 需要写入的数据
    :param excelWriter: 需要写入的workbook
    :param sheet_name:
    :return:
    """
    book = load_workbook(excelWriter.path)
    print(book)
    excelWriter.book = book
    dataframe.to_excel(excel_writer=excelWriter, sheet_name=sheet_name, index=None)
    excelWriter.close()


_excelAddSheet(DataFrame, excelWriter, '123456')
