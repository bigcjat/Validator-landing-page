Use your validator to send information to your webhost to update your toml file, then create a landing page based on the data found in your toml file.

No connection (no holes) to your validator, update every key ledger (or whenever you want)

Be more transparent. Display your validator info, load, amendments, organization and principle. Hands free.

Works on xrpl mainnet, xahau, testnet

Xahau example here: https://xahau.validator.report/

Mainnet example here: https://mainnet.validator.report/ and here: https://mainnet2.validator.report/


Setup Instructions - Validator and Web Host Configuration



Part 1: Validator Server Setup

Prerequisites:

Python3, mpstat, free, df, awk

Python3 requires:

json, websockets, subprocess, asyncio, requests

Optional text editor: nano

Webhost requires:

PHP


Upload Pre-existing Files: Upload update.py and listener.py to the validator server or use nano to create these files and paste the contents accordingly

Editing update.py:
Modify the following lines:
xrpl = 'xahaud': Replace 'xahaud' with your XRPL node executable (e.g., "rippled")
api_url = 'https://yourserver.com/toml.php': Replace with your API URL (The php you will upload)
api_key = 'key': Replace 'key' with your desired API key. This must match the PHP script

Editing listener.py:
Modify the line if necessary:
uri = "ws://127.0.0.1:6009": Replace with the correct WebSocket server URI, you can find this in your validator config "port_ws_admin_local"




Part 2: Web Host Setup

Editing toml.php:

Change the following lines:

$allowedIPAddress = '0.0.0.0': Replace with your validator IP address to reject other sources

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
