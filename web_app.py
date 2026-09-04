import pandas as pd
import streamlit as st

# 设置页面标题
st.set_page_config(page_title="手机 IMEI 查询系统", layout="centered")

st.title("📱 员工手机 IMEI 查询系统")
st.caption("请输入 15 位手机 IMEI 号码进行精确查询")


# 读取 Excel 数据
@st.cache_data
def load_data():
    try:
        # 读取表格并将 IMEI 强制转为字符串，防止长数字被科学计数法损坏
        df = pd.read_excel("data.xlsx", dtype=str)
        # 移除表头和数据中的前后空格
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"数据加载失败，请检查 data.xlsx 文件是否存在！错误信息：{e}")
        return None


df = load_data()

if df is not None:
    # 确认列名（请根据你的 Excel 实际列名微调，这里假设列名为 'IMEI'）
    imei_col = None
    for col in df.columns:
        if "IMEI" in col.upper():
            imei_col = col
            break

    if not imei_col:
        st.error(
            "未在 Excel 表格中找到包含 'IMEI' 的列，请检查 Excel 表头！"
        )
    else:
        # 单一输入框：仅支持 IMEI 查询
        search_query = st.text_input(
            "输入 IMEI 号：", placeholder="请输入完整的 IMEI 号"
        ).strip()

        if search_query:
            # 执行精确或模糊匹配
            result = df[
                df[imei_col].str.contains(search_query, na=False, case=False)
            ]

            if not result.empty:
                st.success(f"找到 {len(result)} 条匹配记录：")
                st.dataframe(result, use_container_width=True)
            else:
                st.warning("未查询到该 IMEI 号对应的员工信息，请检查输入。")
