a = """
文章简介：在四分五裂的國家中要如何從中殘存?跟著範道的步伐一起用求生的意志朝向未來吧!!
★ 8.00  |  作家 : 圖海 & 朴基紅  |  觀看次數 : 4,695
#繁體
"""
import os
import re


b = """
 
        <table style="width:100%;">
        <tbody><tr>
            <td align="center" style="text-align: left;width:15%;min-height:180px;max-width:210px;padding-top:0px;white-space:nowrap;" onclick="episode_click('27235','54882c34332256fc6432a93eb7c0ad24', '6396591');">
                <div style="background:url('//ballerina.toptoon.net/assets/upfile/ep_thumb2/x2/1015_27235_1558419505.2609.jpg');background-size:cover;min-height:168px;width:94%;margin:5% 3% 5% 5%;border-radius:5px;"></div>
            </td>
            <td align="center" style="text-align: left;width:15%;min-height:180px;max-width:210px;padding-top:0px;white-space:nowrap;" onclick="episode_click('27235','54882c34332256fc6432a93eb7c0ad24', '6396591');">
                <div style="background:url('//ballerina.toptoon.net/assets/upfile/ep_thumb4/x2/1015_27235_1558419505.265.jpg');background-size:cover;min-height:168px;width:94%;margin:5% 5% 5% 3%;border-radius:5px;"></div>
            </td>
            <td style="padding:17px 15px 10px 15px;min-height:130px;line-height:19px;height:25px;box-sizing: border-box;vertical-align: top;">
                <div style="float:right; width: 67%; min-height:95px; max-height: 264px; border: 1px solid rgba(0,0,0,0.1);padding:35px 24px;;border-radius:5px;box-sizing: border-box;position: absolute;height: 80%;" onclick="episode_click('27235','54882c34332256fc6432a93eb7c0ad24', '6396591');">
                    
            <span style="font-size:16px; font-weight:600; color:#000;">第1話</span>
                                                    <br>
                                                    <span style="color:#999; font-size:11px;" onclick="episode_click('27235','54882c34332256fc6432a93eb7c0ad24', '6396591');">
                                                    2019.06.03																				</span>
            <br>																			</div>


        
        <div style="right:33px; position:absolute; top:84px;" class="vote_list" onclick="episode_click('27235','54882c34332256fc6432a93eb7c0ad24', '6396591');">
        <span style="background-color:#fff;border:1px solid #e33;padding:14px;border-radius:4px;font-size:14px;font-weight:bold;color:#e33;cursor:pointer;line-height:12px;white-space:nowrap;">&nbsp;免費&nbsp;</span>									</div>

    </td>
</tr>
</tbody></table>
"""
#
# id = re.findall(r'episode_click(.*?),', b, re.S | re.M)
# chapter = re.findall(r'第(.*?)話', b)
# coupon = re.findall(r'&nbsp;(.*?)&nbsp;</span>', b)
# print(id)
# print(chapter)
# print(coupon)
import string
# coupon = re.findall(r'&nbsp;(.*?)&nbsp;</span>', b)
# print(coupon)

with open('2019-09-06更新记录.txt', 'a+', encoding='utf-8') as f:
    f.seek(0)
    # print(f.readlines())
    readlin = [i.strip() for i in f.readlines()]
    print(readlin)
    # print(readlin)
    if '人夫的悸' not in readlin:
        print(1)
    else:
        print(2)
# c = ['免費']
# if ('免費' not in c) and ('收藏中' not in c):
#     print(1)
# else:
#     print(2)