# filepath: polling-app/app.py
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

POLL_KEY = "poll:choices"

@app.route('/vote', methods=['POST'])
def vote():
    choice = request.json.get('choice')
    if not choice:
        return jsonify({'error': 'No choice provided'}), 400
    r.hincrby(POLL_KEY, choice, 1)
    return jsonify({'message': f'Vote for {choice} counted.'})

@app.route('/results', methods=['GET'])
def results():
    results = r.hgetall(POLL_KEY)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)