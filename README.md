Đây là BTL môn mật mã học cơ sở PTIT An toàn thông tin. Các thư mục: 
- apkDetection: chứa phần back-end (trong thu mục templates) và chứa phần API (phần nhận đường dẫn từ front-end, xử lý, trả về kết quả được thực thi từ model)
- model: code python tạo học máy cho phát hiện mã độc Android
- PythonWeb: thư mục gốc, được tạo ra trong quá trình tạo web Django:
    + settings.py: cấu hình cho Web
    + wsgi.py: dùng để deploy web lên server
    + urls: Tạo ra các đường dẫn url để liên kết các page lại với nhau
    + asgi.py: (không biết)
- ngrok.exe: dùng để deploy web 
# Web_ApkMalware
