from logger import Logger
import datetime, dateutil.parser

class ModeleUserStory(object):

    ETAT_SUJETS_A_FAIRE='1438608'
    ETAT_SKETCHING='1438610'
    ETAT_SKETCHING_A_FAIRE='1438612'
    ETAT_SKETCHING_EN_COURS='1438614'
    ETAT_SKETCHING_A_VALIDER='1438616'
    ETAT_SKETCHING_VALIDE='1438618'
    ETAT_US='1438620'
    ETAT_US_A_FAIRE='1438622'
    ETAT_US_EN_COURS='1438624'
    ETAT_US_A_VALIDER='1438626'
    ETAT_DE='1438628'
    ETAT_DE_A_FAIRE='1438630'
    ETAT_DE_EN_COURS='1438632'
    ETAT_DE_A_VALIDER='1438634'
    ETAT_DE_VALIDE='1438636'
    ETAT_STATS='1438638'
    ETAT_STATS_A_FAIRE='1438640'
    ETAT_STATS_OK='1438642'
    ETAT_MURISSEMENT_OK='1438644'
    ETAT_HTML='1438646'
    ETAT_HTML_EN_COURS='1438648'
    ETAT_HTML_A_VALIDER='1438650'
    ETAT_HTML_TERMINE='1438652'
    ETAT_CADRAGE='1438654'
    ETAT_CADRAGE_OK='1438656'
    ETAT_PLANIF_OK='1438658'
    ETAT_DEV_EN_COURS='1438660'
    ETAT_ETAPE2_OK='1438668'
    ETAT_HD_OK='1438670'
    ETAT_PROD_OFF_OK='1438672'



    def __init__(self):

        now = datetime.datetime.now()
        self.id = None
        self.date_murissement_debut= None
        self.date_murissement_fin= None
        self.date_cadrage_debut= None
        self.date_cadrage_fin= None
        self.date_dev_debut= None
        self.date_dev_fin= None
        self.date_chaine_fin= None
        self.date_hd_fin= None
        self.date_prod_off_fin= None
        self.date_prod_on_fin= None
        self.created = now
        self.updated = now

    def getFormatedDate(self, date):
        if (type(date) is datetime.datetime):
            return date.strftime('%Y/%m/%d')
        else:
            if (date != None):
                d = dateutil.parser.parse(date)
                return d.strftime('%Y/%m/%d')
            else:
                return ''


    def setId(self, value):
        self.id = value

    def setName(self, value):
        self.name = value

    def setTheme(self, value):
        self.theme = value

    def setIdTask(self, value):
        self.id_task = value

    def getIdTask(self):
        return self.id_task

    def setDescription (self, value):
        self.description = value

    def setComplexiteInitiale (self, value):
        self.complexite_initiale = value

    def setComplexiteReestimee (self, value):
        self.complexite_reestimee = value

    def setClefFF (self, value):
        self.clef_ff= value
        
    def setIfNotNullDateSujetATraiter (self, value):
        self.date_sujet_a_traiter = value

    def setIfNotNullDateMurissementDebut (self, value):
        self.date_murissement_debut = value

    def setIfNotNullDateMurissementFin (self, value):
        self.date_murissement_fin = value

    def setIfNotNullDateCadrageDebut (self, value):
        self.date_cadrage_debut = value

    def setIfNotNullDateCadrageFin (self, value):
        self.date_cadrage_fin = value

    def setIfNotNullDateDevDebut (self, value):
        self.date_dev_debut = value

    def setIfNotNullDateDevFin (self, value):
        self.date_dev_fin = value

    def setIfNotNullDateChaineDebut (self, value):
        self.date_chaine_debut = value

    def setIfNotNullDateChaineFin (self, value):
        self.date_chaine_fin = value

    def setIfNotNullDateHdDebut (self, value):
        self.date_hd_debut = value

    def setIfNotNullDateHdFin (self, value):
        self.date_hd_fin = value

    def setIfNotNullDateProdOffDebut (self, value):
        self.date_prod_off_debut = value

    def setIfNotNullDateProdOnFin (self, value):
        self.date_prod_on_fin = value

    def getDateMurissementDebut(self):
        return self.getFormatedDate(self.date_murissement_debut)

    def getDateMurissementFin(self):
        return self.getFormatedDate(self.date_murissement_fin)

    def getDateCadrageDebut(self):
        return self.getFormatedDate(self.date_cadrage_debut)

    def getDateCadrageFin(self):
        return self.getFormatedDate(self.date_cadrage_fin)

    def getDateDevDebut(self):
        return self.getFormatedDate(self.date_dev_debut)

    def getDateDevFin(self):
        return self.getFormatedDate(self.date_dev_fin)

    def getDateChaineFin(self):
        return self.getFormatedDate(self.date_chaine_fin)

    def getDateHdFin(self):
        return self.getFormatedDate(self.date_hd_fin)

    def getDateProdOffFin(self):
        return self.getFormatedDate(self.date_prod_off_fin)

    def getDateProdOnFin(self):
        return self.getFormatedDate(self.date_prod_on_fin)

    def getCreated(self):
        return self.getFormatedDate(self.created)

    def getUpdated(self):
        return self.getFormatedDate(self.updated)

    def setDate(self, date, idEtat):
        if (idEtat == self.ETAT_SUJETS_A_FAIRE or
            idEtat == self.ETAT_SKETCHING or
            idEtat == self.ETAT_SKETCHING_A_FAIRE or
            idEtat == self.ETAT_SKETCHING_A_VALIDER or
            idEtat == self.ETAT_SKETCHING_EN_COURS or
            idEtat == self.ETAT_SKETCHING_VALIDE
            ):
            self.setIfNotNullDateSujetATraiter(date)
            self.setIfNotNullDateMurissementDebut(None)
            self.setIfNotNullDateMurissementFin (None)
            self.setIfNotNullDateCadrageDebut (None)
            self.setIfNotNullDateCadrageFin (None)
            self.setIfNotNullDateDevDebut (None)
            self.setIfNotNullDateDevFin (None)
            self.setIfNotNullDateChaineDebut (None)
            self.setIfNotNullDateChaineFin (None)
            self.setIfNotNullDateHdDebut (None)
            self.setIfNotNullDateHdFin (None)
            self.setIfNotNullDateProdOffDebut (None)
            self.setIfNotNullDateProdOnFin (None)
        elif ( idEtat == self.ETAT_US or
              idEtat == self.ETAT_US_A_FAIRE
             ):
            self.setIfNotNullDateSujetATraiter(None)
            self.setIfNotNullDateMurissementDebut(date)
            self.setIfNotNullDateMurissementFin (None)
            self.setIfNotNullDateCadrageDebut (None)
            self.setIfNotNullDateCadrageFin (None)
            self.setIfNotNullDateDevDebut (None)
            self.setIfNotNullDateDevFin (None)
            self.setIfNotNullDateChaineDebut (None)
            self.setIfNotNullDateChaineFin (None)
            self.setIfNotNullDateHdDebut (None)
            self.setIfNotNullDateHdFin (None)
            self.setIfNotNullDateProdOffDebut (None)
            self.setIfNotNullDateProdOnFin (None)

        elif ( idEtat == self.ETAT_CADRAGE or 
               idEtat == self.ETAT_CADRAGE_OK
             ):
            self.setIfNotNullDateSujetATraiter(None)
            self.setIfNotNullDateMurissementDebut(None)
            self.setIfNotNullDateMurissementFin (date)
            self.setIfNotNullDateCadrageDebut (None)
            self.setIfNotNullDateCadrageFin (None)
            self.setIfNotNullDateDevDebut (None)
            self.setIfNotNullDateDevFin (None)
            self.setIfNotNullDateChaineDebut (None)
            self.setIfNotNullDateChaineFin (None)
            self.setIfNotNullDateHdDebut (None)
            self.setIfNotNullDateHdFin (None)
            self.setIfNotNullDateProdOffDebut (None)
            self.setIfNotNullDateProdOnFin (None)

    def toString(self):
        return 'id:' +  self.id + ' name:' + self.name + ' date creation:' + self.date_sujet_a_traiter
