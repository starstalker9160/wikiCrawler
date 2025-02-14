import time
import requests
import networkx as nx
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from urllib.parse import urljoin


def get_wikipedia_links(article_url):
    """Scrapes internal English Wikipedia links from a given article."""
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/wiki/') and not ':' in href:
            full_url = urljoin("https://en.wikipedia.org", href)
            links.add(full_url)
    return links


def build_graph(start_url, depth=2):
    """Builds a graph of English Wikipedia articles and their links."""
    G = nx.DiGraph()
    queue = [(start_url, 0)]
    visited = set()
    
    while queue:
        url, level = queue.pop(0)
        if url in visited or level > depth:
            continue
        
        visited.add(url)
        G.add_node(url)
        print(f"Scraping: {url}")
        
        try:
            links = get_wikipedia_links(url)
            for link in links:
                G.add_edge(url, link)
                queue.append((link, level + 1))
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        
        time.sleep(1)
    
    return G


def visualize_graph(G):
    """Visualizes the graph using matplotlib."""
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.3)
    nx.draw(G, pos, with_labels=False, node_size=50, edge_color='gray')
    plt.title("Wikipedia Article Network")
    plt.show()


start_url = "https://en.wikipedia.org/wiki/Philosophy"
graph = build_graph(start_url, depth=2)
visualize_graph(graph)
