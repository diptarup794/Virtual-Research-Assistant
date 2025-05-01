import os
from autogen import AssistantAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ResearchAgents:
    def __init__(self, api_key):
        self.groq_api_key = api_key
        # Ensure the model name is correct and supported by Groq
        self.llm_config = {'config_list': [{'model': 'llama3-70b-8192', 'api_key': self.groq_api_key, 'api_type': "groq"}]} # Example: using llama3

        # Summarizer Agent - Summarizes research papers
        self.summarizer_agent = AssistantAgent(
            name="summarizer_agent",
            system_message="Summarize the retrieved research papers and present concise summaries to the user. Focus ONLY on the relevant summaries of the research paper, excluding any introductory phrases or thought processes.",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

        # Advantages and Disadvantages Agent - Analyzes pros and cons
        self.advantages_disadvantages_agent = AssistantAgent(
            name="advantages_disadvantages_agent",
            system_message="Analyze the summaries of the research papers and provide a list of advantages and disadvantages for each paper in a clear, pointwise format. Output ONLY the advantages and disadvantages, without any conversational text or thought process.",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

    def summarize_paper(self, paper_summary):
        """Generates a summary of the research paper."""
        summary_response = self.summarizer_agent.generate_reply(
            messages=[{"role": "user", "content": f"Summarize this paper abstract: {paper_summary}"}]
        )
        # Extract content safely, handling potential non-dict responses
        return summary_response.get("content", "Summarization failed!") if isinstance(summary_response, dict) else str(summary_response)

    def analyze_advantages_disadvantages(self, summary):
        """Generates advantages and disadvantages of the research paper based on its summary."""
        adv_dis_response = self.advantages_disadvantages_agent.generate_reply(
            messages=[{"role": "user", "content": f"Provide advantages and disadvantages in pointwise format for this paper summary: {summary}"}]
        )
        # Extract content safely
        return adv_dis_response.get("content", "Advantages and disadvantages analysis failed!") if isinstance(adv_dis_response, dict) else str(adv_dis_response)
