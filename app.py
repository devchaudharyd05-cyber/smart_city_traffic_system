# ------------------------------------------------
# AI SMART TRAFFIC ASSISTANT - DELHI NCR
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
    page_title="Delhi Smart Traffic Assistant",
    layout="wide"
)

# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.title("🚦 Delhi Smart Traffic Assistant")

current_time = datetime.datetime.now()

st.caption(
f"Current Time: {current_time.strftime('%d %B %Y | %H:%M')}"
)

st.write(
"This dashboard helps Delhi commuters plan travel using traffic analytics, machine learning prediction, and route optimization."
)


# ------------------------------------------------
# BEST TRAVEL TIME ADVICE
# ------------------------------------------------

st.subheader("🕒 Best Time to Travel")

hour = current_time.hour

if 6 <= hour < 8:
    st.success("Traffic is light. Good time to travel.")

elif 8 <= hour < 11:
    st.error("Morning rush hour. Heavy traffic expected.")

elif 11 <= hour < 16:
    st.warning("Moderate traffic conditions.")

elif 16 <= hour < 21:
    st.error("Evening peak traffic. Avoid major roads.")

else:
    st.success("Night travel is smoother.")


st.divider()


# ------------------------------------------------
# LIVE TRAFFIC SENSOR DATA (IoT Simulation)
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


# ------------------------------------------------
# SENSOR DATA VISUALIZATION
# ------------------------------------------------

col1,col2 = st.columns(2)

with col1:
    st.dataframe(df,use_container_width=True)

with col2:
    st.bar_chart(df.set_index("Location"),use_container_width=True)


st.divider()


# ------------------------------------------------
# TRAFFIC TREND GRAPH
# ------------------------------------------------

st.subheader("📈 Traffic Trend")

trend_df = pd.DataFrame({
"Time":["6AM","9AM","12PM","3PM","6PM","9PM"],
"Traffic":[20,50,40,35,70,45]
})

st.line_chart(trend_df.set_index("Time"))


st.divider()


# ------------------------------------------------
# MACHINE LEARNING TRAFFIC PREDICTION
# ------------------------------------------------

st.subheader("🤖 Traffic Prediction")

vehicle_input = st.slider(
"Vehicle Count",
10,
80,
30
)

prediction = predict_traffic(vehicle_input)

st.info(f"Predicted Traffic Level: {prediction}")

if prediction == "High":
    st.error("Heavy congestion expected")

elif prediction == "Medium":
    st.warning("Moderate traffic expected")

else:
    st.success("Traffic flow smooth")


st.divider()


# ------------------------------------------------
# TRAVEL MODE SUGGESTION
# ------------------------------------------------

st.subheader("🚗 Suggested Travel Mode")

mode = st.selectbox(
"Select Travel Mode",
["Car","Bike","Metro"]
)

if mode == "Metro":
    st.success("Metro is recommended during peak traffic hours.")

elif mode == "Bike":
    st.info("Bike may help avoid heavy traffic in narrow roads.")

else:
    st.warning("Car travel may face congestion during peak hours.")


st.divider()


# ------------------------------------------------
# FUEL ESTIMATION
# ------------------------------------------------

st.subheader("⛽ Estimated Fuel Usage")

distance = st.slider(
"Estimated Distance (km)",
1,
30,
10
)

fuel = distance / 15

st.write(f"Estimated Fuel Required: {round(fuel,2)} liters")


st.divider()


# ------------------------------------------------
# DELHI TRAFFIC MAP
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
zoom=10
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
# ROUTE OPTIMIZER
# ------------------------------------------------

st.subheader("🚑 Route Planner")

start = st.selectbox(
"Start Location",
["AIIMS","Connaught Place"]
)

destination = st.selectbox(
"Destination",
[
"Connaught Place",
"Noida Sector 62",
"Gurgaon Cyber City"
]
)

if st.button("Find Best Route"):

    route,cost = find_fastest_route(start,destination)

    if route is None:

        st.error("No route available.")

    else:

        minutes = cost * 15

        hours = round(minutes/60,2)

        st.info(
f"Suggested Route: {' → '.join(route)}"
)

        st.success(
f"Estimated Travel Time: approx {hours} hours"
)


# ------------------------------------------------
# TRAFFIC TIPS
# ------------------------------------------------

st.subheader("🚦 Traffic Tips for Delhi")

st.write("""
• Avoid Ring Road during peak hours (8–11 AM, 5–9 PM)  
• Use Delhi Metro for faster travel  
• Plan travel early morning or late night  
• Check traffic updates before leaving  
""")


# ------------------------------------------------
# FOOTER
# ------------------------------------------------

st.caption(
"Delhi Smart Traffic Assistant | Built using IoT, Machine Learning and Graph Algorithms"
)