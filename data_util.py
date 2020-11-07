# coding=utf-8
"""
使用DBUtils数据库连接池中的连接，操作数据库
OperationalError: (2006, ‘MySQL server has gone away’)
"""
import pymysql
import datetime
from dbutils.pooled_db import PooledDB


class DatabaseOperational(object):
    __pool = None

    def __init__(self, mincached=10, maxcached=20, maxshared=10, maxconnections=200, blocking=True,
                 maxusage=100, setsession=None, reset=True,
                 host='localhost', port=3306, db='hnwl',
                 user='root', passwd='123456', charset='utf8'):
        """

        :param mincached:连接池中空闲连接的初始数量
        :param maxcached:连接池中空闲连接的最大数量
        :param maxshared:共享连接的最大数量
        :param maxconnections:创建连接池的最大数量
        :param blocking:超过最大连接数量时候的表现，为True等待连接数量下降，为false直接报错处理
        :param maxusage:单个连接的最大重复使用次数
        :param setsession:optional list of SQL commands that may serve to prepare
            the session, e.g. ["set datestyle to ...", "set time zone ..."]
        :param reset:how connections should be reset when returned to the pool
            (False or None to rollback transcations started with begin(),
            True to always issue a rollback for safety's sake)
        :param host:数据库ip地址
        :param port:数据库端口
        :param db:库名
        :param user:用户名
        :param passwd:密码
        :param charset:字符编码
        """

        if not self.__pool:
            self.__class__.__pool = PooledDB(pymysql,
                                             mincached, maxcached,
                                             maxshared, maxconnections, blocking,
                                             maxusage, setsession, reset,
                                             host=host, port=port, db=db,
                                             user=user, passwd=passwd,
                                             charset=charset,
                                             cursorclass=pymysql.cursors.DictCursor)
        self._conn = None
        self._cursor = None
        self.__get_conn()

    def __get_conn(self):
        self._conn = self.__pool.connection()
        self._cursor = self._conn.cursor()

    def close(self):
        with self._cursor as a:
            a.close()
        with self._conn as b:
            b.close()

    def __execute(self, sql, param=()):
        count = self._cursor.execute(sql, param)
        return count

    @staticmethod
    def __dict_datetime_obj_to_str(result_dict):
        """
        把字典里面的data time对象转成字符串，
        使json转换不出错
        """
        if result_dict:
            result_replace = {k: v.__str__() for k, v in result_dict.items() if isinstance(v, datetime.datetime)}
            result_dict.update(result_replace)
        return result_dict

    def select_one(self, sql, param=()):
        """查询单个结果"""
        count = self.__execute(sql, param)
        result = self._cursor.fetchone()
        """:type result:dict"""
        result = self.__dict_datetime_obj_to_str(result)
        return count, result

    def select_many(self, sql, param=()):
        """
        查询多个结果
        :param sql: qsl语句
        :param param: sql参数
        :return: 结果数量和查询结果集
        """
        count = self.__execute(sql, param)
        result = self._cursor.fetchall()
        """:type result:list"""
        [self.__dict_datetime_obj_to_str(row_dict) for row_dict in result]
        return count, result

    def execute(self, sql, param=()):
        count = self.__execute(sql, param)
        return count

    @staticmethod
    def __getConn(self):
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        return self.__pool.connection()

    def getAll(self, sql, param=None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = False
        return result

    def getOne(self, sql, param=None):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchone()
        else:
            result = False
        return result

    def getMany(self, sql, num, param=None):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchmany(num)
        else:
            result = False
        return result

    def insertOne(self, sql, value):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
        """
        self._cursor.execute(sql, value)
        return self.__getInsertId()

    def insertMany(self, sql, values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = self._cursor.executemany(sql, values)
        return count

    def __getInsertId(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        self._cursor.execute("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]['id']

    def __query(self, sql, param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        return count

    def update(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def delete(self, sql, param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def begin(self):
        """
        @summary: 开启事务
        """
        self._conn.autocommit(0)

    def end(self, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self, isEnd=1):
        """
        @summary: 释放连接池资源
        """
        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()

# if __name__ == '__main__':
#     """
#     示例代码
#     :return:
#     """
#     # 申请资源
#     mysql = DatabaseOperational()
#
#     sqlAll = "SELECT * FROM `url_save_info`"
#
#     result = mysql.getAll(sqlAll)
#
#     print(result)
#     """insert """
#     # 占位符用%s
#     sqlSave = "INSERT INTO `url_reptile`.`url_save_info`(`url`, `path`) VALUES (%s, %s)"
#
#     '''参数使用tuple或list'''
#     data = ['http://www.bing.com', './websites/www.bing.com/www.bing.com.html']
#     '''执行插入操作'''
#     mysql.insertOne(sqlSave, data)
#     '''commit 操作，并关闭连接池'''
#     mysql.dispose()
