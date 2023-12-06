async function post_friend_follow(self_id, other_id) {
    const url = '/api/addFollower/'
    let response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "self": self_id,
            "other": other_id
        })
    })
    if (response.ok) {
        window.location.reload();
    }
}

async function post_friend_unfollow(self_id, other_id) {
    const url = '/api/removeFollower/'
    let response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "self": self_id,
            "other": other_id
        })
    })
    if (response.ok) {
        window.location.reload();
    }
}