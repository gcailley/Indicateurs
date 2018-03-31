import sys;
from logger import Logger
import pymysql; #mysql library (you will need to install this on the system)

#ALTER DATABASE DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci 
class MySQLConnector(object):

    _connection = None;
    _instance = None;
    _log = None;
 
    def __init__(self, host="127.0.0.1", user="", passwd="", database="", debug=False):    # Versi�n 1.0.1
        self._log = Logger('MySQLConnector')
        try:
            if MySQLConnector._instance == None:
                MySQLConnector._instance = self;
                self.dbhost = host
                self.dbuser = user
                self.dbpassword = passwd
                self.dbname = database
                MySQLConnector._instance.connect(debug);    # Versi�n 1.0.1

        except Exception as e :
            self._log.error ("MySQL Error "+str(e));
 
    def instance(self):
        return MySQLConnector._instance;
 
    def get_connection(self):
        return MySQLConnector._connection;
 
    def connect(self, debug=False):
        try:
            MySQLConnector._connection = pymysql.connect(self.dbhost, self.dbuser, self.dbpassword, self.dbname);
            if debug:
                self._log.info("Database connection successfully established")
        except Exception as e:
            self._log.error ("MySQL Connection Couldn't be created... Fatal Error! "+str(e))
            sys.exit()
 
    def disconnect(self):
        try:
            ySQLConnector._connection.close();
        except:
            pass;#connection not open
 
    #query with no result returned
    def query(self, sql):
        cur = MySQLConnector._connection.cursor();
        return cur.execute(sql);
 
    def tryquery(self, sql):
        try:
            cur = MySQLConnector._connection.cursor();
            return cur.execute(sql);
        except:
            return False;
 
    #inserts and returns the inserted row id (last row id in PHP version)
    def insert(self, sql):
        cur = MySQLConnector._connection.cursor();
        cur.execute(sql);
        return self._connection.insert_id();
 
    def tryinsert(self, sql):
        try:
            cur = MySQLConnector._connection.cursor();
            cur.execute(sql);
            return self._connection.insert_id();
        except:
            return -1;
 
    #returns the first item of data
    def queryrow(self, sql):
        cur = MySQLConnector._connection.cursor();
        cur.execute(sql);
        return cur.fetchone();
 
    #returns a list of data (array)
    def queryrows(self, sql):
        cur = MySQLConnector._connection.cursor();
        cur.execute(sql);
        return cur.fetchmany();

    def queryallrows(self, sql):
        cur = MySQLConnector._connection.cursor();
        cur.execute(sql);
        return cur.fetchall();
