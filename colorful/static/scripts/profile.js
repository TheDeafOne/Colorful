document.addEventListener("DOMContentLoaded", async () => {
    document.getElementById("")
});

async function post_friend_follow(self_id, other_id) {
    const url = '/api/addFollower/'
    await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "self": self_id,
            "other": other_id
        })
    })
}

async function test(value) {
    console.log(value);
}