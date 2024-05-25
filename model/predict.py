#Dự đoán 
import pandas as pd
from joblib import load
import numpy as np
from model import extract_feature_file as eff
# from extract_feature_file import file 
# Tải lại mô hình từ tệp đã lưu
modelRF = load(r'D:\HocTap\code\BTL-Python\random_forest_model.joblib')

def sol(file_path):
    #Đường dẫn của file cần dự đoán
    # path = r".\Demo\malwareAD6A2CFAF78C69C5936B35EE4CA59BC09C443DE2AD6447417BC55A1FDF091B00.apk"
    demo_csv = "D:\HocTap\code\BTL-Python\PythonWeb\model\data_predict.csv"

    data = [['feat1', 'feat2', 'feat3', 'feat4', 'feat5', 'feat6', 'feat7', 'feat8', 'feat9', 'feat10', 'feat11', 'feat12', 'feat13', 'feat14', 'feat15', 'feat16', 'feat17', 'feat18', 'feat19', 'feat20', 'feat21', 'feat22', 'feat23', 'feat24', 'feat25', 'feat26', 'feat27', 'feat28', 'feat29', 'feat30', 'feat31', 'feat32', 'feat33', 'feat34', 'feat35', 'feat36', 'feat37', 'feat38', 'feat39', 'feat40', 'feat41', 'feat42', 'feat43', 'feat44', 'feat45', 'feat46', 'feat47', 'feat48', 'feat49', 'feat50', 'feat51', 'feat52', 'feat53', 'feat54', 'feat55', 'feat56', 'feat57', 'feat58', 'feat59', 'feat60', 'feat61', 'feat62', 'feat63', 'feat64', 'feat65', 'feat66', 'feat67', 'feat68', 'feat69', 'feat70', 'label']]
    df = pd.DataFrame(data) 
    df.to_csv(demo_csv, index=False, header=False) #Ghi đè lên tệp đã tồn tại
    eff.file(file_path, demo_csv) #trích xuất đặc trưng và ghi vào file data_demo

    apk_predict = pd.read_csv(demo_csv) #Dự đoán 1 hoac nhieu file dược lưu trong tệp csv này
    feature_files = apk_predict.iloc[:, :-1]  # Chọn tất cả các cột trừ cột cuối cùng làm đặc trưng X
    name_files = apk_predict.iloc[:, -1]

    #Sử dụng mô hình tải lại để dự đoán
    X_pre = np.array(feature_files)

    #dự đoán 
    predictions = modelRF.predict(X_pre)

    for file_name, prediction in zip(name_files, predictions): 
        name = file_name.split('\\')
        if prediction == 1:
            type = 'malware'
        else: 
            type = 'benign'
        print(f"File: {name[-1]}, Dự đoán: {type}")
        return type

# sol("Demo\malwareAD667423ACB7BF3A0C35A8737551CD9380A790D64354C01C22881C2C8A022F6C.apk")