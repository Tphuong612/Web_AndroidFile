from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from model import predict as pr
def index(request):
    return render(request, 'pages/base.html')

@csrf_exempt
def predict(request):
    # Hàm nhận đường dẫn tệp từ front-end và trả lại kết quả cho người dùng
    if request.method == 'POST' or request.method == 'GET':
        apk_file = request.FILES.get('file')
        
        if not apk_file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        
        #Lưu tệp tạm thời để xử lý
        temp_file_path = 'temp.apk'
        with open(temp_file_path, 'wb+') as destination:
            for chunk in apk_file.chunks():
                destination.write(chunk)

        try:
            # Gọi hàm dự đoán của bạn ở đây
            prediction = predict_file(temp_file_path)
            # prediction = predict_file(apk_file)

            # Trả về kết quả dự đoán
            return JsonResponse({'prediction': prediction})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            # Xóa tệp tạm thời
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def predict_file(file_path):
    # Hàm xử lý và dự đoán file APK 
    # Trả về kết quả dự đoán
    type = pr.sol(file_path)
    return type  

