import os
import random
import yaml
import time
from crewai import Task, Crew, Agent
from crewai.process import Process
from langchain_community.llms import HuggingFaceTextGenInference
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_openai import ChatOpenAI


class ConfigLoader:
    """Class to load and manage configuration from YAML files."""

    @staticmethod
    def load(file_path):
        with open(file_path, "r") as file:
            return yaml.safe_load(file)


class ConfigInitializer:
    """Class to handle the initialization of configuration."""

    @staticmethod
    def initialize():
        # Load the main configuration file
        main_config = ConfigLoader.load("config.yaml")
        # Load additional configuration file specified in the main configuration
        agents_config = ConfigLoader.load(main_config["agent_file"])
        return main_config, agents_config


class LLMFactory:
    """Factory class to create LLM instances."""

    @staticmethod
    def openai_llm(model_name, temperature, api_key):
        return ChatOpenAI(
            model_name=model_name, temperature=temperature, openai_api_key=api_key
        )

    @staticmethod
    def tgi_llm(tgi_url, temperature):
        return HuggingFaceTextGenInference(
            inference_server_url=tgi_url,
            top_k=10,
            top_p=0.95,
            typical_p=0.95,
            temperature=temperature,
            repetition_penalty=1.03,
        )


class LLMConfigurator:
    """Configurator class to setup LLM endpoints."""

    def __init__(self, config):
        self.config = config

    def configure_openai_llm(self, llm_factory, model_name, temperature):
        openai_api_key = self.config["openai_api_key"]
        return llm_factory.openai_llm(model_name, temperature, openai_api_key)

    def configure_tgi_llm(self, llm_factory, temperature):
        tgi_urls = random.choice(self.config["tgi_llm_urls"])
        tgi_url = os.environ.get("TGI_URL", tgi_urls["url"])
        return llm_factory.tgi_llm(tgi_url, temperature)


class AgentInitializer:
    """Class to initialize agents based on configuration."""

    @staticmethod
    def initialize(agents_config, llm):
        agents = []
        for agent_conf in agents_config["agents"]:
            agent = Agent(
                name=agent_conf.get("name", "Unnamed Agent"),
                role=agent_conf["role"],
                goal=agent_conf["goal"],
                backstory=agent_conf["backstory"],
                verbose=True,
                llm=llm,
                allow_delegation=False,
            )
            agents.append(agent)
        return agents


class TaskManager:
    """Class to manage task creation and agent assignment."""

    @staticmethod
    def create_task(description, agent, tools):
        return Task(description=description, agent=agent, tools=tools)

    @staticmethod
    def select_agent_for_task(task_description, agents, agents_config):
        task_keywords = task_description.split()
        best_match = None
        best_score = 0
        best_match_name = "Unknown Agent"

        for agent_conf in agents_config["agents"]:
            score = sum(
                1
                for word in task_keywords
                if word in agent_conf["role"] or word in agent_conf["goal"]
            )
            if score > best_score:
                best_match_name = agent_conf["name"]
                best_match = next(
                    (
                        agent
                        for agent in agents
                        if agent.role == agent_conf["role"]
                        and agent.goal == agent_conf["goal"]
                    ),
                    None,
                )
                best_score = score

        return (
            best_match if best_match else agents[0],
            best_match_name if best_match else "Unknown Agent",
        )


class CrewManager:
    """Class to manage the crew setup and execution."""

    def __init__(self, name, description, agents, process):
        self.crew = Crew(
            name=name, description=description, agents=agents, process=process
        )

    def kickoff_with_attribution(self, tasks_with_names):
        self.crew.tasks = [item["task"] for item in tasks_with_names]
        results = self.crew.kickoff()
        attributed_results = []

        for task_with_name, result in zip(tasks_with_names, results):
            attributed_results.append(
                {
                    "task_description": task_with_name["task"].description,
                    "agent": task_with_name["task"].agent,
                    "agent_name": task_with_name["agent_name"],
                    "result": result,
                }
            )

        return attributed_results


def current_timestamp():
    """Return the current timestamp."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def main():
    # Initialize configuration
    config, agents_config = ConfigInitializer.initialize()
    # Load tasks
    tasks_config = ConfigLoader.load(config["task_file"])
    task_descriptions = tasks_config["task_descriptions"]
    ceo_mission = tasks_config["ceo_mission"]
    print(f"===> Starting time: {current_timestamp()}")

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

    # Initialize agents
    agent_initializer = AgentInitializer()
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
    subordinate_agents = agent_initializer.initialize(agents_config, subordinate_llm)

    # Define tasks
    task_manager = TaskManager()
    mission = task_manager.create_task(ceo_mission, ceo, [wikipedia, ddg_search])
    tasks_with_names = [{"task": mission, "agent_name": "CEO"}]

    for desc in task_descriptions:
        selected_agent, agent_name = task_manager.select_agent_for_task(
            desc, subordinate_agents, agents_config
        )
        task = task_manager.create_task(desc, selected_agent, [wikipedia, ddg_search])
        tasks_with_names.append({"task": task, "agent_name": agent_name})

    # Create and kickoff the crew
    crew_manager = CrewManager(
        "Creation Crew",
        "A crew of AI agents that can produce.",
        [ceo] + subordinate_agents,
        Process.sequential,
    )
    attributed_results = crew_manager.kickoff_with_attribution(tasks_with_names)

    # Display results with improved formatting
    print("\n######### Finish time: " + current_timestamp() + " #############\n")
    for result in attributed_results:
        agent_name = result["agent_name"]
        llm_name = getattr(
            getattr(result["agent"], "llm", None), "model_name", "Unknown LLM"
        )
        agent_role = getattr(result["agent"], "role", "Unknown Role")
        task_description = result["task_description"]
        task_result = result["result"]

        print(f"Task Description: {task_description}\n"
              f"Agent Name: {agent_name}\n"
              f"Agent Role: {agent_role}\n"
              f"LLM Used: {llm_name}\n"
              f"Task Result:\n{task_result}\n"
              f"{'-'*60}\n")


if __name__ == "__main__":
    main()
