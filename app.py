# app.py - Railway ATD Monitor
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Railway ATD Monitor",
    page_icon="🚂",
    layout="wide"
)

# Title
st.title("🚂 Railway ATD Monitoring System")
st.markdown("### RDSO Alert Logic - Real-Time Demonstration")

# Create RDSO Master Chart data
tension_lengths = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800]
temperatures = list(range(0, 70, 5))

# Generate master data
master_data = []
for t in temperatures:
    row = [t]
    for length in tension_lengths:
        x_val = int(800 + (length / 10) + (t * 2.5))
        row.append(x_val)
    master_data.append(row)

columns = ['Temperature'] + [f'TL_{l}' for l in tension_lengths]
df_master = pd.DataFrame(master_data, columns=columns)

# Mast configuration
mast_config = pd.DataFrame({
    'Mast_ID': [f'Mast_{i}' for i in range(1, 9)],
    'Tension_Length': [200, 350, 450, 500, 600, 650, 700, 800],
    'Location': ['Station A', 'Station A', 'Station B', 'Station B', 'Station C', 'Station C', 'Station D', 'Station D']
})

# Interpolation function
def interpolate_target_x(tension_length, temperature):
    col_name = f'TL_{tension_length}'
    available_lengths = [int(c.split('_')[1]) for c in df_master.columns if c.startswith('TL_')]
    
    if col_name not in df_master.columns:
        closest = min(available_lengths, key=lambda x: abs(x - tension_length))
        col_name = f'TL_{closest}'
    
    temp_values = df_master['Temperature'].values
    
    if temperature <= temp_values[0]:
        return df_master.loc[0, col_name]
    if temperature >= temp_values[-1]:
        return df_master.loc[len(df_master)-1, col_name]
    
    lower_idx = np.searchsorted(temp_values, temperature) - 1
    upper_idx = lower_idx + 1
    
    T_low = temp_values[lower_idx]
    T_high = temp_values[upper_idx]
    X_low = df_master.loc[lower_idx, col_name]
    X_high = df_master.loc[upper_idx, col_name]
    
    X_target = X_low + (X_high - X_low) * (temperature - T_low) / (T_high - T_low)
    return round(X_target, 1)

# Alert function
def get_alert_level(delta_mm):
    if delta_mm <= 20:
        return "✅ HEALTHY", "green", "Normal operation"
    elif delta_mm <= 40:
        return "⚠️ MAINTENANCE REQUIRED", "yellow", "Schedule maintenance check"
    elif delta_mm <= 60:
        return "🚨 URGENT ALERT", "orange", "Immediate inspection required"
    else:
        return "🔴 CRITICAL FAILURE", "red", "EMERGENCY: Take immediate action!"

# Sidebar controls
with st.sidebar:
    st.header("🎮 Control Panel")
    
    selected_mast = st.selectbox("Select Mast", mast_config['Mast_ID'].tolist())
    mast_info = mast_config[mast_config['Mast_ID'] == selected_mast].iloc[0]
    tension_length = mast_info['Tension_Length']
    
    st.info(f"📍 Tension Length: {tension_length}m\n\n📍 Location: {mast_info['Location']}")
    
    temperature = st.slider("🌡️ Temperature (°C)", 0.0, 65.0, 35.0, 1.0)
    laser_reading = st.slider("🔍 Laser X-Reading (mm)", 0, 3000, 1200, 5)

# Calculate
expected_x = interpolate_target_x(tension_length, temperature)
delta = abs(laser_reading - expected_x)
status_text, color, description = get_alert_level(delta)

# Status display colors
color_map = {"green": "#28a745", "yellow": "#ffc107", "orange": "#fd7e14", "red": "#dc3545"}

# Main status indicator
st.markdown(f"""
<div style="background-color: {color_map[color]}; text-align: center; padding: 40px; border-radius: 20px; margin: 20px 0;">
    <div style="font-size: 56px; font-weight: bold; color: white;">{status_text}</div>
    <div style="font-size: 32px; color: white; margin-top: 10px;">Delta = {delta:.1f} mm</div>
    <div style="font-size: 18px; color: white; margin-top: 10px;">{description}</div>
</div>
""", unsafe_allow_html=True)

# Critical popup
if color == "red" and delta > 60:
    st.toast("🚨 CRITICAL FAILURE ALERT! Delta exceeds 60mm!", icon="🔴")

# Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Mast", selected_mast)
with col2:
    st.metric("Expected X", f"{expected_x:.1f} mm")
with col3:
    st.metric("Laser Reading", f"{laser_reading} mm", delta=f"{laser_reading - expected_x:+.1f} mm")
with col4:
    st.metric("Delta", f"{delta:.1f} mm")

# Data tables
with st.expander("📋 RDSO Master Chart"):
    st.dataframe(df_master, use_container_width=True)

with st.expander("🏗️ Mast Configuration"):
    st.dataframe(mast_config, use_container_width=True)

st.caption("Railway ATD Monitor - RDSO Alert Logic Demo | Runs locally | No internet required")