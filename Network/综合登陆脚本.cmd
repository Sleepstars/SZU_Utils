@echo off
echo.
echo.
echo ███████╗███████╗██╗   ██╗    ███╗   ██╗███████╗████████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗
echo ██╔════╝╚══███╔╝██║   ██║    ████╗  ██║██╔════╝╚══██╔══╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝
echo ███████╗  ███╔╝ ██║   ██║    ██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ 
echo ╚════██║ ███╔╝  ██║   ██║    ██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║   ██║██╔══██╗██╔═██╗ 
echo ███████║███████╗╚██████╔╝    ██║ ╚████║███████╗   ██║   ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗
echo ╚══════╝╚══════╝ ╚═════╝     ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
echo.
echo.
echo Powered by FIX SZUCIEVA
echo 由深大义修组提供技术支持
echo 若有问题欢迎前往我的博客留言：https://blog.sleepstars.net/
echo.
echo ==========================================
echo.

:: 在这里修改你的校园卡账户和密码
set "USER_ACCOUNT=123"
set "USER_PASSWORD=456"

:: 分别是宿舍区和教学区的登录
set "dormitory_login_url=http://172.30.255.42:801/eportal/portal/login/"
set "teaching_login_url=https://net.szu.edu.cn/"


:: 检查网络连接
echo 正在检测网络连通性...
echo.
echo ==========================================
echo.

:: 检查网络连接，分别检查宿舍区、教学区和百度
:: 使用curl检测宿舍区网络连通性
curl -s -I --connect-timeout 1 --max-time 3 --max-redirs 0 http://172.30.255.42/ >nul
if %errorlevel% equ 0 (
    set "dormitory_available=true"
) else (
    set "dormitory_available=false"
)

:: 使用curl检测教学区网络连通性，禁止跳转
curl -s -I --connect-timeout 1 --max-time 3 --max-redirs 0 https://net.szu.edu.cn/ >nul

if %errorlevel% equ 0 (
    set "teaching_available=true"
) else (
    set "teaching_available=false"
)

:: 使用curl检测百度网络连通性
curl -s -I --connect-timeout 1 --max-time 5 --max-redirs 0 https://baidu.com/ >nul
if %errorlevel% equ 0 (
    set "baidu_available=true"
) else (
    set "baidu_available=false"
)

:: 根据检测结果执行相应操作
if "%baidu_available%"=="true" (
    echo 您已登录，无需再次登录。
) else (

if "%dormitory_available%"=="true" (
        echo 检测到宿舍区网络环境...
        echo 正在使用宿舍区登录系统登录...
            curl -G -d "user_account=%USER_ACCOUNT%" -d "user_password=%USER_PASSWORD%" "%dormitory_login_url%"
        echo 宿舍区网络登录完成
    ) else if "%teaching_available%"=="true" (
        echo 检测到教学区网络环境...
        echo 正在使用深澜登录系统登录...
        :: 使用编译好的srun-login程序进行登录
        if exist "srun-login.exe" (
            srun-login.exe --username=%USER_ACCOUNT% --password=%USER_PASSWORD%
            echo 教学区网络登录完成
        ) else (
            echo 错误：未找到srun-login.exe程序
            echo 请确保已经正确防止登陆程序
        )
    ) else (
        echo 请检查您的网络连接或可能处于校外环境。
        echo 如果您已连接校园网，请尝试直接使用浏览器登录网络。
        echo 如果仍无法连接，欢迎联系深大义修组维修网络。
        echo 深大义修组官网：http://fix.szucieva.com/
        echo 或者搜索深大义修组官方微信公众号：深大义修组
    )
)

echo.
pause