# app.py - Railway ATD Monitor with X and Y Parameters
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Railway ATD Monitor - X & Y Parameters",
    page_icon="🚂",
    layout="wide"
)

# ============================================================================
# RDSO MASTER CHART DATA - X Values (mm between 2 moving pulleys)
# ============================================================================
x_data = {
    "Temperature": [-5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90],
    50: [1334, 1330, 1326, 1321, 1317, 1313, 1309, 1304, 1300, 1296, 1292, 1287, 1283, 1279, 1275, 1270, 1266, 1262, 1258, 1253],
    100: [1368, 1360, 1351, 1343, 1334, 1326, 1317, 1309, 1300, 1292, 1283, 1275, 1266, 1258, 1249, 1241, 1232, 1224, 1215, 1207],
    150: [1402, 1389, 1377, 1364, 1351, 1338, 1326, 1313, 1300, 1287, 1275, 1262, 1249, 1236, 1224, 1211, 1198, 1185, 1173, 1160],
    200: [1436, 1419, 1402, 1385, 1368, 1351, 1334, 1317, 1300, 1283, 1266, 1249, 1232, 1215, 1198, 1181, 1164, 1147, 1130, 1113],
    250: [1470, 1449, 1428, 1406, 1385, 1364, 1343, 1321, 1300, 1279, 1258, 1236, 1215, 1194, 1173, 1151, 1130, 1109, 1088, 1066],
    300: [1504, 1479, 1453, 1428, 1402, 1377, 1351, 1326, 1301, 1275, 1249, 1224, 1198, 1173, 1147, 1122, 1096, 1071, 1045, 1020],
    350: [1538, 1508, 1479, 1449, 1419, 1390, 1360, 1330, 1300, 1270, 1241, 1211, 1181, 1151, 1122, 1092, 1062, 1032, 1003, 973],
    400: [1572, 1538, 1504, 1470, 1436, 1402, 1368, 1334, 1300, 1266, 1232, 1198, 1164, 1130, 1096, 1062, 1028, 994, 960, 926],
    450: [1606, 1568, 1530, 1491, 1453, 1415, 1377, 1338, 1300, 1262, 1224, 1185, 1147, 1109, 1071, 1032, 994, 956, 918, 879],
    500: [1640, 1598, 1555, 1513, 1470, 1428, 1385, 1343, 1300, 1258, 1215, 1173, 1130, 1088, 1045, 1003, 960, 918, 875, 833],
    550: [1674, 1632, 1581, 1534, 1487, 1440, 1394, 1347, 1303, 1253, 1207, 1160, 1113, 1066, 1020, 973, 926, 879, 833, 786],
    600: [1708, 1667, 1606, 1555, 1504, 1453, 1402, 1351, 1300, 1249, 1198, 1147, 1096, 1045, 994, 943, 892, 841, 790, 739],
    650: [1742, 1697, 1632, 1576, 1521, 1466, 1411, 1355, 1300, 1245, 1190, 1134, 1079, 1024, 969, 913, 858, 803, 748, 692],
    700: [1776, 1731, 1657, 1598, 1538, 1479, 1419, 1360, 1300, 1241, 1181, 1122, 1062, 1003, 943, 884, 824, 765, 705, 646],
    750: [1810, 1764, 1683, 1619, 1555, 1491, 1428, 1364, 1300, 1236, 1173, 1109, 1045, 981, 918, 854, 790, 726, 663, 599],
}

# ============================================================================
# RDSO MASTER CHART DATA - Y Values (mm from top of Muff to bottom of Counter weight)
# ============================================================================
y_data = {
    "Temperature": [-5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90],
    50: [2702, 2689, 2677, 2664, 2651, 2638, 2626, 2613, 2600, 2587, 2575, 2562, 2549, 2536, 2524, 2511, 2498, 2485, 2473, 2460],
    100: [2804, 2779, 2753, 2728, 2702, 2677, 2651, 2646, 2600, 2575, 2549, 2524, 2498, 2473, 2447, 2422, 2396, 2371, 2345, 2320],
    150: [2906, 2868, 2830, 2791, 2753, 2715, 2677, 2683, 2600, 2562, 2524, 2485, 2447, 2409, 2371, 2332, 2294, 2256, 2218, 2179],
    200: [3008, 2957, 2906, 2855, 2804, 2753, 2702, 2651, 2600, 2549, 2498, 2447, 2396, 2345, 2294, 2243, 2192, 2141, 2090, 2039],
    250: [3110, 3046, 2983, 2919, 2855, 2791, 2728, 2664, 2600, 2536, 2473, 2409, 2345, 2281, 2218, 2154, 2090, 2026, 1963, 1899],
    300: [3212, 3136, 3059, 2983, 2906, 2830, 2753, 2677, 2601, 2524, 2447, 2371, 2294, 2218, 2141, 2065, 1988, 1912, 1835, 1759],
    350: [3314, 3225, 3136, 3066, 2957, 2886, 2779, 2698, 2600, 2511, 2422, 2332, 2233, 2154, 2055, 1975, 1886, 1797, 1708, 1618],
    400: [3416, 3314, 3221, 3136, 3008, 2936, 2840, 2760, 2600, 2498, 2396, 2294, 2192, 2090, 1988, 1886, 1784, 1682, 1580, 1478],
    450: [3518, 3403, 3298, 3174, 3059, 2994, 2890, 2815, 2600, 2485, 2371, 2256, 2141, 2026, 1912, 1797, 1682, 1580, 1478, 1376],
    500: [3620, 3493, 3365, 3238, 3110, 3053, 2936, 2870, 2600, 2473, 2345, 2218, 2090, 1963, 1835, 1708, 1580, 1478, 1376, 1274],
    550: [3722, 3582, 3442, 3301, 3161, 3101, 2981, 2920, 2606, 2460, 2320, 2179, 2039, 1899, 1759, 1618, 1478, 1376, 1274, 1172],
    600: [3824, 3671, 3518, 3365, 3212, 3156, 3021, 2965, 2600, 2447, 2294, 2141, 1988, 1835, 1682, 1529, 1376, 1274, 1172, 1070],
    650: [3926, 3760, 3595, 3429, 3263, 3205, 3079, 3011, 2600, 2434, 2269, 2103, 1937, 1771, 1606, 1440, 1274, 1172, 1070, 947],
    700: [4028, 3850, 3671, 3493, 3314, 3259, 3136, 3056, 2600, 2422, 2243, 2065, 1886, 1708, 1529, 1351, 1172, 1070, 947, 698],
    750: [4130, 3939, 3748, 3556, 3365, 3314, 3174, 3096, 2600, 2409, 2218, 2026, 1835, 1644, 1453, 1261, 1070, 947, 698, 498],
}

# Convert to DataFrames
df_x = pd.DataFrame(x_data)
df_y = pd.DataFrame(y_data)

# Mast Configuration
tension_lengths = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750]

mast_config = pd.DataFrame({
    'Mast_ID': [f'Mast_{i}' for i in range(1, 11)],
    'Tension_Length': [200, 250, 300, 350, 400, 450, 500, 550, 600, 650],
    'Location': ['Station A', 'Station A', 'Station B', 'Station B', 'Station C', 
                 'Station C', 'Station D', 'Station D', 'Station E', 'Station E']
})

# ============================================================================
# INTERPOLATION FUNCTIONS
# ============================================================================
def interpolate_value(df, tension_length, temperature):
    """Generic interpolation function for X or Y values"""
    temp_values = df['Temperature'].values
    
    # Find the column for this tension length
    if tension_length not in df.columns:
        closest = min(tension_lengths, key=lambda x: abs(x - tension_length))
        tension_length = closest
    
    # Boundary checks
    if temperature <= temp_values[0]:
        return df.loc[0, tension_length]
    if temperature >= temp_values[-1]:
        return df.loc[len(df)-1, tension_length]
    
    # Find surrounding temperatures
    lower_idx = np.searchsorted(temp_values, temperature) - 1
    upper_idx = lower_idx + 1
    
    T_low = temp_values[lower_idx]
    T_high = temp_values[upper_idx]
    V_low = df.loc[lower_idx, tension_length]
    V_high = df.loc[upper_idx, tension_length]
    
    # Linear interpolation
    result = V_low + (V_high - V_low) * (temperature - T_low) / (T_high - T_low)
    return round(result, 1)

def get_alert_level(delta_x, delta_y):
    """Determine alert level based on both X and Y deltas"""
    # Use the maximum delta for alert level
    max_delta = max(delta_x, delta_y)
    
    # Alert logic as per RDSO specifications
    if max_delta <= 20:
        return "✅ HEALTHY", "green", f"Delta: {max_delta:.1f}mm (X: {delta_x:.1f}mm, Y: {delta_y:.1f}mm)", max_delta
    elif max_delta <= 40:
        return "⚠️ MAINTENANCE REQUIRED", "yellow", f"Delta: {max_delta:.1f}mm (X: {delta_x:.1f}mm, Y: {delta_y:.1f}mm)", max_delta
    elif max_delta <= 60:
        return "🚨 URGENT ALERT", "orange", f"Delta: {max_delta:.1f}mm (X: {delta_x:.1f}mm, Y: {delta_y:.1f}mm)", max_delta
    else:
        return "🔴 CRITICAL FAILURE", "red", f"Delta: {max_delta:.1f}mm (X: {delta_x:.1f}mm, Y: {delta_y:.1f}mm)", max_delta

# ============================================================================
# MAIN UI
# ============================================================================
st.title("🚂 Railway ATD Monitoring System")
st.markdown("### RDSO Alert Logic - X & Y Parameter Monitoring")
st.caption("Real-time monitoring of both X (moving pulleys) and Y (counter weight) parameters")

# Sidebar controls
with st.sidebar:
    st.header("🎮 Control Panel")
    
    selected_mast = st.selectbox("Select Mast", mast_config['Mast_ID'].tolist())
    mast_info = mast_config[mast_config['Mast_ID'] == selected_mast].iloc[0]
    tension_length = mast_info['Tension_Length']
    
    st.info(f"📍 **Mast Details**\n\n- Tension Length: {tension_length}m\n- Location: {mast_info['Location']}")
    
    st.divider()
    
    st.subheader("🌡️ Temperature Settings")
    temperature = st.slider("Temperature (°C)", -5.0, 90.0, 35.0, 1.0)
    
    st.divider()
    
    st.subheader("📏 Sensor Readings (Simulated)")
    x_reading = st.slider("X Parameter (mm) - Between moving pulleys", 400, 2000, 1300, 5)
    y_reading = st.slider("Y Parameter (mm) - Counter weight position", 500, 4500, 2600, 5)
    
    st.divider()
    
    st.subheader("🎯 Demo Presets")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🟢 Healthy (Delta ≤ 20mm)", use_container_width=True):
            expected_x = interpolate_value(df_x, tension_length, temperature)
            expected_y = interpolate_value(df_y, tension_length, temperature)
            st.session_state.x_reading = expected_x + 10
            st.session_state.y_reading = expected_y + 10
            st.rerun()
    with col2:
        if st.button("🔴 Critical (Delta > 60mm)", use_container_width=True):
            expected_x = interpolate_value(df_x, tension_length, temperature)
            expected_y = interpolate_value(df_y, tension_length, temperature)
            st.session_state.x_reading = expected_x + 70
            st.session_state.y_reading = expected_y + 70
            st.rerun()

# Initialize session state
if 'x_reading' not in st.session_state:
    st.session_state.x_reading = x_reading
    st.session_state.y_reading = y_reading
else:
    x_reading = st.session_state.x_reading
    y_reading = st.session_state.y_reading

# ============================================================================
# CALCULATIONS
# ============================================================================
expected_x = interpolate_value(df_x, tension_length, temperature)
expected_y = interpolate_value(df_y, tension_length, temperature)

delta_x = abs(x_reading - expected_x)
delta_y = abs(y_reading - expected_y)

status_text, color, details, max_delta = get_alert_level(delta_x, delta_y)

# ============================================================================
# VISUAL ALERT INDICATOR
# ============================================================================
# Color mapping for the 4 alert levels
color_map = {
    "green": "#00FF00",      # Bright Green for Healthy
    "yellow": "#FFFF00",     # Yellow for Maintenance Required  
    "orange": "#FFA500",     # Orange for Urgent Alert
    "red": "#FF0000"         # Red for Critical Failure
}

# Display the large status indicator
st.markdown(f"""
<div style="background-color: {color_map[color]}; text-align: center; padding: 50px; border-radius: 25px; margin: 20px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
    <div style="font-size: 64px; font-weight: bold; color: {'#000000' if color == 'yellow' else '#FFFFFF'}; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
        {status_text}
    </div>
    <div style="font-size: 32px; color: {'#000000' if color == 'yellow' else '#FFFFFF'}; margin-top: 15px;">
        Max Delta = {max_delta:.1f} mm
    </div>
    <div style="font-size: 18px; color: {'#000000' if color == 'yellow' else '#FFFFFF'}; margin-top: 10px;">
        {details}
    </div>
</div>
""", unsafe_allow_html=True)

# Critical popup for demo
if color == "red" and max_delta > 60:
    st.toast("🚨 **CRITICAL FAILURE ALERT!** 🚨\nDelta exceeds 60mm - Immediate action required!", icon="🔴")

# ============================================================================
# THRESHOLD LEGEND
# ============================================================================
st.markdown("### 📊 Alert Thresholds")
threshold_cols = st.columns(4)
with threshold_cols[0]:
    st.markdown("🟢 **0 – 20 mm**\n✅ HEALTHY")
with threshold_cols[1]:
    st.markdown("🟡 **21 – 40 mm**\n⚠️ MAINTENANCE REQUIRED")
with threshold_cols[2]:
    st.markdown("🟠 **41 – 60 mm**\n🚨 URGENT ALERT")
with threshold_cols[3]:
    st.markdown("🔴 **> 60 mm**\n🔴 CRITICAL FAILURE")

# ============================================================================
# METRICS DISPLAY
# ============================================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 X Parameter (Moving Pulleys)")
    x_col1, x_col2, x_col3 = st.columns(3)
    with x_col1:
        st.metric("Expected X", f"{expected_x:.1f} mm")
    with x_col2:
        st.metric("Reading X", f"{x_reading} mm", delta=f"{x_reading - expected_x:+.1f} mm", delta_color="inverse")
    with x_col3:
        st.metric("Delta X", f"{delta_x:.1f} mm")

with col2:
    st.subheader("📊 Y Parameter (Counter Weight)")
    y_col1, y_col2, y_col3 = st.columns(3)
    with y_col1:
        st.metric("Expected Y", f"{expected_y:.1f} mm")
    with y_col2:
        st.metric("Reading Y", f"{y_reading} mm", delta=f"{y_reading - expected_y:+.1f} mm", delta_color="inverse")
    with y_col3:
        st.metric("Delta Y", f"{delta_y:.1f} mm")

# ============================================================================
# CALCULATION DETAILS
# ============================================================================
with st.expander("📐 Detailed Calculation", expanded=False):
    st.markdown(f"""
    **Temperature:** {temperature}°C
    
    **For X Parameter:**
    - Expected X (interpolated from RDSO chart): {expected_x:.1f} mm
    - Measured X Reading: {x_reading} mm
    - **Delta X = {delta_x:.1f} mm**
    
    **For Y Parameter:**
    - Expected Y (interpolated from RDSO chart): {expected_y:.1f} mm
    - Measured Y Reading: {y_reading} mm
    - **Delta Y = {delta_y:.1f} mm**
    
    **Alert Decision:**
    - Max Delta = MAX({delta_x:.1f}, {delta_y:.1f}) = {max_delta:.1f} mm
    - Alert Level: **{status_text}**
    """)

# ============================================================================
# DATA TABLES
# ============================================================================
tab1, tab2, tab3 = st.tabs(["📋 RDSO Chart - X Values", "📋 RDSO Chart - Y Values", "🏗️ Mast Configuration"])

with tab1:
    st.dataframe(df_x, use_container_width=True, height=400)
    st.caption("X Parameter (mm) - Distance between 2 moving pulleys")

with tab2:
    st.dataframe(df_y, use_container_width=True, height=400)
    st.caption("Y Parameter (mm) - Distance from top of Muff to bottom of Counter weight")

with tab3:
    st.dataframe(mast_config, use_container_width=True)

# ============================================================================
# TREND CHARTS
# ============================================================================
with st.expander("📈 Expected Values vs Temperature"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("X Parameter Trend")
        temps = np.linspace(-5, 90, 50)
        x_trend = [interpolate_value(df_x, tension_length, t) for t in temps]
        x_trend_df = pd.DataFrame({'Temperature (°C)': temps, 'Expected X (mm)': x_trend})
        st.line_chart(x_trend_df, x='Temperature (°C)', y='Expected X (mm)', use_container_width=True)
    
    with col2:
        st.subheader("Y Parameter Trend")
        y_trend = [interpolate_value(df_y, tension_length, t) for t in temps]
        y_trend_df = pd.DataFrame({'Temperature (°C)': temps, 'Expected Y (mm)': y_trend})
        st.line_chart(y_trend_df, x='Temperature (°C)', y='Expected Y (mm)', use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.caption("🚆 Railway ATD Monitor - RDSO Alert Logic Demonstration")
st.caption("Alert thresholds: 🟢≤20mm | 🟡21-40mm | 🟠41-60mm | 🔴>60mm")

# Update session state
st.session_state.x_reading = x_reading
st.session_state.y_reading = y_reading