#!/bin/sh

# 定义一个函数用于自动登录
auto_login() {
    curl --interface $INTERFACE1 -G -d "user_account=$USER_ACCOUNT1" -d "user_password=$USER_PASSWORD1" $LOGIN_URL
    curl --interface $INTERFACE2 -G -d "user_account=$USER_ACCOUNT2" -d "user_password=$USER_PASSWORD2" $LOGIN_URL
}

# 定义一个函数用于检查网络连接
check_connection() {
    local interface=$1
    value=$(ping -q -c 4 223.5.5.5 -I $interface)
    result=$(echo $value | grep "0 packets received")
    if [[ -n "$result" ]]
    then
        echo "Network connection lost on $interface. Trying to login..."
        auto_login
    fi
}

# 定义登录的 URL 和用户账号密码
LOGIN_URL="http://172.30.255.42:801/eportal/portal/login/"
USER_ACCOUNT1="账号1"
USER_PASSWORD1="账号1密码"
USER_ACCOUNT2="账号2"
USER_PASSWORD2="账号2密码"

# 定义网络接口变量
INTERFACE1="macvlan1"
INTERFACE2="macvlan2"

# 检查 INTERFACE1 的网络连接
check_connection "$INTERFACE1"

# 检查 INTERFACE2 的网络连接
check_connection "$INTERFACE2"
