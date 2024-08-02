import requests

# Lấy địa chỉ IP công khai của EC2 instance
response = requests.get('http://169.254.169.254/latest/meta-data/public-ipv4')
if response.status_code == 200:
    ec2_ip = response.text
else:
    raise Exception("Không thể lấy địa chỉ IP của EC2 instance")

# Đọc nội dung file docker-compose.yml
with open('docker-compose.yml', 'r') as file:
    content = file.read()

# Thay thế placeholder <EC2_PUBLIC_IP> bằng địa chỉ IP mới của EC2 instance
new_content = content.replace('<EC2_PUBLIC_IP>', ec2_ip)

# Ghi lại nội dung mới vào file docker-compose.yml
with open('docker-compose.yml', 'w') as file:
    file.write(new_content)

print(f"Đã thay thế địa chỉ IP thành công với {ec2_ip}.")