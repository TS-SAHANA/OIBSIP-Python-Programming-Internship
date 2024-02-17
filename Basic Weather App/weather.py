# Import necessary libraries
import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
import geocoder

# OpenWeatherMap API key
API_KEY = "3d705e4b300169bfd78d4a6cb34b03eb"

# Custom font configuration
custom_font = ("Helvetica", 12, "bold")

# Function to fetch weather data by city name
def get_weather(api_key, city, units):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": units,
    }

    try:
        # Make API request and parse JSON response
        response = requests.get(base_url, params=params)
        data = response.json()

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return data
        else:
            return None
    except Exception as e:
        return None

# Function to fetch weather data by coordinates (latitude, longitude)
def get_weather_by_coordinates(api_key, latitude, longitude, units):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key,
        "units": units,
    }

    try:
        # Make API request and parse JSON response
        response = requests.get(base_url, params=params, verify=False)
        data = response.json()

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return data
        else:
            return None
    except Exception as e:
        return None

# Function to get user's location based on IP address
def get_location():
    try:
        # Use 'me' to automatically detect the user's location
        location = geocoder.ip('me')
        return location.latlng
    except Exception as e:
        return None

# Function to display weather information for a specific city
def display_weather():
    global API_KEY
    city = city_entry.get()
    choice = units_var.get().lower()  # Get selected temperature unit in lowercase

    # Set the API request units based on user's choice
    if choice == "celsius":
        units = "metric"
    else:
        units = "imperial"

    # Check if API key is provided
    if not API_KEY:
        messagebox.showerror("Error", "Please provide your OpenWeatherMap API key.")
        return

    # Check if a city is entered
    if not city:
        messagebox.showerror("Error", "Unable to fetch location data. Please enter a city or enable GPS.")
        return
    else:
        # Get weather data for the specified city
        weather_data = get_weather(API_KEY, city, units)

    if weather_data:
        # Extract relevant weather information
        temperature = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        country = weather_data["sys"]["country"]

        # Display weather information on the GUI
        result_label = tk.Label(app, textvariable=result_text, bg="skyblue1", fg="gray25", borderwidth=2, relief="solid", font=custom_font)
        result_label.place(relx=0.5, rely=0.78, anchor="center")

        result_text.set(f"Temperature: {temperature}°{choice.upper()}\nDescription: {description}\n"
                        f"Humidity: {humidity}%\nWind Speed: {wind_speed} m/s\nCountry: {country}")

        # Display weather icon
        icon_code = weather_data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
        icon_data = requests.get(icon_url).content
        image_stream = BytesIO(icon_data)

        icon_label = tk.Label(app, bg="dodgerblue1", borderwidth=2, relief="solid")
        icon_label.place(relx=0.85, rely=0.17, anchor="center")

        photo = ImageTk.PhotoImage(Image.open(image_stream))
        icon_label.config(image=photo)
        icon_label.image = photo
    else:
        messagebox.showerror("Error", "Unable to fetch weather data. Please check the city name and try again.")

# Function to get weather information for the current location
def get_weather_from_current_location():
    global API_KEY
    coordinates = get_location()

    if coordinates:
        latitude, longitude = coordinates
        choice = units_var.get().lower()  # Get selected temperature unit in lowercase

        # Set the API request units based on user's choice
        if choice == "celsius":
            units = "metric"
        else:
            units = "imperial"

        # Get weather data for the current location
        weather_data = get_weather_by_coordinates(API_KEY, latitude, longitude, units)
        display_weather_data(weather_data)
    else:
        messagebox.showerror("Error", "Unable to fetch location data. Please enable GPS.")

# Function to display weather information for the current location
def display_weather_data(weather_data):
    choice = units_var.get().lower()  # Get selected temperature unit in lowercase
    temperature = weather_data["main"]["temp"]
    description = weather_data["weather"][0]["description"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    country = weather_data["sys"]["country"]

    # Display weather information on the GUI
    result_label = tk.Label(app, textvariable=result_text, bg="skyblue1", fg="gray25", borderwidth=2, relief="solid", font=custom_font)
    result_label.place(relx=0.5, rely=0.78, anchor="center")

    result_text.set(f"Temperature: {temperature}°{choice.upper()}\nDescription: {description}\n"
                    f"Humidity: {humidity}%\nWind Speed: {wind_speed} m/s\nCountry: {country}")

    # Display weather icon
    icon_code = weather_data["weather"][0]["icon"]
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
    icon_data = requests.get(icon_url).content
    image_stream = BytesIO(icon_data)

    icon_label = tk.Label(app, bg="dodgerblue1", borderwidth=2, relief="solid")
    icon_label.place(relx=0.85, rely=0.17, anchor="center")

    photo = ImageTk.PhotoImage(Image.open(image_stream))
    icon_label.config(image=photo)
    icon_label.image = photo

# Create the main application window
app = tk.Tk()
app.title("Weather App")
app.geometry("612x408")
app.resizable(False, False)

# Load background image
background_image = Image.open("background.png")
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(app, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create GUI elements
city_label = tk.Label(app, text="Enter City:", bg="dodgerblue1", fg="white", font=custom_font)
city_entry = tk.Entry(app, fg="gray25", font=custom_font)
units_label = tk.Label(app, text="Temperature Unit:", bg="dodgerblue1", fg="white", font=custom_font)
units_var = tk.StringVar(value="Celsius")
units_menu = tk.OptionMenu(app, units_var, "Celsius", "Fahrenheit")
units_menu.config(font=("Helvetica", 12, "bold"), bg="gray75", fg="gray20", activebackground="gray65", activeforeground="gray20", pady=0)
get_weather_button = tk.Button(app, text="Get Weather", command=display_weather, bg="goldenrod1", fg="gray20", activebackground="orange", activeforeground="gray20", font=custom_font)
auto_detect_button = tk.Button(app, text="Auto Detect Location", command=get_weather_from_current_location, bg="goldenrod1", fg="gray20", activebackground="orange", activeforeground="gray20", font=custom_font)
result_text = tk.StringVar()

# Place GUI elements on the window
city_label.place(relx=0.1, rely=0.1)
city_entry.place(relx=0.38, rely=0.1)
units_label.place(relx=0.1, rely=0.2)
units_menu.place(relx=0.38, rely=0.2)
get_weather_button.place(relx=0.5, rely=0.45, anchor="center")
auto_detect_button.place(relx=0.5, rely=0.57, anchor="center")

# Start the main event loop
app.mainloop()