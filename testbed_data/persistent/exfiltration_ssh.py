import os
import tempfile
import paramiko
import random
import time

def send_file_via_ssh(file_content, remote_path, ssh_hostname, ssh_username, ssh_password):
    # Create a temporary file from the string content
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as tmp_file:
        tmp_file.write(file_content)
        tmp_file_path = tmp_file.name

    print(f"Created temporary file: {tmp_file_path}")

    try:
        # Initialize the SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SSH server
        ssh.connect(ssh_hostname, username=ssh_username, password=ssh_password)

        # Create SFTP session over an existing SSH transport
        sftp = ssh.open_sftp()

        # Send file from local path to remote path
        print(f"Uploading {tmp_file_path} to {remote_path}")
        sftp.put(tmp_file_path, remote_path)
        print("File uploaded successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the SFTP session and SSH connection
        sftp.close()
        ssh.close()

        # Clean up temporary file
        os.unlink(tmp_file_path)
        print(f"Removed temporary file: {tmp_file_path}")


# Example usage:
file_content = "This is a test string that will be written to a text file and sent via SSH."
remote_path = '/home/kali/ssh_files/file.txt'
ssh_hostname = '172.28.219.62'
ssh_username = 'kali'
ssh_password = 'kali'
counter = 0

with open('rockyou.txt') as r:
    while True:
        passwords = ''
        for _ in range(random.randint(1,5)):
            try:
                line = r.readline()
                passwords += line.strip() + ','
            except:
                passwords += 'utf8err,'
        
        remote_path = f'/home/kali/ssh_files/file{counter}.txt'

        send_file_via_ssh(passwords, remote_path, ssh_hostname, ssh_username, ssh_password)
        counter += 1
        print(f'Sent {passwords}')
        time.sleep(0.1)

