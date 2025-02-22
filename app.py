from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Function to return the response based on the option selected by the user
def get_service_info(option):
    if option == 'work_hours':
        return 'Our working hours are:\n- Weekdays: 9:00 AM to 7:00 PM\n- Weekends: 9:00 AM to 3:00 PM'
    elif option == 'prices':
        return 'Our prices for services are:\n- Basic Service: $50\n- Tire Replacement: $100 - $500\n- Engine Repair: $200 - $1000\n- Oil Change: $30 - $100\n- Brake Service: $50 - $300'
    elif option == 'location':
        return 'A-24/256, Bandra West, Mumbai, 400050.'
    elif option == 'emergency_number':
        return 'For emergency breakdown assistance, please call: +91-1234567890 (24/7)'
    else:
        return "I am sorry, I didn't understand that."

# Function to handle repetitive "okay" responses
def get_okay_response(count):
    responses = [
        "Alright, let me know if you need anything else.",
        "Okay! How can I assist you further?",
        "Sure thing! Do you have any other questions?",
        "Got it! Feel free to ask if you have more queries."
    ]
    return responses[count % len(responses)]

# Function to get a random greeting response
def get_greeting_response():
    responses = [
        "Hello! How can I assist you today?",
        "Hi there! How can I help you?",
        "Hey! What can I do for you today?",
        "Greetings! How may I assist you?"
    ]
    return random.choice(responses)

# Function to get a random farewell response
def get_farewell_response():
    responses = [
        "Goodbye! Have a great day!",
        "Bye! Take care!",
        "Farewell! Have a good day!",
        "See you! Have a nice day!"
    ]
    return random.choice(responses)

# Dictionary to keep track of user sessions and "okay" counts
user_sessions = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])       
def chat():
    user_message = request.json.get('message').lower()
    user_id = request.remote_addr  # Use user's IP address as a session identifier

    # Initialize user session if not exist
    if user_id not in user_sessions:
        user_sessions[user_id] = {'okay_count': 0}

    # Default message when the chat starts (automatically triggered)
    if user_message == '':
        return jsonify({
            'response': 'Hey, I am your friend AI! How can I help you today? Please choose one of the options below:',
            'options': ['Work Hours', 'Prices', 'Location', 'Car Breakdown', 'Other Queries']
        })

    # Check for user greeting or start message
    if any(greeting in user_message for greeting in ['hi', 'hello', 'hey', 'heyy', 'heyya', 'hiya', 'greetings', 'good morning', 'good afternoon', 'good evening']):
        return jsonify({
            'response': get_greeting_response(),
            'options': ['Work Hours', 'Prices', 'Location', 'Car Breakdown', 'Other Queries']
        })

    # Handle various queries
    elif any(keyword in user_message for keyword in ['work hours', 'working hours', 'timing', 'hours of operation', 'business hours']):
        return jsonify({
            'response': get_service_info('work_hours'),
            'options': ['Thank you, my query is solved']
        })

    elif any(keyword in user_message for keyword in ['prices', 'price', 'fees', 'amount', 'services', 'cost', 'charge', 'rates']):
        return jsonify({
            'response': get_service_info('prices'),
            'options': ['Thank you, my query is solved']
        })

    elif any(keyword in user_message for keyword in ['location', 'address', 'place', 'add', 'where are you located', 'find us']):
        return jsonify({
            'response': 'We are located at: A-24/256, Bandra West, Mumbai, 400050.',
            'options': ['Thank you, my query is solved']
        })

    elif any(keyword in user_message for keyword in ['emergency', 'breakdown', 'assistance', 'number', 'help', 'support', 'urgent']):
        return jsonify({
            'response': get_service_info('emergency_number'),
            'options': ['Thank you, my query is solved']
        })

    elif 'other queries' in user_message:
        return jsonify({
            'response': 'For other inquiries, please contact our service executive at: +91 9920088950.',
            'options': ['Thank you, my query is solved']
        })

    # Handling "Thank you, my query is solved" option
    elif any(phrase in user_message for phrase in ['thank you, my query is solved', 'thanks, my query is solved', 'thank you', 'thanks', 'bye', 'goodbye', 'see you', 'farewell']):
        return jsonify({
            'response': get_farewell_response(),
            'options': ['Go to Main Menu']
        })

    # Handling "Go to Main Menu" option
    elif 'go to main menu' in user_message:
        return jsonify({
            'response': 'Welcome back! How can I assist you today?',
            'options': ['Work Hours', 'Prices', 'Location', 'Car Breakdown', 'Other Queries']
        })

    elif 'yes' in user_message:
        return jsonify({
            'response': 'Have a good day!',
            'options': []
        })

    elif 'no' in user_message:
        return jsonify({
            'response': 'Would you like to go to the main menu or do you have another query?',
            'options': ['Main Menu', 'Other Query']
        })

    elif 'main menu' in user_message:
        return jsonify({
            'response': 'Welcome back! How can I assist you today?',
            'options': ['Work Hours', 'Prices', 'Location', 'Car Breakdown', 'Other Queries']
        })

    elif 'other query' in user_message:
        return jsonify({
            'response': 'Please contact our service executive at: +91-9876543210 for further assistance. Have a good day!',
            'options': []
        })

    # Handling "okay" responses
    elif any(phrase in user_message for phrase in ['okay', 'ok', 'kk', 'k', 'alright', 'fine']):
        okay_count = user_sessions[user_id]['okay_count']
        response = get_okay_response(okay_count)
        user_sessions[user_id]['okay_count'] += 1
        return jsonify({
            'response': response,
            'options': []
        })

    else:
        return jsonify({
            'response': 'I am sorry, I didn\'t understand that. Can you please clarify?',
            'options': []
        })

if __name__ == '__main__':
    app.run(debug=True, port=5003)