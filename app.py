# app.py - Railway ATD Monitor with Email Alerts (Critical Only)
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib

st.set_page_config(
    page_title="Railway ATD Monitor - Complete Dashboard",
    page_icon="🚂",
    layout="wide"
)

# ============================================================================
# EMAIL ALERT CONFIGURATION
# ============================================================================

# Email settings (You need to change these)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your_email@gmail.com',  # CHANGE THIS
    'sender_password': 'your_app_password',   # CHANGE THIS (use App Password, not regular password)
    'recipient_emails': [
        'maintenance@railway.gov.in',  # CHANGE THIS
        'control_room@railway.gov.in', # CHANGE THIS
        'supervisor@railway.gov.in'    # CHANGE THIS
    ]
}

# Track sent alerts to avoid spam (store in session state)
if 'sent_alerts' not in st.session_state:
    st.session_state.sent_alerts = {}

def send_critical_alert(atd_id, location, chainage, max_delta, faulty_sensor, temperature, expected_x, expected_y):
    """
    Send email alert for critical failure (RED status only)
    Returns: True if email sent successfully, False otherwise
    """
    
    # Create a unique key for this alert (to avoid sending multiple emails for same issue)
    alert_key = f"{atd_id}_{faulty_sensor}_{int(max_delta)}"
    
    # Check if we already sent this alert in the last 5 minutes
    current_time = datetime.now()
    if alert_key in st.session_state.sent_alerts:
        last_sent = st.session_state.sent_alerts[alert_key]
        time_diff = (current_time - last_sent).total_seconds() / 60
        if time_diff < 5:  # Don't send if less than 5 minutes
            return False
    
    # Prepare email content
    subject = f"🚨 CRITICAL ALERT - {atd_id} - Railway ATD Failure"
    
    body = f"""
    ⚠️⚠️⚠️ CRITICAL FAILURE ALERT ⚠️⚠️⚠️
    
    ATD Assembly: {atd_id}
    Location: {location}
    Chainage: {chainage}
    Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    📊 FAILURE DETAILS:
    
    • Fault Location: {faulty_sensor}
    • Max Delta: {max_delta:.1f} mm (Critical threshold: >60mm)
    • Current Temperature: {temperature}°C
    
    📈 EXPECTED VALUES (as per RDSO Chart):
    
    • Expected X Value: {expected_x} mm
    • Expected Y Value: {expected_y} mm
    
    🔴 ACTUAL SENSOR READINGS:
    
    • X-N (North Pulley): {st.session_state.get(f'{atd_id}_n_x', 'N/A')} mm
    • Y-N (North Weight): {st.session_state.get(f'{atd_id}_n_y', 'N/A')} mm
    • X-S (South Pulley): {st.session_state.get(f'{atd_id}_s_x', 'N/A')} mm
    • Y-S (South Weight): {st.session_state.get(f'{atd_id}_s_y', 'N/A')} mm
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    🚨 REQUIRED ACTION:
    
    1. IMMEDIATE inspection required at {location}
    2. Check both North and South masts
    3. Verify ATD pulley movement
    4. Inspect counterweight assembly
    5. Take photos for documentation
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    This is an automated alert from Railway ATD Monitoring System.
    Please acknowledge receipt.
    
    """
    
    try:
        # Create email message - Fixed: MIMEMultipart
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = ', '.join(EMAIL_CONFIG['recipient_emails'])
        msg['Subject'] = subject
        
        # Fixed: MIMEText
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        server.send_message(msg)
        server.quit()
        
        # Record that we sent this alert
        st.session_state.sent_alerts[alert_key] = current_time
        
        return True
        
    except Exception as e:
        st.error(f"Failed to send email alert: {str(e)}")
        return False

# [REST OF YOUR CODE CONTINUES...]

# ============================================================================
# RDSO MASTER CHART DATA
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

# ============================================================================
# ATD CONFIGURATION
# ============================================================================
atd_config = {
    'ATD 1': {
        'N_Mast': 'ATD 1 - N',
        'S_Mast': 'ATD 1 - S',
        'Tension_Length': 300,
        'Location': 'Station A',
        'Track': 'Track 1',
        'Chainage': '100+200',
    },
    'ATD 2': {
        'N_Mast': 'ATD 2 - N',
        'S_Mast': 'ATD 2 - S',
        'Tension_Length': 400,
        'Location': 'Station B',
        'Track': 'Track 2',
        'Chainage': '105+500',
    },
    'ATD 3': {
        'N_Mast': 'ATD 3 - N',
        'S_Mast': 'ATD 3 - S',
        'Tension_Length': 500,
        'Location': 'Station C',
        'Track': 'Track 1',
        'Chainage': '112+300',
    },
    'ATD 4': {
        'N_Mast': 'ATD 4 - N',
        'S_Mast': 'ATD 4 - S',
        'Tension_Length': 600,
        'Location': 'Station D',
        'Track': 'Track 2',
        'Chainage': '118+900',
    },
    'ATD 5': {
        'N_Mast': 'ATD 5 - N',
        'S_Mast': 'ATD 5 - S',
        'Tension_Length': 650,
        'Location': 'Station E',
        'Track': 'Track 1',
        'Chainage': '125+400',
    },
}

# Initialize session state for all ATDs
for atd_id in atd_config.keys():
    if f'{atd_id}_n_x' not in st.session_state:
        st.session_state[f'{atd_id}_n_x'] = 1300
        st.session_state[f'{atd_id}_n_y'] = 2600
        st.session_state[f'{atd_id}_s_x'] = 1300
        st.session_state[f'{atd_id}_s_y'] = 2600

# ============================================================================
# INTERPOLATION FUNCTION
# ============================================================================
def interpolate_value(df, tension_length, temperature):
    temp_values = df['Temperature'].values
    if tension_length not in df.columns:
        closest = min(tension_lengths, key=lambda x: abs(x - tension_length))
        tension_length = closest
    if temperature <= temp_values[0]:
        return int(df.loc[0, tension_length])
    if temperature >= temp_values[-1]:
        return int(df.loc[len(df)-1, tension_length])
    lower_idx = np.searchsorted(temp_values, temperature) - 1
    upper_idx = lower_idx + 1
    T_low = temp_values[lower_idx]
    T_high = temp_values[upper_idx]
    V_low = df.loc[lower_idx, tension_length]
    V_high = df.loc[upper_idx, tension_length]
    result = V_low + (V_high - V_low) * (temperature - T_low) / (T_high - T_low)
    return int(round(result, 0))

# ============================================================================
# FUNCTION TO GET STATUS COLOR AND TEXT
# ============================================================================
def get_status(delta):
    if delta <= 20:
        return "🟢", "HEALTHY", "green"
    elif delta <= 40:
        return "🟡", "MAINTENANCE", "yellow"
    elif delta <= 60:
        return "🟠", "URGENT", "orange"
    else:
        return "🔴", "CRITICAL", "red"

# ============================================================================
# CREATE ATD STATUS TABLE
# ============================================================================
def create_atd_status_table(temperature):
    """Generate a comprehensive status table for all ATDs"""
    
    table_data = []
    
    for atd_id, atd in atd_config.items():
        tension_length = atd['Tension_Length']
        
        expected_x = interpolate_value(df_x, tension_length, temperature)
        expected_y = interpolate_value(df_y, tension_length, temperature)
        
        n_x = st.session_state.get(f'{atd_id}_n_x', expected_x)
        n_y = st.session_state.get(f'{atd_id}_n_y', expected_y)
        s_x = st.session_state.get(f'{atd_id}_s_x', expected_x)
        s_y = st.session_state.get(f'{atd_id}_s_y', expected_y)
        
        delta_n_x = abs(n_x - expected_x)
        delta_n_y = abs(n_y - expected_y)
        delta_s_x = abs(s_x - expected_x)
        delta_s_y = abs(s_y - expected_y)
        
        max_delta_n = max(delta_n_x, delta_n_y)
        max_delta_s = max(delta_s_x, delta_s_y)
        overall_max = max(max_delta_n, max_delta_s)
        
        n_icon, n_status, n_color = get_status(max_delta_n)
        s_icon, s_status, s_color = get_status(max_delta_s)
        overall_icon, overall_status, overall_color = get_status(overall_max)
        
        table_data.append({
            "ATD": atd_id,
            "Location": atd['Location'],
            "Track": atd['Track'],
            "Chainage": atd['Chainage'],
            "Tension (m)": tension_length,
            "Exp X": expected_x,
            "Exp Y": expected_y,
            "N-X": n_x,
            "N-Y": n_y,
            "S-X": s_x,
            "S-Y": s_y,
            "N Δ": max_delta_n,
            "S Δ": max_delta_s,
            "North": f"{n_icon} {n_status}",
            "South": f"{s_icon} {s_status}",
            "Overall": f"{overall_icon} {overall_status}",
            "Overall Color": overall_color
        })
    
    return pd.DataFrame(table_data)

# ============================================================================
# SIDEBAR CONTROLS
# ============================================================================
with st.sidebar:
    st.header("🎮 Control Panel")
    
    # Email Configuration Warning
    if EMAIL_CONFIG['sender_email'] == 'your_email@gmail.com':
        st.warning("⚠️ **Email alerts not configured!**\n\nUpdate EMAIL_CONFIG in the code with your Gmail credentials to enable critical alerts.")
    
    st.subheader("🌡️ Global Temperature Setting")
    global_temperature = st.slider(
        "Temperature for All ATDs (°C)", 
        -5.0, 90.0, 35.0, 1.0
    )
    
    st.divider()
    
    st.subheader("🔍 Detailed View")
    selected_atd = st.selectbox(
        "Select ATD for Detailed Monitoring",
        options=list(atd_config.keys())
    )
    
    atd = atd_config[selected_atd]
    tension_length = atd['Tension_Length']
    
    exp_x = interpolate_value(df_x, tension_length, global_temperature)
    exp_y = interpolate_value(df_y, tension_length, global_temperature)
    
    current_n_x = st.session_state[f'{selected_atd}_n_x']
    current_n_y = st.session_state[f'{selected_atd}_n_y']
    current_s_x = st.session_state[f'{selected_atd}_s_x']
    current_s_y = st.session_state[f'{selected_atd}_s_y']
    
    st.info(f"""
    📍 **{selected_atd} Details**
    - 🧭 North: {atd['N_Mast']}
    - 🧭 South: {atd['S_Mast']}
    - 📏 Tension: {tension_length}m
    - 📍 Location: {atd['Location']}
    - 🛤️ Track: {atd['Track']}
    - 📊 Chainage: {atd['Chainage']}
    """)
    
    st.divider()
    
    st.subheader("🧭 NORTH DIRECTION")
    n_x = st.number_input(
        f"X-N (mm) - {atd['N_Mast']}", 
        min_value=400, max_value=2000, 
        value=int(current_n_x), step=5
    )
    n_y = st.number_input(
        f"Y-N (mm) - {atd['N_Mast']}", 
        min_value=500, max_value=4500, 
        value=int(current_n_y), step=5
    )
    
    st.divider()
    
    st.subheader("🧭 SOUTH DIRECTION")
    s_x = st.number_input(
        f"X-S (mm) - {atd['S_Mast']}", 
        min_value=400, max_value=2000, 
        value=int(current_s_x), step=5
    )
    s_y = st.number_input(
        f"Y-S (mm) - {atd['S_Mast']}", 
        min_value=500, max_value=4500, 
        value=int(current_s_y), step=5
    )
    
    st.session_state[f'{selected_atd}_n_x'] = n_x
    st.session_state[f'{selected_atd}_n_y'] = n_y
    st.session_state[f'{selected_atd}_s_x'] = s_x
    st.session_state[f'{selected_atd}_s_y'] = s_y
    
    st.divider()
    
    st.subheader("🎯 Quick Actions")
    if st.button("🟢 Set All Sensors to Expected", use_container_width=True):
        for atd_id in atd_config.keys():
            tl = atd_config[atd_id]['Tension_Length']
            exp_x_val = interpolate_value(df_x, tl, global_temperature)
            exp_y_val = interpolate_value(df_y, tl, global_temperature)
            st.session_state[f'{atd_id}_n_x'] = exp_x_val
            st.session_state[f'{atd_id}_n_y'] = exp_y_val
            st.session_state[f'{atd_id}_s_x'] = exp_x_val
            st.session_state[f'{atd_id}_s_y'] = exp_y_val
        st.rerun()
    
    if st.button("🔴 Simulate Critical Failure (Sends Email)", use_container_width=True):
        for atd_id in atd_config.keys():
            tl = atd_config[atd_id]['Tension_Length']
            exp_x_val = interpolate_value(df_x, tl, global_temperature)
            exp_y_val = interpolate_value(df_y, tl, global_temperature)
            st.session_state[f'{atd_id}_n_x'] = exp_x_val + 75
            st.session_state[f'{atd_id}_s_y'] = exp_y_val + 75
        st.rerun()

# ============================================================================
# MAIN DISPLAY - ATD STATUS TABLE
# ============================================================================
st.title("🚂 Railway ATD Monitoring System")
st.markdown(f"### 📊 Live ATD Status Dashboard")
st.caption(f"🔍 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Global Temperature: {global_temperature}°C")

# Create status table
df_status = create_atd_status_table(global_temperature)

# ============================================================================
# CHECK FOR CRITICAL ALERTS AND SEND EMAILS
# ============================================================================

# Check each ATD for critical status and send email alerts
for idx, row in df_status.iterrows():
    if "CRITICAL" in row['Overall']:
        atd_id = row['ATD']
        location = row['Location']
        chainage = row['Chainage']
        
        # Calculate actual delta for this ATD
        n_x_val = row['N-X']
        n_y_val = row['N-Y']
        s_x_val = row['S-X']
        s_y_val = row['S-Y']
        exp_x_val = row['Exp X']
        exp_y_val = row['Exp Y']
        
        delta_n_x = abs(n_x_val - exp_x_val)
        delta_n_y = abs(n_y_val - exp_y_val)
        delta_s_x = abs(s_x_val - exp_x_val)
        delta_s_y = abs(s_y_val - exp_y_val)
        
        deltas = [delta_n_x, delta_n_y, delta_s_x, delta_s_y]
        max_delta = max(deltas)
        sensor_names = ["X-N (North Pulley)", "Y-N (North Weight)", "X-S (South Pulley)", "Y-S (South Weight)"]
        faulty_sensor = sensor_names[deltas.index(max_delta)]
        
        # Send email alert (only if configured)
        if EMAIL_CONFIG['sender_email'] != 'your_email@gmail.com':
            email_sent = send_critical_alert(
                atd_id, location, chainage, max_delta, 
                faulty_sensor, global_temperature, exp_x_val, exp_y_val
            )
            if email_sent:
                st.success(f"📧 Critical email alert sent for {atd_id}!")
        else:
            # Show warning in the UI for demo purposes
            st.warning(f"🔴 CRITICAL on {atd_id} - {faulty_sensor} (Delta: {max_delta:.0f}mm) - Email would be sent in production!")

# ============================================================================
# DISPLAY STATUS TABLE
# ============================================================================
st.subheader("📋 Complete ATD Status Overview")

# Color code the dataframe for display
# Color code the dataframe for display
def color_cells(val):
    if isinstance(val, str):
        if "CRITICAL" in val:
            return 'background-color: #ffcccc; color: #cc0000'
        elif "URGENT" in val:
            return 'background-color: #ffe0cc; color: #ff6600'
        elif "MAINTENANCE" in val:
            return 'background-color: #ffffcc; color: #cc9900'
        elif "HEALTHY" in val:
            return 'background-color: #ccffcc; color: #006600'
    return ''

# Fixed: Changed applymap to map
styled_df = df_status.style.map(color_cells, subset=['North', 'South', 'Overall'])

st.dataframe(
    df_status, 
    use_container_width=True, 
    height=400,
    column_config={
        "ATD": st.column_config.TextColumn("ATD", width="small"),
        "Location": st.column_config.TextColumn("Location", width="small"),
        "Track": st.column_config.TextColumn("Track", width="small"),
        "Chainage": st.column_config.TextColumn("Chainage", width="small"),
        "Tension (m)": st.column_config.NumberColumn("Tension", width="small"),
        "Exp X": st.column_config.NumberColumn("Exp X", width="small"),
        "Exp Y": st.column_config.NumberColumn("Exp Y", width="small"),
        "N-X": st.column_config.NumberColumn("N-X", width="small"),
        "N-Y": st.column_config.NumberColumn("N-Y", width="small"),
        "S-X": st.column_config.NumberColumn("S-X", width="small"),
        "S-Y": st.column_config.NumberColumn("S-Y", width="small"),
        "N Δ": st.column_config.NumberColumn("N Δ", width="small"),
        "S Δ": st.column_config.NumberColumn("S Δ", width="small"),
        "North": st.column_config.TextColumn("North", width="medium"),
        "South": st.column_config.TextColumn("South", width="medium"),
        "Overall": st.column_config.TextColumn("Overall", width="medium"),
    }
)
# Summary statistics
col1, col2, col3, col4, col5 = st.columns(5)

healthy_count = len(df_status[df_status['Overall'].str.contains('HEALTHY')])
maintenance_count = len(df_status[df_status['Overall'].str.contains('MAINTENANCE')])
urgent_count = len(df_status[df_status['Overall'].str.contains('URGENT')])
critical_count = len(df_status[df_status['Overall'].str.contains('CRITICAL')])

with col1:
    st.metric("Total ATDs", len(df_status))
with col2:
    st.metric("🟢 Healthy", healthy_count)
with col3:
    st.metric("🟡 Maintenance", maintenance_count)
with col4:
    st.metric("🟠 Urgent", urgent_count)
with col5:
    st.metric("🔴 Critical", critical_count)

st.divider()

# ============================================================================
# DETAILED VIEW FOR SELECTED ATD
# ============================================================================
st.markdown(f"## 🔍 Detailed View: {selected_atd}")

exp_x_detailed = interpolate_value(df_x, atd['Tension_Length'], global_temperature)
exp_y_detailed = interpolate_value(df_y, atd['Tension_Length'], global_temperature)

delta_n_x_detailed = abs(n_x - exp_x_detailed)
delta_n_y_detailed = abs(n_y - exp_y_detailed)
delta_s_x_detailed = abs(s_x - exp_x_detailed)
delta_s_y_detailed = abs(s_y - exp_y_detailed)

max_delta_n_detailed = max(delta_n_x_detailed, delta_n_y_detailed)
max_delta_s_detailed = max(delta_s_x_detailed, delta_s_y_detailed)
overall_max_detailed = max(max_delta_n_detailed, max_delta_s_detailed)

n_icon_detailed, n_status_detailed, n_color_detailed = get_status(max_delta_n_detailed)
s_icon_detailed, s_status_detailed, s_color_detailed = get_status(max_delta_s_detailed)
overall_icon_detailed, overall_status_detailed, overall_color_detailed = get_status(overall_max_detailed)

color_map = {"green": "#00FF00", "yellow": "#FFFF00", "orange": "#FFA500", "red": "#FF0000"}
bg_color = color_map[overall_color_detailed]
text_color = "#000000" if overall_color_detailed == "yellow" else "#FFFFFF"

st.markdown(f"""
<div style="background-color: {bg_color}; text-align: center; padding: 30px; border-radius: 20px; margin: 20px 0;">
    <div style="font-size: 48px; font-weight: bold; color: {text_color};">{overall_icon_detailed} {overall_status_detailed}</div>
    <div style="font-size: 24px; color: {text_color}; margin-top: 10px;">Max Delta = {overall_max_detailed:.0f} mm</div>
    <div style="font-size: 16px; color: {text_color};">Temperature: {global_temperature}°C | Expected X: {exp_x_detailed}mm | Expected Y: {exp_y_detailed}mm</div>
</div>
""", unsafe_allow_html=True)

if overall_color_detailed == "red" and overall_max_detailed > 60:
    st