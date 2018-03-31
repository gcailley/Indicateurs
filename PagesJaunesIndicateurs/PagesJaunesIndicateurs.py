from logger import Logger
from mysqlconnector import MySQLConnector
from userstory import ModeleUserStory
from kanbantaskservice import KanbanTaskService
from kanbanconfigurationservice import KanbanConfigurationService
from userstoryservice import UserStoryService
import configparser
import os.path

Config = configparser.ConfigParser()

filename = './indicateurs_configuration.ini'
filename_dist = filename + '.dist'

if os.path.isfile(filename_dist ):
    Config.read(filename_dist )
else:
    Config.read(filename )

# coding: utf-8
__author__ = 'gcailley'

config_database = {}
config_database['host'] = Config.get('config_database', 'host')
config_database['user'] = Config.get('config_database', 'user')
config_database['passwd'] = Config.get('config_database', 'passwd')
config_database['database'] = Config.get('config_database', 'database')
config_database['debug'] = Config.get('config_database', 'debug')


config_kanban = {}
config_kanban['apiKey'] = Config.get('config_kanban', 'apiKey')
config_kanban['boardId'] = Config.get('config_kanban', 'boardId')
config_kanban['urlKanbanServer'] = Config.get('config_kanban', 'urlKanbanServer')




if __name__ == "__main__":
    log = Logger('Main')

    log.info('Connecting to ' + config_database['database'])
    mysql = MySQLConnector(**config_database)
    log.info('Connecting to ' +  config_database['database'] + ': [DONE]')

    kanbanConfigurationnService = KanbanConfigurationService(mysql , **config_kanban)
    kanbanConfigurationnService.collectStructure()

    kanbanTaskService = KanbanTaskService(mysql , **config_kanban)
    kanbanTaskService.collectTasks()

    userStoryService = UserStoryService(mysql, kanbanTaskService)
    # creating Missing US
    userStoryService.createMissingUS()
    # updating US
    userStoryService.updateAllUS()


