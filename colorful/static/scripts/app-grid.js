document.addEventListener("colorfulLoaded", async () => { 
    const user_id = document.getElementById("user_id").value;
    status_list = await colorful.getFriendsStatusList(user_id);

    const container = document.getElementById("container");
    container.classList.add(`grid-cols-${calculateGridSize(container)}`);
    for (user_status of status_list) {
        const div = document.createElement("div");
        makeSquare(div, user_status);
        container.appendChild(div);
    }
});

async function makeSquare(div, user_status) {
    div.className = `bg-${colorful.getColorName(user_status.color)}-400 rounded cursor-pointer`;
    div.value = user_status.name;
    div.addEventListener("click", (e) => {
        window.location.href = `/profile/${e.target.value}/`
    })
    
    toolTip = document.createElement("div");
    createToolTip(toolTip, user_status);
    div.appendChild(toolTip);
    
    tooltipTarget = document.createElement("button");
    createTooltipTarget(tooltipTarget, user_status);
    toolTip.appendChild(tooltipTarget);
}

async function createToolTip(element, user_status) {
    element.className = "\
        relative \
        before:content-[attr(data-tip)] \
        before:absolute \
        before:px-3 before:py-2 \
        before:left-1/2 before:-top-3 \
        before:2-max before:max-w-xs \
        before:-translate-x-1/2 before:-translate-y-full \
        before:bg-gray-700 before:text-white \
        before:rounded-md before:opacity-0 \
        before:transition-all \
        \
        after:absolute \
        after:left-1/2 after:-top-3 \
        after:h-0 after:2-0 \
        after:-translate-x-1/2 after:border-8 \
        after:border-t-gray-700 \
        after:border-l-transparent \
        after:border-b-transparent \
        after:border-r-transparent \
        after:opacity-0 \
        after:transition-all \
        \
        hover:before:opacity-100 hover:after:opacity-100 \
        ";
    element.setAttribute("data-tip", `${user_status.name}: ${user_status.status} - (${user_status.latitude}, ${user_status.longitude}) - ${user_status.color}`);
    element.value = user_status.name;
}

async function createTooltipTarget(element, user_status) {
    element.value = user_status.name;
}

function calculateGridSize(container) {
    const min = 2;
    const max = 15;

    let gridSize = Math.floor(Math.sqrt(container.children.length));
    if (gridSize > max) {
        gridSize = max;
    } else if (gridSize < min) {
        gridSize = min;
    }
    return gridSize;
}