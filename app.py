from flask import Flask, jsonify, request, render_template # type: ignore
from flask_mysqldb import MySQL # type: ignore
from config import Config

app = Flask(__name__)

# Load MySQL configurations from config.py
app.config.from_object(Config)

# Initialize MySQL connection
mysql = MySQL(app)

# Serve the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to insert noise data (POST)
@app.route('/add_noise', methods=['POST'])
def add_noise():
    try:
        # Extract data from the request's JSON body
        noise_level = request.json['noise_level']
        timestamp = request.json['timestamp']
        latitude = request.json['latitude']
        longitude = request.json['longitude']
        location_id = request.json['location_id']
        device_id = request.json['device_id']

        # Insert data into the MySQL table
        cur = mysql.connection.cursor()
        query = '''INSERT INTO noise_readings (noise_level, timestamp, latitude, longitude, location_id, device_id) 
                   VALUES (%s, %s, %s, %s, %s, %s)'''
        cur.execute(query, (noise_level, timestamp, latitude, longitude, location_id, device_id))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'Noise data inserted successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint to retrieve noise data (GET)
@app.route('/get_noise', methods=['GET'])
def get_noise():
    try:
        # Fetch noise data from the MySQL table
        cur = mysql.connection.cursor()
        cur.execute('''SELECT noise_level, timestamp, latitude, longitude FROM noise_readings''')
        data = cur.fetchall()
        cur.close()

        # Prepare the data as a list of dictionaries
        results = []
        for row in data:
            results.append({
                'noise_level': row[0],
                'timestamp': row[1].strftime('%Y-%m-%d %H:%M:%S'),
                'latitude': row[2],
                'longitude': row[3]
            })

        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
