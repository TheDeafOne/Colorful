let geolocationMethod = 'SPECIFIC';

document.addEventListener("DOMContentLoaded", async () => {
    displayStatusList();

    // TODO: add an event listener to call search when the button is clicked
    const button = document.getElementById("setStatus-button");
    button.addEventListener("click", addStatus);
});


// adapted from https://stackoverflow.com/a/66259340/10181378
const getGeolocationData = new Promise((resolve, reject) => {
    // use built in geolocation function to get location of user
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            lat = position.coords.latitude
            long = position.coords.longitude

            // pass the values to the resolve function, which lets us access the location data in addStatus
            resolve({
                latitude: lat,
                longitude: long
            })
        },
            (reject) => {
                // user disabled specific geolocation, so set geolocation method to general
                console.log(reject);
                geolocationMethod = 'GENERAL'
            }
        )

    } else {
        reject("your browser doesn't support geolocation API")
    }
})


async function addStatus() {
    const statusStr = document.getElementById("setStatus-bar").value

    // if no status update, ignore
    if (statusStr === "") {
        return
    }

    // get specific location of user
    let latitude = 0;
    let longitude = 0;
    if (geolocationMethod === 'SPECIFIC') {
        await getGeolocationData.then((location) => {
            latitude = location.latitude
            longitude = location.longitude
        }).catch((err) => {
            console.log(err)
        });
    } else { // general location of user
        await fetch('https://ipapi.co/json/')
            .then(response => response.json())
            .then(data => {
                latitude = data.latitude
                longitude = data.longitude
            })
    }

    const url = '/api/setStatus/'
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "status": statusStr,
            "latitude": latitude,
            "longitutde": longitude
        })
    })

    displayStatusList()
}


async function getStatusList() {

    const url = '/api/getStatusList/'
    const response = await fetch(url)
    // console.log(response)
    const responseJSON = await response.json()

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