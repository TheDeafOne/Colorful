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

    // post data to db
    const url = '/api/setStatus/'
    await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "status": statusStr,
            "latitude": latitude,
            "longitude": longitude
        })
    })

    // update status list
    displayStatusList()
}


async function getStatusList() {
    // grab all statuses
    const url = '/api/getStatusList/'
    const response = await fetch(url)
    const responseJSON = await response.json()

    return responseJSON
}

async function displayStatusList() {

    const stati = await getStatusList()
    const statusList = document.getElementById("status-list")
    statusList.innerHTML = ""


    for (user_status of stati) {
        const containerDiv = document.createElement("div")
        containerDiv.className = "border-2 border-black p-4 rounded my-3"
        containerDiv.style = `border-top:solid 0.5rem ${user_status.color};`
        containerDiv.innerHTML = (
            `<span>${user_status.name}: ${user_status.status}</span>
             - <span>(${user_status.latitude}, ${user_status.longitude})</span>
             - <span>${user_status.color}</span>`
        );
        statusList.append(containerDiv)
    }
}