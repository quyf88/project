小米MIUI9 ROOT开启

- ### **adb 常用命令**
  - ```cmd
    错误：adb服务器版本（31）与该客户端（39）不匹配； 杀死...
    原因：这个是socket 的端口被占用了，检查是否开启了手机助手
    ```
- ### **adb 常用命令**
  - ```cmd
    adb connect 127.0.0.1:62001  # 连接设备
    adb devices  # 查看连接设备    
    adb shell /system/bin/screencap -p /sdcard/screenshot.png  # 截图命令
    adb pull /sdcard/screenshot.png D:\download  # 保存
    adb shell input tap x y  # 点击
    adb shell input swipe x1 y1 x2 y2  # 翻页
    ```

- ### **安装Xposed**
  - ```cmd
    1.确认手机开启root
    2.OEM解锁
    3.用ADB命令解锁system
        adb root
        adb disable-verity
        重启手机
    ```