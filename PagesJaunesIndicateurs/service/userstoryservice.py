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



class UserStoryService(object):

    def __init__(self, database, apiKey='', boardId='', urlKanbanServer=''):
        self.database = database
        self.log = Logger('UserStoryService')


    # Methode permettant de récupérer la liste des ID des tasks en base
    def collectTasksId(self):
        return None


    def extractUserStoriesfromXml(self):
        self.log.debug('Converting Tasks into UserStories...')
        builder = BuilderUserStory()

        for task in self.xml.tasks:
            kanbanTask = ModeleKanbanTask(task)
            self.log.info(str.format('Converting Task [ {} ] into Us',  kanbanTask.getId()))
            us = builder.createUserstory(kanbanTask)
            
            #get US from the database
            existingUS = None

            data = self.database.queryrow(str.format(self.SQL_GET_USERSTORY_BY_ID, us.id))
            if (data != None):
                self.log.debug('US found in database')
                existingUS = builder.convertUserstory(data)    

            #check if the US is a new US or existing one
            if (existingUS == None):
                us = builder.updateNewUserstoryWithTask(kanbanTask, us)
            else:
                us = builder.updateExistingUserstoryWithTask(kanbanTask, existingUS)

        self.log.debug('Converting Tasks into UserStories : [DONE]')

   
