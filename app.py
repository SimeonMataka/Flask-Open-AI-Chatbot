from flask import Flask, render_template, request, jsonify
import openai

# Set up your API key
openai.api_key = 'Your API Key' #Put your API key here

app = Flask(__name__)

# Initialize conversation history
messages = [{"role": "system", "content": "You are a helpful assistant."}]

# # Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle user input and chat response
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.form['user_input']
        print(f"User input received: {user_input}")  # Debugging log
    
        # Add user message to the conversation history
        messages.append({"role": "user", "content": user_input})

        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-3.5-turbo"
            messages=messages
        )
        
        # Get assistant response
        assistant_reply = response['choices'][0]['message']['content']
        print(f"Assistant reply: {assistant_reply}")  # Debugging log

        # Add assistant's response to the conversation history
        messages.append({"role": "assistant", "content": assistant_reply})

        return jsonify({'user_input': user_input, 'assistant_reply': assistant_reply})

        #For testing reply try returning the  below code
        # return jsonify({'user_input': user_input, 'assistant_reply': "You can modify the styles, colors, and layout as needed to fit your design preferences. Let me know if you need further customization or improvements!"})

    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({'error': str(e)}), 500  # Return a 500 error with error message

if __name__ == '__main__':
    app.run(debug=True)