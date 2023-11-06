

document.addEventListener("DOMContentLoaded", async () => {
	// TODO: add an event listener to call search when the button is clicked
	const button = document.getElementById("setStatus-button")
	button.addEventListener("click", addStatus)
});

async function addStatus(){
    const statusStr = document.getElementById("setStatus-bar").value

    const url = '/api/setStatus/'

    await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "status": statusStr
        })
    })

    console.log("Success???")
}
