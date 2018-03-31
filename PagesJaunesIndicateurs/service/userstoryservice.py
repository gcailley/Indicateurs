import requests
import json
import argparse
import pprint

from bs4 import BeautifulSoup
from logger import Logger
from userstory import ModeleUserStory
from builders import BuilderUserStory
import requests
from kanbantaskservice import KanbanTaskService



class UserStoryService(object):

    USERSTORY_ID_US = 0;
    USERSTORY_FK_ID_KANBAN = 1;
    USERSTORY_CREATED = 2;
    USERSTORY_UPDATED = 3;
    USERSTORY_MURISSEMENT_TODO = 4;
    USERSTORY_MURISSEMENT_DONE  = 5;
    USERSTORY_CADRAGE_TODO = 6;
    USERSTORY_CADRAGE_DONE = 7;
    USERSTORY_DEV_TODO = 8;
    USERSTORY_DEV_DONE = 9;
    USERSTORY_ETAPE2_DONE = 10;
    USERSTORY_HD_DONE = 11;
    USERSTORY_PROD_OFF = 12;
    USERSTORY_PROD_ON = 13;
    
    SQL_GET_USERSTORY_BY_IDTASK = 'SELECT `ID_US` FROM `user_stories` WHERE `FK_ID_KANBAN` = {}'
    SQL_SEARCH_TASKKANBAN_WITHOUT_US = 'SELECT ID_KANBAN FROM `kanban_tasks` A LEFT JOIN `user_stories` B ON A.ID_KANBAN = B.FK_ID_KANBAN WHERE B.FK_ID_KANBAN IS NULL GROUP BY A.ID_KANBAN'
    SQL_INSERT_USERSTORY = "INSERT INTO `user_stories`(`FK_ID_KANBAN`, `CREATED`, `UPDATED`, `MURISSEMENT_TODO`, `MURISSEMENT_DONE`, `CADRAGE_TODO`, `CADRAGE_DONE`, `DEV_TODO`, `DEV_DONE`, `ETAPE2_DONE`, `HD_DONE`, `PROD_OFF`, `PROD_ON`) VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{})"

    def __init__(self, database, kanbanTaskService):
        self.database = database;
        self.kanbanTaskService = kanbanTaskService;
        self.log = Logger('UserStoryService')
        self.builderUS = BuilderUserStory()


    # Methode permettant détecter les US manquantes et de faire la création
    def createMissingUS(self):
        self.log.info('Searching Missing US ...');
        
        idsMissing = self.database.queryallrows(self.SQL_SEARCH_TASKKANBAN_WITHOUT_US )
        self.log.info(str.format('Number of missing US : {}', len(idsMissing) ));

        if (len(idsMissing) != 0 ):
            self.log.info('Creating Missing US ...');
            for idTask in idsMissing:
                self.log.debug(str.format('Converting Task {} to US ', idTask[0] ));
                modeleKanbanTask = self.kanbanTaskService.getModeleKanbanTaskById(idTask[0]);
                self.saveModeleUserStoryFromModeleKanbanTask(modeleKanbanTask)
        
        self.log.info('All US are created.');
        return None

    #Methode permettant de mettre à jour les toutes US
    def userStoryService.updateAllUS()
        # TODO faire le travail d'update
        self.log.info('All US are updated.');
        return None
    def saveModeleUserStoryFromModeleKanbanTask(self, modeleKanbanTask):
        self.log.info(str.format('Converting Task [ {} ] into Us',  modeleKanbanTask.getId()))
        modeleUserStory = self.builderUS.convertModeleKanbanTaskToModeleUserStory(modeleKanbanTask)
           
        #get US from the database
        existingUS = None

        sqlUserStory = self.database.queryrows(str.format(self.SQL_GET_USERSTORY_BY_IDTASK, modeleUserStory.getIdTask()))
        if (len(sqlUserStory) != 0):
            self.log.debug('US found in database')
            modeleUserStory = self.builderUS.updateExistingModeleUserStoryWithModeleKanbanTask(modeleKanbanTask, modeleUserStory)
            # TODO besoin de mettre à jour l'US dans la base

        else: 
        #check if the US is a new US or existing one
            modeleUserStory = self.builderUS.updateNewModeleUserStoryWithModeleKanbanTask(modeleKanbanTask, modeleUserStory)
            self.database.insert(str.format(self.SQL_INSERT_USERSTORY, 
                    modeleUserStory.getIdTask(), #`FK_ID_KANBAN`,
                    self.sqlDate( modeleUserStory.getCreated()), #`CREATED
                    self.sqlDate( modeleUserStory.getUpdated()), #`UPDATED`
                    self.sqlDate(modeleUserStory.getDateMurissementDebut()), #`MURISSEMENT_TODO`
                    self.sqlDate(modeleUserStory.getDateMurissementFin()), #`MURISSEMENT_DONE`
                    self.sqlDate(modeleUserStory.getDateCadrageDebut()), #`CADRAGE_TODO`
                    self.sqlDate(modeleUserStory.getDateCadrageFin()), #`CADRAGE_DONE`
                    self.sqlDate(modeleUserStory.getDateDevDebut()), #`DEV_TODO`
                    self.sqlDate(modeleUserStory.getDateDevFin()), #`DEV_DONE`
                    self.sqlDate(modeleUserStory.getDateChaineFin()), #`ETAPE2_DONE`
                    self.sqlDate(modeleUserStory.getDateHdFin()), #`HD_DONE`
                    self.sqlDate(modeleUserStory.getDateProdOffFin()), #`PROD_OFF`
                    self.sqlDate(modeleUserStory.getDateProdOnFin()), #`PROD_ON`        
            ) )           
            


        

    def extractModeleUserStoriesfromXml(self, xml):
        self.log.debug('Converting Tasks into UserStories...')

        for xmlTask in xml.tasks:
            modeleKanbanTask = ModeleKanbanTask(xmlTask)
            self.saveUsFromKanbanTask(modeleKanbanTask)

        self.log.debug('Converting Tasks into UserStories : [DONE]')

   
    def sqlDate(self, value):
        if (value == ''):
            return 'Null'
        else:
            return "'" + value + "'"