Example here: https://validator.report/landing/

Setup Instructions - Validator and Web Host Configuration




Part 1: Validator Server Setup

Prerequisites:
Python3, mpstat, free, df, awk
Optional text editor: nano

Upload Pre-existing Files: Upload update.py and listener.py to the validator server or use nano to create these files and paste the contents accordingly

Editing update.py:
Modify the following lines:
xrpl = 'xahaud': Replace 'xahaud' with your XRPL node executable (e.g., "rippled")
api_url = 'https://yourserver.com/toml.php': Replace with your API URL (The php you will upload)
api_key = 'key': Replace 'key' with your desired API key. This must match the PHP script

Editing listener.py:
Modify the line if necessary:
uri = "ws://127.0.0.1:6009": Replace with the correct WebSocket server URI




Part 2: Web Host Setup

Editing toml.php:
Change the following lines:
$allowedIPAddress = '0.0.0.0': Replace with your validator IP address
$apiKey = 'key': Set your API key (must match the one in update.py)
$filePath = '.well-known/xahau.toml': Change the file path as needed (xrp-ledger.toml for Mainnet)
Set file permissions to 644

Editing index.html:
Replace .well-known/xahau.toml with the correct TOML file path (use xrp-ledger.toml for Mainnet)

Updating TOML File:
Add the following lines to the bottom of your existing TOML file at .well-known/:

[[STATUS]]

[[AMENDMENTS]]

Starting the Script:
To run the script, type: nohup python3 listener.py &

Stopping the Script:
Find the process ID with ps aux | grep python
Terminate using kill [process id]
