import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Shipping Audit Portal", layout="wide")

st.title("📦 Shipping Recovery Audit")
st.write("Real-time scan for late deliveries and refund opportunities.")

with st.sidebar:
    st.header("Settings")
    shop_url = st.text_input("Shopify URL", value="auditor-test-engine.myshopify.com")
    api_token = st.text_input("Admin API Token", type="password")
    run_audit = st.button("Run Audit")

if run_audit and api_token:
    headers = {"X-Shopify-Access-Token": api_token, "Content-Type": "application/json"}
    orders_url = f"https://{shop_url}/admin/api/2024-04/orders.json?status=any"
    
    with st.spinner("Analyzing shipping speeds..."):
        response = requests.get(orders_url, headers=headers)
        
        if response.status_code == 200:
            orders = response.json().get('orders', [])
            st.success(f"Audit Complete: {len(orders)} orders analyzed.")
            
            for order in orders:
                # Logic: Check if it's late (simulated for now)
                is_late = order['fulfillment_status'] == 'fulfilled'
                
                with st.container():
                    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
                    col1.write(f"**Order #{order['order_number']}**")
                    col2.write(f"Status: {order['financial_status'].upper()}")
                    
                    if is_late:
                        col3.error("⚠️ LATE")
                        col4.button(f"Generate Refund Claim for #{order['order_number']}")
                    else:
                        col3.success("✅ ON TIME")
        else:
            st.error("Check your API token and try again.")
