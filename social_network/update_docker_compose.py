import requests

try:
    # Lấy địa chỉ IP công khai của EC2 instance
    response = requests.get('http://169.254.169.254/latest/meta-data/public-ipv4')
    response.raise_for_status()  # Kiểm tra nếu có lỗi HTTP
    ec2_ip = response.text
except requests.RequestException as e:
    raise Exception(f"Không thể lấy địa chỉ IP của EC2 instance: {e}")

# Đọc nội dung file docker-compose.yml
try:
    with open('docker-compose.yml', 'r') as file:
        content = file.read()
except FileNotFoundError:
    raise Exception("Không tìm thấy file docker-compose.yml")

# Thay thế placeholder <EC2_PUBLIC_IP> bằng địa chỉ IP mới của EC2 instance
new_content = content.replace('<EC2_PUBLIC_IP>', ec2_ip)

# Ghi lại nội dung mới vào file docker-compose.yml
with open('docker-compose.yml', 'w') as file:
    file.write(new_content)

print(f"Đã thay thế địa chỉ IP thành công với {ec2_ip}.")