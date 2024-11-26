import urllib.request

def download_file_from_user(ip, port, file_path, save_path):

    url = f"http://{ip}:{port}/{file_path}"
    try:
        print(f"Connecting to {ip} and downloading from: {url}")
        urllib.request.urlretrieve(url, save_path)
        print(f"Downloaded in: {save_path}")
    except Exception as e:
        print(f"Error: {e}")

ip_address = "192.168.151.152"
port = 8080
remote_file_path = "test_download.txt"
local_save_path = "txtdownloaded.txt"  

download_file_from_user(ip_address, port, remote_file_path, local_save_path)
