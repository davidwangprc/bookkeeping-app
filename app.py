import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="多人实时记账", page_icon="📒")

def connect_to_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(credentials)
    sheet = client.open("Bookkeeping").sheet1
    return sheet

sheet = connect_to_gsheet()

def read_data():
    records = sheet.get_all_records()
    return pd.DataFrame(records)

def append_row(row):
    sheet.append_row(row)

st.title("📒 实时多人记账 App")

st.sidebar.header("添加新记录")
date = st.sidebar.date_input("日期", datetime.today())
item = st.sidebar.text_input("项目")
amount = st.sidebar.number_input("金额", step=1.0, format="%.2f")
note = st.sidebar.text_input("备注")

if st.sidebar.button("添加"):
    if item:
        new_row = [str(date), item, amount, note]
        append_row(new_row)
        st.success("✅ 记录添加成功")
    else:
        st.warning("请输入项目名称")

st.subheader("📊 当前记录")
df = read_data()
st.dataframe(df)

st.subheader("💰 收支统计")
st.write(f"总金额：{df['金额'].sum():.2f}")
