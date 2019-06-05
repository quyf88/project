[![](https://img.shields.io/badge/%E8%87%AA%E5%8A%A8%E7%99%BB%E5%BD%95-%E8%8E%B7%E5%8F%96%E6%9C%8B%E5%8F%8B%E5%9C%88-%E8%87%AA%E5%8A%A8%E6%B7%BB%E5%8A%A0%E5%A5%BD%E5%8F%8B.svg
)](https://github.com/chenzijie-chenxiaoli-chentong/project/tree/master/%E5%BE%AE%E4%BF%A1)

## **微信自动登录及获取微信朋友圈实时动态**

- ### **环境配置**

  - ```python
    win10  python3.6.7  Appium-desktop-1.12.1-x64 微信版本：7.0.3
    pip install Appium-Python-Client==0.41
    pip install selenium==4.0.0a1
    ```
  - ```python
    pyrcc5 test.ui –o test.py  # qrc 配置文件转py
    
    pyinstaller -F 文件  # 打包成一个exe
    
    pyisntaller -D -w -i logo文件 py文件  # 打包成一个文件夹
    ```