import datetime, dateutil.parser

class ModeleKanbanTasks(object):
    def __init__(self, id, name, description, created, updated, etatId, themeId, clefFF):
        self.id = id
        self.name = name
        self.description = description
        self.created = created
        self.updated = updated
        self.etatId = etatId
        self.themeId = themeId
        self.clefFF = clefFF
   


    def getId(self):
        return self.id

    def getUpdated(self):
        return self.updated

    def getCreated(self):
        return self.created

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getClefFF(self):
        return self.clefFF
    
    def getThemeId(self):
        return self.themeId

    def getEtatId(self):
        return self.etatId


class ModeleKanbanWorkflow(object):
    def __init__(self, xml):
       self.xml = xml

    def get(self, name):
        if (len(self.xml.find(name).contents) > 0):
            return self.xml.find(name).contents[0]
        else:
            return ""

    def getId(self):
        return self.get('id')

    def getName(self):
        return self.get('name')