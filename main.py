import asyncio
import websockets
import json
from aiohttp import web
import tkinter as tk
from tkinter import ttk, messagebox
import socket
import threading
import os
from pathlib import Path
from functools import partial
import configparser
import time
import sys
import base64

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

icon_base64 = """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"""
CONFIG_FILE = os.path.join(BASE_DIR, "config.ini")
SKINS_DIR = os.path.join(BASE_DIR, "skins")
DEFAULT_SKIN = "default.css"
ICONS_DIR = os.path.join(BASE_DIR, "icons")
DEFAULT_ICON = "heart-default.svg"
MISC = "misc.js"
DEFAULT_PORT = 5050

clients = set()

def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        config['Settings'] = {
            'http_port': DEFAULT_PORT,
            'skin': DEFAULT_SKIN,
            'icon': DEFAULT_ICON
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
    else:
        config.read(CONFIG_FILE, encoding='utf-8')
    return config

def save_config(key, value):
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE, encoding='utf-8')
    else:
        config['Settings'] = {}

    config['Settings'][key] = value

    with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
        config.write(configfile)

HTTP_PORT = load_config()['Settings']['http_port']

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        return "127.0.0.1"

async def websocket_handler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            if "heartRate" in data:
                await broadcast(data)
    finally:
        clients.remove(websocket)

async def broadcast(data):
    if clients:
        msg = json.dumps(data)
        await asyncio.gather(*[client.send(msg) for client in clients])

async def http_send_handler(request):
    data = await request.json()
    if "heartRate" in data:
        heartrate = data["heartRate"]
        app.update_heartbeat(heartrate)
        await broadcast(data)
        return web.json_response({"status": "ok"})
    return web.json_response({"error": "No heartRate"}, status=400)

async def handle_index(request):
    state = request.app['state']
    skin = state.skin
    icon = state.icon
    css_path = Path(SKINS_DIR) / skin
    icon_path = Path(ICONS_DIR) / icon
    misc_path = Path(ICONS_DIR) / MISC

    if not css_path.exists():
        css_path = Path(SKINS_DIR) / DEFAULT_SKIN
    
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()

    with open(icon_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()

    with open(misc_path, 'r', encoding='utf-8') as f:
        misc = f.read()

    local_ip = get_local_ip()
    timestamp = int(os.path.getmtime(css_path))

    favicon_base64 = f"""data:image/png;base64,{icon_base64}"""
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Heartrate</title>
        <link rel="icon" type="image/png" href="{favicon_base64}">
        <style>
            {css}
        </style>
        <link rel="stylesheet" href="/skins/{skin}?v={timestamp}">
    </head>
    <body>
        <div id="container">
            <div class="hr">
                <h1 id="heartrate">
                    <span id="hr">--</span>
                    {svg_content}
                </h1>
            </div>
        </div>
        <script>
            const hr = document.querySelector("#hr");
            const heart = document.querySelector(".heart");

            const ws = new WebSocket("ws://{local_ip}:8765");

            ws.onmessage = (event) => {{
                try {{
                    const data = JSON.parse(event.data);
                    if (data.action === "reload") {{
                        window.location.reload();
                    }} else if (data.heartRate) {{
                        const heartRate = data.heartRate;
                        hr.textContent = heartRate;

                        const beatDuration = 60 / heartRate;
                        heart.style.animation = "heartbeat " + beatDuration + "s cubic-bezier(0.215, 0.61, 0.355, 1) infinite";
                        heart.style.animationDelay = (Math.random() * -0.5) + "s";

                        {misc}
                    }}
                }} catch (e) {{
                    console.error("Ошибка при обработке WebSocket-сообщения:", e);
                }}
            }};
        </script>
    </body>
    </html>
    """
    response = web.Response(text=html, content_type='text/html')
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

class AppState:
    def __init__(self, skin, icon):
        self.skin = skin
        self.icon = icon

class HeartRateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HeartRate Monitor Widget")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


        icon_data = base64.b64decode(icon_base64)
        icon_path = os.path.join(BASE_DIR, "temp_icon.ico")

        with open(icon_path, "wb") as temp_icon_file:
            temp_icon_file.write(icon_data)

        self.root.iconbitmap(icon_path)

        os.remove(icon_path)

        config = load_config()
        self.skin_var = tk.StringVar(value=config['Settings']['skin'])
        self.skins = []

        self.icon_var = tk.StringVar(value=config['Settings']['icon'])
        self.icons = []

        self.status_var = tk.StringVar(value="Server running | No input heartrate")
        self.last_heartbeat_time = 0
        
        self.setup_ui()
        self.refresh_skins()
        self.refresh_icons()
        self.start_server()

        self.check_heartbeat_status()
        copyright_label = tk.Label(
            self.root,
            text="© frsvme",
            font=("TkDefaultFont", 8),
            fg="gray",
            anchor="se"
        )
        copyright_label.place(relx=1.0, rely=1.0, x=-5, y=-5, anchor="se")

    def update_heartbeat(self, heartrate):
        self.last_heartbeat_time = time.time()
        self.status_var.set(f"Server running | Heartrate: {heartrate}")

    def check_heartbeat_status(self):
        current_time = time.time()
        if current_time - self.last_heartbeat_time > 5:
            self.status_var.set("Server running | No input heartrate")
        
        self.root.after(1000, self.check_heartbeat_status)

    def show_temporary_status(self, message, duration=3000):
        base_message = "Server running"
        self.root.after(duration, lambda: self.status_var.set(base_message))

    def get_local_ip(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
            return local_ip
        except Exception:
            return "127.0.0.1"

    def refresh_skins(self):
        if not os.path.exists(SKINS_DIR):
            os.makedirs(SKINS_DIR)
        default_css = Path(SKINS_DIR) / DEFAULT_SKIN
        if not default_css.exists():
            with open(default_css, 'w', encoding='utf-8') as f:
                f.write("""body, html {
    margin: 0;
    padding: 0;
    font-family: sans-serif;
    height: 100%;
    background-color: #222;
    overflow: hidden;
}

#container {
    color: #eee;
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

@keyframes heartbeat {
    0% { transform: scale(1); }
    10% { transform: scale(1.1); }
    15% { transform: scale(1.25); }
    20% { transform: scale(1.2); }
    30% { transform: scale(1); }
    40% { transform: scale(1.05); }
    45% { transform: scale(1.15); }
    50% { transform: scale(1.1); }
    60% { transform: scale(1); }
    100% { transform: scale(1); }
}

.heart {
    font-size: 7vw;
    display: inline-block;
    vertical-align: middle;
    margin-left: 0;
    position: relative;
    top: -0.1em;
    backface-visibility: hidden;
    transform: translateZ(0);
    -webkit-font-smoothing: antialiased;
}

#heartrate {
    font-size: 20vw;
    color: #f1f1f1;
    margin: 0;
    text-align: center;
    font-weight: bold;
    line-height: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.03em;
}""")

        new_skins = [f for f in os.listdir(SKINS_DIR) 
                    if f.endswith('.css') and os.path.isfile(os.path.join(SKINS_DIR, f))]
        
        if set(new_skins) != set(self.skins):
            self.skins = new_skins
            self.skin_combobox['values'] = self.skins
            if self.skin_var.get() not in self.skins:
                self.skin_var.set(DEFAULT_SKIN if DEFAULT_SKIN in self.skins 
                                 else self.skins[0] if self.skins else "")

    def refresh_icons(self):
        if not os.path.exists(ICONS_DIR):
            os.makedirs(ICONS_DIR)
        
        if not any(f.endswith('.svg') for f in os.listdir(ICONS_DIR)):
            default_icon_path = os.path.join(ICONS_DIR, "heart-default.svg")
            with open(default_icon_path, 'w', encoding='utf-8') as f:
                f.write("""<svg class="heart" width="1em" height="1em" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M2 9.1371C2 14 6.01943 16.5914 8.96173 18.9109C10 19.7294 11 20.5 12 20.5C13 20.5 14 19.7294 15.0383 18.9109C17.9806 16.5914 22 14 22 9.1371C22 4.27416 16.4998 0.825464 12 5.50063C7.50016 0.825464 2 4.27416 2 9.1371Z" fill="currentColor"/>
</svg>""")

        if not "misc.js" in os.listdir(ICONS_DIR):
            default_misc_path = os.path.join(ICONS_DIR, "misc.js")
            with open(default_misc_path, 'w', encoding='utf-8') as j:
                j.write("""if (heartRate <= 5) {{
    heart.style.color = '#4B0082';
}} else if (heartRate > 5 && heartRate <= 35) {{
    heart.style.color = '#3498DB';
}} else if (heartRate > 35 && heartRate <= 120) {{
    heart.style.color = '#FF0000';
}} else if (heartRate > 120) {{
    heart.style.color = '#FFD700';
}} else {{
    heart.style.color = '#B0C4DE';
}}""")
        
        new_icons = [f for f in os.listdir(ICONS_DIR) 
                     if f.endswith('.svg') and os.path.isfile(os.path.join(ICONS_DIR, f))]
        
        if set(new_icons) != set(self.icons):
            self.icons = new_icons
            self.icon_combobox['values'] = self.icons
            if self.icon_var.get() not in self.icons:
                self.icon_var.set(self.icons[0] if self.icons else "")

    def show_api_info(self):
        api_window = tk.Toplevel(self.root)
        api_window.title("API Information")
        api_window.geometry("400x280")
        api_window.resizable(False, False)

        icon_data = base64.b64decode(icon_base64)
        icon_path = os.path.join(BASE_DIR, "temp_icon.ico")

        with open(icon_path, "wb") as temp_icon_file:
            temp_icon_file.write(icon_data)

        api_window.iconbitmap(icon_path)

        os.remove(icon_path)

        info_text = """
    {
        "heartRate": <int>
    }
    """

        ttk.Label(api_window, text="Format data for API:\n", font=('TkDefaultFont', 12, 'bold')).pack(pady=10)
        ttk.Label(api_window, text=info_text, justify="left", font=('TkDefaultFont', 15)).pack(padx=10, pady=5)
        ttk.Label(api_window, text="\n\nContent-Type: application/json", font=('TkDefaultFont', 12, 'bold')).pack(pady=10)

        ttk.Button(api_window, text="Close", command=api_window.destroy).pack(pady=10)

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        info_frame = ttk.LabelFrame(main_frame, text="Server Information", padding="10")
        info_frame.pack(fill=tk.X, pady=5)

        info_container = ttk.Frame(info_frame)
        info_container.pack(fill=tk.X)
        
        local_ip = self.get_local_ip()
    
        text_frame = ttk.Frame(info_container)
        text_frame.grid(row=0, column=0, sticky="w")
        ttk.Label(text_frame, text=f"Dashboard URL: http://{local_ip}:{HTTP_PORT}", 
                  font=('TkDefaultFont', 10, 'bold')).pack(anchor="w", pady=2)
        ttk.Label(text_frame, text=f"API Endpoint: http://{local_ip}:{HTTP_PORT}/send (POST)", 
                  font=('TkDefaultFont', 9)).pack(anchor="w", pady=2)

        api_info_btn = ttk.Button(info_container, text="API Info", command=self.show_api_info)
        api_info_btn.grid(row=0, column=1, sticky="e", padx=10)

        info_container.columnconfigure(0, weight=1)
        
        skin_frame = ttk.LabelFrame(main_frame, text="Skin Selection", padding="10")
        skin_frame.pack(fill=tk.X, pady=5)
        
        combobox_frame = ttk.Frame(skin_frame)
        combobox_frame.pack(fill=tk.X)
        
        self.skin_combobox = ttk.Combobox(
            combobox_frame,
            textvariable=self.skin_var,
            state="readonly",
            font=('TkDefaultFont', 10)
        )
        self.skin_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.skin_combobox.bind("<Button-1>", lambda e: self.refresh_skins())
        
        apply_btn = ttk.Button(
            skin_frame,
            text="Apply Skin",
            command=self.apply_skin
        )
        apply_btn.pack(pady=(5, 0))
        
        icon_frame = ttk.LabelFrame(main_frame, text="Icon Selection", padding="10")
        icon_frame.pack(fill=tk.X, pady=5)
        
        icon_combobox_frame = ttk.Frame(icon_frame)
        icon_combobox_frame.pack(fill=tk.X)
        
        self.icon_combobox = ttk.Combobox(
            icon_combobox_frame,
            textvariable=self.icon_var,
            state="readonly",
            font=('TkDefaultFont', 10)
        )
        self.icon_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.icon_combobox.bind("<Button-1>", lambda e: self.refresh_icons())
        
        apply_icon_btn = ttk.Button(
            icon_frame,
            text="Apply Icon",
            command=self.apply_icon
        )
        apply_icon_btn.pack(pady=(5, 0))
        
        ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=3
        ).pack(fill=tk.X, pady=(10, 0))

    def apply_skin(self):
        selected_skin = self.skin_var.get()
        if not selected_skin:
            messagebox.showerror("Error", "No skin selected!")
            return

        if 'aiohttp_app' in globals():
            aiohttp_app['state'].skin = selected_skin

        self.show_temporary_status(f"Skin applied: {selected_skin}")

        save_config('skin', selected_skin)

        asyncio.run_coroutine_threadsafe(
            self.reload_clients(),
            loop
        )

    def apply_icon(self):
        selected_icon = self.icon_var.get()
        if not selected_icon:
            messagebox.showerror("Error", "No icon selected!")
            return

        if 'aiohttp_app' in globals():
            aiohttp_app['state'].icon = selected_icon

        self.show_temporary_status(f"Icon applied: {selected_icon}")

        save_config('icon', selected_icon)

        asyncio.run_coroutine_threadsafe(
            self.reload_clients(),
            loop
        )

    async def reload_clients(self):
        await broadcast({"action": "reload"})

    def start_server(self):
        self.server_thread = threading.Thread(target=self.run_server, daemon=True)
        self.server_thread.start()

    def run_server(self):
        global aiohttp_app, loop

        config = load_config()
        skin = config['Settings'].get('skin', DEFAULT_SKIN)
        icon = config['Settings'].get('icon', DEFAULT_ICON)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        app_state = AppState(skin, icon)
        
        aiohttp_app = web.Application()
        aiohttp_app['state'] = app_state
        
        aiohttp_app.router.add_get('/', handle_index)
        aiohttp_app.router.add_post('/send', http_send_handler)
        aiohttp_app.router.add_static('/skins/', path=Path(SKINS_DIR), name='skins', show_index=True)
        aiohttp_app.router.add_static('/icons/', path=Path(ICONS_DIR), name='icons', show_index=True)
        
        runner = web.AppRunner(aiohttp_app)
        loop.run_until_complete(runner.setup())
        
        site = web.TCPSite(runner, '0.0.0.0', HTTP_PORT)
        loop.run_until_complete(site.start())
        
        ws_server = loop.run_until_complete(
            websockets.serve(websocket_handler, '0.0.0.0', 8765)
        )
        
        loop.run_forever()

    def on_close(self):
        if messagebox.askokcancel("Quit", "Stop widget-server and exit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x380")
    root.resizable(False, False)
    
    style = ttk.Style()
    style.configure('TFrame', background='#f0f0f0')
    style.configure('TLabel', background='#f0f0f0')
    style.configure('TButton', font=('TkDefaultFont', 9))
    
    app = HeartRateApp(root)
    root.mainloop()