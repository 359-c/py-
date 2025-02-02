# 导入json模块，用于处理JSON数据
import json
# 导入os模块，用于与操作系统进行交互
import os
# 从pyDes模块中导入des、ECB和PAD_PKCS5，用于加密和解密
from pyDes import des, ECB, PAD_PKCS5
# 导入binascii模块，用于二进制数据和ASCII字符串之间的转换
import binascii
# 导入requests模块，用于发送HTTP请求
import requests
# 导入time和datetime模块，用于处理时间
import time, datetime
# 导入threading模块，用于创建和管理线程
import threading

# 定义一个空列表，用于存储喜欢的活动关键词
like = []
# 定义一个浮点数，用于设置线程睡眠的时间间隔
timeSleep = 0.01

# 定义一个空列表，用于存储活动名称
activeList = []

# 定义一个字典，包含请求头信息
headers = {
    # 标准用户代理字符串，包含设备信息、操作系统版本等
    'standardUA': '{"channelName": "dmkj_Android", "countryCode": "CN", "createTime": 1604663529774, "device": "HUAWEI vmos","hardware": "vphw71", "modifyTime": 1604663529774, "operator": "%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8","screenResolution": "1080-2115", "startTime": 1605884705024, "sysVersion": "Android 25 7.1.2","system": "android", "uuid": "12:34:56:31:97:80", "version": "4.6.0"}',
    # 请求内容类型为表单数据
    'Content-Type': 'application/x-www-form-urlencoded',
    # 请求内容长度为309字节
    'Content-Length': '309',
    # 请求的主机名
    'Host': 'appdmkj.5idream.net',
    # 保持连接
    'Connection': 'Keep-Alive',
    # 接受gzip压缩的响应
    'Accept-Encoding': 'gzip',
    # 用户代理字符串，指定使用的HTTP客户端库
    'User-Agent': 'okhttp/3.11.0',
}

def Apply(account, pwd):
    """
    账号登陆,返回uid和token
    account  登陆账号
    pwd      加密后的密码
    :param account:
    :param pwd:
    :return:
    """
    # 调用get_pwd函数对密码进行加密
    pwd_ = get_pwd(pwd)
    # 定义登陆接口的URL
    url = 'https://appdmkj.5idream.net/v2/login/phone'
    # 构造登陆请求的数据，包括加密后的密码和账号
    data = {
        'pwd': pwd_,
        'account': account,
        'version': '4.7.0'
    }

    # 发送POST请求到登陆接口，并将返回的JSON数据解析为Python字典
    response = requests.post(url=url, headers=headers, data=data).json()
    # 将账号和原始密码添加到返回的字典中
    response.update(account=account, pwd=pwd)
    # 将更新后的字典转换为JSON字符串
    response1 = json.dumps(response)
    # 将JSON字符串写入名为'token'的文件中
    with open('token', mode='w', encoding='utf-8') as f:
        f.write(response1)

    # 返回包含登陆信息的字典
    return response

def get_time(accounts_data, id):
    """
    获取活动开始时间
    :param accounts_data: 包含用户登录信息的字典，如token和uid
    :param id: 活动的ID
    :return: 一个列表，包含活动开始时间的年、月、日、时、分和活动名称
    """
    # 定义获取活动详情的接口URL
    url = 'https://appdmkj.5idream.net/v2/activity/detail'
    # 从accounts_data中获取token和uid
    token = accounts_data['token']
    uid = accounts_data['uid']
    # 构造请求数据，包括uid、token、activityId和version
    data_get_time = {
        'uid': uid,  # 登陆接口获取
        'token': token,  # 登陆接口获取
        'activityId': int(id),  # 活动ID
        'version': '4.6.0',
    }
    # 发送POST请求到活动详情接口，并将返回的JSON数据解析为Python字典
    set_data = requests.post(url=url, headers=headers, data=data_get_time).json()
    # 从返回的字典中提取活动开始时间，并按年、月、日、时、分进行分割
    time_ = set_data['data']['joindate'].split('-')[0]
    # 将分割后的时间和活动名称组合成一个列表
    time_data = [time_[0:4], time_[5:7], time_[8:10], time_[11:13], time_[14:16], set_data['data']['activityName']]
    # 打印活动名称
    print(set_data['data']['activityName'])
    # 返回包含活动开始时间和名称的列表
    return time_data

def get_activit(accounts_data):
    """
    获取可以报名的活动
    uid     每个账号不同的uid
    token   账号的token
    :param accounts_data: 包含用户登录信息的字典，如token和uid
    :return: 一个列表，包含可以报名的活动的信息，如活动ID、名称和状态文本
    """
    # 初始化一个空列表，用于存储活动信息
    activitys = []
    # 定义获取活动列表的接口URL
    url = 'https://appdmkj.5idream.net/v2/activity/activities'
    # 从accounts_data中获取token和uid
    token = accounts_data['token']
    uid = accounts_data['uid']
    # 构造请求数据，包括uid、token和其他参数
    data = {
        'joinStartTime': '',
        'token': token,  # 登陆接口获取
        'startTime': '',
        'endTime': '',
        'joinFlag': '1',
        'collegeFlag': '',
        'catalogId': '',
        'joinEndTime': '',
        'specialFlag': '',
        'status': '',
        'keyword': '',
        'version': '4.6.0',
        'uid': uid,  # 登陆接口获取
        'sort': '',
        'page': '1',
        'catalogId2': '',
        'level': '',
    }
    # 发送POST请求到活动列表接口，并将返回的JSON数据解析为Python字典
    response = requests.post(url=url, headers=headers, data=data).json()
    # 从返回的字典中提取活动列表数据
    lists_data = response['data']['list']

    # 遍历活动列表数据
    for data_ in lists_data:
        # 提取活动ID、名称和状态文本
        activityId = data_['activityId']
        name = data_['name']
        statusText = data_['statusText']
        # 将活动信息组合成一个字典，并添加到activitys列表中
        activity = {'activityId': activityId, 'name': name, 'statusText': statusText}
        activitys.append(activity)
    # 返回包含活动信息的列表
    return activitys

def main(passwd, id):
    """
    提交报名函数
    :param passwd: 包含用户登录信息的字典，如token和uid
    :param id: 活动的ID
    :return:
    """
    while True:
        # 定义一个包含报名信息的列表，这里的信息是示例，实际应用中需要根据活动要求填写
        info = [{"conent": "", "content": "", "fullid": "79857", "key": 1, "notList": "false", "notNull": "false",
                 "system": 0,
                 "title": "姓名"}]

        # 构造报名请求的数据，包括uid、token、活动ID和报名信息
        data1 = {
            'uid': passwd['uid'],  # 从passwd字典中获取uid，该uid是登陆接口获取的
            'token': str(passwd['token']),  # 从passwd字典中获取token，并转换为字符串，该token是登陆接口获取的
            'remark': '',  # 备注信息，这里为空
            'data': str(info),  # 将报名信息列表转换为字符串，作为报名参数
            'activityId': id,  # 活动的ID
            'version': '4.6.0',  # 应用版本号
        }
        # 发送POST请求到报名提交接口，并将返回的JSON数据解析为Python字典
        response1 = requests.post(url='https://appdmkj.5idream.net/v2/signup/submit', data=data1,
                                  headers=headers).json()
        # print(response1)
        try:
            # 检查返回的消息是否表示已经报名成功
            if response1['msg'] == '此活动你已经报名,不能重复报名':
                print('活动报名成功')
                # 如果报名成功，跳出循环
                break
        except KeyError:
            # 如果返回的JSON数据中没有'msg'键，忽略异常
            ...
def get_pwd(s):
    """
    获取密码加密结果
    :param s: 原始密码字符串
    :return: 加密后的密码字符串
    """
    # 定义加密密钥，这里使用固定的字符串'51434574'
    KEY = '51434574'
    # 将密钥赋值给变量secret_key
    secret_key = KEY
    # 使用des算法创建一个加密对象k，使用ECB模式，填充模式为PAD_PKCS5
    k = des(secret_key, ECB, pad=None, padmode=PAD_PKCS5)
    # 使用加密对象k对原始密码s进行加密，填充模式为PAD_PKCS5
    en = k.encrypt(s, padmode=PAD_PKCS5)
    # 将加密后的结果转换为十六进制字符串，并转换为大写，最后解码为UTF-8字符串
    return binascii.b2a_hex(en).upper().decode('utf-8')
def JoinActive(passwd, passwd1, activeId):
    """
    处理活动报名任务的函数
    :param passwd: 包含用户登录信息的字典，如token和uid
    :param passwd1: 包含用户登录信息的字典，如token和uid
    :param activeId: 活动的ID
    :return:
    """
    global timeSleep
    # 获取活动开始时间
    time_ = get_time(passwd['data'], activeId)
    # 将活动开始时间转换为datetime对象
    startTime = datetime.datetime(int(time_[0]), int(time_[1]), int(time_[2]), int(time_[3]), int(time_[4]), 00)
    # 计算活动开始前5秒的时间
    openStartTime = startTime - datetime.timedelta(seconds=5)
    # 打印活动名称、报名开始时间和队列开始执行时间
    print('任务队列准备处理,活动名称:%s,报名开始时间:%s,队列开始执行时间:%s' % (time_[5], startTime, openStartTime))

    # 在活动开始前5秒内，每隔timeSleep秒检查一次时间
    while datetime.datetime.now() < openStartTime:
        time.sleep(float(timeSleep))

    # 打印活动名称和开始执行报名任务的信息
    print('队列活动名称:%s,开始执行报名任务' % time_[5])
    # 启动一个新线程来处理活动报名
    threading.Thread(target=main, args=(passwd1, activeId)).start()

def ActiveDeamon(passwd):
    """
    自动发现活动并处理报名任务的守护进程
    :param passwd: 包含用户登录信息的字典，如token和uid
    :return:
    """
    global activeList
    while True:
        # 获取可以报名的活动列表
        huodong_id = get_activit(passwd['data'])
        for activity in huodong_id:
            # 遍历活动列表
            activityId = activity['activityId']
            name = activity['name']
            statusText = activity['statusText']

            # 准备报名所需的用户信息
            passwd1 = {}
            passwd1['token'] = passwd['data']['token']
            passwd1['uid'] = passwd['data']['uid']

            # 如果没有设置喜欢的活动关键词，则报名所有活动
            if len(like) == 0:
                if name not in activeList:
                    # 启动一个新线程来处理活动报名
                    threading.Thread(target=JoinActive, args=(passwd, passwd1, activityId)).start()
                    print('发现活动: %s,已添加到活动队列' % name)
                    activeList.append(name)
            else:
                # 如果设置了喜欢的活动关键词，则只报名包含关键词的活动
                for like_ in like:
                    if like_ in name:
                        if name not in activeList:
                            # 启动一个新线程来处理活动报名
                            threading.Thread(target=JoinActive, args=(passwd, passwd1, activityId)).start()
                            print('发现活动: %s,已添加到活动队列' % name)
                            activeList.append(name)

        # 每隔60秒检查一次活动列表
        time.sleep(60)

# 发现活动报名关键词，如果为空则报名所有
# 主程序入口
if __name__ == '__main__':
    # 检查是否存在token文件
    if os.path.exists('token'):
        # 读取token文件内容
        with open('token', mode='r', encoding='utf-8') as f:
            datas = f.readlines()[0]
            # 将JSON字符串转换为Python字典
            data_s = json.loads(datas)
            # 获取账号
            account = data_s['account']
            # 获取密码
            pwd = data_s['pwd']
    else:
        # 提示用户输入账号
        account = input('请输入你的账号(手机号):')
        # 提示用户输入密码
        pwd = input('请输入你的密码:')
    # 调用Apply函数进行账号登录，返回登录信息
    passwd = Apply(account=account, pwd=pwd)
    # 初始化一个空字典，用于存储登录信息
    passwd1 = {}

    # 启动一个新线程来运行ActiveDeamon函数，处理活动报名任务
    threading.Thread(target=ActiveDeamon, args=(passwd,)).start()

