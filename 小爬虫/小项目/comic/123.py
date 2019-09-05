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
            <td width="126" align="center" style="padding-top:0px;white-space:nowrap;" onclick="episode_click('7429','cd597b9d386e085f51bb7e6ad963e949', '6502521');">
                <div style="float:center;position:relative;width:126px; height:68px; margin:9px;    background-size:cover;background-position:center 20%;border-radius:0px;background-image:url('//ballerina.toptoon.net/assets/upfile/ep_thumb/x2/330_7429_1469687571.9003.jpg');" class="comic_cell">&nbsp;</div>
            </td>
            <td style="padding:7px 5px 0px 5px;line-height:19px;height:25px;">
                <div style="float:left; position:absolute; top:15px;left:148px; width:calc(100% - 155px);" onclick="episode_click('7429','cd597b9d386e085f51bb7e6ad963e949', '6502521');">
                    
            <span style="font-size:16px; font-weight:600; color:#000;">第3話</span>
                                                    <br>
                                                    <span style="color:#999; font-size:11px;" onclick="episode_click('7429','cd597b9d386e085f51bb7e6ad963e949', '6502521');">
                                                    2016.08.02																				</span>
            <br>																			</div>


        
        <div style="right:33px; position:absolute; top:15px;" class="vote_list" onclick="episode_click('7429','cd597b9d386e085f51bb7e6ad963e949', '6502521');">
                                                    <div style="line-height:20px;margin:0px 0px;">
                <div style="background-color:#fff;border:1px solid #e33;padding:14px;border-radius:4px;font-size:14px;font-weight:bold;color:#e33;cursor:pointer;line-height:12px;text-align:center;white-space:nowrap;">
                
                <span style="text-decoration: line-through;">&nbsp;2點券&nbsp;</span>
                <br>
                &nbsp;免費&nbsp;</div>
                </div>
                                                </div>

    </td>
</tr>
</tbody></table>
"""

id = re.findall(r'episode_click(.*?),', b, re.S | re.M)
chapter = re.findall(r'第(.*?)話', b)
coupon = re.findall(r'&nbsp;(.*?)&nbsp;</span>', b)
print(id)
print(chapter)
print(coupon)
