window.colorful = {};
((self) => {
    self.geolocationMethod = 'SPECIFIC';

    self.getLocation = async () => {
        // get specific location of user
        let latitude = 0;
        let longitude = 0;
        if (self.geolocationMethod === 'SPECIFIC') {
            let location = await self.getGeolocationData();
            return location;
        } else { // general location of user
            let response = await fetch('https://ipapi.co/json/');
            let json = await response.json();
            return {
                latitude: json.latitude,
                longitude: json.longitude
            }
        }
    }

    // adapted from https://stackoverflow.com/a/66259340/10181378
    self.getGeolocationData = () => {
        return  new Promise((resolve, reject) => {
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
                        self.geolocationMethod = 'GENERAL'
                    }
                )

            } else {
                reject("your browser doesn't support geolocation API")
            }
        })
    }

    self.setStatus = async (statusStr, latitude, longitude) => {
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
    }

    self.getStatusList = async () => {
        // grab all statuses
        const url = '/api/getStatusList/'
        const response = await fetch(url)
        const responseJSON = await response.json()

        return responseJSON
    }

    self.getFriendsStatusList = async (user_id) => {
        const url = `/api/getFriendsStatusList/${user_id}/`
        const response = await fetch(url)
        const responseJSON = await response.json()

        return responseJSON
    }

    self.getColorName = (hexColor) => {
        const map = {
            "#FF0000": "red",
            "#00FF00": "green",
            "#0000FF": "blue"
        }
        return map[hexColor]
    }

    const colorfulLoaded = new Event("colorfulLoaded")
    document.dispatchEvent(colorfulLoaded)
})(window.colorful)