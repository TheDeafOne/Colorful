document.addEventListener("colorfulLoaded", async () => {
    displayStatusList();

    // TODO: add an event listener to call search when the button is clicked
    const button = document.getElementById("setStatus-button");
    button.addEventListener("click", addStatus);
});

async function addStatus() {
    const statusStr = document.getElementById("setStatus-bar").value
    const { latitude, longitude } = await colorful.getGeolocationData();

    await colorful.setStatus(statusStr, latitude, longitude);

    // update status list
    await displayStatusList()
}

async function displayStatusList() {
    const stati = await colorful.getStatusList()
    const statusList = document.getElementById("status-list")
    statusList.innerHTML = ""

    for (user_status of stati) {
        console.log(user_status);
        const containerDiv = document.createElement("div")
        containerDiv.className = "border-2 border-black p-4 rounded my-3"
        containerDiv.style = `border-top:solid 0.5rem ${user_status.color};`
        // containerDiv.className = `border-2 border-black p-4 bg-[${user_status.color}]`
        const statusSpan = document.createElement("span");
        statusSpan.innerText = `${user_status.name}: ${user_status.status} - (${user_status.latitude}, ${user_status.longitude}) - ${user_status.color}`

        containerDiv.appendChild(statusSpan);
        statusList.append(containerDiv)
    }
}