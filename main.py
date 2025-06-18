import streamlit as st
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import hashlib
import networkx as nx
import matplotlib.pyplot as plt
import tempfile
import hashlib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import networkx as nx  # Added for Knowledge Graph
import os
from PIL import Image

# --- Define Core Classes ---

class DOMElementNode:
    def __init__(self, tag_name, xpath, attributes, parent=None):
        self.tag_name = tag_name
        self.xpath = xpath
        self.attributes = attributes
        self.parent = parent
        self.children = []
        self.highlight_index = None

# --- DOM Building ---

def generate_xpath(bs_elem):
    path = []
    while bs_elem and bs_elem.name:
        index = ''
        if bs_elem.parent:
            siblings = [s for s in bs_elem.parent.find_all(bs_elem.name, recursive=False)]
            if len(siblings) > 1:
                index = f"[{siblings.index(bs_elem)+1}]"
        path.insert(0, f"/{bs_elem.name}{index}")
        bs_elem = bs_elem.parent
    return ''.join(path)

def build_dom_tree(bs_node, parent=None):
    if not hasattr(bs_node, 'name') or bs_node.name is None:
        return None

    node = DOMElementNode(
        tag_name=bs_node.name,
        xpath=generate_xpath(bs_node),
        attributes=dict(bs_node.attrs),
        parent=parent
    )
    if parent:
        parent.children.append(node)

    for child in bs_node.children:
        build_dom_tree(child, parent=node)

    return node

# --- Knowledge Graph ---

def build_knowledge_graph_from_dom(root_node: DOMElementNode):
    G = nx.DiGraph()

    def recurse(node):
        node_id = node.xpath
        attrs = {f"attr_{k}": str(v) for k, v in node.attributes.items() if not isinstance(v, list)}
        G.add_node(node_id, tag=node.tag_name, **attrs)

        for child in node.children:
            child_id = child.xpath
            G.add_edge(node_id, child_id, relation="contains")
            recurse(child)

        if node.tag_name == "a" and "href" in node.attributes:
            href = node.attributes["href"]
            G.add_edge(node_id, href, relation="links_to")

    recurse(root_node)
    return G

# --- DOM Printer ---

def dom_tree_string(node, depth=0):
    if node is None:
        return ""
    lines = ["  " * depth + f"<{node.tag_name}>"]
    for child in node.children:
        lines.append(dom_tree_string(child, depth + 1))
    return "\n".join(lines)

# --- Streamlit App ---

st.title("🌐 DOM Knowledge Graph Generator")
url = st.text_input("Enter URL", "https://en.wikipedia.org/wiki/Swiggy")

if st.button("Generate Graph"):
    with st.spinner("Fetching and parsing the website..."):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        root_node = build_dom_tree(soup.body)
        dom_text = dom_tree_string(root_node)

        st.subheader("🧱 DOM Structure")
        st.code(dom_text, language="html")

        st.subheader("🧠 Knowledge Graph")
        KG = build_knowledge_graph_from_dom(root_node)

        fig, ax = plt.subplots(figsize=(12, 8))
        pos = nx.spring_layout(KG, k=0.5)
        nx.draw(KG, pos, with_labels=False, node_size=100, node_color="skyblue", edge_color="gray", arrows=True)
        nx.draw_networkx_labels(KG, pos, labels={n: d.get('tag', 'N/A') for n, d in KG.nodes(data=True)}, font_size=7)

        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        plt.savefig(tmpfile.name, dpi=300)
        plt.close(fig)

        image = Image.open(tmpfile.name)
        st.image(image, caption="DOM Knowledge Graph", use_column_width=True)

        os.unlink(tmpfile.name)

        st.success("Graph generation complete ✅")
