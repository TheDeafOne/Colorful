

document.addEventListener("DOMContentLoaded", async () => {
    displayStatusList();

    // TODO: add an event listener to call search when the button is clicked
    const button = document.getElementById("setStatus-button");
    button.addEventListener("click", addStatus);

    const geoLocateButton = document.getElementById("geolocate-button");
    geoLocateButton.addEventListener("click", geolocate);
    // const testButton = document.getElementById("test-button")
    // testButton.addEventListener("click", getStatusList)
});

async function geolocate() {
    fetch('https://ipapi.co/json/')
        .then(response => response.json())
        .then(data => {
            console.log(JSON.stringify(data, null, 2));
        })
        .catch(error => {
            console.error('Error fetching data:', error);
    });
    // Check if geolocation is supported by the browser
    if ("geolocation" in navigator) {
        // Prompt user for permission to access their location
        navigator.geolocation.getCurrentPosition(
            // Success callback function
            (position) => {
                // Get the user's latitude and longitude coordinates
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;

                // Do something with the location data, e.g. display on a map
                console.log(`Latitude: ${lat}, longitude: ${lng}`);
            },
            // Error callback function
            (error) => {
                // Handle errors, e.g. user denied location sharing permissions
                console.error("Error getting user location:", error);
            }
        );
    } else {
        // Geolocation is not supported by the browser
        console.error("Geolocation is not supported by this browser.");
    }
}

async function addStatus() {
    const statusStr = document.getElementById("setStatus-bar").value
    if (statusStr === "") {
        return
    }

    const url = '/api/setStatus/'
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "status": statusStr
        })
    })

    displayStatusList()
}


async function getStatusList() {

    const url = '/api/getStatusList/'
    const response = await fetch(url)
    console.log(response)
    const responseJSON = await response.json()

    // for(i in responseJSON){
    //     console.log(`${i}, ${responseJSON[i]}`)
    // }

    return responseJSON
}

async function displayStatusList() {

    const stati = await getStatusList()
    const statusList = document.getElementById("status-list")
    statusList.innerHTML = ""


    for (username in stati) {

        const containerDiv = document.createElement("div")
        containerDiv.className = "border-2 border-black p-4"

        const userEl = document.createElement("span")
        userEl.innerText = `${username}:`
        userEl.innerHTML += "&nbsp"
        const statusEl = document.createElement("span")
        statusEl.innerText = stati[username]

        containerDiv.append(userEl)
        containerDiv.append(statusEl)
        statusList.append(containerDiv)
    }
}