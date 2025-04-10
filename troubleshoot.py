import subprocess

def check_dns_error():
    try:
        logs = subprocess.check_output(["kubectl", "logs", "-l", "app=interview", "--tail=10"])
        if "DNS Error" in str(logs):
            print("DNS Misconfiguration detected!")
        else:
            raise Exception("No DNS error found.")
    except Exception as e:
        print(f"DNS Error: {e}")

def check_configmap_error():
    try:
        logs = subprocess.check_output(["kubectl", "logs", "-l", "app=interview", "--tail=10"])
        if "ConfigMap Error" in str(logs):
            print("ConfigMap mismatch detected!")
        else:
            raise Exception("No ConfigMap error found.")
    except Exception as e:
        print(f"ConfigMap Error: {e}")

if __name__ == "__main__":
    check_dns_error()
    check_configmap_error()

