
class Logger(object):
    _level = 3

    def __init__(self, clazz):
        self.clazz = clazz

    def changeLogLevel(self, value):
        self._level = value


    def debug(self, message):
        if (self._level >=3 ):
            self.log('DEBUG', message)

    def info(self, message):
        if (self._level >= 2 ):
            self.log('INFO ', message)

    def warn(self, message):
        if (self._level >= 1 ):
            self.log('WARN ', message)

    def error(self, message):
        if (self._level >= 0 ):
            self.log('ERROR', message)

    def log(self, prefix, message):
         print ( '[' + prefix + '] ' + self.clazz + ' : ' + message)



