const onMapLoad = async () => {
    const setStatusDiv = document.getElementById('setStatus');
    setStatusDiv.classList.add("p-2", "bg-white", "text-lg", "drop-shadow", "rounded-sm", "m-2");
    window.map.controls[google.maps.ControlPosition.TOP_CENTER].push(setStatusDiv);

    const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary(
        "marker",
    );
    window.AdvancedMarkerElement = AdvancedMarkerElement;
    window.PinElement = PinElement;

    await displayStatusList();
}
document.addEventListener("colorfulLoaded", () => {
    document.addEventListener("mapCreated", onMapLoad);
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

    for (user_status of stati) {
        // const colorPin =  new PinElement({
        //     background: user_status.color,
        //     borderColor: user_status.color,
        //     glyphColor: "white"
        // })
        const colorThing = document.createElement("div");
        let color = colorful.getColorName(user_status.color)
        if (color !== undefined) {
            color = color + '-400'
        } else {
            color = '[' + user_status.color + ']';
        }
        colorThing.className = `rounded-full p-5 bg-${color}`;
        colorThing.innerHTML = `
        <div class="hidden">
        ${user_status.status}
        </div>
        `
        console.log(user_status);
        const marker = new AdvancedMarkerElement({
            map,
            position: { lat: user_status.latitude, lng: user_status.longitude },
            content: colorThing,
            title: user_status.status
        })
        console.log(user_status)
    }
}