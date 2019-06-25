adb connect 127.0.0.1:62025
adb connect 127.0.0.1:62026
start /b appium -a 127.0.0.1 -p 4730 -U 127.0.0.1:62025 --no-reset
start /b appium -a 127.0.0.1 -p 4735 -U 127.0.0.1:62026 --no-reset
