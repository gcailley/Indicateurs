

import requests
import json
import argparse
import pprint

from bs4 import BeautifulSoup
from logger import Logger
from kanban import ModeleKanbanWorkflow
from builders import BuilderUserStory
import requests



class KanbanConfigurationService(object):

    SQL_INSERT_WORKFLOWKANBAN = "INSERT INTO `kanban_workflow` (`ID_WORKFLOW`, `NAME`) VALUES ('{}', '{}');"
    SQL_GET_WORKFLOWKANBAN_BY_ID = 'SELECT * FROM `kanban_workflow` WHERE ID_WORKFLOW = {}'

    def __init__(self, database, apiKey='', boardId='', urlKanbanServer=''):
        self.database = database
        self.api_key = apiKey
        self.board_id = boardId
        self.log = Logger('KanbanConfigurationService')
        self.url_kanban_server = urlKanbanServer

    # Methode permettant de récupérer la stucuture du kanbantools
    def collectStructure(self):
        url = self.getUrlBoardConfiguration()
 
        #call url and retrieve the xml response
        self.log.debug(str.format('Calling URL : {} ...', url ))   
        proxies = { 'http': 'zscaler-paris.pj.fr:80', 'https': 'zscaler-frankfurt.pj.fr:80' }
        response = requests.get(url, proxies=proxies)
        self.log.debug(str.format('Calling URL : {} : [DONE]', url ))      

        #read xml response
        self.readXml(response.content)

        #Create US
        self.saveConfigurationFromXml()


    #def readXmlConfiguration(response.content)


    def readXml(self, response):
        self.log.debug('Reading Configuration Response...')
        self.xml = BeautifulSoup(response, 'lxml')
        self.log.debug('Reading Configuration Response : [DONE]')

    def saveConfigurationFromXml(self):
        for workflow in self.xml.board.find('workflow-stages'):
            if (len(workflow)> 1):
                kanbanWorkflow = ModeleKanbanWorkflow(workflow)
                
                taskInDatabase = self.database.queryrow(str.format(self.SQL_GET_WORKFLOWKANBAN_BY_ID, kanbanWorkflow.getId()) )
                if (taskInDatabase == None):
                    self.log.info(str.format('Saving Workflow [ {} ] into Database ...',  kanbanWorkflow.getId()))
                    self.database.insert(str.format(self.SQL_INSERT_WORKFLOWKANBAN, kanbanWorkflow.getId(), kanbanWorkflow.getName()) )   
                    self.log.info(str.format('Saving Workflow [ {} ] into Database : [DONE]', kanbanWorkflow.getId()))

  
    def getUrlBoardConfiguration(self):
        return  str.format('{}/api/v1/boards/{}.xml?api_token={}', self.url_kanban_server , self.board_id, self.api_key)
