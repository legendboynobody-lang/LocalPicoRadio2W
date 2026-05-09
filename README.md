# 📻 Pico Emergency Radio

A MicroPython-based captive portal radio station running on the **Raspberry Pi Pico 2W**. Broadcasts a live, updateable text message to any device that connects to its open Wi-Fi hotspot — using the browser's built-in Text-to-Speech API to read it aloud. No app, no internet, no infrastructure required.

---

## 🧭 Overview

Pico Emergency Radio turns a Raspberry Pi Pico 2W into a standalone, offline broadcast station. It creates an open Wi-Fi access point and hijacks DNS to redirect every connected device to a captive portal page displaying the current broadcast message. A single administrator can update the message in real time from a separate panel — making it suitable for both hobbyist experimentation and lightweight emergency communication scenarios.

**Use cases include:**
- Emergency or off-grid local broadcasting (power outages, remote events, disaster scenarios)
- Educational demonstration of DNS spoofing, captive portals, and MicroPython networking
- Campus/event announcement systems with zero infrastructure dependency
- IoT and embedded systems learning projects

---

## ✨ Features

- **Open Wi-Fi Hotspot** — No password required; any device can connect instantly
- **Captive Portal** — Automatically intercepts traffic and serves the broadcast page
- **DNS Spoofing** — All DNS queries are resolved to the Pico's IP, ensuring the portal loads
- **Text-to-Speech** — Broadcast messages are read aloud via the Web Speech API (browser-native)
- **Admin Panel** — Update the live broadcast message remotely via `/admin`
- **Zero Dependencies** — Runs entirely on MicroPython; no external libraries needed
- **Offline Operation** — Functions without internet connectivity

---

## 🛠️ Hardware Requirements

| Component | Specification |
|---|---|
| Microcontroller | Raspberry Pi Pico 2W |
| Power Supply | USB (5V via micro-USB or battery bank) |
| Storage | Onboard flash (no SD card needed) |

No additional components are required.

---

## 📦 Software Requirements

- [MicroPython for Raspberry Pi Pico W](https://micropython.org/download/RPI_PICO2_W/) (v1.23 or later recommended)
- [Thonny IDE](https://thonny.org/) or `mpremote` for flashing files

---

## 🚀 Installation & Setup

### Step 1 — Flash MicroPython

1. Hold the **BOOTSEL** button on the Pico 2W and plug it into your computer via USB.
2. It will appear as a USB mass storage device (`RPI-RP2`).
3. Download the latest **Pico 2W MicroPython UF2** from [micropython.org](https://micropython.org/download/RPI_PICO2_W/).
4. Drag and drop the `.uf2` file onto the drive. The Pico will reboot automatically.

### Step 2 — Upload `main.py`

**Using Thonny:**
1. Open Thonny and connect to the Pico (`Run → Select Interpreter → MicroPython (Raspberry Pi Pico)`).
2. Open `main.py` from this repository.
3. Go to `File → Save As` and save it **to the Pico** as `main.py`.

**Using `mpremote`:**
```bash
mpremote connect auto cp main.py :main.py
```

### Step 3 — Run

Reset the Pico. The radio server starts automatically on boot. You will see the following in the serial console:

```
Radio broadcasting on SSID: 📢 Pico Emergency Radio
Admin Panel available at: http://192.168.4.1/admin
Radio Server is Live!
```

---

## 📡 Usage

### Listener (Public)

1. On any Wi-Fi enabled device, connect to the open network: **`📢 Pico Emergency Radio`**
2. A captive portal prompt will appear automatically — tap it, or navigate to `http://192.168.4.1`
3. The current broadcast message is displayed on screen
4. Tap **🔊 TAP TO LISTEN** to hear the message read aloud via Text-to-Speech

> **Note:** If audio does not play automatically, a warning banner will prompt you to open the page manually in Safari or Chrome.

### Administrator (Broadcast Panel)

1. Connect to the same Wi-Fi network
2. Navigate to `http://192.168.4.1/admin`
3. Type the new broadcast message and tap **Update Radio Broadcast**
4. All listeners who refresh their page will see the updated message immediately

---

## ⚠️ Disclaimers

### Legal & Ethical Use

This project creates an **open Wi-Fi access point** and performs **DNS spoofing** to redirect network traffic. These techniques, while standard in captive portal implementations (hotels, airports, etc.), may be **restricted or regulated** depending on your jurisdiction and deployment context.

- **Do not** deploy this on networks or in locations where you do not have explicit permission to operate a wireless access point.
- **Do not** use this to impersonate legitimate services, intercept sensitive data, or deceive users maliciously.
- The author accepts **no liability** for misuse, legal consequences, or damages arising from the use of this project.
- This project is provided **as-is**, for educational and emergency preparedness purposes only.

### Emergency Use Disclaimer

While this project may assist in low-tech emergency communication, it is **not a certified emergency broadcast system**. Do not rely solely on this device in life-critical situations. Always follow official emergency protocols and use certified communication equipment where applicable.

---

## 🔒 Known Limitations

| Limitation | Detail |
|---|---|
| **No Admin Authentication** | The `/admin` panel has no password protection. Anyone connected to the Wi-Fi can access and update the broadcast. |
| **Single Message Only** | Only one broadcast message is stored in memory at a time. |
| **No HTTPS** | The server runs over plain HTTP. Do not transmit sensitive information. |
| **TTS Browser-Dependent** | Text-to-Speech relies on the Web Speech API; availability varies by browser and OS. |
| **Limited Concurrent Connections** | The non-blocking server handles connections sequentially; heavy load may cause delays. |
| **Message Lost on Reboot** | The current broadcast is stored in RAM only and resets to the default on power cycle. |

---

## 🗂️ Project Structure

```
pico-emergency-radio/
└── main.py       # Complete server — AP setup, DNS, HTTP, and admin panel
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to open a pull request or file an issue.

Suggested improvements:
- Admin panel password protection
- Persistent message storage via `uos` / flash write
- Multi-message queue / broadcast history
- Signal strength indicator on the portal page

---

## 📄 Licence

This project is licensed under the **MIT Licence**.

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

*Built with MicroPython on Raspberry Pi Pico 2W.*
