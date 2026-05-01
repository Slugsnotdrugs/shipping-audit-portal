import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Shipping Audit Portal", layout="wide")

st.title("📦 Shipping Recovery Audit")
st.write("Enter your credentials to scan for late delivery refunds.")

# Sidebar for credentials
with st.sidebar:
    st.header("Settings")
    shop_url = st.text_input("Shopify URL", value="auditor-test-engine.myshopify.com")
    api_token = st.text_input("Admin API Token", type="password")
    run_audit = st.button("Run Audit")

if run_audit and api_token:
    headers = {"X-Shopify-Access-Token": api_token, "Content-Type": "application/json"}
    orders_url = f"https://{shop_url}/admin/api/2024-04/orders.json?status=any"
    
    with st.spinner("Scanning orders..."):
        response = requests.get(orders_url, headers=headers)
        
        if response.status_code == 200:
            orders = response.json().get('orders', [])
            if not orders:
                st.warning("No orders found in this store yet.")
            else:
                st.success(f"Successfully scanned {len(orders)} orders!")
                # This is where we'll add the logic to find late ones
                for order in orders:
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Order Number", f"#{order['order_number']}")
                    col2.metric("Status", order['financial_status'].upper())
                    col3.metric("Fulfillment", order['fulfillment_status'] or "Unfulfilled")
        else:
            st.error(f"Connection Failed: {response.status_code}")
else:
    st.info("Please enter your API token in the sidebar and click 'Run Audit'.")
