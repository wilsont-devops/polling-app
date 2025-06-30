# filepath: polling-app/app.py
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

POLL_KEY = "poll:choices"

@app.route('/create', methods=['POST'])
def create_poll():
    data = request.json
    choices = data.get('choices')
    if not choices or not isinstance(choices, list):
        return jsonify({'error': 'Choices must be a list'}), 400
    # Clear previous poll
    r.delete(POLL_KEY)
    # Initialize choices with 0 votes
    for choice in choices:
        r.hset(POLL_KEY, choice, 0)
    return jsonify({'message': 'Poll created', 'choices': choices})

@app.route('/choices', methods=['GET'])
def list_choices():
    choices = r.hkeys(POLL_KEY)
    return jsonify({'choices': choices})

@app.route('/vote', methods=['POST'])
def vote():
    choice = request.json.get('choice')
    if not choice:
        return jsonify({'error': 'No choice provided'}), 400
    if not r.hexists(POLL_KEY, choice):
        return jsonify({'error': 'Choice does not exist'}), 400
    r.hincrby(POLL_KEY, choice, 1)
    return jsonify({'message': f'Vote for {choice} counted.'})

@app.route('/results', methods=['GET'])
def results():
    results = r.hgetall(POLL_KEY)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)    # ...existing code...
    
    @app.route('/vote', methods=['POST'])
    def vote():
        choice = request.json.get('choice')
        user_ip = request.remote_addr
        voted_key = f"poll:voted:{user_ip}"
        if not choice:
            return jsonify({'error': 'No choice provided'}), 400
        if not r.hexists(POLL_KEY, choice):
            return jsonify({'error': 'Choice does not exist'}), 400
        if r.exists(voted_key):
            return jsonify({'error': 'You have already voted.'}), 403
        r.hincrby(POLL_KEY, choice, 1)
        r.set(voted_key, 1)
        return jsonify({'message': f'Vote for {choice} counted.'})
    
    # ...existing code...