import re
from googlesearch import search
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import requests
import random
from time import sleep
import time
from flask import Flask, request, render_template, jsonify
from docx import Document

app = Flask(__name__)

''' REQUIREMENTS '''
#  Under CMD
# pip install python-docx  googlesearch-python requests
# run application python app.py
# Make sure TXT file does not have any spaces in the new line



def perform_google_search(phrases):
    search_results = []
    
    for phrase in phrases:
        query = phrase

        matched_urls = []

        # Perform the Google search and limit the number of results to 5
        for url in search(query, num_results=5):
            matched_urls.append(url)
            time.sleep(2)

        # import pdb;pdb.set_trace()
        if matched_urls:
            search_results.extend(matched_urls)
            break
        else:
            print(f"No matched URL for '{phrase}'")

    return search_results


# Extract random phrases from file content
def extract_phrases(file_content):
    words = re.findall(r'\b\w+\b', file_content)
    phrases = []
    while len(phrases) < 5:
        start_index = random.randint(0, len(words) - 6)
        phrase = ' '.join(words[start_index: start_index + 5])
        phrases.append(phrase)
    return phrases


# Load the content of a web page using Beautiful Soup and return elements
def load_page_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    page_content = soup.get_text()
    return page_content


# Compare content and calculate similarity score
def compare_content(file_content, search_results):
    similarity_score = 0

    for url in search_results:
        page_content = load_page_content(url)

        # Use difflib.SequenceMatcher to calculate similarity score
        matcher = SequenceMatcher(None, file_content, page_content)
        similarity_score += matcher.ratio()

    similarity_score /= len(search_results)  # Average similarity score
    similarity_score *= 100  # Convert similarity score to a percentage

    return similarity_score


# Home page
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_content = ""

    if file.filename.endswith('.docx'):
        doc = Document(file)
        paragraphs = [p.text for p in doc.paragraphs]
        file_content = ' '.join(paragraphs)
    else:
        # Assume it's a text file
        encodings = ['utf-8', 'latin-1']  # List of encodings to try

        for encoding in encodings:
            try:
                file_content = file.read().decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            # None of the encodings worked
            return jsonify({'error': 'Unable to decode the file.'})

    # Extract words from the file content
    phrases = extract_phrases(file_content)

    # Perform Google search for the extracted words
    search_results = perform_google_search(phrases)

    # Compare content and calculate similarity score
    similarity_score = compare_content(file_content, search_results)

    results = {
        'words': phrases,
        'similarity_score': similarity_score,
        'search_results': search_results
    }

    return jsonify(results)
if __name__ == '__main__':
    app.run()
