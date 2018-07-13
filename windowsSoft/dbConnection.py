import pymysql

class dbConn(object):
    def __init__(self):
        self.connection = pymysql.connect(host='127.0.0.1',
                                          user='root',
                                          password='123',
                                          db='test',
                                          port=3306,
                                          charset='utf8',  # 不能用utf-8
                                          cursorclass=pymysql.cursors.DictCursor)


    def checkuser(self, username, password):
        with self.connection.cursor() as cursor:
            cursor.execute("select * from `user` where username = '%s'and password = '%s'" % (username, password))
            lists = cursor.fetchall()
            if lists:
                return 1




def checkUser(username, password):
  conn = dbConn()
  result = conn.checkuser(username, password)
  conn.connection.close()
  return result
