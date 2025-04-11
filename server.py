from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/api/plotly-data')
def get_plotly_data():
    return send_file('plotly_data.json')

if __name__ == '__main__':
    app.run(port=5000)