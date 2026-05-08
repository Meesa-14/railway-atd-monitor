# app.py - Railway ATD Monitor with 4 Sensors (2X + 2Y)
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Railway ATD Monitor - 4 Sensor System",
    page_icon="🚂",
    layout="wide"
)

# ============================================================================
# RDSO MASTER CHART DATA (Same as before)
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

df_x = pd.DataFrame(x_data)
df_y = pd.DataFrame(y_data)
tension_lengths = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750]

mast_config = pd.DataFrame({
    'Mast_ID': [f'Mast_{i}' for i in range(1, 11)],
    'Tension_Length': [200, 250, 300, 350, 400, 450, 500, 550, 600, 650],
    'Location': ['Station A', 'Station A', 'Station B', 'Station B', 'Station C', 
                 'Station C', 'Station D', 'Station D', 'Station E', 'Station E']
})

# ============================================================================
# INTERPOLATION FUNCTION
# ============================================================================
def interpolate_value(df, tension_length, temperature):
    temp_values = df['Temperature'].values
    if tension_length not in df.columns:
        closest = min(tension_lengths, key=lambda x: abs(x - tension_length))
        tension_length = closest
    if temperature <= temp_values[0]:
        return df.loc[0, tension_length]
    if temperature >= temp_values[-1]:
        return df.loc[len(df)-1, tension_length]
    lower_idx = np.searchsorted(temp_values, temperature) - 1
    upper_idx = lower_idx + 1
    T_low = temp_values[lower_idx]
    T_high = temp_values[upper_idx]
    V_low = df.loc[lower_idx, tension_length]
    V_high = df.loc[upper_idx, tension_length]
    result = V_low + (V_high - V_low) * (temperature - T_low) / (T_high - T_low)
    return round(result, 1)

# ============================================================================
# ALERT FUNCTION (Uses MAX of all 4 deltas)
# ============================================================================
def get_alert_level(delta_x1, delta_x2, delta_y1, delta_y2):
    """Determine alert based on ALL 4 sensors - INDEPENDENT evaluation"""
    deltas = [delta_x1, delta_x2, delta_y1, delta_y2]
    max_delta = max(deltas)
    
    # Find which sensor has max delta
    sensor_names = ["X1 (Left)", "X2 (Right)", "Y1 (Left)", "Y2 (Right)"]
    max_sensor = sensor_names[deltas.index(max_delta)]
    
    if max_delta <= 20:
        return "✅ HEALTHY", "green", f"Max Delta: {max_delta:.1f}mm (All sensors normal)", max_delta, max_sensor
    elif max_delta <= 40:
        return "⚠️ MAINTENANCE REQUIRED", "yellow", f"Max Delta: {max_delta:.1f}mm on {max_sensor}", max_delta, max_sensor
    elif max_delta <= 60:
        return "🚨 URGENT ALERT", "orange", f"Max Delta: {max_delta:.1f}mm on {max_sensor}", max_delta, max_sensor
    else:
        return "🔴 CRITICAL FAILURE", "red", f"Max Delta: {max_delta:.1f}mm on {max_sensor}", max_delta, max_sensor

# ============================================================================
# MAIN UI
# ============================================================================
st.title("🚂 Railway ATD Monitoring System")
st.markdown("### 4-Sensor System: 2X (Left/Right) + 2Y (Left/Right)")
st.caption("⚠️ ANY sensor change triggers real-time alert evaluation")

# Sidebar
with st.sidebar:
    st.header("🎮 Control Panel")
    
    selected_mast = st.selectbox("Select Mast", mast_config['Mast_ID'].tolist())
    mast_info = mast_config[mast_config['Mast_ID'] == selected_mast].iloc[0]
    tension_length = mast_info['Tension_Length']
    
    st.info(f"📍 Tension Length: {tension_length}m | Location: {mast_info['Location']}")
    
    st.divider()
    
    st.subheader("🌡️ Temperature Sensor")
    temperature = st.slider("Temperature (°C)", -5.0, 90.0, 35.0, 1.0, 
                           help="Changing temperature updates expected X/Y values")
    
    st.divider()
    
    st.subheader("📏 X Sensors (Left & Right Pulleys)")
    col1, col2 = st.columns(2)
    with col1:
        x1_reading = st.slider("X1 (Left Pulley) mm", 400, 2000, 1300, 5,
                               help="Left side X parameter - BETWEEN moving pulleys")
    with col2:
        x2_reading = st.slider("X2 (Right Pulley) mm", 400, 2000, 1300, 5,
                               help="Right side X parameter - BETWEEN moving pulleys")
    
    st.subheader("📏 Y Sensors (Left & Right)")
    col3, col4 = st.columns(2)
    with col3:
        y1_reading = st.slider("Y1 (Left) mm", 500, 4500, 2600, 5,
                               help="Left side Y parameter - Muff to counterweight")
    with col4:
        y2_reading = st.slider("Y2 (Right) mm", 500, 4500, 2600, 5,
                               help="Right side Y parameter - Muff to counterweight")
    
    st.divider()
    
    st.subheader("🎯 Demo Scenarios")
    if st.button("🟢 All Sensors Healthy", use_container_width=True):
        expected_x = interpolate_value(df_x, tension_length, temperature)
        expected_y = interpolate_value(df_y, tension_length, temperature)
        st.session_state.x1_reading = expected_x + 5
        st.session_state.x2_reading = expected_x + 5
        st.session_state.y1_reading = expected_y + 5
        st.session_state.y2_reading = expected_y + 5
        st.rerun()
    
    if st.button("🔴 X1 Sensor Failure (Stuck)", use_container_width=True):
        expected_x = interpolate_value(df_x, tension_length, temperature)
        st.session_state.x1_reading = expected_x + 75  # Stuck high
        st.rerun()
    
    if st.button("🟡 X2 Sensor Slight Deviation", use_container_width=True):
        expected_x = interpolate_value(df_x, tension_length, temperature)
        st.session_state.x2_reading = expected_x + 35  # 35mm delta → Yellow
        st.rerun()

# Initialize session state
if 'x1_reading' not in st.session_state:
    st.session_state.x1_reading = x1_reading
    st.session_state.x2_reading = x2_reading
    st.session_state.y1_reading = y1_reading
    st.session_state.y2_reading = y2_reading
else:
    x1_reading = st.session_state.x1_reading
    x2_reading = st.session_state.x2_reading
    y1_reading = st.session_state.y1_reading
    y2_reading = st.session_state.y2_reading

# ============================================================================
# CALCULATIONS - Each sensor compared independently
# ============================================================================
expected_x = interpolate_value(df_x, tension_length, temperature)
expected_y = interpolate_value(df_y, tension_length, temperature)

delta_x1 = abs(x1_reading - expected_x)
delta_x2 = abs(x2_reading - expected_x)
delta_y1 = abs(y1_reading - expected_y)
delta_y2 = abs(y2_reading - expected_y)

status_text, color, details, max_delta, faulty_sensor = get_alert_level(delta_x1, delta_x2, delta_y1, delta_y2)

# ============================================================================
# MAIN ALERT INDICATOR
# ============================================================================
color_map = {"green": "#00FF00", "yellow": "#FFFF00", "orange": "#FFA500", "red": "#FF0000"}
text_color = "#000000" if color in ["yellow"] else "#FFFFFF"

st.markdown(f"""
<div style="background-color: {color_map[color]}; text-align: center; padding: 40px; border-radius: 20px; margin: 20px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
    <div style="font-size: 56px; font-weight: bold; color: {text_color};">
        {status_text}
    </div>
    <div style="font-size: 28px; color: {text_color}; margin-top: 15px;">
        Max Delta = {max_delta:.1f} mm
    </div>
    <div style="font-size: 18px; color: {text_color}; margin-top: 10px;">
        {details}
    </div>
</div>
""", unsafe_allow_html=True)

# Critical popup
if color == "red" and max_delta > 60:
    st.toast(f"🚨 CRITICAL FAILURE on {faulty_sensor}! Delta = {max_delta:.1f}mm", icon="🔴")

# ============================================================================
# THRESHOLD LEGEND
# ============================================================================
st.markdown("### 📊 Alert Thresholds (Applies to EVERY sensor independently)")
thresh_cols = st.columns(4)
with thresh_cols[0]:
    st.markdown("🟢 **0-20mm**\n✅ HEALTHY")
with thresh_cols[1]:
    st.markdown("🟡 **21-40mm**\n⚠️ MAINTENANCE")
with thresh_cols[2]:
    st.markdown("🟠 **41-60mm**\n🚨 URGENT")
with thresh_cols[3]:
    st.markdown("🔴 **>60mm**\n🔴 CRITICAL")

# ============================================================================
# 4 SENSOR DISPLAY
# ============================================================================
st.subheader("📊 Individual Sensor Status")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔵 LEFT SIDE")
    
    # X1 Sensor
    x1_color = "🟢" if delta_x1 <= 20 else ("🟡" if delta_x1 <= 40 else ("🟠" if delta_x1 <= 60 else "🔴"))
    st.metric(
        "X1 (Left Pulley)", 
        f"{x1_reading} mm", 
        delta=f"{x1_reading - expected_x:+.1f} mm (Expected: {expected_x}mm)",
        delta_color="inverse"
    )
    st.caption(f"{x1_color} Delta X1 = {delta_x1:.1f} mm")
    
    # Y1 Sensor
    y1_color = "🟢" if delta_y1 <= 20 else ("🟡" if delta_y1 <= 40 else ("🟠" if delta_y1 <= 60 else "🔴"))
    st.metric(
        "Y1 (Left Counterweight)", 
        f"{y1_reading} mm", 
        delta=f"{y1_reading - expected_y:+.1f} mm (Expected: {expected_y}mm)",
        delta_color="inverse"
    )
    st.caption(f"{y1_color} Delta Y1 = {delta_y1:.1f} mm")

with col2:
    st.markdown("### 🔴 RIGHT SIDE")
    
    # X2 Sensor
    x2_color = "🟢" if delta_x2 <= 20 else ("🟡" if delta_x2 <= 40 else ("🟠" if delta_x2 <= 60 else "🔴"))
    st.metric(
        "X2 (Right Pulley)", 
        f"{x2_reading} mm", 
        delta=f"{x2_reading - expected_x:+.1f} mm (Expected: {expected_x}mm)",
        delta_color="inverse"
    )
    st.caption(f"{x2_color} Delta X2 = {delta_x2:.1f} mm")
    
    # Y2 Sensor
    y2_color = "🟢" if delta_y2 <= 20 else ("🟡" if delta_y2 <= 40 else ("🟠" if delta_y2 <= 60 else "🔴"))
    st.metric(
        "Y2 (Right Counterweight)", 
        f"{y2_reading} mm", 
        delta=f"{y2_reading - expected_y:+.1f} mm (Expected: {expected_y}mm)",
        delta_color="inverse"
    )
    st.caption(f"{y2_color} Delta Y2 = {delta_y2:.1f} mm")

# ============================================================================
# SUMMARY TABLE
# ============================================================================
with st.expander("📋 Complete Sensor Summary", expanded=True):
    summary_data = {
        "Sensor": ["X1 (Left Pulley)", "X2 (Right Pulley)", "Y1 (Left Weight)", "Y2 (Right Weight)"],
        "Expected (mm)": [expected_x, expected_x, expected_y, expected_y],
        "Actual (mm)": [x1_reading, x2_reading, y1_reading, y2_reading],
        "Delta (mm)": [delta_x1, delta_x2, delta_y1, delta_y2],
        "Status": [
            "🟢" if delta_x1 <= 20 else ("🟡" if delta_x1 <= 40 else ("🟠" if delta_x1 <= 60 else "🔴")),
            "🟢" if delta_x2 <= 20 else ("🟡" if delta_x2 <= 40 else ("🟠" if delta_x2 <= 60 else "🔴")),
            "🟢" if delta_y1 <= 20 else ("🟡" if delta_y1 <= 40 else ("🟠" if delta_y1 <= 60 else "🔴")),
            "🟢" if delta_y2 <= 20 else ("🟡" if delta_y2 <= 40 else ("🟠" if delta_y2 <= 60 else "🔴")),
        ]
    }
    st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

# ============================================================================
# EXPLANATION OF ALERT TRIGGERS
# ============================================================================
with st.expander("ℹ️ How Alerts are Triggered", expanded=True):
    st.markdown("""
    ### Alert Logic - ANY sensor change triggers re-evaluation:
    
    | Action | What changes | Alert updates? |
    |--------|-------------|----------------|
    | Change Temperature | Expected X/Y values | ✅ YES - All deltas recalculated |
    | Change X1 slider | X1 reading | ✅ YES - Delta X1 recalculated |
    | Change X2 slider | X2 reading | ✅ YES - Delta X2 recalculated |
    | Change Y1 slider | Y1 reading | ✅ YES - Delta Y1 recalculated |
    | Change Y2 slider | Y2 reading | ✅ YES - Delta Y2 recalculated |
    
    ### Real-World Failure Scenarios detected:
    
    1. **Left pulley stuck (X1 high, X2 normal)** → Delta X1 high → Alert triggered
    2. **Right counterweight problem (Y2 abnormal)** → Delta Y2 high → Alert triggered  
    3. **Temperature sensor failure** → Expected values wrong → All deltas affected
    4. **One side working, other failed** → Independent detection per sensor
    
    ### Alert uses MAXIMUM delta across ALL 4 sensors:
    - If ANY sensor has delta > threshold → Alert triggers
    - Shows which sensor caused the alert
    """)

# Update session state
st.session_state.x1_reading = x1_reading
st.session_state.x2_reading = x2_reading
st.session_state.y1_reading = y1_reading
st.session_state.y2_reading = y2_reading

st.divider()
st.caption("🚆 Railway ATD Monitor - 4 Sensor System (2X + 2Y) | ANY sensor change triggers real-time alert")