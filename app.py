# ------------------------------------------------
# AI SMART TRAFFIC MANAGEMENT SYSTEM - DELHI NCR
# ------------------------------------------------

import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import pydeck as pdk

from iot_module import get_traffic_data
from ml_model import predict_traffic
from route_optimizer import find_fastest_route


# ------------------------------------------------
# PAGE SETTINGS
# ------------------------------------------------

st.set_page_config(
    page_title="AI Smart Traffic System",
    layout="wide"
)


# ------------------------------------------------
# CUSTOM UI STYLE
# ------------------------------------------------

st.markdown("""
<style>

body {
background: linear-gradient(135deg,#020617,#0f172a);
}

h1 {
color:#22c55e;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------
# HEADER SECTION
# ------------------------------------------------

st.title("🚦 AI Smart Traffic Management System — Delhi NCR")

current_time = datetime.datetime.now().strftime("%d %B %Y | %H:%M:%S")

st.caption(f"System Time: {current_time}")

st.write(
"This dashboard demonstrates how IoT sensors, Machine Learning, and Graph Algorithms monitor traffic congestion in Delhi NCR."
)


# ------------------------------------------------
# IOT TRAFFIC SENSOR DATA
# ------------------------------------------------

st.subheader("📡 Live Traffic Sensors")

traffic = get_traffic_data()

df = pd.DataFrame(
traffic.items(),
columns=["Location","Vehicle Count"]
)


# ------------------------------------------------
# DASHBOARD METRICS
# ------------------------------------------------

col1,col2,col3 = st.columns(3)

col1.metric("Active Junctions",len(df))
col2.metric("Highest Traffic",max(df["Vehicle Count"]))
col3.metric("Lowest Traffic",min(df["Vehicle Count"]))

st.info("System Status: All IoT traffic sensors operational.")


# ------------------------------------------------
# SENSOR DATA TABLE + BAR CHART
# ------------------------------------------------

col1,col2 = st.columns(2)

with col1:
    st.dataframe(df,use_container_width=True)

with col2:
    st.bar_chart(df.set_index("Location"),use_container_width=True)


st.divider()


# ------------------------------------------------
# MACHINE LEARNING TRAFFIC PREDICTION
# ------------------------------------------------

st.subheader("🤖 AI Traffic Prediction")

vehicle_input = st.slider(
"Select vehicle count",
10,
80,
30
)

prediction = predict_traffic(vehicle_input)

st.success(f"Predicted Traffic Level: {prediction}")

if prediction == "High":
    st.error("Heavy congestion expected. Suggested alternate routes.")

elif prediction == "Medium":
    st.warning("Moderate traffic detected.")

else:
    st.success("Traffic conditions are smooth.")


st.divider()


# ------------------------------------------------
# WEATHER IMPACT
# ------------------------------------------------

st.subheader("🌦 Weather Impact")

weather = st.selectbox(
"Current Weather",
["Clear","Rain","Fog"]
)

if weather == "Rain":
    st.warning("Rain may increase traffic congestion.")

elif weather == "Fog":
    st.warning("Fog may reduce visibility and slow traffic.")


st.divider()


# ------------------------------------------------
# TRAFFIC ALERTS
# ------------------------------------------------

st.subheader("🚨 Traffic Alerts")

alerts = [
"Accident reported near AIIMS Ring Road",
"Heavy congestion detected at Gurgaon Cyber City",
"Road maintenance ongoing near Noida Sector 62"
]

for alert in alerts:
    st.warning(alert)


st.divider()


# ------------------------------------------------
# DELHI NCR TRAFFIC MAP
# ------------------------------------------------

st.subheader("🗺 Delhi NCR Traffic Map")

locations = {
"Connaught Place":[28.6315,77.2167],
"AIIMS":[28.5672,77.2100],
"Noida Sector 62":[28.6280,77.3649],
"Gurgaon Cyber City":[28.4947,77.0890]
}

map_rows=[]

for location,count in traffic.items():

    lat,lon = locations.get(location,[28.61,77.20])

    map_rows.append({
        "location":location,
        "lat":lat,
        "lon":lon,
        "traffic":count
    })

map_data=pd.DataFrame(map_rows)


layer = pdk.Layer(
"ScatterplotLayer",
map_data,
get_position='[lon,lat]',
get_radius='traffic * 40',
get_fill_color='[255,0,0,160]',
pickable=True
)

view = pdk.ViewState(
latitude=28.61,
longitude=77.20,
zoom=10,
pitch=45
)

deck = pdk.Deck(
layers=[layer],
initial_view_state=view,
tooltip={"text":"{location}\nTraffic:{traffic}"}
)

st.pydeck_chart(deck)


st.divider()


# ------------------------------------------------
# TRAFFIC HEATMAP
# ------------------------------------------------

st.subheader("🔥 Traffic Congestion Heatmap")

heatmap_df = df.copy()
heatmap_df["Index"] = 1

heatmap_data = heatmap_df.pivot_table(
values="Vehicle Count",
index="Location",
columns="Index"
)

fig = px.imshow(
heatmap_data,
color_continuous_scale="reds"
)

st.plotly_chart(fig)


st.divider()


# ------------------------------------------------
# EMERGENCY ROUTE OPTIMIZER
# ------------------------------------------------

st.subheader("🚑 Emergency Route Optimizer")

start = st.selectbox(
"Start Location",
["AIIMS","Connaught Place"]
)

destination = st.selectbox(
"Destination",
["Connaught Place","Noida Sector 62","Gurgaon Cyber City"]
)

if st.button("Find Fastest Route"):

    route,cost = find_fastest_route(start,destination)

    if route is None:
        st.error("No route available between selected locations")

    else:

        minutes = cost * 15
        hours = round(minutes / 60,2)

        st.info(f"Recommended Route: {' → '.join(route)}")

        st.success(f"Estimated Travel Time: approx {hours} hours")


# ------------------------------------------------
# FOOTER
# ------------------------------------------------

st.caption("AI Smart Traffic System | Built using IoT Sensors, Machine Learning, and Graph Algorithms")