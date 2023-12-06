
document.addEventListener("DOMContentLoaded", async () => {
    let userSearchInput = document.getElementById('user-search');
    userSearchInput.addEventListener("keydown", (e) => {
        if (e.code === 'Enter') {
            get_users()
        }
    })
});
async function get_users() {
    const userSearchInput = document.getElementById('user-search');
    const query = userSearchInput.value;
    const url = `/api/searchUser/?query=${query}`;
    let response = await fetch(url);
    let users = await response.json();

    // get empty user list container
    const listElement = document.getElementById("search-results-list");
    listElement.innerHTML = ""

    // handle no users
    if (users.length == 0) {
        const textContainer = document.createElement('div');
        textContainer.className = 'mt-10 flex align-center justify-center'
        const noUsersText = document.createElement("span");
        noUsersText.innerText = `No user with the name '${query}' found.`
        textContainer.appendChild(noUsersText);
        listElement.appendChild(textContainer);
    }

    // add user card for each user with a username similar to the given query
    for (user of users) {
        // make user container div redirect to user profile
        const containerDiv = document.createElement("div")
        containerDiv.addEventListener("click", () => window.location.href = `/profile/${user.username}`)
        containerDiv.className = `bg-white drop-shadow p-4 rounded my-3 border-t-8 border-t-${colorful.getColorName(user.color)}-400 cursor-pointer`
        const statusSpan = document.createElement("span");
        statusSpan.innerText = user.username;
        containerDiv.appendChild(statusSpan);
        listElement.appendChild(containerDiv);
    }

    // clear search bar
    document.getElementById("user-search").value = ""
}