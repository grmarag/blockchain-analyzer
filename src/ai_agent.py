from openai import OpenAI
from src.config import Config

class AIAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
        self.client = OpenAI(api_key=self.api_key)

    def generate_insight_report(self, summary: str) -> str:
        """Generate a detailed insight report using OpenAI's API."""
        prompt = (
            f"Based on the blockchain analysis results provided below, generate a comprehensive report that includes the following sections:\n\n"
            f"1. Clustering & Address Profiling:\n"
            f"   - Describe transaction behavior patterns, such as frequent transactors, large-value movers, and inactive accounts.\n"
            f"   - Specify the clustering algorithms used (e.g., HDBSCAN or KMeans) and provide insights into their outcomes.\n\n"
            f"2. Anomaly Detection:\n"
            f"   - Identify outliers, including abnormally high-value transfers and sudden spikes in activity.\n"
            f"   - Detail the methods used, such as machine learning models (Isolation Forest, Local Outlier Factor) and statistical methods.\n\n"
            f"3. Network Analysis:\n"
            f"   - Analyze the constructed transaction graph by discussing network properties like centrality and connected components.\n"
            f"   - Identify potential hubs or influential addresses.\n\n"
            f"Additionally, please include sections that explain the methodology, the findings, and any assumptions made during the analysis.\n\n"
            f"Results Summary:\n{summary}\n"
        )
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert in blockchain analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0
            )
            report = response.choices[0].message.content.strip()
            return report
        except Exception as e:
            return f"Error generating report: {e}"