import pandas as pd
import streamlit as st

st.set_page_config(page_title="手机号查询系统", layout="centered")
st.title("📱 员工手机号/IMEI 查询系统")


# 1. 自动加载本地 Excel 数据（支持缓存加速）
@st.cache_data
def load_data():
  try:
    df = pd.read_excel("data.xlsx", dtype=str)
    for col in df.columns:
      df[col] = df[col].astype(str).str.strip()
    return df
  except Exception as e:
    st.error(f"数据加载失败，请检查 data.xlsx 文件是否存在！错误信息：{e}")
    return None


df = load_data()

# 2. 搜索输入框与查询逻辑
if df is not None:
  kw = st.text_input("请输入员工姓名或手机 IMEI 号：", "").strip()

  if kw:
    # 模糊匹配姓名或 IMEI
    result = df[
        (df["员工姓名"].str.contains(kw, case=False, na=False))
        | (df["手机IMEI"].str.contains(kw, case=False, na=False))
    ]

    if not result.empty:
      st.success(f"找到 {len(result)} 条匹配记录：")
      # 以网页表格形式展示
      st.dataframe(
          result[["员工姓名", "手机号", "手机IMEI"]],
          use_container_width=True,
          hide_index=True,
      )
    else:
      st.warning("未查找到相关信息，请检查输入是否正确。")