import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import time
import pandas as pd

# 设置页面
st.set_page_config(page_title="科研经费管理系统", layout="wide")
st.markdown(
    """
    <h1 style='margin-top:2.5rem; margin-bottom:1.5rem; font-size:2.3rem; display:flex; align-items:center;'>
        <span style="font-size:2.3rem; margin-right:0.5rem;">🔬</span> 科研经费管理系统
    </h1>
    """,
    unsafe_allow_html=True
)

def inject_custom_css():
    theme = st.get_option("theme.base")
    if theme == "dark":
        bg_color = "#22272e"
        card_color = "#2d333b"
        text_color = "#e67e22"
        border_color = "#444c56"
    else:
        bg_color = "#f5f6fa"
        card_color = "#fff"
        text_color = "#e67e22"
        border_color = "#e0e0e0"
    st.markdown(f"""
    <style>
    body {{
        background: {bg_color};
        color: {text_color};
    }}
    .block-container {{
        padding-top: 1.5rem;
    }}
    .custom-card {{
        background: {card_color};
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid {border_color};
        padding: 1.5rem 1.2rem 1.2rem 1.2rem;
        margin-bottom: 1.5rem;
    }}
    .custom-title {{
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        color: {text_color};

    }}
    .stButton>button, .stDownloadButton>button {{
        border-radius: 8px;
        font-weight: 600;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }}
    .stDataFrame, .stTable {{
        border-radius: 8px;
        overflow: hidden;
    }}
    hr {{
        border: none;
        border-top: 1.5px solid {border_color};
        margin: 1.2rem 0;
    }}
    .stat-card {{
        background: rgba(0,0,0,0.03);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.5rem;
        border: 1px solid {border_color};
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }}
    .stat-title {{
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }}
    .stat-value {{
        font-size: 1.2rem;
        color: #2e7d32;
        font-weight: 700;
    }}
    .stat-count {{
        font-size: 0.95rem;
        color: #888;
    }}
    </style>
    """, unsafe_allow_html=True)

# 认证Google Sheets
def authenticate():
    scope = ["https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    return client

# 获取或创建工作表
def get_sheet(client, sheet_name, worksheet_name):
    try:
        # 先尝试打开现有工作表
        sheet = client.open(sheet_name).worksheet(worksheet_name)
    except gspread.exceptions.WorksheetNotFound:
        # 工作表不存在时创建
        workbook = client.open(sheet_name)
        sheet = workbook.add_worksheet(title=worksheet_name, rows=100, cols=10)
        # 设置新表头
        headers = ["项目代码", "日期", "科目名称", "报销到账", "用户", "备注"]
        sheet.append_row(headers)
    except gspread.exceptions.SpreadsheetNotFound:
        # 整个表格不存在时创建（需要drive权限）
        st.error(f"未找到表格 '{sheet_name}'，请确保已正确共享")
        st.stop()
    return sheet

# 主应用
def main():
    inject_custom_css()
    # 用户会话状态初始化
    if 'user' not in st.session_state:
        st.session_state.user = "用户" + str(int(time.time()) % 1000)
    
    client = authenticate()
    sheet = get_sheet(client, "bookkeeping", "报销记录")
    
    # 用户选择
    user = st.sidebar.selectbox("您的身份", ["林依爽", "王大伟"], index=1)
    st.session_state.user = user
    st.sidebar.markdown(f"**当前用户:** {st.session_state.user}")
    
    # 项目选择
    project = st.sidebar.selectbox("项目类型", ["孵化卡(FHJ)", "横向课题(KHJ)"], index=0)
    
    # 获取所有记录
    records = sheet.get_all_records()
    
    # 记账表单
    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="custom-title">📝 新增报销记录</div>', unsafe_allow_html=True)
        with st.form("报销表单", clear_on_submit=True):
            st.subheader("新增报销记录")
            cols = st.columns([1, 1, 1])
            date = cols[0].date_input("日期", datetime.today())
            
            # 报销人选择（入账用户）
            reimbursement_user = cols[1].selectbox("报销人", ["林依爽", "王大伟"], index=1)
            
            # 项目代码
            project_code = cols[2].text_input("项目代码", 
                                             value="FHJ1620004" if "孵化卡" in project else "KHJ1625606")
            
            # 科目选择 - 根据项目类型提供不同的科目选项
            if "孵化卡" in project:
                subject_options = [
                    "其他",
                    "公务接待费/食宿费",
                    "劳务费",
                    "交通费",
                    "维修(护)费/设备维修费"
                ]
            else:
                subject_options = [
                    "其他",
                    "公务接待费/食宿费",
                    "劳务费",
                    "交通费",
                    "维修(护)费/设备维修费"
                ]
            
            subject = st.selectbox("科目名称", subject_options)
            
            # 金额输入
            amount = st.number_input("报销到账金额 (元)", min_value=0.0, step=0.01)
            
            description = st.text_area("备注", placeholder="详细描述报销内容")
            
            submitted = st.form_submit_button("提交记录")
            
            if submitted:
                new_row = [
                    project_code,
                    date.strftime("%Y-%m-%d"),
                    subject,
                    amount,
                    reimbursement_user,
                    description
                ]
                sheet.append_row(new_row)
                st.success("报销记录已保存!")
                time.sleep(1)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 统计显示区域
    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="custom-title">📊 经费统计概览</div>', unsafe_allow_html=True)
        st.markdown('<div style="display:flex; flex-direction:column; gap:1.2rem;">', unsafe_allow_html=True)
        if not records:
            st.info("暂无报销记录")
            return
        
        # 转换为DataFrame
        df = pd.DataFrame(records)
        
        # 转换金额为数值类型
        df['报销到账'] = pd.to_numeric(df['报销到账'], errors='coerce')
        
        # 按项目和用户统计
        project_stats = df.groupby('项目代码').agg(
            总报销金额=('报销到账', 'sum'),
            记录数=('项目代码', 'count')
        ).reset_index()
        
        user_stats = df.groupby('用户').agg(
            总报销金额=('报销到账', 'sum'),
            记录数=('用户', 'count')
        ).reset_index()
        
        subject_stats = df.groupby('科目名称').agg(
            总报销金额=('报销到账', 'sum'),
            记录数=('科目名称', 'count')
        ).reset_index().sort_values('总报销金额', ascending=False)

        st.subheader("项目统计")
        st.dataframe(project_stats, hide_index=True)
        
        # 用户统计
        for _, row in user_stats.iterrows():
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-title">👤 用户：{row['用户']}</div>
                    <div class="stat-value">总报销金额：<b>{row['总报销金额']:.2f} 元</b></div>
                    <div class="stat-count">记录数：{row['记录数']}</div>
                </div>
                """, unsafe_allow_html=True
            )

        
        # 科目统计
        subject_stats = df.groupby('科目名称').agg(
            总报销金额=('报销到账', 'sum'),
            记录数=('科目名称', 'count')
        ).reset_index().sort_values('总报销金额', ascending=False)
        
        st.subheader("科目统计")
        st.dataframe(subject_stats, hide_index=True)

       
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 详细数据展示
    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="custom-title">📋 报销明细</div>', unsafe_allow_html=True)
        # 添加筛选器
        with st.expander("筛选选项"):
            col_filter1, col_filter2, col_filter3 = st.columns(3)
            selected_project = col_filter1.multiselect("项目代码", df['项目代码'].unique(), default=df['项目代码'].unique())
            selected_user = col_filter2.multiselect("用户", df['用户'].unique(), default=df['用户'].unique())
            selected_subject = col_filter3.multiselect("科目名称", df['科目名称'].unique(), default=df['科目名称'].unique())
            
            # 日期范围筛选
            if '日期' in df.columns and not df.empty:
                df['日期'] = pd.to_datetime(df['日期'], errors='coerce')
                min_date = df['日期'].min().date() if pd.notnull(df['日期'].min()) else datetime.today().date()
                max_date = df['日期'].max().date() if pd.notnull(df['日期'].max()) else datetime.today().date()
                date_range = st.date_input("日期范围", [min_date, max_date])
        
        # 应用筛选
        filtered_df = df.copy()
        
        if '项目代码' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['项目代码'].isin(selected_project)]
        
        if '用户' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['用户'].isin(selected_user)]
        
        if '科目名称' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['科目名称'].isin(selected_subject)]
        
        if '日期' in filtered_df.columns and len(date_range) == 2:
            filtered_df = filtered_df[
                (filtered_df['日期'] >= pd.Timestamp(date_range[0])) &
                (filtered_df['日期'] <= pd.Timestamp(date_range[1]))
            ]
        
        st.dataframe(filtered_df, use_container_width=True)
        
        # 导出数据按钮
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="导出筛选数据为CSV",
            data=csv,
            file_name=f"科研经费报销记录_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv',
        )
        
        # 刷新按钮
        if st.button("刷新数据"):
            st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()