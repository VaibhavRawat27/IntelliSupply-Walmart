# modules/route_optimizer.py
import requests
import streamlit as st
import folium
import streamlit.components.v1 as components

def optimize_route(locations):
    try:
        coord_str = ";".join([f"{loc['CustomerLon']},{loc['CustomerLat']}" for loc in locations])
        url = f"http://router.project-osrm.org/route/v1/driving/{coord_str}?overview=full&geometries=geojson"
        response = requests.get(url)
        data = response.json()

        if 'routes' not in data:
            st.warning("No route found. Check coordinates.")
            return None

        geometry = data['routes'][0]['geometry']
        coords = geometry['coordinates']

        # Create Map
        start_lat = locations[0]['CustomerLat']
        start_lon = locations[0]['CustomerLon']
        m = folium.Map(location=[start_lat, start_lon], zoom_start=12, control_scale=True)

        # Add route
        folium.PolyLine([(lat, lon) for lon, lat in coords], color="blue", weight=5).add_to(m)

        # Add markers
        for loc in locations:
            folium.Marker(
                location=[loc['CustomerLat'], loc['CustomerLon']],
                popup=f"{loc['CustomerName']} (OrderID: {loc['OrderID']})",
                tooltip=loc['CustomerName'],
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)

        # Display map with iframe
        m.save("route_map.html")
        with open("route_map.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=550)

        return geometry

    except Exception as e:
        st.error(f"Error optimizing route: {e}")
        return None
