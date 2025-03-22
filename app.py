from flask import Flask, render_template
import requests

app = Flask(__name__)

GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/contributors"

def get_contributors(owner, repo):
    contributors = []
    per_page = 100  # Max allowed per request
    page = 1

    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page={per_page}&page={page}"
        response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})

        if response.status_code != 200:
            print(f"Error fetching contributors: {response.status_code}")
            return None

        data = response.json()
        if not data:
            break  # No more contributors left

        contributors.extend(data)
        page += 1

        if len(data) < per_page:
            break  # Last page reached

    print(f"Total Contributors for {owner}/{repo}: {len(contributors)}")
    return contributors

@app.route("/<owner>/<repo>")
def repo_contributors(owner, repo):
    contributors = get_contributors(owner, repo)
    if not contributors:
        return "<h2>Repository not found or private!</h2>", 404
    return render_template("index.html", contributors=contributors, repo=repo, owner=owner)

if __name__ == "__main__":
    app.run(debug=True)