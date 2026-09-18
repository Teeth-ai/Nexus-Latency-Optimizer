import customtkinter as ctk
import ctypes
import sys
import subprocess
import threading

# Запрос прав администратора
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Базовые настройки темы
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nexus Latency Optimizer v1.0")
        self.geometry("850x500")
        self.resizable(False, False)

        self.accent_color = "#00FFA6"
        self.hover_color = "#00CC85"
        self.dark_bg = "#1A1A1A"

        title_font = ctk.CTkFont(family="Trebuchet MS", size=32, weight="bold")
        subtitle_font = ctk.CTkFont(family="Trebuchet MS", size=14, slant="italic")
        switch_font = ctk.CTkFont(family="Consolas", size=13)
        btn_font = ctk.CTkFont(family="Trebuchet MS", size=16, weight="bold")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # --- ЛЕВАЯ ПАНЕЛЬ ---
        self.left_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, padx=25, pady=40, sticky="nsew")

        self.header = ctk.CTkLabel(self.left_frame, text="NEXUS\nOPTIMIZER", font=title_font, text_color=self.accent_color, justify="left")
        self.header.pack(anchor="w", pady=(0, 5))
        
        self.subheader = ctk.CTkLabel(self.left_frame, text="Advanced System Tweaks\nfor Games", font=subtitle_font, text_color="gray", justify="left")
        self.subheader.pack(anchor="w", pady=(0, 30))

        self.separator = ctk.CTkFrame(self.left_frame, height=2, fg_color="#333333")
        self.separator.pack(fill="x", pady=(0, 20))

        self.desc = ctk.CTkLabel(self.left_frame, text="Select the parameters on the\nright and apply changes to\nreduce input lag & boost FPS.", font=ctk.CTkFont(size=12), text_color="#777777", justify="left")
        self.desc.pack(anchor="w")

        # Кнопка с привязанной командой (command=self.start_apply)
        self.btn_apply = ctk.CTkButton(
            self.left_frame, 
            text="APPLY TWEAKS", 
            height=55, 
            font=btn_font, 
            fg_color=self.accent_color, 
            hover_color=self.hover_color, 
            text_color="black",
            command=self.start_apply
        )
        self.btn_apply.pack(fill="x", side="bottom", pady=(0, 10))

        # --- ПРАВАЯ ПАНЕЛЬ ---
        self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=15, fg_color=self.dark_bg)
        self.scroll_frame.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")

        # Словарь твиков: Название -> Системная команда
        self.tweaks_logic = {
            "Enable Ultimate Performance Power Plan": 'powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61 & powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c',
            "Disable HPET & Dynamic Ticks": 'bcdedit /set disabledynamictick yes & bcdedit /set useplatformclock no',
            "Disable Nagle's Algorithm (Zero Ping Tweak)": 'reg add "HKLM\\SOFTWARE\\Microsoft\\MSMQ\\Parameters" /v "TCPNoDelay" /t REG_DWORD /d "1" /f',
            "Remove Network Throttling Limits": 'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile" /v "NetworkThrottlingIndex" /t REG_DWORD /d "4294967295" /f',
            "Force High GPU Priority for Games": 'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "GPU Priority" /t REG_DWORD /d "8" /f',
            "Disable Windows Mouse Acceleration (1:1 Aim)": 'reg add "HKCU\\Control Panel\\Mouse" /v "MouseSpeed" /t REG_SZ /d "0" /f',
            "Disable Xbox Game Bar & Game DVR": 'reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_Enabled" /t REG_DWORD /d "0" /f',
            "Disable Windows Telemetry & Data Collection": 'sc stop DiagTrack & sc config DiagTrack start= disabled',
            "Disable SysMain (Superfetch) & Indexing": 'sc stop "SysMain" & sc config "SysMain" start=disabled'
        }

        self.switches = {}
        for tweak_name in self.tweaks_logic.keys():
            sw = ctk.CTkSwitch(
                self.scroll_frame, 
                text=tweak_name, 
                font=switch_font, 
                progress_color=self.accent_color,
                button_hover_color=self.hover_color
            )
            sw.pack(pady=15, padx=20, anchor="w")
            sw.select() # Включены по умолчанию
            self.switches[tweak_name] = sw

    # Запуск в фоновом потоке, чтобы окно не зависло
    def start_apply(self):
        self.btn_apply.configure(text="APPLYING...", state="disabled", fg_color="gray")
        threading.Thread(target=self.execute_tweaks, daemon=True).start()

    # Физическое выполнение команд
    def execute_tweaks(self):
        for tweak_name, switch_obj in self.switches.items():
            if switch_obj.get() == 1: # Если тумблер включен
                command = self.tweaks_logic[tweak_name]
                try:
                    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except Exception:
                    pass
        
        # Обновление интерфейса после завершения
        self.btn_apply.configure(text="DONE! RESTART PC", fg_color="#00FFA6", text_color="black")

if __name__ == "__main__":
    if is_admin():
        app = App()
        app.mainloop()
    else:
        # Перезапуск скрипта с запросом прав админа
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)