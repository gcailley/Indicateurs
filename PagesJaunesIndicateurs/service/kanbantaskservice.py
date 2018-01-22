

import requests
import json
import argparse
import pprint

from bs4 import BeautifulSoup
from logger import Logger
from kanban import ModeleKanbanTask
from userstory import ModeleUserStory
from builders import BuilderUserStory
import requests



class KanbanTaskService(object):

    SQL_INSERT_TASKKANBAN = "INSERT INTO `kanban_tasks` (`ID_KANBAN`, `NAME`, `DESCRIPTION`, `CREATED`, `UPDATED`) VALUES ('{}', '{}', '{}', '{}', '{}');"
    SQL_GET_TASKKANBAN_BY_ID_UPDATED = "SELECT ID_KANBAN FROM `kanban_tasks` WHERE ID_KANBAN='{}' AND UPDATED='{}'"
    SQL_GET_USERSTORY_BY_ID = 'SELECT * FROM USERSTORIES WHERE ID = {}'

    def __init__(self, database, apiKey='', boardId='', urlKanbanServer=''):
        self.database = database
        self.api_key = apiKey
        self.board_id = boardId
        self.log = Logger('KanbanTaskService')
        self.url_kanban_server = urlKanbanServer

  
    def collectTasks(self):
        url = self.getUrlBoard()
 
        #call url and retrieve the xml response
        self.log.debug(str.format('Calling URL : {} ...', url ))   
        proxies = { 'http': 'zscaler-paris.pj.fr:80', 'https': 'zscaler-frankfurt.pj.fr:80' }
        response = requests.get(url, proxies=proxies)
        self.log.debug(str.format('Calling URL : {} : [DONE]', url ))      

        #read xml response
        self.readXml(response.content)

        #Create US
        self.saveTasksFromXml()


    def readXml(self, response):
        self.log.debug('Reading Response...')
        self.xml = BeautifulSoup(response, 'lxml')
        self.log.debug('Reading Response : [DONE]')

    def saveTasksFromXml(self):
        for task in self.xml.tasks:
            if (len(task)> 1):
                kanbanTask = ModeleKanbanTask(task)
                
                taskInDatabase = self.database.queryrow(str.format(self.SQL_GET_TASKKANBAN_BY_ID_UPDATED, kanbanTask.getId(), kanbanTask.getUpdated()) )
                if (taskInDatabase == None):
                    self.log.info(str.format('Saving Task [ {} ] into Database ...',  kanbanTask.getId()))
                    self.database.insert(str.format(self.SQL_INSERT_TASKKANBAN, kanbanTask.getId(), kanbanTask.getName(), kanbanTask.getDescription(), kanbanTask.getCreated(), kanbanTask.getUpdated()) )   
                    self.log.info(str.format('Saving Task [ {} ] into Database : [DONE]', kanbanTask.getId()))


    def getUrlBoard(self):
        return  str.format('{}/api/v1/boards/{}/tasks.xml?api_token={}', self.url_kanban_server , self.board_id, self.api_key)
