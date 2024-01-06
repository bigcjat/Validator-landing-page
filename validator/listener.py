import json
import websockets
import subprocess
import asyncio

async def ledger_stream():
    uri = "ws://127.0.0.1:6009"  # Replace with the correct WebSocket server URI

    try:
        async with websockets.connect(uri) as websocket:
            subscription_payload = {
                "id": "ledger stream",
                "command": "subscribe",
                "streams": ["ledger"]
            }

            await websocket.send(json.dumps(subscription_payload))

            while True:
                response = await websocket.recv()
                response_data = json.loads(response)
                
                ledger_index = response_data.get("ledger_index")
                if ledger_index and ledger_index % 256 == 0:
                    print(f"Received ledger stream update (divisible by 256): {response}")
                    ledger_time = response_data.get("ledger_time", "")
                    
                    subprocess.run(["python3", "update.py", str(ledger_index), str(ledger_time)])

    except websockets.exceptions.ConnectionClosedError:
        print("WebSocket connection closed.")

asyncio.get_event_loop().run_until_complete(ledger_stream())

