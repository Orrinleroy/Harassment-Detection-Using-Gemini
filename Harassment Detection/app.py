from flask import Flask, render_template, send_from_directory
import json

app = Flask(__name__)

@app.route('/')
def show_results():
    with open("results.json", "r") as f:
        results = json.load(f)
    return render_template("results.html", results=results)

# Serve static files like images
@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(debug=True)
