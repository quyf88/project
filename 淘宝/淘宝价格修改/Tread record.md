# **error 记录**


####selenium定位不到元素   
1.新窗口打开后定位不到新窗口元素
    获取当前句柄列表 并切换至新窗口
    num = self.driver.window_handles
    self.driver.switch_to.window(num[1])
2.元素为隐藏属性
    模拟鼠标移动 到隐藏元素位置 显示出元素后再定位
    from selenium.webdriver.common.action_chains import ActionChains
    
    mouse = self.driver.find_element_by_xpath('//tr[@class="next-table-row last first"]')
    ActionChains(self.driver).move_to_element(mouse).perform()
    self.driver.find_elements_by_xpath('//i[@class="next-icon next-icon-edit2 next-icon-small table-cell-edit-icon"]')[0].click()
        
#### js 获取当前页面HTML
html = self.driver.execute_script("return document.documentElement.outerHTML")
print(html)


#### 翻页后获取不到元素
# 翻页后刷新一下页面 在定位
driver.refresh()

# 如果是在页面底部翻页获取不到元素的话
```