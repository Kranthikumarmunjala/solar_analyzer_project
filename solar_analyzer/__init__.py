# import pymysql
# pymysql.install_as_MySQLdb()


import pymysql

# Trick Django into thinking we are using a newer version of mysqlclient
pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.install_as_MySQLdb()