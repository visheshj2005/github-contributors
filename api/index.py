from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/api/<owner>/<repo>', methods=['GET'])
def get_contributors(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    headers = {"Accept": "application/vnd.github.v3+json"}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Repository not found or rate-limited"}), 404

    contributors = response.json()
    result = [{"username": user["login"], "contributions": user["contributions"], "avatar": user["avatar_url"]} for user in contributors]

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
