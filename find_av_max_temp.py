import concurrent.futures
import requests
import ast

# Cities and corresponding API urls
locations_dict = {
    "Salt Lake City": "https://www.metaweather.com/api/location/2487610/",
    "Los Angeles": "https://www.metaweather.com/api/location/2442047/",
    "Boise": "https://www.metaweather.com/api/location/2366355/"
}

# call API and calculate average max temperature
def find_average_max_temp(city_url, timeout = 10):
    response = requests.get(city_url, timeout = timeout)
    byte = response.content     # convert bytes object to dict
    consolidated_weather = ast.literal_eval(byte.decode('utf-8'))["consolidated_weather"]
    num_days = len(consolidated_weather)
    av_max = sum([i["max_temp"] for i in consolidated_weather]) / num_days
    return av_max


with concurrent.futures.ThreadPoolExecutor(max_workers=len(locations_dict)) as executor:
    futures = []

    cities=[]
    [cities.extend([k]) for k,v in locations_dict.items()] # create list of cities

    urls = []
    [urls.extend([v])for k,v in locations_dict.items()] # create list of urls

    for url in urls:
        futures.append(executor.submit(find_average_max_temp, city_url=url))

    for city, future in enumerate(concurrent.futures.as_completed(futures)):
        print(cities[city] + " Average Max Temp: " + str(future.result())) # print results