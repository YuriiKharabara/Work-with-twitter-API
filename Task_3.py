from matplotlib.pyplot import get
import hidden
import requests
import json
from geopy.geocoders import Nominatim
from pprint import pprint
import folium
from flask import Flask, render_template, redirect, render_template, request, url_for
app=Flask(__name__)







def get_info_API(url):
    authorization = {"Authorization": "Bearer " +
                     hidden.oauth()['token_secret']}
    response = requests.get(url, headers=authorization,
                            params={'user.fields': 'location'})
    return response.json()


def get_followers(url):
    authorization = {"Authorization": "Bearer " +
                     hidden.oauth()['token_secret']}
    response = requests.get(url, headers=authorization,
                            params={'user.fields': 'location'})
    return response.json()


def get_coords(place):
    geolocator = Nominatim(user_agent="main.py", timeout=10)
    location = geolocator.geocode(place)
    if location==None:
        return None
    return location.latitude, location.longitude
# @app.route('/add')
# def get_username():
#     main(user_name)
#     return render_template('Map.html')
@app.route('/', methods=("GET", "POST"))
def get_info():
    if request.method == 'POST':
        user_name=request.form["user"]
        main(user_name)
        return render_template("Map.html")
    return render_template("main_page.html")

@app.route('/map', methods=("GET", "POST"))
def main(username):
    information = get_info_API(
        f'https://api.twitter.com/2/users/by/username/{username}')
    id = information['data']['id']
    followers = get_followers(
        f'https://api.twitter.com/2/users/{id}/following')
    print(followers)
    coords = {}
    for i in followers['data']:
        try:
            coords_place = get_coords(i['location'])
            if coords_place!=None:
                if coords_place not in coords:
                    coords[coords_place] = [i['name']]
                else:
                    coords[coords_place].append(i['name'])
                pprint(coords)
        except KeyError:
            continue
    map = folium.Map()
    markers_of_followers = folium.FeatureGroup(name=f"followers of {information['data']['name']}")
    for i in coords:
        markers_of_followers.add_child(folium.Marker(location=[i[0], i[1]], popup=',\n\n'.join(coords[i]), icon=folium.Icon()))
    map.add_child(markers_of_followers)
    map.add_child(folium.LayerControl())
    map.save('templates/Map.html')
    return render_template('Map.html')

app.run(debug=True)
