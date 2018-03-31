from logger import Logger
from mysqlconnector import MySQLConnector
from userstory import ModeleUserStory
from kanbantaskservice import KanbanTaskService
from kanbanconfigurationservice import KanbanConfigurationService
from userstoryservice import UserStoryService



# coding: utf-8
__author__ = 'gcailley'

config_database = {
    'host' : "127.0.0.1",
    'user' : "charly", 
    'passwd' : "charly", 
    'database' :"indicateurs_charly",
    'debug' : True
}

config_kanban = {
    'apiKey' : 'FD0FMV5J9TGB',
    'boardId' : '185986', 
    'urlKanbanServer' : 'https://pagesjaunes.kanbantool.com'
 }



if __name__ == "__main__":
    log = Logger('Main')

    log.info('Connecting to ' + config_database['database'])
    mysql = MySQLConnector(**config_database)
    log.info('Connecting to ' +  config_database['database'] + ': [DONE]')

    kanbanConfigurationnService = KanbanConfigurationService(mysql , **config_kanban)
    # kanbanConfigurationnService.collectStructure()

    kanbanTaskService = KanbanTaskService(mysql , **config_kanban)
    # kanbanTaskService.collectTasks()

    userStoryService = UserStoryService(mysql, kanbanTaskService)
    # creating Missing US
    userStoryService.createMissingUS()
    # updating US
    userStoryService.updateAllUS()


