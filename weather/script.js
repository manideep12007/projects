const apiKey = "cc61721f3e95dceb826c0c7e6d0455a7";
const apiURL = "https://api.openweathermap.org/data/2.5/weather?";
const reverseGeocodeURL = "https://api.bigdatacloud.net/data/reverse-geocode-client";

const checkWeather = async (city='Chennai') => {
    try {
        const response = await fetch(apiURL + `&units=metric&q=${city}&appid=${apiKey}`);
        const data = await response.json();
        console.log(data);
        const cityElement = document.querySelector('.city');
        const tempElement = document.querySelector('.temp');
        const humidityElement = document.querySelector('.humidity');
        const windElement = document.querySelector('.wind');
        const weatherIcon = document.querySelector('.weather-icon');
        if (cityElement && tempElement && humidityElement && windElement && weatherIcon) {
            cityElement.innerHTML = data.name;
            tempElement.innerHTML = Math.round(data.main.temp) + `&deg;C`;
            humidityElement.innerHTML = data.main.humidity + '&percnt;';
            windElement.innerHTML = data.wind.speed + ' km/hr';
            const condition = data.weather[0].main.toLowerCase();
            weatherIcon.src = `/weather/images/${condition}.png`;            console.log(`Condition: ${condition}`);
        } else {
            console.log('One or more elements are missing');
        }
    } catch (err) {
        console.log(`Error: ${err}`);
    }
}

const getCity = async () => {
    if (navigator.geolocation) {
        try {
            navigator.geolocation.getCurrentPosition(async (position) => {
                const { latitude, longitude } = position.coords;
                console.log(`Latitude: ${latitude}, Longitude: ${longitude}`);
                const response = await fetch(`${reverseGeocodeURL}?latitude=${latitude}&longitude=${longitude}&localityLanguage=en`);
                const data = await response.json();
                const city = data.city || 'Chennai';
                checkWeather(city);
            }, (error) => {
                console.log(`Error: ${error}`);
                checkWeather(); // Default to Hyderabad if location access is denied
            });
        } catch (err) {
            console.log(`Error: ${err}`);
            checkWeather(); // Default to Hyderabad if there is an error
        }
    } else {
        console.error('Geolocation is not supported by your browser');
        checkWeather(); // Default to Hyderabad if geolocation is not supported
    }
}

document.addEventListener('DOMContentLoaded', function() {
    getCity(); // Get user location on page load
    const btn = document.querySelector("#btn");
    btn.addEventListener('click', function() {
        const city = document.querySelector("#city").value;
        checkWeather(city);
    });
});
