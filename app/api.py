'''
-------------------------------------------------
    File name:    api.py
    Description:    api接口
    Author:     RGDZ
    Data:    2020/01/17 12:35:26
-------------------------------------------------
   Version:    v1.0
   Contact:    rgdz.gzu@qq.com
   License:    (C)Copyright 2020-2021
'''
import pymysql
from flask import Blueprint, request, jsonify
from functools import wraps

from .models import *



api = Blueprint("api", __name__)

class Code:
    """ 后台状态枚举类 """
    NULL = 0 # 什么都没有
    ERROR = 100 # 执行错误
    SUCCESS = 200 #成功
    NOT_ADMIN = 300 # 非管理员
    ADMIN_BUT_NOEXEC = 301 #是管理员，但未执行代码
    NOT_LOGIND = 400 #未登录
    LOGIND_BUT_NOEXEC = 401 # 已经验证登录，但未执行代码
    TOKEN_LOSE = 500 #Token 失效
    FLAG_ERROR = 600 # flag 错误
    FLAG_EXISTED = 700 # flag 已提交
    VERIFY_DATA = 800 # 验证数据
    VERIFYD_BUT_NOEXEC = 801 # 已验证数据，但未执行代码
    BAD_DATA = 900 # 坏数据
    NO_EXISTSED = 1000 # 数据不存在
    EXISTSED = 1001 #数据已存在



def get_conn():
    '''
    :return: 返回conn、cursor
    '''
    # 连接数据库,此前在数据库中创建数据库TESTDB
    # conn = pymysql.connect(host="10.112.3.14", port=3366,
    #                        user="root", password="zk@963852",
    #                        db="userinfo", charset="utf8")
    # conn = pymysql.connect(host="10.100.32.59", port=3366,
    #                        user="root", password="zk@963852",
    #                        db="userinfo", charset="utf8")
    conn = pymysql.connect(host="localhost", port=3306,
                           user="root", password="123456",
                           db="bishe", charset="utf8")
    # 创建cursor负责操作conn接口
    cursor=conn.cursor()  #默认返回的结果是元组形式
    # 开启事务
    conn.begin()
    return conn, cursor


def close_conn(conn, cursor):
    '''
    :param conn
    :param cursor
    :return: 销毁conn、cursor
    '''
    if cursor:
        cursor.close()
    if conn:
        conn.close()


# 接口权限控制装饰器
# def verify_data(func):
#     """ 验证数据是否可靠，相当于waf层，TODO: 封装可扩展 """
#     @wraps(func)
#     def wrapper(*args, **kw):
#         ret = {'code': Code.NULL}
#         json_data = request.get_json(force=True)
#         username = json_data.get('username')
#         email = json_data.get('email')
#         password = json_data.get('pass')
#         if password and email or username:
#             ret['code'] = Code.VERIFYD_BUT_NOEXEC
#             return func(json_data, ret)
#         ret['code'] = Code.BAD_DATA
#         return jsonify(ret)
#     return wrapper

# def require_login(func):
#     """ 登录控制 """
#     @wraps(func)
#     def wrapper(*args, **kw):
#         ret={'code':Code.NOT_LOGIND}
#         user_data = request.get_json(force=True).get('user')
#         token = user_data.get('token')
#         uid = user_data.get('uid')
#         role = user_data.get('role')
#         if token:
#             user = User.verify_auth_token(token)
#             if user and str(user.id)==uid and user.role==role:
#                 ret['code'] = Code.LOGIND_BUT_NOEXEC
#                 return func(user=user, ret=ret)
#             ret['code'] = Code.TOKEN_LOSE
#         return func(user=None, ret=ret)
#     return wrapper
#
# def admin(func):
#     """ 管理员权限控制 """
#     @wraps(func)
#     def wrapper(user: User, ret: {}):
#         if user:
#             if user.isAdmin:
#                 ret['code'] = Code.ADMIN_BUT_NOEXEC
#                 return func(ret)
#             ret['code'] = Code.NOT_ADMIN
#         return jsonify(ret)
#     return wrapper


# API接口

@api.route("/")
def index():
    return jsonify({"msg":"hello"})


@api.route("/searchcar", methods=["GET"])
# @verify_data
def searchcar():
    """ 登录接口
        请求数据:
        {
            查询类型
            "type":,

        }
        返回数据:
        {
            "code":200,
            "user": {
                'data':[  {
                            },
                           {
                             }
                ]
            }
        }
    """
    ret = {
        'data': [],
        'coordmap': {}
    }
    guiji=[]
    print("进入")
    conn, cursor = get_conn()
    # type = json_data.get('type')
    terminal = request.args.get('data')
    print(terminal)
    #注意此处type类型

    if terminal == '0':
        sql = "select * from car_current_location;"  # 要加单引号！
    else :
        sql = "select * from location_info_copy2;"
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()

        if terminal == '0':
            for ele in results:
                point = [ele[2], ele[3]]
                ret['coordmap'][ele[0]] = point
                eledata = {
                    'name': ele[0],
                    'value': 10
                }
                ret['data'].append(eledata)
        else:
            single = []
            for ele in results:
                point = [ele[2], ele[3]]
                eledata = {'coord': point, 'time': str(ele[1])}
                single.append(eledata)
                # ret['data'].append(eledata)
            guiji.append(single)
            print(guiji)
            return jsonify(guiji)
        print(ret)
        msg = 1
        # return 1
        content = "登录成功"
        if len(results) == 1:
            msg = 1
            content = "登录成功"
            ret["code"] = Code.SUCCESS
            ret['user'] = {
                'uid': str(1),
                'role': 11,
                'token': 1111
            }
            return jsonify(ret)
        else:
            msg = 0
            content = "用户名或密码不正确"
            ret["code"] = Code.ERROR
            ret['user'] = {
                'uid': str(1),
                'role': 11,
                'name': 'ma',
                'token': 1111
            }
            return jsonify(ret)
    except:
        conn.rollback()
        close_conn(conn, cursor)
        ret["code"] = Code.ERROR

        return jsonify(ret)


@api.route("/search", methods=["GET"])
# @verify_data
def search():
    """ 登录接口
        请求数据:
        {
            查询类型
            "type":,

        }
        返回数据:
        {
            "code":200,
            "user": {
                'data':[  {
                            },
                           {
                             }
                ]
            }
        }
    """
    ret = {
        'data': []
    }
    print("进入")
    conn, cursor = get_conn()
    # type = json_data.get('type')
    type = int(request.args.get('data'))
    print(type)
    #注意此处type类型
    if type == 1:
        sql = "select * from car_data_distance;"  # 要加单引号！
    elif type == 2:
        sql = "select * from car_data_distance;"
    elif type == 3:
        sql = "select * from car_speed_exceed;"
    elif type == 4:
        sql = "select * from car_data_frequency;"
    elif type == 5:
        sql = "select * from car_direction_change;"
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()

        if type == 2:
            for ele in results:
                eledata = {
                    'date': str(ele[1]),
                    'name': ele[0],
                    'address': str(ele[2])+"米"
                }
                ret['data'].append(eledata)
        if type == 3:
            for ele in results:
                eledata = {
                    'date': str(ele[1]),
                    'name': ele[0],
                    'address': str(ele[2])+"公里/小时"
                }
                ret['data'].append(eledata)

        if type == 4:
            for ele in results:
                # print(ele)
                eledata = {
                    'date': str(ele[1]),
                    'name': ele[0],
                    'dataFrequency': ele[2],
                    'maxdataFrequency': ele[3],
                    'mindataFrequency': ele[4],

                }
                ret['data'].append(eledata)

        if type == 5:
            for ele in results:
                # print(ele)
                eledata = {
                    'date': str(ele[1]),
                    'name': ele[0],
                    'lastDirection': ele[2],
                    'nowDirection': ele[3]

                }
                ret['data'].append(eledata)
        print(ret['data'])
        msg = 1
        # return 1
        content = "登录成功"
        if len(results) == 1:
            msg = 1
            content = "登录成功"
            ret["code"] = Code.SUCCESS
            ret['user'] = {
                'uid': str(1),
                'role': 11,
                'token': 1111
            }
            return jsonify(ret)
        else:

            ret["code"] = Code.ERROR
            ret['user'] = {
                'uid': str(1),
                'role': 11,
                'name': 'ma',
                'token': 1111
            }
            return jsonify(ret)
    except:
        conn.rollback()
        close_conn(conn, cursor)
        ret["code"] = Code.ERROR

        return jsonify(ret)





@api.route("/login", methods=["POST"])
# @verify_data
def login():
    """ 登录接口
        请求数据:
        {
            "email":email,
            "pass":pass
        }
        返回数据:
        {
            "code":200,
            "user": {
                'uid':uid,
                'role:role,
                'name':name,
                'token':token
            }
        }
    """

    json_data = request.get_json(force=True)
    ret = {}
    conn, cursor = get_conn()
    email = json_data.get('email')
    password = json_data.get('pass')

    sql = "select username from usertable where email=" + "'" + email + "'" + "and " + "password=" + "'" + password + "'"  # 要加单引号！
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        username = results[0][0]
        msg = 1
        content = "登录成功"
        if len(results) == 1:
            msg = 1
            content = "登录成功"
            ret["code"] = Code.SUCCESS
            ret['user'] = {
                'uid': str(1),
                'role': 11,
                'name': username,
                'token': 1111
            }
            close_conn(conn, cursor)
            return jsonify(ret)
        else:

            msg = 0
            content = "用户名或密码不正确"
            ret["code"] = Code.ERROR
            ret['user'] = {
                'uid': str(1),
                'role': 11,
                'name': 'ma',
                'token': 1111
            }
            close_conn(conn, cursor)
            return jsonify(ret)
        # conn.commit()
        # close_conn(conn, cursor)


    except:
        conn.rollback()
        close_conn(conn, cursor)
        ret["code"] = Code.ERROR

        return jsonify(ret)
    #
    # user = User.objects(userEmail=email).first()
    # if user:
    #     if user.verify_pass(password):
    #         ret["code"] = Code.SUCCESS
    #         ret['user']={
    #             'uid':str(user.id),
    #             'role':user.role,
    #             'name':user.userName,
    #             'token':user.token
    #         }
    #         return jsonify(ret)
    #     ret["code"] = Code.ERROR
    #     return jsonify(ret)
    # return jsonify(ret)


@api.route("/register", methods=["POST"])
# @verify_data
def register():
    """ 注册接口
        请求数据:
        {
            "username": username,
            "email": email,
            "pass": password
        }
        返回数据:
        {
            "code":200,
            "user": {
                'uid':uid,
                'role:role,
                'name':name,
                'token':token
            }
        }
    """
    json_data = request.get_json(force=True)
    ret = {}
    username = json_data.get('username')
    email = json_data.get('email')
    password = json_data.get('pass')

    conn, cursor = get_conn()
    # 提取表单
    print("连接")
    print(username, email, password)
    # SQL 插入语句
    sql = "INSERT INTO usertable(username, email, password) VALUES (" + "'" + username + "'" + "," + "'" + email + "'" + "," + "'" + password + "'" + ")"
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        conn.commit()
        # 关闭数据库连接

        close_conn(conn, cursor)

        ret['code'] = Code.SUCCESS
        ret['user'] = {
            'uid': 1,
            'role': '1',
            'name': username,
            'token': 111
        }
        return jsonify(ret)
        # 注册成功之后跳转到登录页面

    except:
        # 如果发生错误则回滚
        conn.rollback()
        # 关闭数据库连接
        close_conn(conn, cursor)
        ret['code'] = Code.ERROR
        return jsonify(ret)
        # return dict(msg=0, content="注册失败")  # email是主键，要是重名，自然会注册失败

    # if not User.isexist(username, email):
    #     user = User.init(username, email, password)
    #     ret['code'] = Code.SUCCESS
    #     ret['user']={
    #         'uid':str(user.id),
    #         'role': user.role,
    #         'name':user.userName,
    #         'token':user.token
    #     }
    #     return jsonify(ret)
    # ret['code'] = Code.ERROR
    # return jsonify(ret)

@api.route("/check_exists", methods=["GET"])
def check_exists():
    """ 检查用户名,邮箱是否存在 
        请求参数:
        ?value=value
        返回数据:
        {
            'code':200
        }
    """
    ret = {'code':Code.NULL}
    value = request.args.get('value')
    if User.isexist(username=value, email=value):
        ret['code'] = Code.EXISTSED # 用户已存在
        return jsonify(ret)
    ret['code'] = Code.NO_EXISTSED
    return jsonify(ret)

@api.route("/userInfo", methods=["GET"])
def userInfo():
    """ 获取用户信息接口 
        请求参数: ?uid=uid
        返回数据: 
        {
            'code':200,
            'userInfo':{
                'scoreData':scoreData,
                'score':score
                'scoreDFS':scoreDFS
            }
        }
    """
    ret={'code':Code.NULL, 'userInfo':{}}
    uid = request.args.get('uid')
    user = User.objects(pk=uid).first()
    if user:
        ret.update({
        'userInfo':{
            'name': user.userName,
            'scoreData':user.scoreData,
            'solvedStatic':user.solvedStatic,
            'score':user.score,
            'scoreDFS':{user.userName:user.scoreDFS}
        }
    })
    ret['code'] = Code.SUCCESS
    return jsonify(ret)


@api.route("/challenges", methods=["POST"])
# @require_login
def challenges(user: User, ret: {}):
    """ 获取challenges数据接口 
        请求数据:
        {
            'ctype':'Pwn',
            'toke':'token' （可选）
        }
        返回数据:
        {
            "code":200,
            "challenges":[
                {
                    'cid':cid,
                    'type':type,
                    'title':title,
                    'des':des,
                    'socre':score,
                    'solved':solved (根据token)
                },
                ...
            ]
        }
    """
    ret['challenges'] = []
    ctype = request.get_json(force=True).get('ctype')
    challenges = Challenge.objects(tIdx=cTypes.index(ctype)).order_by("-createTime")
    for challenge in challenges:
        data = {
            'cid':str(challenge.id),
            'type':challenge.ctype,
            'title':challenge.title,
            'des': challenge.description,
            'score': challenge.score,
            'solvers': len(challenge.solvers),
            'solved': False
            }
        if user:
            data.update({'solved':challenge in user.solveds})
        ret['challenges'].append(data)
    return jsonify(ret)
        


@api.route("/submit_flag", methods=['POST'])
# @require_login
def submit_flag(user: User, ret: {}):
    """ 提交flag接口 
        请求数据:
        {
            'token':token,
            'cid':cid,
            'flag':flag
        }
        返回数据:
        {
            "code":200,
        }
    """
    json_data = request.get_json(force=True)
    cid = json_data.get('cid')
    flag = json_data.get('flag')
    if user:
        challenge = Challenge.objects(pk=cid).first()
        ret['code'] = Code.FLAG_EXISTED
        if challenge not in user.solveds:
            ret['code'] = Code.FLAG_ERROR
            if challenge.verify_flag(flag):
                user.solved_challenge(challenge)
                ret['code'] = Code.SUCCESS
    return jsonify(ret)
    
    

@api.route('/add_challenge', methods=['POST'])
# @require_login
# @admin
def add_challenge(ret: {}):
    """ 添加题目接口 
        请求数据:
        {
            'token':token
            'type':type,
            'title':title,
            'des':des,
            'score':score,
            'flag':flag
        }
        返回数据:
        {
            "code":200,
        }
    """
    json_data = request.get_json(force=True)
    tIdx = cTypes.index(json_data.get('type'))
    title = json_data.get('title')
    des = json_data.get('des')
    score = json_data.get('score')
    flag = json_data.get('flag')
    Challenge.init(tIdx, title, des, score, flag)
    ret['code'] = Code.SUCCESS
    return jsonify(ret)


@api.route('/del_challenge', methods=['POST'])
# @require_login
# @admin
def del_challenge(ret: {}):
    """ 删除题目接口 
        请求数据:
        {
            'token':token,
            'cid':cid
        }
    """
    cid = request.get_json(force=True).get('cid')
    Challenge.objects(id=cid).first().delete()
    Challenge.objects(id=cid).delete()
    ret['code'] = Code.SUCCESS
    return jsonify(ret)


@api.route('/announcements', methods=['GET'])
def announcements():
    """ 获取公告信息接口 
        请求参数: /
        返回数据: 
        {
            'code':200,
            'anncs':[]
        }
    """
    ret = {
        'code':Code.NULL,
        'anncs':[]
    }
    for annc in Announcement.objects().order_by("-createTime"):
        ret['anncs'].append({
            'aid':str(annc.id),
            'title':annc.title,
            'body':annc.body,
            'createTime':annc.date
        })
    ret['code'] = Code.SUCCESS
    return jsonify(ret)


@api.route('/add_announcement', methods=['POST'])
# @require_login
# @admin
def add_announcement(ret: {}):
    """ 添加公告接口 
        请求数据: 
        {
            'token':token,
            'title':title,
            'body':body
        }
        返回数据:
        {
            'code':200,
        }
    """
    json_data = request.get_json(force=True)
    title = json_data['title']
    body = json_data['body']
    Announcement.init(title, body)
    ret['code'] = Code.SUCCESS
    return jsonify(ret)


@api.route('/del_announcement', methods=['POST'])
# @require_login
# @admin
def del_announcement(ret: {}):
    """ 删除公告接口 
        请求数据: 
        {
            'aid':aid
        }
        返回数据:
        {
            'code':200,
        }
    """
    aid = request.get_json(force=True).get('aid')
    Announcement.objects(pk=aid).delete()
    ret['code'] = Code.SUCCESS
    return jsonify(ret)


@api.route('/score_card', methods=["GET"])
def score_card():
    """ 计分板数据接口
        返回数据:
        {
            'code':200,
            'msg':success,
            'data':[
                {
                    'rank': 1,
                    'name': 'aaa',
                    'solved': 5,
                    'score': 900
                },
                ...
            ]
        }
    """
    ret = {'code':Code.NULL, 'table':[], 'top10':{}}
    ret['table'] = User.static()
    for idx in range(len(ret['table'])):
        if idx>10:
            break
        user = User.objects(pk=ret['table'][idx]['uid']).first()
        ret['top10'].update({user.userName:user.scoreDFS})
    ret['code'] = Code.SUCCESS
    return jsonify(ret)