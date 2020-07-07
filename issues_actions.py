
from add_issue import AddIssue

class IssuesActions():
    def __init__(self, parent):
        self.Parent = parent

    def funcAddIssue(self):
        self.newIssue = AddIssue(self)