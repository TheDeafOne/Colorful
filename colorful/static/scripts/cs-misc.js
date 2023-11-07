

document.addEventListener("DOMContentLoaded", async () => {
    displayStatusList()

	// TODO: add an event listener to call search when the button is clicked
	const button = document.getElementById("setStatus-button")
	button.addEventListener("click", addStatus)

    // const testButton = document.getElementById("test-button")
	// testButton.addEventListener("click", getStatusList)
});

async function addStatus(){
    const statusStr = document.getElementById("setStatus-bar").value
    if(statusStr === ""){
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
    // console.log(response)
}


async function getStatusList(){

    const url = '/api/getStatusList/'
    const response = await fetch(url)
    console.log(response)
    const responseJSON = await response.json()

    // for(i in responseJSON){
    //     console.log(`${i}, ${responseJSON[i]}`)
    // }

    return responseJSON
}

async function displayStatusList(){

    const stati = await getStatusList()
    const statusList = document.getElementById("status-list")
    statusList.innerHTML = ""


    for(username in stati){

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