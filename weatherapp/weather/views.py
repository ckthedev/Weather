import json
import urllib.request
import urllib.error
from django.shortcuts import render

def home(request):
    context = {}
    
    if request.method == 'POST':
        # Get the city name from the user input and clean it
        city = request.POST.get('city', '').strip()
        
        if city:
            # Your API key from OpenWeatherMap
            api_key = '7b9f53be4ca5e9447b8c24cbee509517'
            
            # Create the API URL
            api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={api_key}'
            
            try:
                # Retrieve weather data from the API
                source = urllib.request.urlopen(api_url).read()
                # Convert JSON data into Python dictionary
                list_of_data = json.loads(source)
                
                # Create context dictionary with weather details
                context = {
                    'city': city,
                    'country_code': str(list_of_data['sys']['country']),
                    'coordinate': str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
                    'temp': str(list_of_data['main']['temp']) + '°F',
                    'pressure': str(list_of_data['main']['pressure']) + ' hPa',
                    'humidity': str(list_of_data['main']['humidity']) + '%',
                }
            except urllib.error.HTTPError as e:
                if e.code == 401:
                    context['error'] = "Unauthorized: Invalid API key."
                elif e.code == 404:
                    context['error'] = "City not found. Please check the spelling."
                else:
                    context['error'] = f"HTTP error occurred: {e.reason}"
            except Exception as e:
                context['error'] = f"Error occurred: {str(e)}"
        else:
            context['error'] = "Please enter a valid city name."

    return render(request, 'index.html', context)
