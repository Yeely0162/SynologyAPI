import requests
import time

# New a admin account
account = "XXXX"
passwd = "XXXXX"

DSMService = "http://XXXXXXX:80"  # Synology IP Address Format: http://domain:port        demo: https://nimocass.com:80

sid_head_url = "/webapi/auth.cgi?api=SYNO.API.Auth&version=3&method=login&account=" + account + "&passwd=" + passwd  # + "&otp_code=539248"  # Primarily get sid before you get other API method
SystemUtilization_head_url = "/webapi/entry.cgi?api=SYNO.Core.System.Utilization&method=get&version=1&object_id=NOTE_ID&_sid="

DiskInfo_head_url = "/webman/modules/SystemInfoApp/SystemInfo.cgi?query=storage&object_id=NOTE_ID&_sid="  #  Invalid API In DSM 7.0+ for System Disk Information
System_storage = "/webapi/entry.cgi?api=SYNO.Core.System&type=storage&method=info&version=3&_sid=" # Use In over than DSM 7.0+

System_Info = "/webapi/entry.cgi?api=SYNO.Core.System&method=info&version=3&_sid="  # System Information(CPU Info include)

System_network = "/webapi/entry.cgi?api=SYNO.Core.System&type=network&method=info&version=3&_sid=" # System NetWork Information(All about Network)

System_UPS = "/webapi/entry.cgi?api=SYNO.Core.ExternalDevice.UPS&method=get&version=1&_sid=" # If you have UPS , Information For UPS

CpuCoreGroup = "/webapi/entry.cgi?api=SYNO.Core.System.ProcessGroup&method=list&version=1&object_id=NOTE_ID&_sid="
logout = "/webapi/entry.cgi?api=SYNO.API.Auth&version=6&method=logout&_sid="  # User logout
CPUaRAMused = "/webapi/entry.cgi?api=SYNO.Virtualization.Cluster&method=get_host&version=1&object_id=NOTE_ID&_sid="  # Get CPU & RAM & Network Info # StatusCode in  error , healthy , warning
api_url = "https://dsm.yeely.top:1666/webapi/query.cgi?api=SYNO.API.Info&version=1&method=query&query=all" # All Synology API Page



# Code Error
# 100 Unknown error
# 101 Invalid parameters
# 102 API does not exist
# 103 Method does not exist
# 104 This API version is not supported
# 105 Insufficient user privilege //用户权限不足
# 106 Connection time out //超时
# 107 Multiple login detected
# 110 The network connection is unstable or the system is busy.
# 111 The network connection is unstable or the system is busy.
# 112 Preserve for other purpose.
# 113 Preserve for other purpose.
# 114 Lost parameters for this API.
# 115 Not allowed to upload a file.
# 116 Not allowed to perform for a demo site.
# 117 The network connection is unstable or the system is busy.
# 118 The network connection is unstable or the system is busy.
# 119 Invalid session. //会话无效
# 120-149 Preserve for other purpose.
# 150 Request source IP does not match the login IP.

# 400 Invalid password.
# 401 Guest or disabled account.
# 402 Permission denied.
# 403 One time password not specified.
# 404 One time password authenticate failed.
# 405 App portal incorrect.
# 406 OTP code enforced.
# 407 Max Tries (if auto blocking is set to true).
# 408 Password Expired Can not Change.
# 409 Password Expired.
# 410 Password must change (when first time use or after reset password by admin).
# 411 Account Locked (when account max try exceed
# 412 Filename too long in the non-encrypted file system
# 413 Filename too long in the encrypted file system
# 414 File already exists
# 415 Disk quota exceeded
# 416 No space left on device
# 417 Input/output error
# 418 Illegal name or path
# 419 Illegal file name
# 420 Illegal file name on FAT file system
# 421 Device or resource busy
# 599 No such task of the file operation

def RequestUrl(Url):
    try:
        global Sid
        kv = {'user-agent': 'Mozilla/5.0'}  # 以浏览器头文报文来访问
        r = requests.get(Url, headers=kv, timeout=30)
        # r = requests.get(Url, timeout=30)
        r.raise_for_status()
        return r.json()
    # print(r.json())
    except:
        print("Failed!")


def One_Request():
    # 首先获取登录的Sid
    JsonText = RequestUrl(DSMService + sid_head_url)
    print(JsonText)
    Sid = JsonText['data']['sid']  # 通过JSON获取到的内容
    SystemInformation = RequestUrl(DSMService + SystemUtilization_head_url + Sid)
    print(SystemInformation)
    lg = RequestUrl(DSMService + logout + Sid)  # 用户登出
    print(lg)


def for_Api():
    JsonText = RequestUrl(DSMService + sid_head_url)
    Sid = JsonText['data']['sid']  # 通过JSON获取到的内容
    json = RequestUrl(api_url)
    print(json['data'].keys())
    api_list = []
    for i in json['data'].keys():
        try:
            t = "/webapi/entry.cgi?api=" + str(i) + "&method=get&version=1&object_id=NOTE_ID&_sid=" + str(Sid)
            ret = RequestUrl(DSMService + t)
            # print(ret)
            if bool(ret["success"]):
                api_list.append(i)
                print("成功添加:" + str(i))
            # else:
            #     if int(ret["error"]['code']) == 104:
            #         t = "/webapi/entry.cgi?api=" + i + "&method=list&version=2&object_id=NOTE_ID&_sid="
            #         ret = RequestUrl(t)
            #         if bool(ret["success"]):
            #             api_list.append(i)
            #             print("成功添加:" + str(i))
            #     elif int(ret["error"]['code']) == 105:
            #         print("权限不足:" + str(i))
        except:
            print("异常api报错：" + str(i))
            pass

    for k in api_list:
        print(k)


# 模拟一分钟内多次请求
def Request_60_In_Minute():
    # 首先获取登录的Sid 仅需获取一次即可不需要参加后面的循环
    JsonText = RequestUrl(DSMService + sid_head_url)
    print(JsonText)
    Sid = JsonText['data']['sid']  # 通过JSON获取到的内容
    for i in range(60):
        time.sleep(1)  # 群晖更新的速度很慢，一秒内重复2-3条相同的信息 所以设置请求速度时：3 s/min 这样获取最合理
        SystemInformation = RequestUrl(
            DSMService + CPUaRAMused + Sid)  # 通过Sid已经建立链接了，当用户退出时候才会失效，当失效后只需要重新获取Sid即可
        print("第" + str(i) + "次获取信息：", end=" ")
        print(SystemInformation)
    RequestUrl(DSMService + logout + Sid)  # 用户登出


test0 = "/webapi/entry.cgi?api=SYNO.Core.Desktop.Timeout&method=check&version=1&_sid="
test1 = "/webapi/entry.cgi?api=SYNO.Core.ExternalDevice.Storage.eSATA&method=list&version=1&_sid="


def New_Request():
    # 首先获取登录的Sid
    JsonText = RequestUrl(DSMService + sid_head_url)
    print(JsonText)
    Sid = JsonText['data']['sid']  # 通过JSON获取到的内容
    Systemstatus = RequestUrl(DSMService + CPUaRAMused + Sid)
    SystemInformation = RequestUrl(DSMService + SystemUtilization_head_url + Sid)
    # SystemUtilization= RequestUrl(DSMService + SystemUtilization_head_url + Sid)
    print(Systemstatus)
    print(SystemInformation)
    # print(SystemUtilization)
    lg = RequestUrl(DSMService + logout + Sid)  # 用户登出
    print(lg)


Request_60_In_Minute()
# New_Request()

