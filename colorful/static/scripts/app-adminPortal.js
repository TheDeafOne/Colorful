document.addEventListener("DOMContentLoaded", async () => {
    displayUserList();
});

async function displayUserList(){
    const url = '/api/getUsersList/'
    const response = await fetch(url)
    const responseJSON = await response.json()

    console.log(responseJSON)

    const usersList = document.getElementById("users-list")
    for (user of responseJSON) {
        // console.log(user_status);
        const containerDiv = document.createElement("div")
        containerDiv.className = `bg-white drop-shadow p-4 rounded my-3 border-t-8 border-t-${colorful.getColorName(user.status.color)}-400`
        // containerDiv.className = `border-2 border-black p-4 bg-[${user_status.color}]`
        const statusSpan = document.createElement("span");
        statusSpan.innerText = `${user.username}: ${user.status.text} - (${user.status.latitude}, ${user.status.longitude}) - ${user.status.color}`

        containerDiv.appendChild(statusSpan);
        usersList.append(containerDiv)
    }


}