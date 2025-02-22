import requests  #  API calls
import pandas as pd  # CSV file operations
import time  # Add delays to API calls
from datetime import datetime  # Handle date and time
import os  # Checking file existence

def fetch_weather_data(api_key, city):
    """
    Fetches current weather data using the Weatherbit API.

    Parameters:
    - api_key 
    - city 

    Returns:
    - dict: A dictionary containing the weather data
    """
    # API URL 
    url = f"https://api.weatherbit.io/v2.0/current?city={city}&key={api_key}&units=M"
    # GET request to fetch weather data from the API
    response = requests.get(url)
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        # Get relevant weather data and store it in a dictionary
        weather_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Current timestamp 
            "city": city,  # City name
            "temperature": data["data"][0]["temp"],  # Temperature in Celsius
            "humidity": data["data"][0]["rh"],  # Humidity percentage
            "weather": data["data"][0]["weather"]["description"]  # Weather description
        }
        return weather_data  # Return the weather data as a dictionary
    else:
        # Error handling 
        print(f"Error: {response.status_code}")
        return None  # Return none if the API request fails

def write_to_csv(data, file_name):
    """
    Writes weather data to a CSV file.

    Parameters:
    - data 
    - file_name 
    """
    # Convert the data dictionary to a DataFrame
    df = pd.DataFrame([data])
    # Check if the file exists and is not empty
    file_exists = os.path.isfile(file_name) and os.path.getsize(file_name) > 0
    # Write the DataFrame to the CSV file
    df.to_csv(file_name, mode='a', header=not file_exists, index=False)

def main():
    """
    Main function to fetch weather data every 60 seconds and write it to a CSV file.
    """
    api_key = "eb740340da3846059dc4264b1962d705"  
    city = "Manila" 
    file_name = "weather_data.csv"  

    while True:
        # Fetch weather data 
        weather_data = fetch_weather_data(api_key, city)
        # Check if the weather data is not none
        if weather_data:
            # Output for the console (weather data)
            print(f"Fetched Data: {weather_data}")
            # Weather data to the CSV file
            write_to_csv(weather_data, file_name)
        else:
            # Error message 
            print("Failed to fetch weather data.")
        # 60 second interval for API call
        time.sleep(60)

if __name__ == "__main__":
    main()  