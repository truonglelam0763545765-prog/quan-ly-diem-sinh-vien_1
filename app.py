import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# 1. Tạo dữ liệu mẫu cho 10 sinh viên
data = {
    "Ho_ten": [
        "Nguyễn Văn An",
        "Trần Thị Bích",
        "Lê Hoàng Cường",
        "Phạm Thị Dung",
        "Hoàng Văn Em",
        "Vũ Thị Phương",
        "Đỗ Minh Giáp",
        "Bùi Thị Hằng",
        "Ngô Văn Hùng",
        "Dương Thị Linh",
    ],
    "Chuyen_can": [8.0, 9.0, 7.5, 6.0, 10.0, 8.5, 5.5, 9.0, 7.0, 8.0],
    "Giua_ky": [7.0, 8.5, 6.5, 5.0, 9.0, 7.5, 4.5, 8.0, 6.0, 7.5],
    "Cuoi_ky": [7.5, 8.0, 7.0, 5.5, 8.5, 8.0, 5.0, 8.5, 6.5, 7.0],
}

df = pd.DataFrame(data)

# 2. Tính điểm tổng kết
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"] + 0.3 * df["Giua_ky"] + 0.5 * df["Cuoi_ky"]
).round(2)


# 3. Xếp loại sinh viên
def xep_loai(diem):
  if diem >= 8.5:
    return "Giỏi"
  elif diem >= 7.0:
    return "Khá"
  elif diem >= 5.0:
    return "Trung bình"
  else:
    return "Yếu"


df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# 4. Thống kê cơ bản
dtb_lop = round(df["Tong_ket"].mean(), 2)
sv_max = df.loc[df["Tong_ket"].idxmax()]
sv_min = df.loc[df["Tong_ket"].idxmin()]
so_luong_dat = len(df[df["Tong_ket"] >= 5.0])

# ==================== 5. Giao diện Streamlit ====================
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# Hiển thị bảng điểm
st.subheader("📋 Bảng điểm chi tiết của sinh viên")
st.dataframe(df, use_container_width=True)

# Hiển thị các chỉ số thống kê
st.subheader("📊 Thống kê chung của lớp")
col1, col2, col3, col4 = st.columns(4)
with col1:
  st.metric(label="Điểm TB lớp", value=dtb_lop)
with col2:
  st.metric(label="Số sinh viên đạt", value=f"{so_luong_dat}/10")
with col3:
  st.metric(label="Điểm cao nhất", value=f"{sv_max['Tong_ket']} ({sv_max['Ho_ten']})")
with col4:
  st.metric(label="Điểm thấp nhất", value=f"{sv_min['Tong_ket']} ({sv_min['Ho_ten']})")

# Danh sách chọn sinh viên để xem chi tiết
st.subheader("🔍 Tra cứu thông tin sinh viên")
selected_student = st.selectbox("Chọn tên sinh viên:", df["Ho_ten"].tolist())

# Lọc thông tin sinh viên được chọn
student_info = df[df["Ho_ten"] == selected_student].iloc[0]
scol1, scol2, scol3, scol4, scol5 = st.columns(5)
scol1.metric("Chuyên cần", student_info["Chuyen_can"])
scol2.metric("Giữa kỳ", student_info["Giua_ky"])
scol3.metric("Cuối kỳ", student_info["Cuoi_ky"])
scol4.metric("Tổng kết", student_info["Tong_ket"])
scol5.metric("Xếp loại", student_info["Xep_loai"])

# Trực quan hóa biểu đồ cột bằng Matplotlib
st.subheader("📈 Biểu đồ điểm tổng kết của lớp")
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(df["Ho_ten"], df["Tong_ket"], color="skyblue", edgecolor="navy")
ax.set_xlabel("Họ và tên sinh viên", fontsize=10)
ax.set_ylabel("Điểm tổng kết", fontsize=10)
ax.set_title("Biểu đồ điểm tổng kết 10 sinh viên", fontsize=12, fontweight="bold")
plt.xticks(rotation=45, ha="right")
ax.set_ylim(0, 10)

# Hiển thị giá trị lên trên mỗi cột
for bar in bars:
  height = bar.get_height()
  ax.annotate(
      f"{height}",
      xy=(bar.get_x() + bar.get_width() / 2, height),
      xytext=(0, 3),  # 3 points vertical offset
      textcoords="offset points",
      ha="center",
      va="bottom",
      fontsize=9,
  )

st.pyplot(fig)

# Thông tin người tạo ứng dụng ở chân trang
st.markdown("---")
st.markdown(
    """<p style='text-align: center; font-size: small; color: gray;'>Ứng dụng được tạo bởi: LÊ LÂM TRƯỜNG - MSSV: [051208013991]</p>""",
    unsafe_allow_html=True,
)
