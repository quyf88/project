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
										<td width="126" align="center" style="padding-top:0px;white-space:nowrap;" onclick="episode_click('9223','29d48edda9697f0f66e50fbf7d59de50', '6502521');">
											<div style="float:center;position:relative;width:126px; height:68px; margin:9px;    background-size:cover;background-position:center 20%;border-radius:0px;background-image:url('//ballerina.toptoon.net/assets/upfile/ep_thumb/x2/330_9223_1481090741.8126.jpg');" class="comic_cell">&nbsp;</div>
										</td>
										<td style="padding:7px 5px 0px 5px;line-height:19px;height:25px;">
											<div style="float:left; position:absolute; top:15px;left:148px; width:calc(100% - 155px);" onclick="episode_click('9223','29d48edda9697f0f66e50fbf7d59de50', '6502521');">
												
										<span style="font-size:16px; font-weight:600; color:#000;">最終話</span>
																				<br>
																				<span style="color:#999; font-size:11px;" onclick="episode_click('9223','29d48edda9697f0f66e50fbf7d59de50', '6502521');">
																				2017.01.03																				</span>
										<br>																			</div>


																											<div style="float:right;position:absolute;right:10px;bottom:18px;display:none;" class="checkbox_list">
									<div class="checkbox custom">
									    <input id="box9223" style="display:none;" class="css-checkbox checkbox_data" type="checkbox" value="9223" data="2" onchange="package_buy_checkbox();" checked="">
									    <label for="box9223" style="display:none;" class="css-label">&nbsp;</label> 2點券									</div>
									</div>
									
									<div style="right:33px; position:absolute; top:35px;" class="vote_list" onclick="episode_click('9223','29d48edda9697f0f66e50fbf7d59de50', '6502521');">
																													<span style="background-color:#fff;border:1px solid #ccc;padding:14px;border-radius:4px;font-size:14px;font-weight:bold;color:#000;cursor:pointer;line-height:12px;white-space:nowrap;">&nbsp;2點券&nbsp;</span>
																												</div>

								</td>
							</tr>
							</tbody></table>
						
"""

c = re.findall(r'episode_click(.*?),', b, re.S | re.M)[0]
print(''.join(re.findall(r'(\d)', c)))
