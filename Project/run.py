from app import create_app
from flask import render_template
from flask import Flask, request, jsonify
#from path_finder import calculate_route
from algorithms.path_finder2 import calculate_route_custom
from algorithms.trie import Trie
import json

app = create_app()

# Create and populate the Trie
trie = Trie()

# Load datasets from JSON files
with open('app/static/vegan.json') as f:
    vegan_data = json.load(f)
with open('app/static/halal.json') as f:
    halal_data = json.load(f)
with open('app/static/mrt.json') as f:
    mrt_data = json.load(f)

# Populate the Trie with restaurant names (Titles) from the dataset
# and mrt station name
for data in vegan_data:
    trie.insert(data["Title"])
for data in halal_data:
    trie.insert(data["Title"])
for data in mrt_data:
    trie.insert(data["STN_NAME"])

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/map')
def map_view():
    return render_template('map.html')

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    results = trie.search(query)
    return jsonify(results)

@app.route('/api/get_route', methods=['POST'])
def get_route():
    data = request.json
    start = data['start']
    end = data['end']
    path_coords = calculate_route_custom(start, end)
    return jsonify({'path': path_coords})


if __name__ == '__main__':
    app.run(debug=True)
