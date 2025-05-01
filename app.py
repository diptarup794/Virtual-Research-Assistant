import os
from flask import Flask, render_template, request, jsonify, abort
from dotenv import load_dotenv
from agents import ResearchAgents  # Assuming these are in the same directory
from data_loader import DataLoader # Assuming these are in the same directory

load_dotenv()

app = Flask(__name__)

# Retrieve the API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")

# Check if API key is set, else raise an error during startup
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing. Please set it in your .env file.")

# Initialize AI Agents and DataLoader (outside request context for efficiency)
try:
    agents = ResearchAgents(groq_api_key)
    data_loader = DataLoader()
except Exception as e:
    # Handle potential initialization errors (e.g., invalid API key format)
    print(f"Error initializing agents or data loader: {e}")
    # Depending on the severity, you might want to exit or handle differently
    agents = None
    data_loader = None

@app.route('/')
def index():
    """Renders the main HTML page."""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Handles the search request from the frontend."""
    if not agents or not data_loader:
         return jsonify({"error": "Server components not initialized correctly."}), 500

    query = request.json.get('query')
    if not query:
        return jsonify({"error": "Search query is missing."}), 400

    try:
        # Fetch research papers (only ArXiv for now, as per original logic)
        # You might want to add Google Scholar fetching here later if needed
        # e.g., google_papers = data_loader.fetch_google_scholar_papers(query)
        # all_papers = arxiv_papers + google_papers
        arxiv_papers = data_loader.fetch_arxiv_papers(query)
        all_papers = arxiv_papers # Keep consistency with the original app logic

        if not all_papers:
            return jsonify({"papers": [], "message": "No papers found for this topic."})

        processed_papers = []
        # Process each paper: generate summary and analyze advantages/disadvantages
        for paper in all_papers:
            # Ensure paper dictionary has expected keys
            if 'summary' not in paper or 'title' not in paper or 'link' not in paper:
                 print(f"Skipping paper due to missing keys: {paper.get('title', 'N/A')}")
                 continue # Skip this paper if essential data is missing

            try:
                summary = agents.summarize_paper(paper['summary'])
                adv_dis = agents.analyze_advantages_disadvantages(summary)

                processed_papers.append({
                    "title": paper["title"],
                    "link": paper["link"],
                    "summary": summary,
                    "advantages_disadvantages": adv_dis,
                })
            except Exception as e:
                print(f"Error processing paper '{paper.get('title', 'N/A')}': {e}")
                # Optionally append an error message for this specific paper
                processed_papers.append({
                    "title": paper["title"],
                    "link": paper["link"],
                    "error": f"Could not process this paper: {e}"
                })


        return jsonify({"papers": processed_papers})

    except Exception as e:
        print(f"An error occurred during search: {e}") # Log the error server-side
        # Consider logging traceback for debugging: import traceback; traceback.print_exc()
        return jsonify({"error": f"An internal server error occurred: {e}"}), 500

if __name__ == '__main__':
    # Use debug=True only for development
    # Run on a different port if 5000 is in use (e.g., by Streamlit)
   app.run(debug=True, port=5001, use_reloader=False)