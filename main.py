from flask import Flask, render_template, request
import csv
import requests
import os

app = Flask(__name__)

# Replace with your Google API key
google_api_key = 'AIzaSyACNNqf1GszcxCJH9XQJLyvDkQ5Khs8dHA'

@app.route('/')
def index():
    return render_template('index.html')


def clear_csv(csv_file):
    # Clear the existing file
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        headers = ['name', 'latitude', 'longitude']
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()


@app.route('/map', methods=['POST'])
def generate_map():
    point1 = tuple(map(float, request.form['point1'].split(',')))
    point2 = tuple(map(float, request.form['point2'].split(',')))

    # Calculate the midpoint of the route
    midpoint = ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)

    # Checkboxes'tan gelen verileri al
    include_gas_stations = 'gas_station' in request.form
    include_restaurants = 'restaurant' in request.form

    if include_restaurants:
        # Find the nearest restaurants to the midpoint
        nearest_restaurants = find_nearest_restaurants(midpoint, keywords2)

        # Save the gas stations to CSV
        save_to_csv2(nearest_restaurants)
    else:
        clear_csv('static/restoran.csv')

    if include_gas_stations:
        # Find the nearest gas stations to the midpoint
        nearest_gas_stations = find_nearest_gas_stations(midpoint,keywords)

        # Save the gas stations to CSV
        save_to_csv(nearest_gas_stations)
    else:
        clear_csv('static/gas_stations.csv')

    return render_template('map.html', point1=point1, point2=point2)


keywords = ['akaryakıt istasyonu', 'benzinlik', 'benzin istasyonu', 'opet','shell','petrol ofisi','bp','petrol istasyonu']
keywords2 = ['restoran', 'kebap', 'lokanta', 'döner']

def find_nearest_restaurants(midpoint, keywords, radius=5000):
    # Google Places API endpoint for nearby search
    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    restaurants = []

    for keyword in keywords:
        params = {
            'key': google_api_key,
            'location': f"{midpoint[0]},{midpoint[1]}",
            'radius': radius,  # Search within the specified radius
            'keyword': keyword
        }

        response = requests.get(endpoint, params=params)
        data = response.json()

        if 'results' in data:
            for result in data['results']:
                location = result['geometry']['location']
                name = result['name']
                place = {
                    'name': name,
                    'latitude': location['lat'],
                    'longitude': location['lng']
                }
                restaurants.append(place)

    return restaurants
def find_nearest_gas_stations(midpoint, keywords, radius=5000):
    # Google Places API endpoint for nearby search
    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    gas_stations = []

    for keyword in keywords:
        params = {
            'key': google_api_key,
            'location': f"{midpoint[0]},{midpoint[1]}",
            'radius': radius,  # Search within the specified radius
            'keyword': keyword
        }

        response = requests.get(endpoint, params=params)
        data = response.json()

        if 'results' in data:
            for result in data['results']:
                location = result['geometry']['location']
                name = result['name']
                place = {
                    'name': name,
                    'latitude': location['lat'],
                    'longitude': location['lng']
                }
                gas_stations.append(place)

    return gas_stations

def save_to_csv2(restaurants):
    csv_file = 'static/restoran.csv'
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        headers = ['name', 'latitude', 'longitude']
        writer = csv.DictWriter(file, fieldnames=headers)

        writer.writeheader()
        for station in restaurants:
            writer.writerow(station)
def save_to_csv(gas_stations):
    csv_file = 'static/gas_stations.csv'
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        headers = ['name', 'latitude', 'longitude']
        writer = csv.DictWriter(file, fieldnames=headers)

        writer.writeheader()
        for station in gas_stations:
            writer.writerow(station)

if __name__ == '__main__':
    app.run(debug=True)
