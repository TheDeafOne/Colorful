document.addEventListener("colorfulLoaded", async () => {
    const usersFilter = document.getElementById("usersFilter");
    usersFilter.addEventListener("change", loadStati);
    if (sessionStorage.getItem("usersFilter") !== null) {
        usersFilter.value = sessionStorage.getItem("usersFilter");
    }
    loadStati();
});

async function loadStati() {
    const usersFilter = document.getElementById("usersFilter");
    sessionStorage.setItem('usersFilter', usersFilter.value);
    status_list = await colorful.getStatusList(usersFilter.value);

    const container = document.getElementById("container");
    container.className = `grid gap-4 grid-cols-${calculateGridSize(status_list.length)}`
    container.innerHTML = "";
    for (user_status of status_list) {
        const div = document.createElement("div");
        makeSquare(div, user_status);
        container.appendChild(div);
    }
}

async function makeSquare(div, user_status) {
    let color = colorful.getColorName(user_status.color)
    if (color !== undefined) {
        color = color + '-400'
    } else {
        color = '[' + user_status.color + ']';
    }
    div.className = `bg-${color} group relative rounded cursor-pointer p-8 border `;
    div.value = user_status.name;
    div.addEventListener("click", (e) => {
        window.location.href = `/profile/${e.target.value}/`;
    })

    const tooltip = document.createElement("div");
    tooltip.className = "pointer-events-none absolute left-0 w-full opacity-0 transition-opacity group-hover:opacity-100 bg-gray-500 text-gray-50 px-2 align-baseline z-50";
    tooltip.innerText = `${user_status.name}: ${user_status.status}`;
    // tooltip.innerText = `${user_status.name}: ${user_status.status} - (${user_status.latitude}, ${user_status.longitude}) - ${user_status.color}`;

    div.appendChild(tooltip);
    console.log(tooltip.offsetHeight)
}

function calculateGridSize(length) {
    const min = 2;
    const max = 10;

    let gridSize = Math.floor(Math.sqrt(length));
    if (gridSize > max) {
        gridSize = max;
    } else if (gridSize < min) {
        gridSize = min;
    }
    return gridSize;
}