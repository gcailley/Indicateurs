from logger import Logger
from userstory import ModeleUserStory



class BuilderUserStory(object):

    def createUserstory(self, task):
        us = ModeleUserStory(task.getId())
        return us


    def convertUserstory(self, row):
        us = ModeleUserStory(row[0])
        return us

    def updateUserstoryWithTask(self, task, us):
        us.setName(task.getName())
        us.setDescription(task.getDescription())
        us.setClefFF(task.getCustomField2())
        us.setThemeId(task.getCardTypeId())
        return us

    def updateNewUserstoryWithTask(self, task, us):
        us = self.updateUserstoryWithTask(task, us)
        us.setDate(task.getCreated(), task.getWorkflowStageIdTypeId())
        us.setComplexiteInitiale(task.getComplexity())
        return  us

    def updateExistingUserstoryWithTask(self, task, us):
        us = self.updateUserstoryWithTask(task, us)
        us.setDate(task.getUpdated(), task.getWorkflowStageIdTypeId())
        us.setComplexiteReestimee(task.getComplexity())
        return  us


