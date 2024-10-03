from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Default Rates
BASE_RATE = 0.15
BATHROOM_RATE = 50
BEDROOM_RATE = 25
WINDOW_RATE = 10
DOOR_RATE = 5

def calculate_detailed_cleaning_cost(square_footage, cleaners, hours, bathrooms, bedrooms, windows, doors):
    base_cost = square_footage * BASE_RATE
    bathroom_cost = bathrooms * BATHROOM_RATE
    bedroom_cost = bedrooms * BEDROOM_RATE
    window_cost = windows * WINDOW_RATE
    door_cost = doors * DOOR_RATE
    
    total_cost = base_cost + bathroom_cost + bedroom_cost + window_cost + door_cost
    labor_adjustment = total_cost * (cleaners * hours / 10)
    
    return total_cost + labor_adjustment

def validate_and_sanitize_params(params):
    try:
        # Convert and validate parameter types and ranges
        square_footage = float(params.get('square_footage'))
        cleaners = int(params.get('cleaners'))
        hours = float(params.get('hours'))
        bathrooms = int(params.get('bathrooms'))
        bedrooms = int(params.get('bedrooms'))
        windows = int(params.get('windows'))
        doors = int(params.get('doors'))

        # Define maximum limits
        max_square_footage = 100000
        max_cleaners = 50
        max_hours = 24
        max_bathrooms = 20
        max_bedrooms = 20
        max_windows = 100
        max_doors = 50

        # Check value ranges
        if square_footage <= 0 or square_footage > max_square_footage:
            raise ValueError(f"Square footage must be between 1 and {max_square_footage}.")
        if cleaners <= 0 or cleaners > max_cleaners:
            raise ValueError(f"Number of cleaners must be between 1 and {max_cleaners}.")
        if hours <= 0 or hours > max_hours:
            raise ValueError(f"Hours must be between 1 and {max_hours}.")
        if bathrooms < 0 or bathrooms > max_bathrooms:
            raise ValueError(f"Bathrooms must be between 0 and {max_bathrooms}.")
        if bedrooms < 0 or bedrooms > max_bedrooms:
            raise ValueError(f"Bedrooms must be between 0 and {max_bedrooms}.")
        if windows < 0 or windows > max_windows:
            raise ValueError(f"Windows must be between 0 and {max_windows}.")
        if doors < 0 or doors > max_doors:
            raise ValueError(f"Doors must be between 0 and {max_doors}.")


        return square_footage, cleaners, hours, bathrooms, bedrooms, windows, doors
    except (TypeError, ValueError) as e:
        raise ValueError(f"Parameter error: {e}")

@app.route('/detailed-cleaning-cost', methods=['GET'])
def detailed_cleaning_cost():
    try:
        # Validate and sanitize input parameters
        square_footage, cleaners, hours, bathrooms, bedrooms, windows, doors = validate_and_sanitize_params(request.args)
        
        # Calculate cost
        cost = calculate_detailed_cleaning_cost(square_footage, cleaners, hours, bathrooms, bedrooms, windows, doors)

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
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred.'}), 500

if __name__ == '__main__':
    app.run(debug=True)

