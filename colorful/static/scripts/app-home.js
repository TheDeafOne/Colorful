document.addEventListener("colorfulLoaded", async () => {
    displayStatusList();
    colorful.getLocation()

    // TODO: add an event listener to call search when the button is clicked
    const button = document.getElementById("setStatus-button");
    const bar = document.getElementById("setStatus-bar");
    bar.addEventListener("keydown", (e) => {
        if (e.code === "Enter") {
            bar.value = "";
        }
    })
    button.addEventListener("click", addStatus);
});

async function addStatus() {
    const statusStr = document.getElementById("setStatus-bar").value
    const { latitude, longitude } = await colorful.getLocation();
    document.getElementById("setStatus-bar").value = ""
    await colorful.setStatus(statusStr, latitude, longitude);


    // update status list
    await displayStatusList()
}

async function displayStatusList() {
    const stati = await colorful.getStatusList()
    const statusList = document.getElementById("status-list")
    statusList.innerHTML = ""

    for (user_status of stati) {
        // console.log(user_status);
        const containerDiv = document.createElement("div")
        containerDiv.className = `bg-white drop-shadow p-4 rounded my-3 border-t-8 border-t-${colorful.getColorName(user_status.color)}-400`
        const statusSpan = document.createElement("span");
        statusSpan.innerText = `${user_status.name}: ${user_status.status} - (${user_status.latitude}, ${user_status.longitude}) - ${user_status.color}`

        containerDiv.appendChild(statusSpan);
        statusList.append(containerDiv)
    }
}