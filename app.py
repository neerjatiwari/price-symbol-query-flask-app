from flask import Flask, render_template, jsonify, request
import csv

app = Flask(__name__)

def get_price_for_symbol(data, symbol):
    for entry in data:
        if entry['symbol'] == symbol:
            return entry['price']
    return 'Symbol not found'

def read_csv():
    data = []
    with open('Prices_file_For Python Deve.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

@app.route('/')
def home():
    return render_template('index.html')

# API endpoint to fetch data
@app.route('/get_data')
def get_data():
    # Get data from the CSV file
    data = read_csv()
    return jsonify(data)

# API endpoint to get the price for a symbol
@app.route('/get_price', methods=['GET'])
def get_price():
    data = read_csv();
    symbol = request.args.get('symbol')
    price = get_price_for_symbol(data, symbol)
    return jsonify({'price': price})

# Append data to the CSV file
def append_to_csv(symbol, price):
    with open('Prices_file_For Python Deve.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([symbol, price])

@app.route('/add_data', methods=['POST'])
def add_data():
    symbol = request.form.get('symbol')
    price = request.form.get('price')
    
    existing_symbols = [entry['symbol'] for entry in read_csv()]
    if symbol in existing_symbols:
        return '2'
    
    # Validate input (you may want to add more validation)
    if symbol and price:
        append_to_csv(symbol, price)
        return '1'
    else:
        return '0'

# Remove data from the CSV file
def remove_from_csv(symbol):
    data = read_csv()
    
    with open('Prices_file_For Python Deve.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['symbol', 'price'])  # Write header row
        
        
        for entry in data:
            if entry['symbol'] != symbol:
                writer.writerow([entry['symbol'], entry['price']])
                
@app.route('/remove_data', methods=['POST'])
def remove_data():
    symbol = request.form.get('symbol')
    
    # Validate input (you may want to add more validation)
    if symbol:
        remove_from_csv(symbol)
        return 'Data removed successfully'
    else:
        return 'Invalid input'
    
if __name__ == '__main__':
    app.run(debug=False)