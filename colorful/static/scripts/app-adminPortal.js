document.addEventListener("DOMContentLoaded", async () => {
    displayUserList();
});

async function displayUserList(){
    const url = '/api/getUsersList/'
    const response = await fetch(url)
    const responseJSON = await response.json()

    const usersList = document.getElementById("users-list")
    usersList.innerHTML = ""
    for (user of responseJSON) {
        const containerDiv = document.createElement("div")
        containerDiv.className = `bg-white drop-shadow p-4 rounded my-3 flex justify-between`

        const dataDiv = document.createElement("div")
        const statusSpan = document.createElement("span");
        const statusColorSpan = document.createElement("span");
        if(user.status){
            statusSpan.innerText = `${user.username}: ${user.status.text}`
            statusColorSpan.className = `px-4 bg-[${user.status.color}] mx-2`
        } else{
            statusSpan.innerText = `${user.username}: None`

        }
        dataDiv.appendChild(statusSpan);
        dataDiv.appendChild(statusColorSpan)

        const controlsDiv = document.createElement("div")
        const muteButton = document.createElement("button")
        muteButton.setAttribute("userID", user.id)
        if(user.isMuted == false){
            muteButton.innerText = "Mute User"
            muteButton.className = "bg-gray-300 active:bg-gray-700 p-1 hover:bg-gray-400 rounded-sm"
        } else{
            muteButton.innerText = "Unmute User"
            muteButton.className = "bg-red-500 active:bg-gray-700 p-1 hover:bg-red-600 rounded-sm"
        }
        muteButton.addEventListener("click", muteUser)
        controlsDiv.append(muteButton)

        containerDiv.append(dataDiv)
        if(user.isAdmin !== true){
            containerDiv.append(controlsDiv)
        }
        usersList.append(containerDiv)
    }
}

async function muteUser(event){
    userid = event.target.attributes.userid.value

    const url = '/api/toggleMuteForUser/'
    const response = await fetch(url,{
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "user": userid,
        })
    })
    displayUserList()

}