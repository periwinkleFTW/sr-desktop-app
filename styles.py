############################################################
# styles.py
# This file contains stylesheets for GUI elements
############################################################


def mainStyle():
    return '''  
    QTabWidget::pane {
    background-color: #F4F7F9;
    border: 0;
    padding: 0;
    }
    
    QTabWidget::tab-bar {
    left: 20px; /* move to the right by 20px */
    }
    
    QTabBar::tab:!selected {
    margin: 4px; /* make non-selected tabs look smaller */
    border: 1px;
    border-color: #5E6770;
    padding: 1px;
    background-color: #F4F7F9;
    }
    
    QTabBar::tab {
    font: 18px bold;
    color: gray;
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
    border-radius: 10px;
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
    border: 1px;
    border-color: #5E6770;
    }

    QTabBar::tab:selected {
    color: #438CDE;
    background-color: #DAEBFF;
    border-color: #5E6770; 
    border-radius: 10px;
    }
    
    QGroupBox {
    background-color:#edf3f6;
    font: 15px Bold;
    color: white;
    border: 1px solid gray;
    border-radius: 5px;
    margin-top: 1ex;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f6f7fa, stop: 1 #edf3f6);
    }
    
    QTableWidget {
    border: 1px solid gray;
    padding: -2px;
    background-color: white;
    alternate-background-color: #FAFBFC;
    }
    
    QTableWidget::item {
    border-style: none;
    border-bottom: 1px solid gray;
    }

    QHeaderView::section {
    border: 1px solid gray;
    font: 15px;
    background-color: #EDF1F5;
    }

    

    
    
    
    '''

def groupBoxFillerStyle():
    return '''
    QGroupBox {
    border: none;
    background: none;
    }
    '''

