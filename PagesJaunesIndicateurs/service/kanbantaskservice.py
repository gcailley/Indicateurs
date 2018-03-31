

import requests
import json
import argparse
import pprint

from bs4 import BeautifulSoup
from logger import Logger
from kanban import ModeleKanbanTasks
from userstory import ModeleUserStory
from builders import BuilderUserStory, BuilderKanbanTasks
import requests



class KanbanTaskService(object):

    SQL_INSERT_TASKKANBAN = "INSERT INTO `kanban_tasks` (`ID_KANBAN`, `NAME`, `DESCRIPTION`, `CREATED`, `UPDATED`,`ETAT_ID`, `THEME_ID`, `CLEFFF`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"
    SQL_GET_TASKKANBAN_BY_ID_UPDATED = "SELECT ID_KANBAN FROM `kanban_tasks` WHERE ID_KANBAN='{}' AND UPDATED='{}'"
    SQL_GET_TASKKANBAN_BY_ID = "SELECT `ID_KANBAN`, `NAME`, `DESCRIPTION`, `CREATED`, `UPDATED`, `INSERTION`, `ETAT_ID`, `THEME_ID`, `CLEFFF` FROM kanban_tasks WHERE ID_KANBAN = '{}'"

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

        #Create ModeleKanbanTask
        self.saveModeleKanbanTasksFromXml()


    def readXml(self, response):
        self.log.debug('Reading Response...')
        self.xml = BeautifulSoup(response, 'lxml')
        self.log.debug('Reading Response : [DONE]')

    def saveModeleKanbanTasksFromXml(self):
        savedTasks = 0
        for xmlTask in self.xml.tasks:
            if (len(xmlTask)> 1):
                builderKanbanTask = BuilderKanbanTasks()
                modeleKanbanTask = builderKanbanTask.convertXmlToModeleKanbanTask(xmlTask)

                #Recherche de l'existance du modeleKanbanTask dans la base
                taskInDatabase = self.database.queryrow(str.format(self.SQL_GET_TASKKANBAN_BY_ID_UPDATED, modeleKanbanTask.getId(), modeleKanbanTask.getUpdated()) )
                if (taskInDatabase == None):
                    self.log.debug(str.format('Saving Task [ {} ] into Database ...',  modeleKanbanTask.getId()))
                    self.database.insert(str.format(self.SQL_INSERT_TASKKANBAN, 
                                                    modeleKanbanTask.getId(), 
                                                    modeleKanbanTask.getName(), 
                                                    modeleKanbanTask.getDescription(), 
                                                    modeleKanbanTask.getCreated(), 
                                                    modeleKanbanTask.getUpdated(),
                                                    modeleKanbanTask.getEtatId(),
                                                    modeleKanbanTask.getThemeId(),
                                                    modeleKanbanTask.getClefFF()))
                                         
                    self.log.debug(str.format('Saving Task [ {} ] into Database : [DONE]', modeleKanbanTask.getId()))
                    savedTasks += 1

        self.log.debug(str.format('Number of XmlTasks          Found : {} ...', len(self.xml.tasks) ))
        self.log.debug(str.format('Number of ModeleKanbanTasks Saved : {} ...', savedTasks ))

    def getModeleKanbanTaskById(self, id):
        sqlTask = self.database.queryrow(str.format(self.SQL_GET_TASKKANBAN_BY_ID , id) );
        builder = BuilderKanbanTasks()
        return builder.convertSqlToModeleKanbanTask(sqlTask)
    
    def getUrlBoard(self):
        return  str.format('{}/api/v1/boards/{}/tasks.xml?api_token={}', self.url_kanban_server , self.board_id, self.api_key)
