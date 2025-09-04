from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from algorithms.dijkstra import dijkstra
from algorithms.quickSortFilter import quick_sort_filter
from algorithms.sequential_search import sequential_search
from .models import UserReview
from . import db
import pandas as pd
import json
import osmnx as ox
import networkx as nx

main = Blueprint('main', __name__)

@main.route('/location', methods=['POST'])
def location():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    response = {
        'latitude': latitude,
        'longitude': longitude,
        'message': 'Location received successfully!'
    }
    return jsonify(response)

@main.route('/api/get_route', methods=['POST'])
def get_route():
    data = request.json
    start = data['start']
    end = data['end']
    
    try:
        path_coords = calculate_route(start, end)
        return jsonify({'path': path_coords})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def calculate_route(start_coords, end_coords):
    G = ox.graph_from_point(start_coords, dist=1000, network_type='walk')
    orig_node = ox.nearest_nodes(G, start_coords[1], start_coords[0])
    dest_node = ox.nearest_nodes(G, end_coords[1], end_coords[0])
    shortest_path = nx.shortest_path(G, orig_node, dest_node, weight='length')
    path_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_path]
    return path_coords

@main.route('/addReview', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        title = request.form['title']
        rating = float(request.form['rating'])
        type_of_food = request.form['category']

        # Save the new review in the database
        new_review = UserReview(title=title, rating=rating, type_of_food=type_of_food)
        db.session.add(new_review)
        db.session.commit()

        flash('Review added successfully!', 'success')
        return redirect(url_for('main.add_review'))
    
    return render_template('addReview.html')

@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/filter', methods=['POST'])
def filter():
    rating = float(request.form['rating'])
    dataset_choice = request.form['dataset']
    file_path, encoding, dataset_name, image_url = get_dataset_info(dataset_choice)
    
    data = pd.read_csv(file_path, encoding=encoding)
    data['Numerical Rating'] = data['Rating'].str.extract(r'(\d\.\d)').astype(float)
    sorted_data = quick_sort_filter(data, 'Numerical Rating')
    
    min_rating = rating
    max_rating = rating + 0.5
    filtered_data = sorted_data[(sorted_data['Numerical Rating'] >= min_rating) & (sorted_data['Numerical Rating'] <= max_rating)]
    results = filtered_data.to_dict(orient='records')

    return render_template('filter.html', results=results, dataset_name=dataset_name, image_url=image_url)

def get_dataset_info(dataset_choice):
    if dataset_choice == 'halal':
        return (
            'Datasets/halal.csv',
            'utf-8',
            'Halal Food',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/800px-Good_Food_Display_-_NCI_Visuals_Online.jpg'
        )
    else:
        return (
            'Datasets/veganRestaurant.csv',
            'ISO-8859-1',
            'Vegan Food',
            'https://images.everydayhealth.com/images/diet-nutrition/what-is-a-vegan-diet-benefits-food-list-beginners-guide-alt-1440x810.jpg?sfvrsn=1d260c85_1'
        )

@main.route('/calculate_distances', methods=['POST'])
def calculate_distances():
    data = request.get_json()
    nodes = data['nodes']
    edges = data['edges']
    source_index = data['source']
    source = nodes[source_index]

    distances = dijkstra(source_index, edges)

    return jsonify(distances)

@main.route('/reviews/<dataset_type>')
def view_reviews(dataset_type):
    try:
        file_path, encoding = get_dataset_file_path_and_encoding(dataset_type)
        data_coords = pd.read_csv(file_path, encoding=encoding)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return "Error loading data", 500

    page = request.args.get('page', 1, type=int)
    reviews_per_page = 20
    reviews, total_pages = aggregate_reviews(data_coords, dataset_type, page, reviews_per_page)

    dataset_name = "Halal Food" if dataset_type == "halal" else "Vegan Food"
    
    return render_template('reviews.html', dataset_name=dataset_name, dataset_type=dataset_type, reviews_dict=reviews, page=page, total_pages=total_pages, max=max, min=min)

def get_dataset_file_path_and_encoding(dataset_type):
    if dataset_type == 'halal':
        return 'Datasets/halal.csv', 'utf-8'
    elif dataset_type == 'vegan':
        return 'Datasets/veganRestaurant.csv', 'Windows-1252'
    else:
        raise ValueError(f"Unknown dataset type: {dataset_type}")

def aggregate_reviews(data, dataset_type, page=1, reviews_per_page=5):
    reviews_dict = {}
    for index, row in data.iterrows():
        title = row['Title']
        rating_info = row['Rating']

        if dataset_type == 'vegan' and row['Food Court'] != "Yes":
            continue
        if dataset_type == 'halal' and row['Halal'] != "Yes":
            continue

        if pd.notna(rating_info) and "reviews" in rating_info:
            rating = float(rating_info.split("/")[0])
            review_count = int(rating_info.split("(")[1].split(" ")[0])
        else:
            continue

        reviews_dict[title] = {
            'total_rating': rating * review_count,
            'review_count': review_count,
            'reviews': [f'{rating}/5.0 ({review_count} reviews)']
        }

        # Fetch user reviews from the database
        user_reviews = UserReview.query.filter_by(type_of_food=dataset_type).all()

    for review in user_reviews:
        title = review.title
        rating = review.rating

        if title in reviews_dict:
            reviews_dict[title]['total_rating'] += rating
            reviews_dict[title]['review_count'] += 1
            reviews_dict[title]['reviews'].append(f'{rating}/5.0')
        else:
            reviews_dict[title] = {
                'total_rating': rating,
                'review_count': 1,
                'reviews': [f'{rating}/5.0']
            }

    for title in reviews_dict:
        total_rating = reviews_dict[title]['total_rating']
        review_count = reviews_dict[title]['review_count']
        reviews_dict[title]['average_rating'] = round(total_rating / review_count, 2) if review_count > 0 else 0

    sorted_reviews_dict = dict(sorted(reviews_dict.items(), key=lambda item: (item[1]['average_rating'], item[1]['review_count']), reverse=True))
    total_reviews = len(sorted_reviews_dict)
    total_pages = (total_reviews + reviews_per_page - 1) // reviews_per_page
    start = (page - 1) * reviews_per_page
    end = start + reviews_per_page

    paginated_reviews = dict(list(sorted_reviews_dict.items())[start:end])

    return paginated_reviews, total_pages

@main.route('/search_reviews', methods=['GET'])
def search_reviews():
    search_term = request.args.get('term', '')
    dataset_type = request.args.get('dataset', 'halal')
    page = request.args.get('page', 1, type=int)
    reviews_per_page = 20

    try:
        file_path, encoding = get_dataset_file_path_and_encoding(dataset_type)
        data_coords = pd.read_csv(file_path, encoding=encoding)
        
        data_dict = data_coords.to_dict(orient='records')
        csv_results = sequential_search(data_dict, search_term)

        user_reviews = UserReview.query.filter_by(type_of_food=dataset_type).all()
        db_results = []
        for review in user_reviews:
            if search_term.lower() in review.title.lower():
                db_results.append({
                    'Title': review.title,
                    'Rating': f'{review.rating}/5.0 (1 reviews)'
                })

        combined_results = csv_results + db_results

        reviews_dict = {}
        for item in combined_results:
            title = item['Title']
            rating_info = item['Rating']
            if pd.notna(rating_info) and "reviews" in rating_info:
                rating = float(rating_info.split("/")[0])
                review_count = int(rating_info.split("(")[1].split(" ")[0])
            else:
                continue

            if title in reviews_dict:
                reviews_dict[title]['total_rating'] += rating * review_count
                reviews_dict[title]['review_count'] += review_count
                reviews_dict[title]['reviews'].append(rating_info)
            else:
                reviews_dict[title] = {
                    'total_rating': rating * review_count,
                    'review_count': review_count,
                    'reviews': [rating_info]
                }

        for title in reviews_dict:
            total_rating = reviews_dict[title]['total_rating']
            review_count = reviews_dict[title]['review_count']
            reviews_dict[title]['average_rating'] = round(total_rating / review_count, 2) if review_count > 0 else 0

        sorted_reviews_dict = dict(sorted(reviews_dict.items(), key=lambda item: (item[1]['average_rating'], item[1]['review_count']), reverse=True))

        total_reviews = len(sorted_reviews_dict)
        total_pages = (total_reviews + reviews_per_page - 1) // reviews_per_page
        start = (page - 1) * reviews_per_page
        end = start + reviews_per_page

        paginated_reviews = dict(list(sorted_reviews_dict.items())[start:end])

                # Ensure JSON response includes correct fields
        response_reviews = [
            {
                'title': title,
                'average_rating': review_data['average_rating'],
                'review_count': review_data['review_count'],
                'reviews': review_data['reviews']
            } for title, review_data in paginated_reviews.items()
        ]

        return jsonify({
            'reviews': response_reviews,
            'page': page,
            'total_pages': total_pages
        })
    except Exception as e:
        print(f"Error during search: {e}")
        return jsonify({'error': str(e)}), 500

def paginate_results(results, page, reviews_per_page):
    total_reviews = len(results)
    total_pages = (total_reviews + reviews_per_page - 1) // reviews_per_page
    start = (page - 1) * reviews_per_page
    end = start + reviews_per_page

    if start >= total_reviews:
        return [], total_pages

    paginated_results = results[start:end]
    return paginated_results, total_pages
