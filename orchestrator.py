from agents import ResearcherAgent, WriterAgent
from memory import ShortTermMemory, LongTermMemory
from dotenv import load_dotenv
load_dotenv()

class AIOrchestrator:
    def __init__(self):
        self.short_term_memory = ShortTermMemory()
        self.long_term_memory = LongTermMemory("user_memory.json")

        self.researcher_agent = ResearcherAgent(
            name="Explorer",
            role="Researcher in software topics, producing refined and technical summaries")
        
        self.writer_agent = WriterAgent(
            name="Writer",
            role="Technical presentations and content tailored to end-user needs")
    
    def run_task(self, user_input: str) -> str:
        l_memory_dict = self.long_term_memory.load()
        context = str(l_memory_dict)  
        research_output = self.researcher_agent.execute(user_input, context)
        final_output = self.writer_agent.execute(research_output, context)
        self.short_term_memory.save({"user": user_input, "assistant" : final_output})

        return final_output
    