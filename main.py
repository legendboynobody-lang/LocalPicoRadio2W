import network
import socket
import select
import time

# --- CONFIGURATION ---
SSID = "📢 Pico Emergency Radio"
current_broadcast = "Welcome to Pico Radio. Stand by for incoming broadcasts."

# --- HTML TEMPLATES ---
def get_broadcast_html():
    return f"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
    <!DOCTYPE html>
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
    <body style="font-family:sans-serif; background:#1a1a1a; color:white; text-align:center; padding: 20px;">
        <h1 style="color: #ff4747;">📻 Radio Station</h1>
        <p style="color: #888;">INCOMING BROADCAST:</p>
        <h2 id="msg" style="border: 2px solid #333; padding: 20px; border-radius: 10px;">{current_broadcast}</h2>
        
        <div id="warning" style="display:none; background:#ff9900; color:black; padding:10px; border-radius:5px; margin-top:10px; font-weight:bold;">
            ⚠️ Audio Blocked! Open Safari/Chrome and type 192.168.4.1 to listen.
        </div>

        <button onclick="playRadio()" style="background:#ff4747; color:white; border:none; padding:20px; width:100%; font-size:20px; border-radius:10px; font-weight:bold; margin-top:20px;">
            🔊 TAP TO LISTEN
        </button>
        
        <script>
            function playRadio() {
                if (!window.speechSynthesis) {
                    document.getElementById("warning").style.display = "block";
                    return;
                }
                
                let text = document.getElementById("msg").innerText;
                let utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 0.9; 
                
                utterance.onerror = function(event) {
                    document.getElementById("warning").style.display = "block";
                };

                window.speechSynthesis.speak(utterance);
                
                setTimeout(function() {
                    if(!window.speechSynthesis.speaking) {
                        document.getElementById("warning").style.display = "block";
                    }
                }, 500);
            }
        </script>
    </body>
    </html>
    """

ADMIN_HTML = """HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body style="font-family:sans-serif; padding:20px;">
    <h2>Admin Broadcast Panel</h2>
    <form action="/admin" method="POST">
        <textarea name="msg" rows="5" style="width:100%; font-size:16px;" placeholder="Type broadcast here..."></textarea>
        <br><br>
        <button type="submit" style="padding:15px; background:blue; color:white; width:100%; border:none; border-radius:5px; font-size:18px;">Update Radio Broadcast</button>
    </form>
</body>
</html>
"""

# --- UTILITY: URL Decoder ---
def url_decode(s):
    s = s.replace('+', ' ')
    parts = s.split('%')
    out = parts[0]
    for p in parts[1:]:
        if len(p) >= 2:
            try: out += chr(int(p[:2], 16)) + p[2:]
            except: out += '%' + p
        else: out += '%' + p
    return out

# --- 1. SETUP ACCESS POINT (OPEN WI-FI) ---
ap = network.WLAN(network.AP_IF)
ap.config(essid=SSID, security=0)
ap.active(True)
IP_ADDRESS = ap.ifconfig()[0]
print(f"Radio broadcasting on SSID: {SSID}")
print(f"Admin Panel available at: http://{IP_ADDRESS}/admin")

# --- 2. SETUP DNS SERVER (CAPTIVE PORTAL MAGIC) ---
udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udps.setblocking(False)
udps.bind(('0.0.0.0', 53))

# --- 3. SETUP WEB SERVER ---
tcps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcps.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcps.setblocking(False)
tcps.bind(('0.0.0.0', 80))
tcps.listen(5)

poller = select.poll()
poller.register(udps, select.POLLIN)
poller.register(tcps, select.POLLIN)

# --- MAIN LOOP ---
print("Radio Server is Live!")
while True:
    events = poller.poll(1000)
    for sock, event in events:
        
        if sock == udps:
            try:
                data, addr = udps.recvfrom(1024)
                response = data[:2] + b'\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00' + data[12:]
                response += b'\xC0\x0C\x00\x01\x00\x01\x00\x00\x00\x3C\x00\x04' + bytes(map(int, IP_ADDRESS.split('.')))
                udps.sendto(response, addr)
            except: pass
            
        elif sock == tcps:
            try:
                client, addr = tcps.accept()
                client.settimeout(2.0)
                request = client.recv(1024).decode('utf-8')
                
                path = request.split(' ')[1] if len(request.split(' ')) > 1 else '/'
                
                if path == '/admin' and "POST" in request:
                    body = request.split('\r\n\r\n')[1]
                    if "msg=" in body:
                        raw_msg = body.split('msg=')[1].split('&')[0]
                        current_broadcast = url_decode(raw_msg)
                        print("Broadcast updated:", current_broadcast)
                    client.send(ADMIN_HTML)
                
                elif path == '/admin':
                    client.send(ADMIN_HTML)
                
                else:
                    client.send(get_broadcast_html())
                
                client.close()
            except:
                pass
