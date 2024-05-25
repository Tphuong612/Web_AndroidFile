from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import os
from model import predict as pr
def index(request):
    return render(request, 'pages/base.html')

def predict(request):
    if request.method == 'POST':
        apk_file = request.FILES['file']
        # Lưu tệp tạm thời để xử lý
        with open('temp.apk', 'wb+') as destination:
            for chunk in apk_file.chunks():
                destination.write(chunk)

        # Gọi hàm dự đoán của bạn ở đây
        prediction = predict_file('temp.apk')

        # Xóa tệp tạm thời
        os.remove('temp.apk')

        return JsonResponse({'prediction': prediction})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def predict_file(file_path):
    # Hàm xử lý và dự đoán file APK của bạn
    # Trả về kết quả dự đoán
    # Thay đoạn này bằng logic dự đoán thực tế của bạn
    type = pr.sol(file_path)
    return type  # hoặc "malware"
# def predict(request):
#     if request.method == 'POST':
#         # Nhận đường dẫn từ front-end
#         filepath = request.POST.get('filepath')
#         if filepath:
#             # Thực hiện dự đoán ở đây, đây chỉ là một ví dụ đơn giản
#             prediction = predict_malware(filepath)
#             return JsonResponse({'prediction': prediction})
#         else:
#             return JsonResponse({'error': 'No filepath provided'}, status=400)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)

# def predict_malware(filepath):
#     # Trong hàm này, bạn thực hiện quá trình dự đoán xem đường dẫn là malware hay benign
#     # Đây chỉ là một ví dụ đơn giản, bạn cần thay thế bằng logic dự đoán thực tế
#     if 'malware' in filepath.lower():
#         return 'Malicious'
#     else:
#         return 'Benign'  
# # Create your views here.
