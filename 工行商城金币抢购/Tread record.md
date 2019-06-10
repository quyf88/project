#### **error 记录**

```python
"""
error:
    在执行脚本时报Selenium.common.exceptions.WebDriverException: Message: Invalid locator strategy: 	 css selector 的错
Solution:
	https://www.cnblogs.com/nvhanzhi/p/9799908.html
	selenium和Appium-Python-Client 版本兼容问题
	selenium -->0.44
	Appium-Python-Client -->3.141.0
"""
```
```python

"""
error:
    无法定位页面元素 整个页面只有一个元素
Solution:
    1.页面为APP内嵌H5页面：
        https://blog.csdn.net/qq_37941471/article/details/87861733
	    如何判断一个APP页面是原生的还是H5页面
	    
	2.强制开启android webview debug模式使用Chrome inspect：	
	    在Chrome浏览器地址栏输入chrome://inspect，进入调试模式；
	    https://blog.csdn.net/zhulin2609/article/details/51437821
    error:
        No Chromedriver found that can automate Chrome '39.0.0'
    Solution:
        Appium中的Chromedriver版本与手机Android System WebView版本不匹配
	    https://testerhome.com/topics/15503
	    https://www.jianshu.com/p/b96755bf4916
	    http://npm.taobao.org/mirrors/chromedriver/  # chromedriver版本下载
	3.原生状态和H5切换
	    https://www.cnblogs.com/yoyoketang/p/7217818.html
""" 
```

```python

"""
error:
    识别不到夜神模拟器
Solution:
    adb connect 127.0.0.1:62001  # 手动启动模拟器
    adb devices  # 查看连接

"""
```