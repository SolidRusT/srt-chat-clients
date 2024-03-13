import sys
import os
import yaml
import collections
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QStyleFactory,
    QToolBar,
    QFileDialog,
    QMessageBox,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QComboBox,
)
from PySide6.QtGui import QIcon, QAction, QFontMetrics
from PySide6.QtCore import Qt

class StyleSheetLoader:
    @staticmethod
    def load(filename):
        with open(filename, "r") as file:
            return file.read()


class YAMLFileHandler:
    @staticmethod
    def isValidYAML(content):
        try:
            data = yaml.safe_load(content)
            if "agents" in data and isinstance(data["agents"], list):
                return True
            else:
                return False
        except yaml.YAMLError:
            return False

    @staticmethod
    def readYAML(filename):
        load_ordered_dict = lambda loader, node: collections.OrderedDict(
            loader.construct_pairs(node)
        )
        yaml.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, load_ordered_dict
        )
        with open(filename, "r") as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    @staticmethod
    def writeYAML(data, filename):
        represent_ordered_dict = lambda dumper, data: dumper.represent_dict(
            data.items()
        )
        yaml.add_representer(collections.OrderedDict, represent_ordered_dict)
        with open(filename, "w") as file:
            yaml.dump(data, file, Dumper=yaml.Dumper, default_flow_style=False)

class AutoWidthComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

    def showEvent(self, event):
        super().showEvent(event)
        self.updateWidth()

    def updateWidth(self):
        width = self.width()
        font_metrics = QFontMetrics(self.font())
        max_item_width = max(font_metrics.horizontalAdvance(self.itemText(i)) for i in range(self.count()))
        arrow_width = 255  # Approximate width for the dropdown arrow and padding
        self.setMinimumWidth(max_item_width + arrow_width)

class AgentDetailsEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self._createEditorWidgets()

    def _createEditorWidgets(self):
        self.nameEdit = QLineEdit()
        self.roleEdit = QLineEdit()
        self.goalEdit = QLineEdit()
        self.backstoryEdit = QTextEdit()

        fields = [
            ("Name:", self.nameEdit),
            ("Role:", self.roleEdit),
            ("Goal:", self.goalEdit),
            ("Backstory:", self.backstoryEdit),
        ]

        for label, widget in fields:
            self.layout.addWidget(QLabel(label))
            self.layout.addWidget(widget)

    def displayAgentDetails(self, agent):
        self.nameEdit.setText(agent["name"])
        self.roleEdit.setText(agent["role"])
        self.goalEdit.setText(agent["goal"])
        self.backstoryEdit.setPlainText(agent["backstory"])


class ThemeManager:
    def __init__(self):
        self.isDarkMode = False

    def applyTheme(self, widget):
        if self.isDarkMode:
            stylesheet = StyleSheetLoader.load("styles/default-dark.qss")
            icon = QIcon("icons/sun_icon.png")
            # tooltip = "Light Mode"
        else:
            stylesheet = StyleSheetLoader.load("styles/default-light.qss")
            icon = QIcon("icons/moon_icon.png")
            # tooltip = "Light Mode"
        widget.setStyleSheet(stylesheet)
        return icon  # , tooltip

    def toggleTheme(self):
        self.isDarkMode = not self.isDarkMode


class AgentEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.currentFile = ""
        self.agentsData = {}
        self.selectedAgentIndex = None
        self.agentIndexMapping = []
        self.themeManager = ThemeManager()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Agent Manager")
        self.setGeometry(100, 100, 1000, 400)

        #self.roleFilterComboBox = QComboBox()
        self.roleFilterComboBox = AutoWidthComboBox() 
        self.roleFilterComboBox.addItem("All Roles", None)
        self.roleFilterComboBox.currentIndexChanged.connect(self.populateAgentSelector)

        self.agentSelector = QComboBox()
        self.agentSelector.currentIndexChanged.connect(self.displayAgentDetails)

        self.toolbarLayout = QVBoxLayout()
        self.toolbarLayout.addWidget(self.roleFilterComboBox)
        self.toolbarLayout.addWidget(self.agentSelector)

        self.toolbarWidget = QWidget()
        self.toolbarWidget.setLayout(self.toolbarLayout)
        self.addToolBar(Qt.LeftToolBarArea, self.createToolbar("Agent Selector", self.toolbarWidget))

        self.agentDetailsEditor = AgentDetailsEditor()
        self.setCentralWidget(self.agentDetailsEditor)

        self.createActions()
        self.createToolbars()
        self.applyTheme()

    def createActions(self):
        self.loadAction = QAction("&Load", self)
        self.loadAction.triggered.connect(self.openFile)

        self.saveAction = QAction("&Save", self)
        self.saveAction.triggered.connect(self.saveFile)

        self.saveAsAction = QAction("Save &As...", self)
        self.saveAsAction.triggered.connect(self.saveAsFile)

        self.exitAction = QAction("&Exit", self)
        self.exitAction.triggered.connect(self.close)

        self.newAgentAction = QAction("&New Agent", self)
        self.newAgentAction.triggered.connect(self.createNewAgent)

        self.toggleThemeAction = QAction(self)
        self.toggleThemeAction.triggered.connect(self.toggleTheme)

        self.deleteAgentAction = QAction("&Delete Agent", self)
        self.deleteAgentAction.triggered.connect(self.deleteAgent)

    def createActionWithIcon(self, action, iconPath, tooltip):
        action.setIcon(QIcon(iconPath))
        action.setToolTip(tooltip)
        return action

    def createToolbar(self, title, widget):
        toolbar = QToolBar(title)
        toolbar.addWidget(widget)
        return toolbar

    def createToolbars(self):
        fileToolbar = QToolBar("File")
        self.addToolBar(fileToolbar)
        fileToolbar.addAction(self.loadAction)
        fileToolbar.addSeparator()
        fileToolbar.addAction(self.saveAction)
        fileToolbar.addSeparator()
        fileToolbar.addAction(self.saveAsAction)

        agentToolbar = QToolBar("Agent")
        self.addToolBar(agentToolbar)
        agentToolbar.addAction(
            self.createActionWithIcon(
                self.newAgentAction, "icons/plus_icon.png", "New Agent"
            )
        )
        agentToolbar.addAction(
            self.createActionWithIcon(
                self.deleteAgentAction, "icons/minus_icon.png", "Delete Agent"
            )
        )

        themeToolbar = QToolBar("Theme")
        self.addToolBar(themeToolbar)
        themeToolbar.addAction(self.toggleThemeAction)

    def applyTheme(self):
        icon = self.themeManager.applyTheme(self)
        self.toggleThemeAction.setIcon(icon)
        self.toggleThemeAction.setToolTip("Toggle Theme")

    def toggleTheme(self):
        self.themeManager.toggleTheme()
        self.applyTheme()

    def createNewAgent(self):
        new_agent = collections.OrderedDict(
            [
                ("name", "New Agent"),
                ("role", ""),
                ("goal", ""),
                ("backstory", ""),
            ]
        )

        self.agentsData["agents"].append(new_agent)
        self.populateAgentSelector()
        self.agentSelector.setCurrentIndex(len(self.agentsData["agents"]) - 1)
        self.displayAgentDetails(len(self.agentsData["agents"]) - 1)

    def deleteAgent(self):
        if self.selectedAgentIndex is None or len(self.agentsData["agents"]) == 0:
            return

        del self.agentsData["agents"][self.selectedAgentIndex]
        self.populateAgentSelector()

        # Update the selected agent index
        new_index = min(self.selectedAgentIndex, len(self.agentsData["agents"]) - 1)
        if new_index >= 0:
            self.agentSelector.setCurrentIndex(new_index)
            self.displayAgentDetails(new_index)
        else:
            self.clearAgentDetails()

    def clearAgentDetails(self):
        # Clears the agent details editor
        self.agentDetailsEditor.nameEdit.clear()
        self.agentDetailsEditor.roleEdit.clear()
        self.agentDetailsEditor.goalEdit.clear()
        self.agentDetailsEditor.backstoryEdit.clear()

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "YAML Files (*.yaml *.yml)"
        )
        if filename:
            try:
                self.agentsData = YAMLFileHandler.readYAML(filename)
                self.currentFile = filename
                self.statusBar().showMessage(f"Opened {os.path.basename(filename)}")
                self.updateRoleFilter()
                self.populateAgentSelector()
            except yaml.YAMLError as e:
                QMessageBox.warning(self, "Error", f"Invalid YAML format: {e}")

    def populateAgentSelector(self):
        selected_role = self.roleFilterComboBox.currentData()
        self.agentSelector.blockSignals(True)
        self.agentSelector.clear()
        self.agentIndexMapping.clear()  # Reset the mapping

        for i, agent in enumerate(self.agentsData["agents"]):
            if selected_role is None or agent["role"] == selected_role:
                self.agentSelector.addItem(agent["name"])
                self.agentIndexMapping.append(i)  # Map comboBox index to actual agent index

        self.agentSelector.blockSignals(False)

        if self.agentSelector.count() > 0:
            self.agentSelector.setCurrentIndex(0)
            self.displayAgentDetails(0)
        else:
            self.clearAgentDetails()

    def displayAgentDetails(self, comboBoxIndex):
        if comboBoxIndex < 0 or comboBoxIndex >= len(self.agentIndexMapping):
            return

        actualIndex = self.agentIndexMapping[comboBoxIndex]  # Use the mapping
        self.selectedAgentIndex = actualIndex
        agent = self.agentsData["agents"][actualIndex]
        self.agentDetailsEditor.displayAgentDetails(agent)

    def updateRoleFilter(self):
        roles = set()
        for agent in self.agentsData.get("agents", []):
            roles.add(agent["role"])

        self.roleFilterComboBox.blockSignals(True)
        self.roleFilterComboBox.clear()
        self.roleFilterComboBox.addItem("All Roles", None)

        for role in sorted(roles):
            self.roleFilterComboBox.addItem(role, role)

        self.roleFilterComboBox.blockSignals(False)

    def updateAgentDataFromUI(self):
        # Update the current agent's data from the UI fields
        agent = self.agentsData["agents"][self.selectedAgentIndex]
        agent["name"] = self.agentDetailsEditor.nameEdit.text()
        agent["role"] = self.agentDetailsEditor.roleEdit.text()
        agent["goal"] = self.agentDetailsEditor.goalEdit.text()
        agent["backstory"] = self.agentDetailsEditor.backstoryEdit.toPlainText()

    def saveFile(self):
        if self.selectedAgentIndex is not None:
            self.updateAgentDataFromUI()

        if self.currentFile:
            try:
                YAMLFileHandler.writeYAML(self.agentsData, self.currentFile)
                self.statusBar().showMessage(
                    f"Saved {os.path.basename(self.currentFile)}"
                )
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error saving file: {e}")
        else:
            self.saveAsFile()

    def saveAsFile(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "YAML Files (*.yaml *.yml)"
        )
        if filename:
            YAMLFileHandler.writeYAML(self.agentsData, filename)
            self.currentFile = filename
            self.statusBar().showMessage(f"Saved as {os.path.basename(filename)}")

    def closeEvent(self, event):
        response = QMessageBox.question(
            self, "Exit", "Do you want to save changes before exiting?"
        )
        if response == QMessageBox.Yes:
            self.saveFile()
        event.accept()


def main():
    app = QApplication(sys.argv)
    system_style = QStyleFactory.create(QStyleFactory.keys()[0])
    app.setStyle(system_style)

    mainWin = AgentEditor()
    mainWin.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
