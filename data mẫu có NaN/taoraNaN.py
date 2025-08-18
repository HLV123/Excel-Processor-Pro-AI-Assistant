import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducible data
np.random.seed(42)
random.seed(42)

def create_sample_data_with_nan():
    """Tạo file Excel mẫu có chứa giá trị NaN để test xử lý"""
    
    print("Tạo file dữ liệu có NaN: doanh_so_co_nan.xlsx")
    
    # Base data
    regions = ['Hà Nội', 'TP.HCM', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ', 'Nha Trang', 'Huế', 'Vũng Tàu']
    products = ['Laptop Dell', 'Laptop HP', 'Laptop Asus', 'iPhone 15', 'Samsung Galaxy', 'iPad Pro', 
                'MacBook Air', 'Surface Pro', 'Gaming PC', 'Monitor 4K', 'Chuột gaming', 'Bàn phím cơ']
    months = ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06',
              '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12']
    salespeople = ['Nguyễn Văn A', 'Trần Thị B', 'Lê Văn C', 'Phạm Thị D', 'Hoàng Văn E', 'Vũ Thị F']
    
    sales_data = []
    for i in range(300):  # 300 bản ghi
        sales_data.append({
            'STT': i + 1,
            'Region': np.random.choice(regions),
            'Product': np.random.choice(products),
            'Month': np.random.choice(months),
            'Sales': np.random.randint(50000, 2000000),
            'Quantity': np.random.randint(1, 50),
            'Cost': np.random.randint(20000, 1500000),
            'Salesperson': np.random.choice(salespeople),
            'Customer_Type': np.random.choice(['Cá nhân', 'Doanh nghiệp', 'Đại lý']),
            'Discount': np.random.uniform(0, 0.3),
            'Rating': np.random.randint(1, 6),
            'Notes': f'Ghi chú {i+1}' if np.random.random() > 0.3 else ''
        })
    
    df = pd.DataFrame(sales_data)
    
    # Calculate derived columns
    df['Profit'] = df['Sales'] - df['Cost']
    df['Profit_Margin'] = (df['Profit'] / df['Sales']) * 100
    df['Revenue_Per_Item'] = df['Sales'] / df['Quantity']
    
    # INJECT NaN VALUES STRATEGICALLY
    print("🔧 Đang chèn giá trị NaN...")
    
    # 1. REGION - 5% NaN (ít NaN)
    nan_indices = np.random.choice(df.index, size=int(len(df) * 0.05), replace=False)
    df.loc[nan_indices, 'Region'] = np.nan
    print(f"   • Region: {len(nan_indices)} NaN (5%)")
    
    # 2. SALES - 10% NaN (trung bình NaN)  
    nan_indices = np.random.choice(df.index, size=int(len(df) * 0.10), replace=False)
    df.loc[nan_indices, 'Sales'] = np.nan
    print(f"   • Sales: {len(nan_indices)} NaN (10%)")
    
    # 3. QUANTITY - 15% NaN (khá nhiều NaN)
    nan_indices = np.random.choice(df.index, size=int(len(df) * 0.15), replace=False)
    df.loc[nan_indices, 'Quantity'] = np.nan
    print(f"   • Quantity: {len(nan_indices)} NaN (15%)")
    
    # 4. COST - 20% NaN (nhiều NaN)
    nan_indices = np.random.choice(df.index, size=int(len(df) * 0.20), replace=False)
    df.loc[nan_indices, 'Cost'] = np.nan
    print(f"   • Cost: {len(nan_indices)} NaN (20%)")
    
    # 5. SALESPERSON - 25% NaN (rất nhiều NaN)
    nan_indices = np.random.choice(df.index, size=int(len(df) * 0.25), replace=False)
    df.loc[nan_indices, 'Salesperson'] = np.nan
    print(f"   • Salesperson: {len(nan_indices)} NaN (25%)")
    
    # 6. DISCOUNT - 30% NaN (cực nhiều NaN)
    nan_indices = np.random.choice(df.index, size=int(len(df) * 0.30), replace=False)
    df.loc[nan_indices, 'Discount'] = np.nan
    print(f"   • Discount: {len(nan_indices)} NaN (30%)")
    
    # 7. RATING - 60% NaN (quá nhiều NaN - nên cảnh báo)
    nan_indices = np.random.choice(df.index, size=int(len(df) * 0.60), replace=False)
    df.loc[nan_indices, 'Rating'] = np.nan
    print(f"   • Rating: {len(nan_indices)} NaN (60%) - Cảnh báo!")
    
    # 8. NOTES - 40% NaN (nhiều NaN cho text)
    nan_indices = np.random.choice(df.index, size=int(len(df) * 0.40), replace=False)
    df.loc[nan_indices, 'Notes'] = np.nan
    print(f"   • Notes: {len(nan_indices)} NaN (40%)")
    
    # Recalculate derived columns (will have NaN where input is NaN)
    df['Profit'] = df['Sales'] - df['Cost']
    df['Profit_Margin'] = (df['Profit'] / df['Sales']) * 100
    df['Revenue_Per_Item'] = df['Sales'] / df['Quantity']
    
    # Save to Excel
    df.to_excel('doanh_so_co_nan.xlsx', index=False)
    
    # Print summary
    print(f"\n✅ Đã tạo file: doanh_so_co_nan.xlsx")
    print(f"📊 Tổng quan:")
    print(f"   • Tổng bản ghi: {len(df)}")
    print(f"   • Tổng cột: {len(df.columns)}")
    print(f"   • Tổng ô: {df.size:,}")
    
    total_nan = df.isnull().sum().sum()
    nan_percentage = (total_nan / df.size) * 100
    print(f"   • Tổng ô NaN: {total_nan:,} ({nan_percentage:.1f}%)")
    
    print(f"\n📋 Chi tiết NaN theo cột:")
    for col in df.columns:
        nan_count = df[col].isnull().sum()
        if nan_count > 0:
            nan_pct = (nan_count / len(df)) * 100
            print(f"   • {col}: {nan_count} NaN ({nan_pct:.1f}%)")
    
    print(f"\n🎯 TEST SCENARIOS ĐƯÜỢC:")
    print(f"   ✅ Cột ít NaN (5%): Region - Có thể fill/drop")
    print(f"   ⚠️ Cột trung bình NaN (10-20%): Sales, Cost - Cần chiến lược")  
    print(f"   ❌ Cột nhiều NaN (25-60%): Salesperson, Rating - Cảnh báo")
    print(f"   🔢 Cột số: Sales, Quantity, Cost, Discount - Test fill median/mean")
    print(f"   📝 Cột text: Region, Product, Salesperson - Test fill mode/unknown")
    
    return 'doanh_so_co_nan.xlsx'

def create_extreme_nan_data():
    """Tạo file có NaN cực độ để test edge cases"""
    
    print("\nTạo file dữ liệu NaN cực độ: du_lieu_nan_cuc_do.xlsx")
    
    data = {
        'ID': range(1, 101),  # 100 bản ghi
        'Name': [f'Item {i}' for i in range(1, 101)],
        'Value1': np.random.randint(1, 100, 100),
        'Value2': np.random.randint(1, 100, 100),
        'Category': np.random.choice(['A', 'B', 'C'], 100),
        'Status': np.random.choice(['Active', 'Inactive'], 100),
        'Score': np.random.uniform(0, 10, 100),
        'Comment': [f'Comment {i}' if i % 3 == 0 else '' for i in range(100)]
    }
    
    df = pd.DataFrame(data)
    
    # EXTREME NaN injection
    
    # 1. Cột 95% NaN - Gần như vô dụng
    nan_indices = np.random.choice(df.index, size=95, replace=False)
    df.loc[nan_indices, 'Value1'] = np.nan
    print(f"   • Value1: 95% NaN - Gần như vô dụng")
    
    # 2. Cột 80% NaN - Rất khó sử dụng
    nan_indices = np.random.choice(df.index, size=80, replace=False)
    df.loc[nan_indices, 'Value2'] = np.nan
    print(f"   • Value2: 80% NaN - Rất khó sử dụng")
    
    # 3. Cột 70% NaN - Nhiều NaN
    nan_indices = np.random.choice(df.index, size=70, replace=False)
    df.loc[nan_indices, 'Score'] = np.nan
    print(f"   • Score: 70% NaN - Nhiều NaN")
    
    # 4. Cột toàn NaN - Edge case
    df['All_NaN'] = np.nan
    print(f"   • All_NaN: 100% NaN - Edge case")
    
    # 5. Cột không NaN - Baseline
    df['No_NaN'] = range(1, 101)
    print(f"   • No_NaN: 0% NaN - Baseline")
    
    df.to_excel('du_lieu_nan_cuc_do.xlsx', index=False)
    
    total_nan = df.isnull().sum().sum()
    nan_percentage = (total_nan / df.size) * 100
    print(f"✅ Tạo xong file cực độ: {total_nan:,} NaN ({nan_percentage:.1f}%)")
    
    return 'du_lieu_nan_cuc_do.xlsx'

def create_mixed_data_types_with_nan():
    """Tạo file có nhiều kiểu dữ liệu khác nhau với NaN"""
    
    print("\nTạo file đa kiểu dữ liệu có NaN: da_kieu_du_lieu_nan.xlsx")
    
    dates = pd.date_range('2024-01-01', periods=150, freq='D')
    
    data = {
        'Date': dates,
        'Integer_Col': np.random.randint(1, 1000, 150),
        'Float_Col': np.random.uniform(0.1, 99.9, 150),
        'String_Col': [f'Text_{i}' for i in range(150)],
        'Boolean_Col': np.random.choice([True, False], 150),
        'Category_Col': np.random.choice(['Cat1', 'Cat2', 'Cat3', 'Cat4'], 150),
        'Mixed_Col': [str(i) if i % 2 == 0 else i for i in range(150)],  # Mixed types
        'Email_Col': [f'user{i}@example.com' for i in range(150)],
        'Phone_Col': [f'09{np.random.randint(10000000, 99999999)}' for _ in range(150)],
        'Currency_Col': np.random.uniform(100000, 10000000, 150)
    }
    
    df = pd.DataFrame(data)
    
    # Inject NaN into different data types
    
    # Dates - 10% NaN
    nan_indices = np.random.choice(df.index, size=15, replace=False)
    df.loc[nan_indices, 'Date'] = pd.NaT
    
    # Integers - 20% NaN  
    nan_indices = np.random.choice(df.index, size=30, replace=False)
    df.loc[nan_indices, 'Integer_Col'] = np.nan
    
    # Floats - 15% NaN
    nan_indices = np.random.choice(df.index, size=22, replace=False)
    df.loc[nan_indices, 'Float_Col'] = np.nan
    
    # Strings - 25% NaN
    nan_indices = np.random.choice(df.index, size=37, replace=False)
    df.loc[nan_indices, 'String_Col'] = np.nan
    
    # Booleans - 30% NaN (tricky case)
    nan_indices = np.random.choice(df.index, size=45, replace=False)
    df.loc[nan_indices, 'Boolean_Col'] = np.nan
    
    # Categories - 12% NaN
    nan_indices = np.random.choice(df.index, size=18, replace=False)
    df.loc[nan_indices, 'Category_Col'] = np.nan
    
    # Mixed types - 40% NaN (very tricky)
    nan_indices = np.random.choice(df.index, size=60, replace=False)
    df.loc[nan_indices, 'Mixed_Col'] = np.nan
    
    # Emails - 8% NaN
    nan_indices = np.random.choice(df.index, size=12, replace=False)
    df.loc[nan_indices, 'Email_Col'] = np.nan
    
    # Currency - 18% NaN
    nan_indices = np.random.choice(df.index, size=27, replace=False)
    df.loc[nan_indices, 'Currency_Col'] = np.nan
    
    df.to_excel('da_kieu_du_lieu_nan.xlsx', index=False)
    
    total_nan = df.isnull().sum().sum()
    nan_percentage = (total_nan / df.size) * 100
    print(f"✅ Tạo xong file đa kiểu: {total_nan:,} NaN ({nan_percentage:.1f}%)")
    
    # Print data type info
    print(f"\n📋 Kiểu dữ liệu và NaN:")
    for col in df.columns:
        nan_count = df[col].isnull().sum()
        dtype = df[col].dtype
        print(f"   • {col} ({dtype}): {nan_count} NaN")
    
    return 'da_kieu_du_lieu_nan.xlsx'

if __name__ == "__main__":
    print("🏗️ ĐANG TẠO CÁC FILE TEST CHỨC NĂNG XỬ LÝ NaN...")
    print("=" * 60)
    
    files = []
    
    # 1. File chính để test
    files.append(create_sample_data_with_nan())
    
    # 2. File edge cases
    files.append(create_extreme_nan_data())
    
    # 3. File đa kiểu dữ liệu
    files.append(create_mixed_data_types_with_nan())
    
    print("\n" + "=" * 60)
    print("✅ HOÀN THÀNH! Đã tạo 3 file test chức năng xử lý NaN:")
    print("=" * 60)
    
    print(f"\n1. 📊 {files[0]} - File chính để test")
    print("   • Nhiều tình huống NaN khác nhau (5% đến 60%)")
    print("   • Cả cột số và cột text")
    print("   • Phù hợp test mọi chiến lược xử lý")
    
    print(f"\n2. ⚠️ {files[1]} - File edge cases")
    print("   • NaN cực độ (80-95%)")
    print("   • Cột toàn NaN")
    print("   • Test khả năng xử lý tình huống khó")
    
    print(f"\n3. 🔧 {files[2]} - File đa kiểu dữ liệu")
    print("   • Date, Boolean, Mixed types với NaN") 
    print("   • Test xử lý NaN cho mọi kiểu dữ liệu")
    
    print(f"\n🎯 KHUYẾN NGHỊ:")
    print(f"   • Bắt đầu với: {files[0]}")
    print(f"   • Test với các cột có NaN ít (Region, Sales)")
    print(f"   • Thử các chiến lược: Auto, Fill median/mode, Drop rows")
    print(f"   • Quan sát cảnh báo với cột Rating (60% NaN)")
    
    print(f"\n📈 CÁC SCENARIO TEST NaN:")
    print(f"   1. Region (5% NaN) + Sales (10% NaN) → Biểu đồ cột")
    print(f"   2. Product + Quantity (15% NaN) → Biểu đồ tròn") 
    print(f"   3. Salesperson (25% NaN) + Cost (20% NaN) → Test cảnh báo")
    print(f"   4. So sánh kết quả với/không xử lý NaN")
    
    print(f"\n⚙️ TEST CHỨC NĂNG:")
    print(f"   ✅ Phát hiện NaN tự động")
    print(f"   ✅ Gợi ý giá trị thay thế thông minh")
    print(f"   ✅ Cảnh báo cột có quá nhiều NaN")
    print(f"   ✅ Preview trước/sau xử lý")
    print(f"   ✅ Export kết quả đã xử lý")