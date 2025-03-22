from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

def get_contributors(owner, repo):
    contributors = []
    per_page = 100
    page = 1
    
    # Get GitHub token from environment variable
    github_token = os.getenv('GITHUB_TOKEN')
    
    # Set up headers with authentication
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {github_token}" if github_token else None
    }

    try:
        while True:
            url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page={per_page}&page={page}"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 404:
                print(f"Repository {owner}/{repo} not found")
                return None
            elif response.status_code == 403:
                print(f"Rate limit exceeded or authentication required")
                return None
            elif response.status_code != 200:
                print(f"Error fetching contributors: {response.status_code}")
                print(f"Response: {response.text}")
                return None

            data = response.json()
            if not data:
                break

            contributors.extend(data)
            page += 1

            if len(data) < per_page:
                break

        print(f"Total Contributors for {owner}/{repo}: {len(contributors)}")
        return contributors
        
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return None

@app.route("/<owner>/<repo>")
def repo_contributors(owner, repo):
    contributors = get_contributors(owner, repo)
    if contributors is None:
        return render_template("error.html", 
                             message="Repository not found or private, or rate limit exceeded!"), 404
    return render_template("index.html", contributors=contributors, repo=repo, owner=owner)

if __name__ == "__main__":
    app.run(debug=True)