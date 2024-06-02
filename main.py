from flask import Flask, render_template, request
import csv
import requests
import os

app = Flask(__name__)

# Replace with your Google API key
google_api_key = 'AIzaSyBqL-YqdqWSb4lFv4EEzfIR1HSPwqxoFec'

@app.route('/')
def index():
    return render_template('index.html')


def clear_csv(csv_file):
    # Clear the existing file
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        headers = ['name', 'latitude', 'longitude', 'rating']
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

def csv_kopyala(kaynak, hedef):
    # Kaynak dosyayı oku
    with open(kaynak, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        veriler = list(csv_reader)  # CSV verilerini oku ve listeye dönüştür

    # Hedef dosyaya yaz
    with open(hedef, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(veriler)  # CSV verilerini hedef dosyaya yaz

    print(f'{kaynak} dosyası {hedef} dosyasına başarıyla kopyalandı.')
def clear_csv_ispark(csv_file):
    # Clear the existing file
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        headers = ['name', 'LOCATION_NAME', 'PARK_TYPE_ID', 'PARK_TYPE_DESC', 'CAPACITY_OF_PARK', 'WORKING_TIME', 'COUNTY_NAME', 'LONGITUDE', 'LATITUDE']
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()


@app.route('/map', methods=['POST'])
def generate_map():
    point1 = tuple(map(float, request.form['point1'].split(',')))
    point2 = tuple(map(float, request.form['point2'].split(',')))

    # Calculate the midpoint of the route
    midpoint = ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)

    # Checkboxes'tan gelen verileri al
    include_ispark = 'ispark' in request.form
    include_gas_stations = 'gas_station' in request.form
    include_restaurants = 'restaurant' in request.form
    include_hastane = 'hastane' in request.form
    user_input = request.form['user_input']

    if user_input:
        nearest_yer = find_nearest_yer(midpoint, user_input)
        nearest_yer_point1 = find_nearest_yer(point1, user_input)
        nearest_yer_point2 = find_nearest_yer(point2, user_input)

        # Combine the results and remove duplicates
        nearest_yer = nearest_yer + nearest_yer_point1 + nearest_yer_point2
        # Remove duplicates by using a dictionary
        unique_yer = {station['name']: station for station in nearest_yer}.values()
        save_to_csv4(unique_yer)
    else:
        clear_csv('static/yerler.csv')

    if include_ispark:
        csv_kopyala("static/ispark_parking.csv","static/ispark.csv")
    else:
        clear_csv_ispark('static/ispark.csv')

    if include_hastane:
        nearest_hastane = find_nearest_hastane(midpoint, keywords3)
        save_to_csv3(nearest_hastane)
    else:
        clear_csv('static/hastane.csv')

    if include_restaurants:
        nearest_restaurants = find_nearest_restaurants(midpoint, keywords2)
        save_to_csv2(nearest_restaurants)
    else:
        clear_csv('static/restoran.csv')

    if include_gas_stations:
        # En yakın akaryakıt istasyonlarını bul: orta nokta, başlangıç ve bitiş
        nearest_gas_stations_midpoint = find_nearest_gas_stations(midpoint, keywords)
        nearest_gas_stations_point1 = find_nearest_gas_stations(point1, keywords)
        nearest_gas_stations_point2 = find_nearest_gas_stations(point2, keywords)

        # Sonuçları birleştir
        nearest_gas_stations = nearest_gas_stations_midpoint + nearest_gas_stations_point1 + nearest_gas_stations_point2
        # Tekrarları sil
        unique_gas_stations = {station['name']: station for station in nearest_gas_stations}.values()

        # CSV'ye kaydet
        save_to_csv(unique_gas_stations)
    else:
        clear_csv('static/gas_stations.csv')

    return render_template('map.html', point1=point1, point2=point2)


keywords = ['akaryakıt istasyonu', 'benzinlik', 'benzin istasyonu',
            'opet', 'shell', 'petrol ofisi', 'bp', 'petrol istasyonu']
keywords2 = ['restoran', 'kebap', 'lokanta', 'döner', 'lokantası', 'restoranı']
keywords3 = ['hastane', 'hospital', 'araştırma hastanesi']

def find_nearest_restaurants(midpoint, keywords, radius=5000):
    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    restaurants = []

    for keyword in keywords:
        params = {
            'key': google_api_key,
            'location': f"{midpoint[0]},{midpoint[1]}",
            'radius': radius,
            'keyword': keyword
        }

        response = requests.get(endpoint, params=params)
        data = response.json()

        if 'results' in data:
            for result in data['results']:
                location = result['geometry']['location']
                name = result['name']
                rating = result.get('rating', 'No rating')
                place = {
                    'name': name,
                    'latitude': location['lat'],
                    'longitude': location['lng'],
                    'rating': rating
                }
                restaurants.append(place)

    return restaurants

def find_nearest_gas_stations(midpoint, keywords, radius=2000):
    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    gas_stations = []

    for keyword in keywords:
        params = {
            'key': google_api_key,
            'location': f"{midpoint[0]},{midpoint[1]}",
            'radius': radius,
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

def find_nearest_hastane(midpoint, keywords, radius=5000):
    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    hastaneler = []

    for keyword in keywords:
        params = {
            'key': google_api_key,
            'location': f"{midpoint[0]},{midpoint[1]}",
            'radius': radius,
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
                hastaneler.append(place)

    return hastaneler

def find_nearest_yer(midpoint, user_input, radius=5000):
    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    restaurants = []


    params = {
        'key': google_api_key,  # replace with your actual API key
        'location': f"{midpoint[0]},{midpoint[1]}",
        'radius': radius,
        'keyword': user_input
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if 'results' in data:
        for result in data['results']:
            location = result['geometry']['location']
            name = result['name']
            rating = result.get('rating', 'No rating')  # default to 'No rating' if rating is not available
            place = {
                'name': name,
                'latitude': location['lat'],
                'longitude': location['lng'],
                'rating': rating
            }
            restaurants.append(place)

    return restaurants

def save_to_csv4(yerler):
    csv_file = 'static/yerler.csv'
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        headers = ['name', 'latitude', 'longitude', 'rating']
        writer = csv.DictWriter(file, fieldnames=headers)

        writer.writeheader()
        for station in yerler:
            writer.writerow(station)

def save_to_csv3(hastaneler):
    csv_file = 'static/hastane.csv'
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        headers = ['name', 'latitude', 'longitude']
        writer = csv.DictWriter(file, fieldnames=headers)

        writer.writeheader()
        for station in hastaneler:
            writer.writerow(station)

def save_to_csv2(restaurants):
    csv_file = 'static/restoran.csv'
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        headers = ['name', 'latitude', 'longitude', 'rating']
        writer = csv.DictWriter(file, fieldnames=headers)

        writer.writeheader()
        for station in restaurants:
            writer.writerow(station)

def save_to_csv(gas_stations):
    csv_file = 'static/gas_stations.csv'
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        headers = ['name', 'latitude', 'longitude']
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for station in gas_stations:
            writer.writerow(station)

if __name__ == '__main__':
    app.run(debug=True)
