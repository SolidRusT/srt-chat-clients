from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QMenuBar, QToolBar, QStatusBar, QFileDialog, QMessageBox
from PySide6.QtGui import QAction
import os
import sys
import yaml

class YAMLAgentEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.currentFile = ''
        self.initUI()

    def initUI(self):
        self.setWindowTitle("YAML Agent Editor")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTextEdit {
                border: 1px solid #ccc;
                font: 12pt "Courier";
            }
            QToolBar {
                background-color: #e0e0e0;
            }
            QStatusBar {
                background-color: #e0e0e0;
            }
        """)

        # Editor Area
        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)

        # Menu Bar
        self.menuBar = QMenuBar()
        self.setMenuBar(self.menuBar)
        fileMenu = self.menuBar.addMenu('&File')

        # File Menu Actions
        newAction = QAction('&New', self)
        newAction.triggered.connect(self.newFile)
        fileMenu.addAction(newAction)

        openAction = QAction('&Open', self)
        openAction.triggered.connect(self.openFile)
        fileMenu.addAction(openAction)

        saveAction = QAction('&Save', self)
        saveAction.triggered.connect(self.saveFile)
        fileMenu.addAction(saveAction)

        saveAsAction = QAction('Save &As...', self)
        saveAsAction.triggered.connect(self.saveAsFile)
        fileMenu.addAction(saveAsAction)

        exitAction = QAction('&Exit', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        toolbar.addAction(newAction)
        toolbar.addAction(openAction)
        toolbar.addAction(saveAction)

        # Status Bar
        self.statusBar = self.statusBar()

    def isValidYAML(self, content):
        try:
            data = yaml.safe_load(content)
            # Validate specific structure (e.g., check for 'agents' key)
            if 'agents' in data and isinstance(data['agents'], list):
                return True
            else:
                return False
        except yaml.YAMLError:
            return False

    def newFile(self):
        self.editor.clear()
        self.currentFile = ''
        self.statusBar.showMessage("New file")

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "YAML Files (*.yaml *.yml)")
        if filename:
            with open(filename, 'r') as file:
                content = file.read()
                if self.isValidYAML(content):
                    self.editor.setText(content)
                    self.currentFile = filename
                    self.statusBar.showMessage(f"Opened {os.path.basename(filename)}")
                else:
                    QMessageBox.warning(self, "Error", "Invalid YAML format")
                    self.currentFile = ''
                    self.editor.clear()

    def saveFile(self):
        if self.isValidYAML(self.editor.toPlainText()):
            if self.currentFile:
                with open(self.currentFile, 'w') as file:
                    file.write(self.editor.toPlainText())
                self.statusBar.showMessage(f"Saved {os.path.basename(self.currentFile)}")
            else:
                self.saveAsFile()
        else:
            QMessageBox.warning(self, "Error", "Cannot save. Invalid YAML format.")

    def saveAsFile(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "YAML Files (*.yaml *.yml)")
        if filename:
            with open(filename, 'w') as file:
                file.write(self.editor.toPlainText())
            self.currentFile = filename
            self.statusBar.showMessage(f"Saved as {os.path.basename(filename)}")

    def closeEvent(self, event):
        # Prompt to save if unsaved changes
        response = QMessageBox.question(self, "Exit", "Do you want to save changes before exiting?")
        if response == QMessageBox.Yes:
            self.saveFile()
        event.accept()

def main():
    app = QApplication(sys.argv)
    mainWin = YAMLAgentEditor()
    mainWin.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
