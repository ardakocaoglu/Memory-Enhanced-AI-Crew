from google import genai
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()

class BaseAgent(ABC):
    """
    BaseAgent is an abstract class that defines the structure for all agents in the system.
    Each agent must have a name, a role to define its purpose, and an execute method to perform tasks based on input and context.
    """
    @abstractmethod
    def __init__(self, name:str, role: str):
        self.name = name
        self.role = role
        #gemini api configuration
        #genai.configure(api_key=api_key)
        #with google genai sdk, we can directly create a model instance without needing to specify the model name in the configuration
        self.client = genai.Client()

        self.model_name = "gemini-2.5-flash"

    def execute(self, task_input: str, context: str = "") -> str:
        """
        Executes a task based on the provided input and context.
        This method should be implemented by all subclasses to define specific behaviors.
        """
        pass


class ResearcherAgent(BaseAgent):
    """ResearcherAgent is responsible for gathering information and conducting research based on the given task input and context."""
    def __init__(self, name: str, role: str):
        super().__init__(name, role)

    def execute(self, task_input: str, context: str = "") -> str:
        # Implement the logic for the ResearcherAgent to perform research and return findings
        system_prompt = f"You are a {self.role}. Your role is to gather information and conduct research based on the given task input and context. Use the following context to inform your research: {context}"

        full_prompt = system_prompt + f"\n\nTask Input: {task_input}\n\nPlease provide your research findings based on the task input and context."

        response = self.client.models.generate_content(model = self.model_name, contents = full_prompt)

        return response.text

class WriterAgent(BaseAgent):
    """WriterAgent is responsible for creating and editing written content based on the given task input and context."""
    def __init__(self, name: str, role: str):
        super().__init__(name, role)


    def execute(self, task_input: str, context: str = "") -> str:
        # Implement the logic for the WriterAgent to create or edit content and return the result
        system_prompt = f"You are a {self.role}. Your role is to create and edit written content based on the given task input and context. Use the following context to inform your writing: {context}"

        full_prompt = system_prompt + f"\n\nTask Input: {task_input}\n\nPlease provide your written content based on the task input and context."

        response = self.client.models.generate_content(model = self.model_name, contents = full_prompt)
        return response.text
    