import streamlit as st

# Cấu hình giao diện
st.set_page_config(
    page_title="Tính chỉ số DTI",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 HỆ THỐNG TÍNH CHỈ SỐ DTI")
st.write("Nhập thông tin khoản vay và tình hình tài chính của khách hàng.")

# Nhập thông tin khách hàng
st.subheader("1. Thông tin khoản vay")

STV = st.number_input(
    "Số tiền vay (đồng)",
    min_value=0,
    value=800_000_000,
    step=10_000_000
)

THV = st.number_input(
    "Thời hạn vay (năm)",
    min_value=1,
    value=5,
    step=1
)

LS = st.number_input(
    "Lãi suất vay (%/năm)",
    min_value=0.0,
    value=12.0,
    step=0.5
)

st.subheader("2. Thông tin tài chính khách hàng")

TN = st.number_input(
    "Thu nhập hàng tháng (đồng)",
    min_value=0,
    value=45_000_000,
    step=1_000_000
)

NC = st.number_input(
    "Khoản nợ cũ phải trả hàng tháng (đồng)",
    min_value=0,
    value=10_000_000,
    step=1_000_000
)

CPSH = st.number_input(
    "Chi phí sinh hoạt mỗi người/tháng (đồng)",
    min_value=0,
    value=4_000_000,
    step=500_000
)

SN = st.number_input(
    "Số người trong gia đình",
    min_value=1,
    value=3,
    step=1
)

# Nút tính toán
if st.button("TÍNH CHỈ SỐ DTI", type="primary"):

    # Kiểm tra dữ liệu
    if THV <= 0:
        st.error("Thời hạn vay phải lớn hơn 0.")
    elif TN <= CPSH * SN:
        st.error(
            "Thu nhập phải lớn hơn tổng chi phí sinh hoạt "
            "của gia đình."
        )
    else:
        # Quy đổi lãi suất từ % sang số thập phân
        lai_suat = LS / 100

        # Tính tiền gốc phải trả hàng tháng
        tien_goc_thang = STV / (THV * 12)

        # Tính tiền lãi hàng tháng theo công thức ban đầu
        tien_lai_thang = STV * (lai_suat / 12)

        # Tổng nghĩa vụ nợ hàng tháng
        tong_no_thang = (
            tien_goc_thang
            + tien_lai_thang
            + NC
        )

        # Tổng chi phí sinh hoạt gia đình
        tong_chi_phi_sinh_hoat = CPSH * SN

        # Thu nhập còn lại sau chi phí sinh hoạt
        thu_nhap_con_lai = TN - tong_chi_phi_sinh_hoat

        # Tính chỉ số DTI
        DTI = tong_no_thang / thu_nhap_con_lai

        # Hiển thị kết quả
        st.subheader("3. Kết quả đánh giá")

        st.metric(
            label="Chỉ số DTI",
            value=f"{DTI * 100:.2f}%"
        )

        st.write(
            f"**Tiền gốc hàng tháng:** "
            f"{tien_goc_thang:,.0f} đồng"
        )

        st.write(
            f"**Tiền lãi hàng tháng:** "
            f"{tien_lai_thang:,.0f} đồng"
        )

        st.write(
            f"**Tổng nghĩa vụ nợ hàng tháng:** "
            f"{tong_no_thang:,.0f} đồng"
        )

        st.write(
            f"**Thu nhập còn lại sau chi phí sinh hoạt:** "
            f"{thu_nhap_con_lai:,.0f} đồng"
        )

        # Kết luận theo điều kiện trong code gốc
        if DTI < 0.7:
            st.success(
                "KẾT LUẬN: ĐƯỢC VAY"
            )
            st.write(
                "Chỉ số DTI nhỏ hơn 70%."
            )
        else:
            st.error(
                "KẾT LUẬN: KHÔNG ĐƯỢC VAY"
            )
            st.write(
                "Chỉ số DTI lớn hơn hoặc bằng 70%."
            )
