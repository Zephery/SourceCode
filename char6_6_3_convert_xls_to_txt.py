__author__ = 'pqh'
import xlrd

info = xlrd.open_workbook('图书信息.xls')

content = info.sheets()[0]

nrows = content.nrows
ncols = content.ncols
2
f_txt = '图书信息.txt'

f = open(f_txt, 'w')

for i in range(1, nrows):
    row_str = ''
    for j in range(0, ncols-1):
        row_str += str(content.cell(i, j).value)+','

    row_str = (row_str+'\n').replace(',\n','\n')
    f.write(row_str)

f.close()