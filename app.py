from flask import Flask, json, jsonify, request
from flask_cors import CORS

import pymysql

app = Flask(__name__)
CORS(app, resources=r'/*')


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


@app.route("/login", methods=["POST"])

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
    json_data = {}
    ret = {}
    conn, cursor = get_conn()
    email = json_data.get('email')
    password = json_data.get('pass')
    print(email, password )
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
            ret["code"] = 200
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
            ret["code"] = 300
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
        ret["code"] = 300

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


@app.route("/register", methods=["POST"])
# @verify_data
def register(json_data: {}, ret: {}):
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

        ret['code'] = 200
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
        ret['code'] = 300
        return jsonify(ret)
#
# # 注册
# # 获取注册请求及处理
# @app.route('/register', methods=['POST'])
# def register(json_data: {}, ret: {}):
#     print("hello")
#     conn, cursor = get_conn()
#     # 提取表单
#     print("连接")
#     username = json_data.get('name')
#     email = json_data.get('email')
#     password = json_data.get('pass')
#     print(username, email, password)
#     # SQL 插入语句
#     sql = "INSERT INTO usertable(username, email, password) VALUES (" +"'"+ username + "'"+ ","+ "'"+ email + "'" +"," +"'"+ password + "'"+")"
#     try:
#         # 执行sql语句
#         cursor.execute(sql)
#         # 提交到数据库执行
#         conn.commit()
#         # 关闭数据库连接
#         close_conn(conn, cursor)
#         # 注册成功之后跳转到登录页面
#         return dict(msg=1, content="注册成功")
#     except:
#         # 如果发生错误则回滚
#         conn.rollback()
#         # 关闭数据库连接
#         close_conn(conn, cursor)
#         return dict(msg=0, content="注册失败") # email是主键，要是重名，自然会注册失败
#
#
# # 登录
# @app.route('/login', methods=['POST'])
# def getLoginRequest():
#     conn, cursor = get_conn()
#     # 提取表单
#     username = str(request.form.get('username'))
#     password = str(request.form.get('password'))
#     # SQL 查询语句
#     # sql = "select * from usertable where username=" +username+ " and password=" +password
#     sql = "select * from usertable where username=" + "'" + username + "'" + "and " + "password=" + "'" + password + "'"# 要加单引号！
#     try:
#         # 执行sql语句
#         cursor.execute(sql)
#         results = cursor.fetchall()
#         msg = 1
#         content = "登录成功"
#         if len(results) == 1:
#             msg = 1
#             content = "登录成功"
#         else:
#             msg = 0
#             content = "用户名或密码不正确"
#         conn.commit()
#         close_conn(conn, cursor)
#         return dict(msg=msg, content=content)
#     except:
#         conn.rollback()
#         close_conn(conn, cursor)
#         return dict(msg=-1, content="数据库发生错误")


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5013)
    app.run()
