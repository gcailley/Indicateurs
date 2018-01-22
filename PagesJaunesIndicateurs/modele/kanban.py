import datetime, dateutil.parser


class ModeleKanbanTask(object):
    def __init__(self, xml):
       self.xml = xml

    def get(self, name):
        if (len(self.xml.find(name).contents) > 0):
            return self.xml.find(name).contents[0]
        else:
            return ""

    def cleaner(self, value):
        eltToRemove= ['<p>','</p>','<br>','</br>']
        eltToReplace= [['\'',' '], ['\u2019','"'], ['\u2018','"'], ['\u0153','oe'], ['\u200b','??']]

        valueUpdated = value.encode('utf-8').strip().decode("utf-8") 
        print( valueUpdated)
        for elt in eltToRemove:
            valueUpdated = valueUpdated.replace(elt, '')
        for elt in eltToReplace:
            valueUpdated = valueUpdated.replace(elt[0], elt[1])

        return valueUpdated;

    def getId(self):
        return self.get('id')

    def getName(self):
        return self.cleaner(self.get('name'))

    def getDescription(self):
        return self.cleaner(self.get('description'))

    def getCreated(self):
        date = self.get('created-at')
        return self.getFormatedDate(date)

    def getUpdated(self):
        date = self.get('updated-at')
        return self.getFormatedDate(date)

    def getComplexity(self):
        return self.get('size-estimate')

    def getCardTypeId(self):
        return self.get('card-type-id')

    def getWorkflowStageIdTypeId(self):
        return self.get('workflow-stage-id')

    def getExternalLink(self):
        return self.get('external-link')

    def getCustomField2(self):
        return self.get('custom-field-2')


    def getFormatedDate(self, date):
        if (date != None):
            d = dateutil.parser.parse(date)
            return d.strftime('%Y/%m/%d')
        else:
            return ''



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