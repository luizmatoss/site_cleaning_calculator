from flask import Flask, request, jsonify

app = Flask(__name__)

# Define default rates
BASE_RATE = 0.15  # Base rate per square foot
BATHROOM_RATE = 50  # Additional rate per bathroom
BEDROOM_RATE = 25  # Additional rate per bedroom
WINDOW_RATE = 10  # Additional rate per window
DOOR_RATE = 5  # Additional rate per door

def calculate_detailed_cleaning_cost(square_footage, cleaners, hours, bathrooms, bedrooms, windows, doors):
    # Calculate base cost by square footage
    base_cost = square_footage * BASE_RATE
    
    # Calculate additional costs
    bathroom_cost = bathrooms * BATHROOM_RATE
    bedroom_cost = bedrooms * BEDROOM_RATE
    window_cost = windows * WINDOW_RATE
    door_cost = doors * DOOR_RATE
    
    # Calculate total cost
    total_cost = base_cost + bathroom_cost + bedroom_cost + window_cost + door_cost

    # Adjust for labor (number of cleaners and hours)
    labor_adjustment = total_cost * (cleaners * hours / 10)  # Adjust weight as needed
    
    return total_cost + labor_adjustment

@app.route('/detailed-cleaning-cost', methods=['GET'])
def detailed_cleaning_cost():
    try:
        # Parse parameters from request
        square_footage = float(request.args.get('square_footage'))
        cleaners = int(request.args.get('cleaners'))
        hours = float(request.args.get('hours'))
        bathrooms = int(request.args.get('bathrooms'))
        bedrooms = int(request.args.get('bedrooms'))
        windows = int(request.args.get('windows'))
        doors = int(request.args.get('doors'))

        # Calculate detailed cost
        cost = calculate_detailed_cleaning_cost(square_footage, cleaners, hours, bathrooms, bedrooms, windows, doors)
        
        # Return result as JSON
        return jsonify({
            'square_footage': square_footage,
            'cleaners': cleaners,
            'hours': hours,
            'bathrooms': bathrooms,
            'bedrooms': bedrooms,
            'windows': windows,
            'doors': doors,
            'cost': cost
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
