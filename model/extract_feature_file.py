#dich nguoc ra FCG
from joblib import load
import matplotlib.pyplot as plt
import networkx as nx
from androguard.misc import AnalyzeAPK

# Tải lại mô hình từ tệp đã lưu
modelAPI = load('D:/HocTap/code/BTL-Python/PythonWeb/model/modelAPI.joblib')
modelUser = load('D:/HocTap/code/BTL-Python/PythonWeb/model/modelUser2.joblib')

def generate_fcg(apk_file): #dich nguoc APK sang do thi FCG
    try:
        _, _, dx = AnalyzeAPK(apk_file)
        fcg = dx.get_call_graph()
        return fcg
    except Exception as e:
        print("file {apk_file} gap loi, bo qua")
        return None

#GCN
import dgl
import torch
import torch.nn as nn
import dgl.function as fn
from dgl.nn import GraphConv

class GCN(nn.Module):
    def __init__(self, in_feats, hidden_dims, out_feats):
        torch.manual_seed(1234) #đảm bảo rằng mỗi lần chạy mô hình, kết quả sẽ luôn giống nhau
        super(GCN, self).__init__()
        
        #Khai báo các lớp Conv
        self.conv1 = GraphConv(in_feats, hidden_dims[0])
        self.conv2 = GraphConv(hidden_dims[0], hidden_dims[1])
        self.conv3 = GraphConv(hidden_dims[1], hidden_dims[2])
        self.fc = nn.Linear(hidden_dims[2], out_feats)

    def forward(self, g, features):
        # First layer
        h = torch.relu(self.conv1(g, features))
        # Second layer
        h = torch.relu(self.conv2(g, h))
        # Third layer
        h = torch.relu(self.conv3(g, h))
        # Output layer
        h = self.fc(h)
        #return h
        return torch.mean(h, dim=0)
       
        '''
        Dua h vao ham Liner classifier
        Là một lớp tuyến tính cuối cùng để ánh xạ embedding node thu được từ lớp GCN 
        sang các lớp đầu ra dự đoán (ví dụ: phân loại).
        '''   
         
        '''
        Mục đích chính của việc sử dụng ReLU là giúp mô hình học được các biểu diễn phi tuyến tính của dữ liệu đồ thị, 
        làm cho nó có khả năng học được các đặc trưng phức tạp và hiệu quả hơn. 
        Đồng thời, ReLU cũng giúp giảm nguy cơ hiện tượng "vanishing gradient" 
        và tăng tính tích cực của các đầu ra, giúp cho quá trình huấn luyện mạng GCN được dễ dàng hơn.
        '''
from androguard.core.analysis.analysis import ExternalMethod

def process(path_apkFile):
    '''
    Hàm trả về kết quả đầu ra của 1 file apk sau khi đi qua GCN
    '''
    try:
        fcg = generate_fcg(path_apkFile)
        if fcg is None:
            return None
        # Lấy các đặc trưng user (đặc trưng của các node) --> DatasetInternal
        if fcg is not None and fcg.size != 0:
            # Tổng hợp các đặc trưng, nếu node ngoài thì lấy các đặc trưng API, nếu node trong thì lấy đặc trưng User
            feature_graph = {}
            for node in fcg.nodes:
                if node is not None:
                    features =[]
                    if isinstance(node, ExternalMethod):
                        name = str(node.class_name)[1:-1]
                        features = modelAPI.infer_vector(name.split("/"))
                    else:
                        opcode_groups = set()
                        for instr in node.get_instructions():
                            opcode_groups.add(instr.get_name())
                        features = modelUser.infer_vector(list(opcode_groups))
                    feature_graph[node] = features

            # Xử lý dữ liệu để đưa vào model GCN
            nx.set_node_attributes(fcg, feature_graph, name="features")
            fcg = nx.convert_node_labels_to_integers(fcg)
            features = [x for x in feature_graph.values()]
            features = torch.tensor(features)
            g = dgl.from_networkx(fcg)
            g = dgl.add_self_loop(g)
            model = GCN(100, [80, 70, 70], 70)
            t = model.forward(g, features)
            return t
    except Exception as e:
        print(f"Error in processing APK file: {e}")
        return None


#Phân tích dữ liệu để chuẩn bị train, các đặc trưng và nhãn của 1 file apk được lưu trong 1 file csv
import os
import csv

def process_apks(directory_path, output_file): #Predict cả thư mục
    """
    Xử lý các file APK trong một thư mục và ghi kết quả vào một file văn bản.
    Parameters:
    directory_path (str): Đường dẫn đến thư mục chứa các file APK.
    process_function (function): Hàm xử lý mỗi file APK, nhận một đường dẫn file APK và trả về tensor.
    output_file (str): Đường dẫn đến file csv để ghi kết quả, mỗi tensor sẽ được ghi trên một dòng.
    """
    with open(output_file, 'a', newline='') as f_out:
        writer = csv.writer(f_out)
        for file_name in os.listdir(directory_path):
            if file_name.endswith('.apk'):
                file_path = os.path.join(directory_path, file_name)
                    # Xử lý FCG và ghi kết quả vào file csv
                tensor = process(file_path)
                if tensor is not None:
                    tensor = tensor.tolist()
                    tensor.append(file_name)
                    writer.writerow(tensor)
    print("Đã xử lý xong")
    
def file(file_path, output_file): #Predict 1 file 
    with open(output_file, 'a', newline='') as f:
        writer = csv.writer(f)
            # Xử lý FCG và ghi kết quả vào file csv
        tensor = process(file_path)

        if tensor is not None:
            tensor = tensor.tolist()
            tensor.append(file_path)
            writer.writerow(tensor)
            print(f"Đã xử lý thành công APK {file_path}")
        else:
            print(f"File APK {file_path} gặp lỗi")       
                                       
# # Đường dẫn đến thư mục chứa các file APK
# directory_path = r'DataAPK\dataBegin2\thuMuc1-dùng để làm predict'

# # Đường dẫn đến file csv để ghi kết quả
# output_file = r'D:\HocTap\code\BTL-Python\data_predict2.csv'   
# process_apks(directory_path, output_file)
