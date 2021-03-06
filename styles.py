############################################################
# styles.py
# This file contains stylesheets for GUI elements
############################################################

#  background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f6f7fa, stop: 1 #edf3f6);

def mainStyle():
    return '''  
    QTabWidget::pane {
    background-color: #F4F7F9;
    border: 0;
    padding: 0;
    }
    
    QTabWidget::tab-bar {
    left: 17px; /* move to the right by 20px */
    }
    
    QTabBar::tab:!selected {
    margin: 4px; /* make non-selected tabs look smaller */
    padding: 1px;
    background-color: #F4F7F9;
    border: 1px solid gray;
    }
    
    QTabBar::tab {
    font: 18px bold;
    color: gray;
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
    border-radius: 5px;
    width: 14ex; /* Tab width */
    height: 3ex;
    min-width: 8ex;
    padding: 1x;
    margin: 3px;
    }

    QTabBar::tab:selected, QTabBar::tab:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
    background-color: #EBF7FF;
    padding: 2px;
    border: 1px solid gray;
    }

    QTabBar::tab:selected {
    color: #438CDE;
    background-color: #DAEBFF;
    border-color: #438CDE; 
    border-radius: 5px;
    }
    
    QGroupBox {
    background-color:#E6EFF3;
    font: 15px Bold;
    color: white;
    border: 1px solid gray;
    border-color: #EBEBEB;
    border-radius: 5px;
    margin-top: 1ex;
    }
        
    QTableWidget {
    border: 1px solid gray;
    padding: -2px;
    background-color: white;
    alternate-background-color: #FAFBFC;
    selection-background-color: #DFF9E3;
    selection-color: black;
    }
    
    QTableWidget::item {
    border-style: none;
    border-bottom: 1px solid gray;
    }

    QHeaderView::section {
    border: 1px solid gray;
    font: 13px;
    background-color: #EDF1F5;
    }
    
    QPushButton {
    min-width: 60px;
    height: 20px;
    border: 1px solid gray;
    border-radius: 5px;
    border-style: outset;
    background-color: #FDFEFA;
    }
    
    QPushButton:hover {
    border-style: double;
    background-color: #F7FFFD;
    }
    
    QPushButton:pressed {
    background-color: #80B9FF;
    }
    

    
    QPushButton:disabled {
    border: none;
    }
    
    '''

def groupBoxFillerStyle():
    return '''
    QGroupBox {
    border: none;
    background: none;
    }
    '''

def addPopups():
    return '''
    QWidget {
    background-color: #F4F7F9;
    }
    
    QWidget > QLabel#add_issue_title_txt {
    border: 1px solid gray; 
    padding-top: 30px; 
    padding-bottom: 30px; 
    border-radius: 5; 
    font: 16px;
    }
    
    QWidget#add_person_popup {
    background-color: #F4F7F9;
    }
    
    QWidget > QLabel#add_person_title_txt {
    border: 1px solid gray; 
    padding-top: 30px; 
    padding-bottom: 30px; 
    border-radius: 5; font: 16px;
    }
    
    QWidget#add_facility_popup {
    background-color: #F4F7F9;
    }
    
    QWidget > QLabel#add_fcl_title_txt {
    border: 1px solid gray; 
    padding-top: 30px; 
    padding-bottom: 30px; 
    border-radius: 5; 
    font: 16px;
    }
    
    QWidget > QScrollArea {
    background-color: transparent;
    }
    
    QScrollArea > QWidget > QWidget {
    border: none;
    background-color: #F4F7F9;
    }  
    
    QPushButton {
    min-width: 60px;
    width: 60px;
    height: 20px;
    border: 1px solid gray;
    border-radius: 5px;
    border-style: outset;
    background-color: #FDFEFA;
    }
    
    QPushButton:pressed {
    background-color: #CCE3FF;
    }
    
    QPushButton:hover {
    border-style: double;
    }
    
    QPushButton:disabled {
    border: none;
    }
    
    QComboBox {
        background: white;
        border: 1px solid gray;
        border-radius: 3px;
        padding: 1px 18px 1px 3px;
        min-width: 6em;
    }
    
    QComboBox:editable {
        background: white;
    }
    
    QComboBox:!editable, QComboBox::drop-down:editable {
         background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                     stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                     stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
    }
    
    /* QComboBox gets the "on" state when the popup is open */
    QComboBox:!editable:on, QComboBox::drop-down:editable:on {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,
                                    stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);
    }
    
    QComboBox:on { /* shift the text when the popup opens */
        padding-top: 3px;
        padding-left: 4px;
    }
    
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
    
        border-left-width: 1px;
        border-left-color: darkgray;
        border-left-style: solid; /* just a single line */
        border-top-right-radius: 3px; /* same radius as the QComboBox */
        border-bottom-right-radius: 3px;
    }
    
    QComboBox::down-arrow {
        image: url(assets/icons/ui_icons/dropdown_arrow.jpg);
    }
    
    QComboBox::down-arrow:on { /* shift the arrow when popup is open */
        top: 1px;
        left: 1px;
    }
    
    '''

