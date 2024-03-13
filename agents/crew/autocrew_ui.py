from autocrew import (
    CrewManager,
    AgentInitializer,
    TaskManager,
    ConfigInitializer,
    LLMFactory,
    LLMConfigurator,
)
from crewai import Agent
from crewai.process import Process
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QInputDialog,
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import os
import random
import sys
import yaml


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.setup_connections()
        self.current_yaml_data = None

    def load_ui(self):
        loader = QUiLoader()
        file = QFile("autocrew.ui")
        file.open(QIODevice.ReadOnly)
        self.ui = loader.load(file, self)
        file.close()

    def setup_connections(self):
        self.ui.addTaskButton.clicked.connect(self.add_task)
        self.ui.editTaskButton.clicked.connect(self.edit_task)
        self.ui.removeTaskButton.clicked.connect(self.remove_task)
        self.ui.openButton.clicked.connect(self.open_file)
        self.ui.saveButton.clicked.connect(self.save_file)
        self.ui.startJobButton.clicked.connect(self.start_job)

    def add_task(self):
        task, ok = QInputDialog.getText(self, "Add Task", "Enter task description:")
        if ok and task:
            self.ui.tasksListWidget.addItem(task)
            self.current_yaml_data["task_descriptions"].append(task)

    def edit_task(self):
        selected_item = self.ui.tasksListWidget.currentItem()
        if selected_item:
            task, ok = QInputDialog.getText(
                self, "Edit Task", "Edit task description:", text=selected_item.text()
            )
            if ok and task:
                selected_item.setText(task)
                index = self.ui.tasksListWidget.row(selected_item)
                self.current_yaml_data["task_descriptions"][index] = task

    def remove_task(self):
        selected_item = self.ui.tasksListWidget.currentItem()
        if selected_item:
            index = self.ui.tasksListWidget.row(selected_item)
            del self.current_yaml_data["task_descriptions"][index]
            self.ui.tasksListWidget.takeItem(index)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "YAML Files (*.yaml)"
        )
        if filename:
            with open(filename, "r") as file:
                self.current_yaml_data = yaml.safe_load(file)
                self.ui.ceoMissionLineEdit.setText(
                    self.current_yaml_data.get("ceo_mission", "")
                )
                self.ui.tasksListWidget.clear()
                for task in self.current_yaml_data.get("task_descriptions", []):
                    self.ui.tasksListWidget.addItem(task)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "YAML Files (*.yaml)"
        )
        if filename:
            self.current_yaml_data["ceo_mission"] = self.ui.ceoMissionLineEdit.text()
            with open(filename, "w") as file:
                yaml.dump(self.current_yaml_data, file)

    def start_job(self):
        # Collect data from UI
        ceo_mission = self.ui.ceoMissionLineEdit.text()
        tasks = [
            self.ui.tasksListWidget.item(i).text()
            for i in range(self.ui.tasksListWidget.count())
        ]

        # Prepare and execute the application logic
        config, agents_config = ConfigInitializer.initialize()
        # Initialize LLMs
        llm_factory = LLMFactory()
        llm_configurator = LLMConfigurator(config)

        openai_fast = llm_configurator.configure_openai_llm(
            llm_factory, "gpt-3.5-turbo-1106", 0.7
        )
        openai_smart = llm_configurator.configure_openai_llm(
            llm_factory, "gpt-4-1106-preview", 0.5
        )
        openai_long = llm_configurator.configure_openai_llm(
            llm_factory, "gpt-3.5-turbo-16k", 0.9
        )

        tgi_accurate = llm_configurator.configure_tgi_llm(llm_factory, 0.5)
        tgi_balanced = llm_configurator.configure_tgi_llm(llm_factory, 0.7)
        tgi_creative = llm_configurator.configure_tgi_llm(llm_factory, 0.9)
        
        # Select LLMs for agents
        ceo_llm = openai_smart
        subordinate_llm = openai_fast

        # Define agent tools
        ddg_search = DuckDuckGoSearchRun()
        wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

        # Initialize agents and tasks
        ceo_config = next(
            agent for agent in agents_config["agents"] if agent["name"] == "CEO"
        )
        ceo = Agent(
            role=ceo_config["role"],
            goal=ceo_config["goal"],
            backstory=ceo_config["backstory"],
            verbose=True,
            llm=ceo_llm,
            allow_delegation=True,
        )
        subordinate_agents = AgentInitializer.initialize(agents_config, subordinate_llm)
        task_manager = TaskManager()
        mission = task_manager.create_task(ceo_mission, ceo, [wikipedia, ddg_search])
        tasks_with_names = [{"task": mission, "agent_name": "CEO"}]

        for desc in tasks:
            selected_agent, agent_name = task_manager.select_agent_for_task(
                desc, subordinate_agents, agents_config
            )
            task = task_manager.create_task(
                desc, selected_agent, [wikipedia, ddg_search]
            )
            tasks_with_names.append({"task": task, "agent_name": agent_name})

        # Create and kickoff the crew
        crew_manager = CrewManager(
            "Creation Crew",
            "A crew of AI agents that can produce.",
            [ceo] + subordinate_agents,
            Process.sequential,
        )
        attributed_results = crew_manager.kickoff_with_attribution(tasks_with_names)

        # Handle the results
        result_text = "\n".join(
            [
                f"Agent Name: {result['agent_name']}\nResult: {result['result']}"
                for result in attributed_results
            ]
        )
        QMessageBox.information(self, "Results", result_text)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
