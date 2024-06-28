from flask import Flask, render_template, request, jsonify
import re
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend')

# Step 1: Define Stop Words
STOP_WORDS = """
a about above after again against all am an and any are aren't as at be because been before being below between both but by can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor not of off on once only or other ought our ours ourselves out over own same shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them themselves then there there's these they they'd they'll they're they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's which while who who's whom why why's with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves
""".split()

# Step 2: Tokenize Text
def tokenize_text(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    words = [re.findall(r'\w+', sentence.lower()) for sentence in sentences]
    return sentences, words

# Step 3: Compute TF-IDF Scores
def compute_tfidf(sentences):
    vectorizer = TfidfVectorizer(stop_words=STOP_WORDS)
    tfidf_matrix = vectorizer.fit_transform(sentences)
    return tfidf_matrix

# Step 4: Build Similarity Matrix using TextRank
def build_similarity_matrix(sentences, tfidf_matrix):
    similarity_matrix = cosine_similarity(tfidf_matrix)
    nx_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(nx_graph)
    return scores

# Step 5: Select Top Sentences
def summarize(text, num_sentences=5):
    if not text:
        return "Input text is empty."
    
    sentences, _ = tokenize_text(text)
    num_sentences = min(num_sentences, len(sentences))
    
    tfidf_matrix = compute_tfidf(sentences)
    scores = build_similarity_matrix(sentences, tfidf_matrix)
    
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    
    # Ensure that first and last sentences are always included if they exist
    first_sentence_idx = 0
    last_sentence_idx = len(sentences) - 1 if len(sentences) > 1 else None
    
    selected_indices = set()
    if last_sentence_idx is not None:
        selected_indices.add(first_sentence_idx)
        selected_indices.add(last_sentence_idx)
    
    # Add the highest-ranked sentences to the summary
    for _, sentence in ranked_sentences:
        idx = sentences.index(sentence)
        if len(selected_indices) >= num_sentences:
            break
        selected_indices.add(idx)
    
    # Sort the selected indices to maintain the order of sentences
    selected_indices = sorted(selected_indices)
    
    # Form the summary
    summary = ' '.join(sentences[i] for i in selected_indices)
    return summary

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarizer():
    text = request.form['input']
    num_sentences = int(request.form.get('num_sentences', 4))  # Default to 5 sentences if not specified

    if not text:
        return jsonify({'error': 'Input text is empty.'})

    summary = summarize(text, num_sentences)
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)