
# import os
# path = os.getcwd()
#
# cmd = path + '/copy/b video/痴女責め連続射精16発/*.ts 1.mp4'
# print(cmd)
# res = os.popen(r'copy/b X:\project\project\小爬虫\小项目\video\video\痴女責め連続射精16発\*.ts 1.mp4')
# print(res.read())
#
# print(os.sep)

# import os
# path="video/MIAA-079/"  #待读取的文件夹
# path_list=os.listdir(path)
# path_list=[i for i in path_list if 'mp4' in i]
# print(path_list)
# path_list.sort(key= lambda x:int(x[:-4]))
#
# for filename in path_list:
# 	print(os.path.join(path,filename))
# import wget
# count=0
# while count<3: #count的值表示总共要下多少ts文件，要查阅m3u8文件
#     try:
#         result=wget.download("https://cdn.av01.tv/v2/20190529_2/miaa00079/content/file4500-67-v1.ts?hdnea=ip=194.156.230.114~st=1568096216~exp=1568182616~acl=/v2/20190529_2/miaa00079/content/*~hmac=100a1884a5a9c8f1e028cc67ae7f1fa6bb257f2d7589b84f20153ff098bd0022",
#                              out='video/')
#         count=count+1
#     except:
#         continue





import os
filelist=os.listdir('./')
for file in filelist:
    orgName=file
    file=file.split("_")
    if len(file[3])<7:
        for i in range(7-len(file[3])):
            file[3]="0"+file[3]
        print(file)
        filename="_".join(file)
        print(filename)
        os.rename(orgName,filename)
    else:
        pass
