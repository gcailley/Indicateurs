from logger import Logger
from userstory import ModeleUserStory
from kanban import ModeleKanbanTasks
import datetime, dateutil.parser


class BuilderKanbanTasks(object):
    TASKKANBAN_ID_KANBAN=0;
    TASKKANBAN_NAME=1;
    TASKKANBAN_DESCRIPTION=2;
    TASKKANBAN_CREATED=3;
    TASKKANBAN_UPDATED=4;
    TASKKANBAN_INSERTION=5;
    TASKKANBAN_ETAT_ID=6;
    TASKKANBAN_THEME_ID=7;
    TASKKANBAN_CLEFFF=8;
    
    def convertXmlToModeleKanbanTask(self, xml):
        return ModeleKanbanTasks(
            self.getId(xml), 
            self.getName(xml), 
            self.getDescription(xml), 
            self.getCreated(xml), 
            self.getUpdated(xml),
            self.getWorkflowStageIdTypeId(xml),
            self.getCardTypeId(xml),
            self.getCustomField1(xml)
        )

    def convertSqlToModeleKanbanTask(self, sql):
        return ModeleKanbanTasks(
            sql[BuilderKanbanTasks.TASKKANBAN_ID_KANBAN], 
            sql[BuilderKanbanTasks.TASKKANBAN_NAME],
            sql[BuilderKanbanTasks.TASKKANBAN_DESCRIPTION],
            sql[BuilderKanbanTasks.TASKKANBAN_CREATED],
            sql[BuilderKanbanTasks.TASKKANBAN_UPDATED],
            sql[BuilderKanbanTasks.TASKKANBAN_ETAT_ID],
            sql[BuilderKanbanTasks.TASKKANBAN_THEME_ID],
            sql[BuilderKanbanTasks.TASKKANBAN_CLEFFF]
            );

    def get(self, xml, name):
        if (len(xml.find(name).contents) > 0):
            return xml.find(name).contents[0]
        else:
            return ""

    def cleaner(self, value):
        eltToRemove= ['<p>','</p>','<br>','</br>']
        eltToReplace= [['\'',' '], ['\u2019','"'], ['\u2018','"'], ['\u0153','oe'], ['\u200b','??']]

        valueUpdated = value.encode('utf-8').strip().decode("utf-8") 
        for elt in eltToRemove:
            valueUpdated = valueUpdated.replace(elt, '')
        for elt in eltToReplace:
            valueUpdated = valueUpdated.replace(elt[0], elt[1])

        return valueUpdated;

    def getId(self, xml):
        return self.get(xml, 'id')

    def getName(self, xml):
        return self.cleaner(self.get(xml, 'name'))

    def getDescription(self, xml):
        return self.cleaner(self.get(xml, 'description'))

    def getCreated(self, xml):
        date = self.get(xml, 'created-at')
        return self.getFormatedDate(date)

    def getUpdated(self, xml):
        date = self.get(xml,'updated-at')
        return self.getFormatedDate(date)

    def getComplexity(self, xml,):
        return self.get(xml,'size-estimate')

    def getCardTypeId(self, xml):
        return self.get(xml,'card-type-id')

    def getWorkflowStageIdTypeId(self, xml):
        return self.get(xml,'workflow-stage-id')

    def getExternalLink(self, xml):
        return self.get(xml,'external-link')

    def getCustomField1(self, xml):
        return self.get(xml,'custom-field-1')

    def getCustomField2(self, xml):
        return self.get(xml,'custom-field-2')

    def getFormatedDate(self, date):
        if (date != None):
            d = dateutil.parser.parse(date)
            return d.strftime('%Y/%m/%d')
        else:
            return ''




class BuilderUserStory(object):

    def convertModeleKanbanTaskToModeleUserStory(self, modeleKanbanTask):
        modeleUserStory = ModeleUserStory()
        modeleUserStory.setIdTask(modeleKanbanTask.getId())
        return modeleUserStory


    def convertSqlToModeleUserStory(self, row):
        modeleUserStory = ModeleUserStory()
        modeleUserStory.setId(row[0])
        return modeleUserStory

    def updateModeleUserStoryWithModeleKanbanTask(self, modeleKanbanTask, modeleUserStory):
        modeleUserStory.setName(modeleKanbanTask.getName())
        modeleUserStory.setDescription(modeleKanbanTask.getDescription())
        modeleUserStory.setClefFF(modeleKanbanTask.getClefFF())
        #TODO convertir en name 
        modeleUserStory.setTheme(modeleKanbanTask.getThemeId())
        modeleUserStory.setIdTask(modeleKanbanTask.getId())
        
        return modeleUserStory

    def updateNewModeleUserStoryWithModeleKanbanTask(self, modeleKanbanTask, modeleUserStory):
        modeleUserStory = self.updateModeleUserStoryWithModeleKanbanTask(modeleKanbanTask, modeleUserStory)
        modeleUserStory.setDate(modeleKanbanTask.getCreated(), modeleKanbanTask.getEtatId())
        # TODO 
        # modeleUserStory.setComplexiteInitiale(modeleKanbanTask.getComplexity())
        return  modeleUserStory

    def updateExistingModeleUserStoryWithModeleKanbanTask(self, modeleKanbanTask, modeleUserStory):
        modeleUserStory = self.updateModeleUserStoryWithModeleKanbanTask(modeleKanbanTask, modeleUserStory)
        modeleUserStory.setDate(modeleKanbanTask.getUpdated(), modeleKanbanTask.getEtatId())
        # modeleUserStory.setComplexiteReestimee(modeleKanbanTask.getComplexity())
        return  modeleUserStory


