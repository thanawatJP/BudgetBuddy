# ใช้ Python 3.9 เป็น base image
FROM python:3.9

# ตั้ง working directory
WORKDIR /app

# คัดลอกไฟล์ requirements.txt
COPY requirements.txt /app/

# ติดตั้ง dependencies   no-cache-dir -r requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt


# คัดลอกไฟล์แอปทั้งหมดไปยัง working directory
COPY . /app/

# เปิดพอร์ตที่ Django จะทำงาน
EXPOSE /app/budgetbuddy

# คำสั่งในการเริ่มแอป Django
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000]
