@echo off
set "USER_ACCOUNT=your_username"  :: 设置账号
set "USER_PASSWORD=your_password" :: 设置密码
set "LOGIN_URL=https://192.168.254.220/a70.htm"  :: 登录URL

:: 使用Windows的curl工具发送POST请求
curl -X POST "%LOGIN_URL%" ^
-H "Host: drcom.szu.edu.cn" ^
-H "Origin: https://drcom.szu.edu.cn" ^
-H "Referer: https://drcom.szu.edu.cn/a70.htm" ^
--data "DDDDD=%USER_ACCOUNT%&upass=%USER_PASSWORD%&R1=0&R2=&R6="

:: 暂停脚本，查看输出
pause
