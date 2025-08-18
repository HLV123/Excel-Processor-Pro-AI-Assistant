import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducible data
np.random.seed(42)
random.seed(42)

def create_sample_excel_files():
    """Tạo nhiều file Excel mẫu với dữ liệu đa dạng"""
    
    # 1. DOANH SỐ BÁN HÀNG - File chính để test
    print("Tạo file: doanh_so_ban_hang.xlsx")
    
    regions = ['Hà Nội', 'TP.HCM', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ', 'Nha Trang', 'Huế', 'Vũng Tàu']
    products = ['Laptop Dell', 'Laptop HP', 'Laptop Asus', 'iPhone 15', 'Samsung Galaxy', 'iPad Pro', 
                'MacBook Air', 'Surface Pro', 'Gaming PC', 'Monitor 4K', 'Chuột gaming', 'Bàn phím cơ']
    months = ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06',
              '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12']
    
    sales_data = []
    for _ in range(500):  # 500 bản ghi
        sales_data.append({
            'Region': np.random.choice(regions),
            'Product': np.random.choice(products),
            'Month': np.random.choice(months),
            'Sales': np.random.randint(50000, 2000000),  # 50k - 2M VNĐ
            'Quantity': np.random.randint(1, 50),
            'Cost': np.random.randint(20000, 1500000),
            'Profit': lambda x: x['Sales'] - x['Cost'],
            'Salesperson': np.random.choice(['Nguyễn Văn A', 'Trần Thị B', 'Lê Văn C', 'Phạm Thị D', 'Hoàng Văn E'])
        })
    
    # Calculate profit
    for record in sales_data:
        record['Profit'] = record['Sales'] - record['Cost']
        record['Profit_Margin'] = round((record['Profit'] / record['Sales']) * 100, 2)
    
    df_sales = pd.DataFrame(sales_data)
    df_sales.to_excel('doanh_so_ban_hang.xlsx', index=False)
    
    # 2. NHÂN SỰ CÔNG TY
    print("Tạo file: nhan_su_cong_ty.xlsx")
    
    departments = ['IT', 'Marketing', 'Sales', 'HR', 'Finance', 'Operations', 'R&D']
    positions = ['Nhân viên', 'Trưởng nhóm', 'Quản lý', 'Giám đốc']
    cities = ['Hà Nội', 'TP.HCM', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ']
    
    hr_data = []
    for i in range(300):  # 300 nhân viên
        base_salary = np.random.randint(8000000, 50000000)  # 8M - 50M VNĐ
        hr_data.append({
            'Employee_ID': f'EMP{i+1:03d}',
            'Name': f'Nhân viên {i+1}',
            'Department': np.random.choice(departments),
            'Position': np.random.choice(positions),
            'City': np.random.choice(cities),
            'Age': np.random.randint(22, 60),
            'Years_Experience': np.random.randint(0, 30),
            'Base_Salary': base_salary,
            'Bonus': np.random.randint(0, base_salary//4),
            'Total_Salary': lambda x: x['Base_Salary'] + x['Bonus'],
            'Performance_Score': round(np.random.uniform(1.0, 5.0), 1),
            'Hire_Date': (datetime.now() - timedelta(days=np.random.randint(30, 3650))).strftime('%Y-%m-%d')
        })
    
    # Calculate total salary
    for record in hr_data:
        record['Total_Salary'] = record['Base_Salary'] + record['Bonus']
    
    df_hr = pd.DataFrame(hr_data)
    df_hr.to_excel('nhan_su_cong_ty.xlsx', index=False)
    
    # 3. KHẢO SÁT HÀI LÒNG KHÁCH HÀNG
    print("Tạo file: khao_sat_khach_hang.xlsx")
    
    services = ['Dịch vụ A', 'Dịch vụ B', 'Dịch vụ C', 'Dịch vụ D', 'Dịch vụ E']
    age_groups = ['18-25', '26-35', '36-45', '46-55', '55+']
    genders = ['Nam', 'Nữ']
    
    survey_data = []
    for i in range(800):  # 800 phản hồi
        survey_data.append({
            'Response_ID': f'R{i+1:04d}',
            'Service': np.random.choice(services),
            'Age_Group': np.random.choice(age_groups),
            'Gender': np.random.choice(genders),
            'Region': np.random.choice(regions),
            'Satisfaction_Score': np.random.randint(1, 6),  # 1-5 scale
            'Recommend_Score': np.random.randint(1, 11),   # 1-10 scale
            'Price_Rating': np.random.randint(1, 6),
            'Quality_Rating': np.random.randint(1, 6),
            'Support_Rating': np.random.randint(1, 6),
            'Overall_Experience': np.random.choice(['Rất tốt', 'Tốt', 'Trung bình', 'Kém', 'Rất kém']),
            'Will_Return': np.random.choice(['Có', 'Không', 'Có thể']),
            'Survey_Date': (datetime.now() - timedelta(days=np.random.randint(1, 365))).strftime('%Y-%m-%d')
        })
    
    df_survey = pd.DataFrame(survey_data)
    df_survey.to_excel('khao_sat_khach_hang.xlsx', index=False)
    
    # 4. BÁO CÁO TÀI CHÍNH
    print("Tạo file: bao_cao_tai_chinh.xlsx")
    
    quarters = ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023', 
                'Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
    categories = ['Doanh thu', 'Chi phí vận hành', 'Chi phí marketing', 'Chi phí nhân sự', 
                  'Lợi nhuận gộp', 'Thuế', 'Lợi nhuận ròng']
    
    finance_data = []
    for quarter in quarters:
        for category in categories:
            if category == 'Doanh thu':
                amount = np.random.randint(50000000, 200000000)  # 50M - 200M
            elif 'Chi phí' in category:
                amount = np.random.randint(10000000, 80000000)   # 10M - 80M
            elif 'Lợi nhuận' in category:
                amount = np.random.randint(5000000, 50000000)    # 5M - 50M
            else:  # Thuế
                amount = np.random.randint(2000000, 15000000)    # 2M - 15M
            
            finance_data.append({
                'Quarter': quarter,
                'Category': category,
                'Amount': amount,
                'Currency': 'VNĐ',
                'Year': int(quarter.split()[-1]),
                'Quarter_Number': quarter.split()[0]
            })
    
    df_finance = pd.DataFrame(finance_data)
    df_finance.to_excel('bao_cao_tai_chinh.xlsx', index=False)
    
    # 5. THỐNG KÊ WEBSITE
    print("Tạo file: thong_ke_website.xlsx")
    
    pages = ['Trang chủ', 'Sản phẩm', 'Dịch vụ', 'Liên hệ', 'Blog', 'Giới thiệu']
    sources = ['Google', 'Facebook', 'Direct', 'Email', 'YouTube', 'Instagram']
    devices = ['Desktop', 'Mobile', 'Tablet']
    
    web_data = []
    base_date = datetime.now() - timedelta(days=90)
    
    for i in range(1000):  # 1000 sessions
        session_date = base_date + timedelta(days=np.random.randint(0, 90))
        web_data.append({
            'Date': session_date.strftime('%Y-%m-%d'),
            'Page': np.random.choice(pages),
            'Traffic_Source': np.random.choice(sources),
            'Device': np.random.choice(devices),
            'Sessions': np.random.randint(1, 50),
            'Page_Views': np.random.randint(1, 100),
            'Bounce_Rate': round(np.random.uniform(0.1, 0.8), 2),
            'Avg_Session_Duration': np.random.randint(30, 600),  # seconds
            'Conversions': np.random.randint(0, 10),
            'Revenue': np.random.randint(0, 5000000),  # VNĐ
            'New_Users': np.random.randint(0, 30),
            'Returning_Users': np.random.randint(0, 20)
        })
    
    df_web = pd.DataFrame(web_data)
    df_web.to_excel('thong_ke_website.xlsx', index=False)
    
    # 6. QUẢN LÝ KHO HÀNG
    print("Tạo file: quan_ly_kho.xlsx")
    
    warehouses = ['Kho A - Hà Nội', 'Kho B - TP.HCM', 'Kho C - Đà Nẵng', 'Kho D - Cần Thơ']
    product_categories = ['Điện tử', 'Gia dụng', 'Thời trang', 'Sách', 'Thể thao', 'Làm đẹp']
    
    inventory_data = []
    for i in range(400):  # 400 sản phẩm
        current_stock = np.random.randint(0, 1000)
        min_stock = np.random.randint(10, 100)
        max_stock = np.random.randint(500, 2000)
        
        inventory_data.append({
            'Product_Code': f'P{i+1:04d}',
            'Product_Name': f'Sản phẩm {i+1}',
            'Category': np.random.choice(product_categories),
            'Warehouse': np.random.choice(warehouses),
            'Current_Stock': current_stock,
            'Min_Stock_Level': min_stock,
            'Max_Stock_Level': max_stock,
            'Unit_Price': np.random.randint(50000, 2000000),
            'Total_Value': lambda x: x['Current_Stock'] * x['Unit_Price'],
            'Supplier': f'Nhà cung cấp {np.random.randint(1, 20)}',
            'Last_Restock_Date': (datetime.now() - timedelta(days=np.random.randint(1, 180))).strftime('%Y-%m-%d'),
            'Status': 'Thiếu hàng' if current_stock < min_stock else 'Bình thường',
            'Lead_Time_Days': np.random.randint(1, 30)
        })
    
    # Calculate total value
    for record in inventory_data:
        record['Total_Value'] = record['Current_Stock'] * record['Unit_Price']
    
    df_inventory = pd.DataFrame(inventory_data)
    df_inventory.to_excel('quan_ly_kho.xlsx', index=False)
    
    print("\n✅ Đã tạo thành công 6 file Excel mẫu:")
    print("1. doanh_so_ban_hang.xlsx - Dữ liệu bán hàng (500 bản ghi)")
    print("2. nhan_su_cong_ty.xlsx - Dữ liệu nhân sự (300 nhân viên)")
    print("3. khao_sat_khach_hang.xlsx - Khảo sát hài lòng (800 phản hồi)")
    print("4. bao_cao_tai_chinh.xlsx - Báo cáo tài chính (56 bản ghi)")
    print("5. thong_ke_website.xlsx - Thống kê web (1000 sessions)")
    print("6. quan_ly_kho.xlsx - Quản lý kho (400 sản phẩm)")
    
    return [
        'doanh_so_ban_hang.xlsx',
        'nhan_su_cong_ty.xlsx', 
        'khao_sat_khach_hang.xlsx',
        'bao_cao_tai_chinh.xlsx',
        'thong_ke_website.xlsx',
        'quan_ly_kho.xlsx'
    ]

if __name__ == "__main__":
    files = create_sample_excel_files()
    
    # In thông tin chi tiết về từng file
    print("\n" + "="*60)
    print("CHI TIẾT CÁC FILE MẪU:")
    print("="*60)
    
    print("\n📊 DOANH SỐ BÁN HÀNG (doanh_so_ban_hang.xlsx)")
    print("- Cột X gợi ý: Region, Product, Month")  
    print("- Cột Y gợi ý: Sales, Quantity, Profit")
    print("- Phù hợp: Biểu đồ cột, tròn, đường")
    
    print("\n👥 NHÂN SỰ CÔNG TY (nhan_su_cong_ty.xlsx)")
    print("- Cột X gợi ý: Department, Position, City")
    print("- Cột Y gợi ý: Base_Salary, Total_Salary, Age")
    print("- Phù hợp: Biểu đồ cột, tròn")
    
    print("\n📋 KHẢO SÁT KHÁCH HÀNG (khao_sat_khach_hang.xlsx)")
    print("- Cột X gợi ý: Service, Age_Group, Region")
    print("- Cột Y gợi ý: Satisfaction_Score, Recommend_Score")
    print("- Phù hợp: Biểu đồ cột, tròn")
    
    print("\n💰 BÁO CÁO TÀI CHÍNH (bao_cao_tai_chinh.xlsx)")
    print("- Cột X gợi ý: Quarter, Category")
    print("- Cột Y gợi ý: Amount")
    print("- Phù hợp: Biểu đồ cột, đường")
    
    print("\n🌐 THỐNG KÊ WEBSITE (thong_ke_website.xlsx)")
    print("- Cột X gợi ý: Page, Traffic_Source, Device")
    print("- Cột Y gợi ý: Sessions, Page_Views, Revenue")
    print("- Phù hợp: Biểu đồ cột, tròn, đường")
    
    print("\n📦 QUẢN LÝ KHO (quan_ly_kho.xlsx)")
    print("- Cột X gợi ý: Category, Warehouse, Status")
    print("- Cột Y gợi ý: Current_Stock, Total_Value, Unit_Price")
    print("- Phù hợp: Biểu đồ cột, tròn")
    
    print(f"\n🎯 FILE KHUYẾN NGHỊ ĐỂ TEST: doanh_so_ban_hang.xlsx")
    print("   (Có nhiều dữ liệu đa dạng, phù hợp test mọi tính năng)")