from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Tüm domain'lerden gelen isteklere izin verir

# MySQL bağlantısı
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="mysql_db",
            user="temp",
            password="temp",
            database="testdb"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def insert_sum_into_db(num1, num2, result):
    connection = connect_to_database()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        query = "INSERT INTO results (num1, num2, result) VALUES (%s, %s, %s)"
        cursor.execute(query, (num1, num2, result))
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error inserting into database: {err}")
        return False
    finally:
        cursor.close()
        connection.close()
    
    return True

def get_results_from_db():
    connection = connect_to_database()
    if connection is None:
        return None

    results = []
    try:
        cursor = connection.cursor()
        query = "SELECT num1, num2, result FROM results"
        cursor.execute(query)
        results = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching results from database: {err}")
    finally:
        cursor.close()
        connection.close()

    return results

@app.route('/add', methods=['POST'])
def add_numbers():
    try:
        num1 = request.form.get('num1')
        num2 = request.form.get('num2')

        if num1 is None or num2 is None:
            return jsonify({"error": "num1 and num2 are required"}), 400

        num1 = int(num1)
        num2 = int(num2)
        
        result = num1 + num2
        print(f"{num1} + {num2} = {result}")

        if not insert_sum_into_db(num1, num2, result):
            return jsonify({"error": "Failed to insert result into database."}), 500

        return jsonify({"result": result}), 200

    except ValueError:
        return jsonify({"error": "Invalid input. Please provide integers."}), 400
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {str(err)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/results', methods=['GET'])
def get_results():
    results = get_results_from_db()
    if results is None:
        return jsonify({"error": "Failed to fetch results from database."}), 500

    # Verileri JSON formatında döndür
    return jsonify(results), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
