import requests
import xml.etree.ElementTree as ET
# from scholarly import scholarly, ProxyGenerator # Remove this line

# Optional: Configure proxy for scholarly if needed
# pg = ProxyGenerator() # Remove this line
# pg.FreeProxies() # Or configure your own proxies # Remove this line
# scholarly.use_proxy(pg) # Remove this line

class DataLoader:
    def __init__(self):
        # No need for search_agent initialization here unless expanding search
        print("DataLoader Initialized")

    def fetch_arxiv_papers(self, query, max_results=5):
        """
        Fetches research papers from ArXiv based on the user query.
        Returns:
            list: A list of dictionaries containing paper details (title, summary, link).
        """
        papers = []
        try:
            # URL encode the query to handle special characters
            encoded_query = requests.utils.quote(query)
            url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}"
            response = requests.get(url, timeout=10) # Add timeout
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

            root = ET.fromstring(response.text)
            atom_ns = "{http://www.w3.org/2005/Atom}" # Namespace for Atom feed

            for entry in root.findall(f"{atom_ns}entry"):
                title = entry.find(f"{atom_ns}title").text.strip()
                summary = entry.find(f"{atom_ns}summary").text.strip()
                # Link often points to the abstract page, which is usually preferred
                link = entry.find(f"{atom_ns}id").text.strip()
                # Sometimes a PDF link is available directly
                pdf_link_element = entry.find(f"{atom_ns}link[@title='pdf']")
                if pdf_link_element is not None:
                    link = pdf_link_element.get('href')

                papers.append({
                    "title": title,
                    "summary": summary,
                    "link": link
                })
        except requests.exceptions.RequestException as e:
            print(f"Error fetching ArXiv papers: {e}")
        except ET.ParseError as e:
            print(f"Error parsing ArXiv XML response: {e}")
        except Exception as e:
            print(f"An unexpected error occurred fetching ArXiv papers: {e}")

        return papers

    # Remove the entire fetch_google_scholar_papers method
    # def fetch_google_scholar_papers(self, query, max_results=5):
    #     """
    #     Fetches research papers from Google Scholar.
    #     Returns:
    #         list: A list of dictionaries containing paper details (title, summary, link)
    #     """
    #     papers = []
    #     try:
    #         print(f"Searching Google Scholar for: {query}")
    #         search_results = scholarly.search_pubs(query)
    #
    #         for i, paper in enumerate(search_results):
    #             if i >= max_results:
    #                 break
    #             # Extract details safely using .get()
    #             bib = paper.get('bib', {})
    #             title = bib.get('title', 'No Title Available')
    #             summary = bib.get('abstract', 'No Summary Available')
    #             # Prioritize 'pub_url', fallback to 'eprint_url' or provide a default message
    #             link = paper.get('pub_url', paper.get('eprint_url', 'No Link Available'))
    #
    #             print(f"Found Scholar Paper {i+1}: {title}")
    #             papers.append({
    #                 "title": title,
    #                 "summary": summary,
    #                 "link": link
    #             })
    #     except Exception as e:
    #         # Catch potential errors from scholarly (rate limits, proxy issues, etc.)
    #         print(f"Error fetching Google Scholar papers: {e}")
    #         # Depending on the error, you might want to inform the user or retry
    #
    #     return papers
