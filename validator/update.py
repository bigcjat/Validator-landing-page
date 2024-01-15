import subprocess
import json
import requests

# You can change these variables to match your setup
xrpl = 'xahaud' # Replace with your XRPL node executable eg. "rippled" or "xahaud"
api_url = 'https://yourhost.com/toml.php'  # Replace with your API URL
api_key = 'key'  # Replace with your API key, this can be anything you want, you need to update the php script to match


def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def get_xrpl_server_info(key, time):
    try:
        server_info_result = subprocess.run([xrpl, "server_info"], capture_output=True, text=True)
        server_info_data = json.loads(server_info_result.stdout)

        status = server_info_data['result']['info']['server_state']
        version = server_info_data['result']['info']['build_version']
        status_time = server_info_data['result']['info']['server_state_duration_us']
        node_size = server_info_data['result']['info']['node_size']
        ledgers = server_info_data['result']['info']['complete_ledgers']
        # Mainnet doesn't provide a network id, so default 0
        network = server_info_data['result']['info'].get('network_id', 0)
        cpu_usage = run_command("mpstat 1 1 | awk '/Average:/ {print 100 - $12\"%\"}'")
        ram_usage = run_command("free | awk '/Mem:/ {printf(\"%.2f%\"), $3/$2 * 100}'")
        disk_usage = run_command("df -h . | awk 'NR==2{print $5}'")
        swap_usage = run_command("free | awk '/Swap:/ {printf(\"%.2f%\"), $3/$2 * 100}'")

        feature_result = subprocess.run([xrpl, "feature"], capture_output=True, text=True)
        feature_data = json.loads(feature_result.stdout)
        amendments = feature_data['result']['features']
        filtered_amendments = {
            value['name']: key
            for key, value in amendments.items()
            if value.get('enabled') == False and value.get('supported') == True and value.get('vetoed') == False
        }

        status_output = f"""
CPU = "{cpu_usage}"
RAM = "{ram_usage}"
DISK = "{disk_usage}"
SWAP = "{swap_usage}"
STATUS = "{status}"
STATUSTIME = "{status_time}"
BUILDVERSION = "{version}"
NODESIZE = "{node_size}"
LEDGERS = "{ledgers}"
NETWORK = "{network}"
KEY = "{key}"
TIME = "{time}"
"""

        amendments_output = "\n".join([f"{name} = \"{id}\"" for name, id in filtered_amendments.items()])

        return {
            'STATUS': status_output,
            'AMENDMENTS': amendments_output
        }
    except Exception as e:
        return str(e)

def send_to_api(data):

    try:
        headers = {'Content-Type': 'application/json'}
        params = {'apiKey': api_key}
        response = requests.post(api_url, json=data, headers=headers, params=params)
        response.raise_for_status()

        print("Response from API:", response.text)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Oops: Something Else", err)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: script.py <KEY> <TIME>")
    else:
        key = sys.argv[1]
        time = sys.argv[2]
        info = get_xrpl_server_info(key, time)
        send_to_api(info)

