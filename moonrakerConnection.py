import websocket
import json

#websocket url
MOONRAKER_WS_URL = "ws://autochess:7125/websocket"

request_counter = 0

def send_gcode(ws, command):
    global request_counter
    payload = {
        "jsonrpc": "2.0",
        "method": "printer.gcode.script",
        "params": {"script": command},
        "id": request_counter
    }
    ws.send(json.dumps(payload))
    print(f"Sent G-code: {command} (id: {request_counter})")

    gcode_responses = []

    #poll for response
    while True:
        message = ws.recv()
        data = json.loads(message)

        # get gcode response
        if data.get("method") == "notify_gcode_response":
            gcode_responses.append(data["params"][0])
            continue
        
        #got command response
        if data.get("id") == request_counter:
            print("\nCommand acknowledged:")
            print(json.dumps(data, indent=4))
            break

    if gcode_responses:
        print("\nG-code response(s):")
        for line in gcode_responses:
            print(line)
    else:
        print("\nNo G-code response received.")

    request_counter += 1
    
print("Connecting to Moonraker...")
ws = websocket.WebSocket()
ws.connect(MOONRAKER_WS_URL)
print("Connected to Moonraker WebSocket")

while True:
    cmd = input("Enter G-code (or macro): ").strip()
    if cmd.lower() == "exit":
        break

    send_gcode(ws, cmd)

print("Exiting. Closing WebSocket...")
ws.close()
