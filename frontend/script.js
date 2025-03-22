function fetchContributors() {
    let owner = document.getElementById("owner").value.trim();
    let repo = document.getElementById("repo").value.trim();
    let output = document.getElementById("output");

    if (!owner || !repo) {
        output.innerHTML = "<p>Please enter both owner and repository.</p>";
        return;
    }

    let apiUrl = `https://github-contributors-api.onrender.com/api/${owner}/${repo}`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            output.innerHTML = "";
            if (data.error) {
                output.innerHTML = `<p>${data.error}</p>`;
                return;
            }

            data.forEach(user => {
                output.innerHTML += `
                    <div class="user-card">
                        <img src="${user.avatar}" alt="${user.username}" />
                        <p><strong>${user.username}</strong> - ${user.contributions} contributions</p>
                    </div>
                `;
            });
        })
        .catch(error => {
            output.innerHTML = `<p>Error fetching data.</p>`;
            console.error(error);
        });
}
