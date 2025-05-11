import folium
from streamlit_folium import st_folium
import geocoder
import requests

def show_nearby_doctors():
    """Show nearby pediatricians using Leaflet and OpenStreetMap"""
    st.sidebar.title("🏥 Find Nearby Pediatricians")
    
    # Get user's location
    try:
        g = geocoder.ip('me')
        user_lat, user_lng = g.latlng
        location_name = "Your Location"
    except:
        st.sidebar.warning("Could not automatically detect your location. Using default coordinates.")
        user_lat, user_lng = 40.7128, -74.0060  # Default to New York
        location_name = "Default Location"
    
    # Create map centered at user's location
    m = folium.Map(location=[user_lat, user_lng], zoom_start=13)
    
    # Add user's location marker
    folium.Marker(
        [user_lat, user_lng],
        popup=location_name,
        tooltip="Your Location",
        icon=folium.Icon(color="blue", icon="user")
    ).add_to(m)
    
    # Search for nearby pediatricians using Overpass API (OpenStreetMap)
    try:
        overpass_url = "http://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json];
        (
          node["amenity"="doctors"]["healthcare"="doctor"](around:5000,{user_lat},{user_lng});
          node["amenity"="hospital"](around:5000,{user_lat},{user_lng});
          node["amenity"="clinic"](around:5000,{user_lat},{user_lng});
        );
        out center;
        """
        response = requests.get(overpass_url, params={'data': overpass_query})
        data = response.json()
        
        # Add markers for each healthcare facility
        doctors_found = 0
        for element in data.get('elements', []):
            if 'tags' in element:
                name = element['tags'].get('name', 'Unknown')
                amenity = element['tags'].get('amenity', 'facility')
                
                # Only count pediatricians if specified in tags
                is_pediatric = 'pediatric' in name.lower() or 'children' in name.lower()
                
                if amenity == 'doctors' and not is_pediatric:
                    continue  # Skip non-pediatric doctors
                    
                lat = element.get('lat', element.get('center', {}).get('lat'))
                lon = element.get('lon', element.get('center', {}).get('lon'))
                
                if lat and lon:
                    doctors_found += 1
                    icon_color = "green" if is_pediatric else "red"
                    icon_type = "child" if is_pediatric else "plus-sign"
                    
                    folium.Marker(
                        [lat, lon],
                        popup=f"<b>{name}</b><br>{amenity}",
                        tooltip=name,
                        icon=folium.Icon(color=icon_color, icon=icon_type, prefix="glyphicon")
                    ).add_to(m)
        
        if doctors_found == 0:
            st.sidebar.warning("No pediatricians found nearby. Showing all healthcare facilities.")
    except Exception as e:
        st.sidebar.error(f"Error fetching healthcare facilities: {str(e)}")
    
    # Display the map
    st_folium(m, width=350, height=400)