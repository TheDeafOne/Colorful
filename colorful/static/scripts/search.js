
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
    clearSearchList();

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
    for (other_user of users) {
        // make user container div redirect to user profile
        const containerDiv = document.createElement("div")
        containerDiv.value = other_user.username;
        containerDiv.addEventListener("click", (e) => {
            window.location.href = `/profile/${e.target.value}`
        })
        let color = colorful.getColorName(other_user.color)
        if (color !== undefined) {
            color = color + '-400'
        } else {
            color = '[' + other_user.color + ']';
        }
        containerDiv.className = `bg-white drop-shadow p-4 rounded my-3 border-t-8 border-t-${color} cursor-pointer`
        const statusSpan = document.createElement("span");
        statusSpan.classList.add('pointer-events-none')
        statusSpan.innerText = other_user.username;
        containerDiv.appendChild(statusSpan);
        listElement.appendChild(containerDiv);
    }

    // clear search bar
    document.getElementById("user-search").value = ""
}

function clearSearchList() {
    // get empty user list container
    const listElement = document.getElementById("search-results-list");
    listElement.innerHTML = ""
}