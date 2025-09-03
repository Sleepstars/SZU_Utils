@echo off
set "USER_ACCOUNT1=your_username"
set "USER_PASSWORD1=your_password"
set "LOGIN_URL=http://172.30.255.42:801/eportal/portal/login/"

:: 使用Windows的curl工具发送GET请求
curl -G -d "user_account=%USER_ACCOUNT1%" -d "user_password=%USER_PASSWORD1%" "%LOGIN_URL%"


:: 暂停脚本，查看输出（可选），如果不需要查看输出，可以删除下面这行
pause
