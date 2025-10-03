import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # API Key
        self.api_key = "3831b2a593b0fa5cd66538cc2b9133d5" 
        
        
        # Create GUI elements
        self.setup_gui()
        
    def setup_gui(self):
        # Style configuration
        style = ttk.Style()
        style.configure('TLabel', padding=5, font=('Helvetica', 12))
        style.configure('TButton', padding=5, font=('Helvetica', 10))
        style.configure('TEntry', padding=5)

        # Search Frame
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=20)

        self.city_entry = ttk.Entry(search_frame, width=30, font=('Helvetica', 12))
        self.city_entry.pack(side=tk.LEFT, padx=5)
        self.city_entry.insert(0, "Enter city name")
        self.city_entry.bind('<FocusIn>', lambda e: self.city_entry.delete(0, tk.END))

        search_button = ttk.Button(search_frame, text="Search", command=self.get_weather)
        search_button.pack(side=tk.LEFT, padx=5)

        # Weather Info Frame
        self.weather_frame = ttk.Frame(self.root)
        self.weather_frame.pack(pady=20)

        # Labels for weather information
        self.temp_label = ttk.Label(self.weather_frame, text="", font=('Helvetica', 20))
        self.temp_label.pack()

        self.city_label = ttk.Label(self.weather_frame, text="", font=('Helvetica', 16))
        self.city_label.pack()

        self.weather_label = ttk.Label(self.weather_frame, text="", font=('Helvetica', 14))
        self.weather_label.pack()

        self.humidity_label = ttk.Label(self.weather_frame, text="", font=('Helvetica', 12))
        self.humidity_label.pack()

        self.wind_label = ttk.Label(self.weather_frame, text="", font=('Helvetica', 12))
        self.wind_label.pack()

    def get_weather(self):
        city = self.city_entry.get()
        
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return

        try:
            # Make API request
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                # Extract weather information
                temp = data['main']['temp']
                weather = data['weather'][0]['description']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                city_name = data['name']
                country = data['sys']['country']

                # Update labels
                self.temp_label.config(text=f"{temp:.1f}°C")
                self.city_label.config(text=f"{city_name}, {country}")
                self.weather_label.config(text=f"Weather: {weather.capitalize()}")
                self.humidity_label.config(text=f"Humidity: {humidity}%")
                self.wind_label.config(text=f"Wind Speed: {wind_speed} m/s")
            else:
                messagebox.showerror("Error", f"Error: {data['message']}")

        except requests.RequestException:
            messagebox.showerror("Error", "Error fetching weather data. Please check your internet connection.")
        except KeyError:
            messagebox.showerror("Error", "Error parsing weather data")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()