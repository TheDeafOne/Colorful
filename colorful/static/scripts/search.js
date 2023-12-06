
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
    let json = await response.json();
    console.log(json);
}