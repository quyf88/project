#### **获取标签value值**
  - ```cmd
    # 商品ID   a/@data-nid 获取a标签下 data-nid的value值        
    commodity_id = self.driver.find_element_by_xpath('//div[@class="pic"]/a/@data-nid') 
    ```
#### **根据标签文本 定位标签**
  - ```cmd
    self.wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "下一页")]')))
    ```
#### **元素click点击失败 用 ENTER点击**
- ```cmd
    .send_keys(Keys.ENTER)
   ```