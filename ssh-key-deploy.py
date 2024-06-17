import os
import subprocess
import paramiko
import getpass

def show_menu():
    print("\n请选择一个选项：")
    print("1. 创建 SSH 密钥")
    print("2. 上传现有密钥到服务器")
    print("3. 退出")
    choice = input("输入选项编号：")
    return choice

def create_ssh_key(key_name="id_rsa_dev", key_password=""):
    home_dir = os.path.expanduser("~")
    ssh_dir = os.path.join(home_dir, ".ssh")
    if not os.path.exists(ssh_dir):
        os.makedirs(ssh_dir)

    key_path = os.path.join(ssh_dir, key_name)
    if os.path.exists(key_path):
        print(f"密钥文件 {key_path} 已存在。")
    else:
        try:
            if key_password:
                subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "2048", "-f", key_path, "-N", key_password], check=True)
            else:
                subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "2048", "-f", key_path, "-N", ""], check=True)
            print(f"密钥已创建，路径：{key_path}")
        except subprocess.CalledProcessError as e:
            print(f"创建密钥时出现错误：{e}")

def list_local_keys():
    home_dir = os.path.expanduser("~")
    ssh_dir = os.path.join(home_dir, ".ssh")

    if not os.path.exists(ssh_dir):
        print("没有找到任何密钥文件。请先创建密钥。")
        return []

    keys = [f for f in os.listdir(ssh_dir) if os.path.isfile(os.path.join(ssh_dir, f)) and f.endswith('.pub')]
    if not keys:
        print("没有找到任何密钥文件。请先创建密钥。")
    return keys

def choose_local_key(keys):
    print("\n本地存在的密钥：")
    for idx, key in enumerate(keys, 1):
        print(f"{idx}. {key}")

    choice = input("请选择要上传的密钥编号：")
    try:
        index = int(choice) - 1
        if 0 <= index < len(keys):
            return keys[index]
        else:
            print("无效选择。")
            return None
    except ValueError:
        print("无效选择。")
        return None

def upload_ssh_key(server_ip, username, password, key_name):
    home_dir = os.path.expanduser("~")
    pub_key_path = os.path.join(home_dir, ".ssh", key_name)
    key_path = os.path.join(home_dir, ".ssh", key_name.replace('.pub', ''))

    if not os.path.exists(pub_key_path) or not os.path.exists(key_path):
        print(f"密钥文件 {pub_key_path} 或 {key_path} 不存在，请检查。")
        return

    with open(pub_key_path, 'r') as key_file:
        pub_key = key_file.read().strip()

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server_ip, username=username, password=password)

        sftp = client.open_sftp()
        remote_ssh_dir = ".ssh"
        remote_key_path = os.path.join(remote_ssh_dir, key_name.replace('.pub', ''))
        remote_pub_key_path = os.path.join(remote_ssh_dir, key_name)

        try:
            sftp.mkdir(remote_ssh_dir)
        except IOError:
            pass

        # 上传密钥文件
        sftp.put(key_path, remote_key_path)
        sftp.put(pub_key_path, remote_pub_key_path)

        # 将公钥添加到 authorized_keys
        sftp_file = sftp.file(f'{remote_ssh_dir}/authorized_keys', 'a')
        sftp_file.write(f"\n{pub_key}\n")
        sftp_file.close()

        print(f"密钥已上传到 {username}@{server_ip}")

        sftp.close()
        client.close()
    except Exception as e:
        print(f"上传密钥时出现错误：{e}")

def main():
    while True:
        try:
            choice = show_menu()
            if choice == "1":
                key_name = input("输入密钥名称（默认: id_rsa_dev）：") or "id_rsa_dev"
                key_password = getpass.getpass("输入密钥密码（留空表示没有密码）：") or ""
                create_ssh_key(key_name, key_password)
            elif choice == "2":
                keys = list_local_keys()
                if keys:
                    chosen_key = choose_local_key(keys)
                    if chosen_key:
                        server_ip = input("输入服务器 IP：")
                        username = input("输入 SSH 用户名：")
                        password = getpass.getpass("输入 SSH 密码：")
                        upload_ssh_key(server_ip, username, password, chosen_key)
            elif choice == "3":
                print("操作完成。")
                break
            else:
                print("无效选项，请重新输入。")
        except KeyboardInterrupt:
            print("\n中断操作，返回主菜单。")

if __name__ == "__main__":
    main()
