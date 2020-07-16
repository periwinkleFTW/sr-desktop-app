############################################################
# styles.py
# This file contains stylesheets for GUI elements
############################################################


def mainStyle():
    return '''
    QTabWidget {
    background-color: #ffffff;
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
    
    QPushButton {
    border: 1px solid gray;
    border-radius: 5px;
    width: 200px;
    height: 30px;
    font: 15px bold;
    }
    '''

def groupBoxFillerStyle():
    return '''
    QGroupBox {
    border: none;
    background: none;
    }
    '''

