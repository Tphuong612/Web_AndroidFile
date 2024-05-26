from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from model import predict as pr
def index(request):
    return render(request, 'pages/base.html')

# def predict(request):
#     if request.method == 'POST' or request.method == "GET":
#         apk_file = request.FILES['file']
#         # Lưu tệp tạm thời để xử lý
#         with open('temp.apk', 'wb+') as destination:
#             for chunk in apk_file.chunks():
#                 destination.write(chunk)

#         # Gọi hàm dự đoán của bạn ở đây
#         prediction = predict_file('temp.apk')

#         # Xóa tệp tạm thời
#         os.remove('temp.apk')

#         return JsonResponse({'prediction': prediction})
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)
@csrf_exempt
def predict(request):
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
# def predict(request):
#     if request.method == 'POST':
#         # Nhận đường dẫn từ front-end
#         filepath = request.POST.get('filepath')
#         if filepath:
#             # Thực hiện dự đoán ở đây, đây chỉ là một ví dụ đơn giản
#             prediction = predict_file(filepath)
#             return JsonResponse({'prediction': prediction})
#         else:
#             return JsonResponse({'error': 'No filepath provided'}, status=400)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)

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
