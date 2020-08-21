from backend import Database

db = Database("sr-data.db")

class IssuesDropdownData():

    def priorityItems(self):
        itemlist = ["Low", "Medium", "High"]
        return itemlist

    def observerItems(self):
        itemlist = []

        query = "SELECT person_id, person_first_name, person_last_name FROM people"
        peopleRecords = db.cur.execute(query).fetchall()

        for i, person in enumerate(peopleRecords):
            itemlist.append(peopleRecords[i][1] + " " + peopleRecords[i][2])

        return itemlist

    def revTeamItems(self):
        itemlist = ["RevTeam1", "RevTeam2", "RevTeam3"]
        return itemlist

    def inspNameItems(self):
        itemlist = [
            "Internal scheduled audit",
            "Internal unscheduled inspection of teams/departments",
            "Internal scheduled inspection of departments",
            "Internal scheduled inspection of contractor/subcontractor",
            "Learning from incidents",
            "RCA / incident investigation"
        ]
        return itemlist

    def hseThemeItems(self):
        itemlist = ["In-vehicle monitoring system audit",
            "In-field roads audit",
            "Audit of excavation works",
            "Audit of work at height",
            "Audit of communication and shift handover process",
            "Audit of instances of Process Safeguarding Systems",
            "Fitness/Wellness compliance audit",
            "HSSE MS Audit",
            "Hazard management effectiveness audit",
            "Fire and gas detection system audit",
            "RSMT daily report",
            "HSSE site inspection",
            "Camps and production sites complex audit",
            "Complex vehicle, documents, and loading procedures audit",
            "Transportation contractors audit",
            "Actions from shareholders LFI",
            "Hazard hunt",
            "Hardware barrier assessment",
            "Standing committee lvl 2",
            "Standing committee lvl 3",
            "Management site inspection",
            "Falling objects audit",
            '"Hands-free" program inspection',
            "Lifting equipment inspection",
            "Contractor demobilization inspection",
            "Camp and trailer inspection during hazard period",
            "ISA quality check",
            "Quality check of IRP action items closure",
            "Training quality check",
            "Contractor mobilization inspection",
            "Equipment inspection",
            "Camp general conditions inspection",
            "Check of isolation equipment (electrical, mechanical, etc)",
            "Fire-fighting condition inspection",
            "Hygiene inspection",
            "Grey area inspection",
            "Permits/Work orders effectiveness inspection",
            "Well control inspection",
            "PPE compliance inspection",
            "Record keeping audit",
            "Inspection of compliance with environmental requirements",
            "Start-up criterion inspection",
            "Camp Fire & Electric safety conditions inspection"
            "Camp trailer inspection",
            "Punch lists",
            "Sponsorship audit"
        ]
        return itemlist

    def facilityItems(self):
        itemlist = []

        query = "SELECT facility_id, facility_name FROM facilities"
        facilitiesRecords = db.cur.execute(query).fetchall()

        for i, person in enumerate(facilitiesRecords):
            itemlist.append(facilitiesRecords[i][1])

        return itemlist

    def facSupervisorItems(self):
        itemlist = []

        query = "SELECT person_id, person_first_name, person_last_name FROM people"
        peopleRecords = db.cur.execute(query).fetchall()

        for i, person in enumerate(peopleRecords):
            itemlist.append(peopleRecords[i][1] + " " + peopleRecords[i][2])

        return itemlist

    def inspDeptItems(self):
        itemlist = ["Dept1", "Dept2", "Dept3"]
        return itemlist

    def inspContrItems(self):
        itemlist = []

        query = "SELECT person_id, person_first_name, person_last_name FROM people"
        peopleRecords = db.cur.execute(query).fetchall()

        for i, person in enumerate(peopleRecords):
            itemlist.append(peopleRecords[i][1] + " " + peopleRecords[i][2])

        return itemlist

    def inspSubcontrItems(self):
        itemlist = []

        query = "SELECT person_id, person_first_name, person_last_name FROM people"
        peopleRecords = db.cur.execute(query).fetchall()

        for i, person in enumerate(peopleRecords):
            itemlist.append(peopleRecords[i][1] + " " + peopleRecords[i][2])

        return itemlist

    def statusItems(self):
        itemlist = ["Open", "Closed"]
        return itemlist

class PeopleDropdownData():
    def emplTypeItems(self):
        itemlist = ["Employee", "Contractor", "Subcontractor"]
        return itemlist



class FacilitiesDropdownData():
    def facSupervisorItems(self):
        pass
