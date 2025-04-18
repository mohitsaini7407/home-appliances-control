import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime
import colorsys
import math
import random

class HomeApplianceControl:
    def __init__(self, root):
        self.root = root
        self.root.title("Home Appliance Control System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        self.bg_color = "#f0f0f0"

        self.appliance_states = {
            "Living Room Light": False,
            "Bedroom Light": False,
            "Kitchen Light": False,
            "Living Room Fan": False,
            "Bedroom Fan": False,
            "Air Conditioner": False,
            "TV": False,
            "Speaker": False,
            "Radio": False
        }

        self.on_color = "#4CAF50"
        self.off_color = "#f0f0f0"
        
        self.buttons = {}
        
        self.animations = {}
        
        self.animation_canvases = {}
        self.animation_angles = {}
        
        self.ac_particles = {}
        
        self.bulb_brightness = {}
        
        self.tv_state = {"channel": 0, "frame": 0}
        
        self.speaker_waves = {}
        
        self.radio_bars = {}
        
        self.create_widgets()
        self.load_states()

    def create_widgets(self):
        title_label = tk.Label(
            self.root,
            text="Home Appliance Control Panel",
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg="#333333"
        )
        title_label.pack(pady=20)

        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        self.create_lighting_section(main_frame)
        self.create_climate_section(main_frame)
        self.create_entertainment_section(main_frame)
        
        control_frame = ttk.Frame(self.root)
        control_frame.pack(padx=20, pady=10, fill="x")
        
        save_btn = ttk.Button(
            control_frame, 
            text="Save Configuration",
            command=self.save_states
        )
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        self.status_var = tk.StringVar()
        self.status_var.set("System Ready")
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_lighting_section(self, parent):
        light_frame = ttk.LabelFrame(parent, text="Lighting Control", padding=10)
        light_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        lights = ["Living Room Light", "Bedroom Light", "Kitchen Light"]
        for i, light in enumerate(lights):
            self.create_control_widget(light_frame, light, i)

    def create_climate_section(self, parent):
        climate_frame = ttk.LabelFrame(parent, text="Climate Control", padding=10)
        climate_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        climate_devices = ["Living Room Fan", "Bedroom Fan", "Air Conditioner"]
        for i, device in enumerate(climate_devices):
            self.create_control_widget(climate_frame, device, i)

    def create_entertainment_section(self, parent):
        entertainment_frame = ttk.LabelFrame(parent, text="Entertainment", padding=10)
        entertainment_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        entertainment_devices = ["TV", "Speaker", "Radio"]
        for i, device in enumerate(entertainment_devices):
            self.create_control_widget(entertainment_frame, device, i)

    def create_control_widget(self, parent, appliance, row):
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, padx=5, pady=5, sticky="ew")
        
        label = ttk.Label(frame, text=f"{appliance}:")
        label.pack(side=tk.LEFT, padx=5)
        
        button_text = "ON" if self.appliance_states[appliance] else "OFF"
        button_bg = self.on_color if self.appliance_states[appliance] else self.off_color
        
        button = tk.Button(
            frame,
            text=button_text,
            bg=button_bg,
            width=8,
            relief=tk.RAISED
        )
        
        self.buttons[appliance] = button
        
        button.config(command=lambda a=appliance: self.toggle_appliance(a))
        button.pack(side=tk.LEFT, padx=5)
        
        canvas_width = 40
        canvas_height = 40
        
        if appliance == "Air Conditioner":
            canvas_width = 60
            canvas_height = 30
        elif appliance == "TV":
            canvas_width = 50
            canvas_height = 40
        
        canvas = tk.Canvas(
            frame, 
            width=canvas_width, 
            height=canvas_height, 
            bg=self.bg_color, 
            highlightthickness=0
        )
        canvas.pack(side=tk.LEFT, padx=5)
        
        self.animation_canvases[appliance] = canvas
        
        if "Fan" in appliance:
            self.animation_angles[appliance] = 0
        elif "Light" in appliance:
            self.bulb_brightness[appliance] = 0.0
        elif appliance == "Air Conditioner":
            self.ac_particles[appliance] = []
        elif appliance == "Speaker":
            self.speaker_waves[appliance] = []
        elif appliance == "Radio":
            self.radio_bars[appliance] = []
        elif appliance == "TV":
            pass
        
        if self.appliance_states[appliance]:
            self.start_animation(appliance)

    def toggle_appliance(self, appliance):
        self.appliance_states[appliance] = not self.appliance_states[appliance]
        state = "ON" if self.appliance_states[appliance] else "OFF"
        color = self.on_color if self.appliance_states[appliance] else self.off_color
        
        self.buttons[appliance].configure(text=state, bg=color)
        self.update_status(f"{appliance} turned {state}")
        
        if self.appliance_states[appliance]:
            self.start_animation(appliance)
        else:
            self.stop_animation(appliance)
            
        self.save_states()
    
    def start_animation(self, appliance):
        self.stop_animation(appliance)
        
        if "Fan" in appliance:
            self.animate_fan(appliance)
        elif "Light" in appliance:
            self.animate_light_bulb(appliance, 1)
        elif appliance == "Air Conditioner":
            self.animate_ac_wind(appliance)
        elif appliance == "TV":
            self.animate_tv(appliance)
        elif appliance == "Speaker":
            self.animate_speaker(appliance)
        elif appliance == "Radio":
            self.animate_radio(appliance)
        else:
            self.animate_button(appliance, 1, 0)
    
    def stop_animation(self, appliance):
        if appliance in self.animations:
            self.root.after_cancel(self.animations[appliance])
            del self.animations[appliance]
            
            if self.appliance_states[appliance]:
                self.buttons[appliance].configure(bg=self.on_color)
            
            if appliance in self.animation_canvases:
                self.animation_canvases[appliance].delete("all")
    
    def animate_button(self, appliance, direction, step):
        if not self.appliance_states[appliance] or appliance not in self.buttons:
            return
        
        current_color = self.buttons[appliance].cget("bg")
        r, g, b = self.hex_to_rgb(current_color)
        
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        
        v += direction * 0.02
        
        if v >= 1.0:
            v = 1.0
            direction = -1
        elif v <= 0.7:
            v = 0.7
            direction = 1
            
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        hex_color = self.rgb_to_hex(int(r*255), int(g*255), int(b*255))
        
        self.buttons[appliance].configure(bg=hex_color)
        
        animation_id = self.root.after(100, lambda: self.animate_button(appliance, direction, step+1))
        self.animations[appliance] = animation_id
    
    def draw_fan(self, appliance):
        if appliance not in self.animation_canvases:
            return
            
        canvas = self.animation_canvases[appliance]
        canvas.delete("all")
            
        canvas.create_oval(15, 15, 25, 25, fill="#333333", outline="#333333")
        
        angle = self.animation_angles.get(appliance, 0)
        
        for i in range(4):
            blade_angle = angle + (i * 90)
            x1 = 20 + 5 * math.cos(math.radians(blade_angle))
            y1 = 20 + 5 * math.sin(math.radians(blade_angle))
            x2 = 20 + 18 * math.cos(math.radians(blade_angle))
            y2 = 20 + 18 * math.sin(math.radians(blade_angle))
            
            canvas.create_line(x1, y1, x2, y2, width=3, fill="#333333")
            tip_angle = blade_angle + 30
            x3 = x2 + 5 * math.cos(math.radians(tip_angle))
            y3 = y2 + 5 * math.sin(math.radians(tip_angle))
            canvas.create_line(x2, y2, x3, y3, width=3, fill="#333333")
    
    def animate_fan(self, appliance):
        if not self.appliance_states[appliance] or appliance not in self.animation_canvases:
            return
        
        self.animation_angles[appliance] = (self.animation_angles[appliance] + 10) % 360
        
        self.draw_fan(appliance)
        
        animation_id = self.root.after(50, lambda: self.animate_fan(appliance))
        self.animations[appliance] = animation_id
    
    def draw_light_bulb(self, appliance):
        if appliance not in self.animation_canvases:
            return
            
        canvas = self.animation_canvases[appliance]
        canvas.delete("all")
            
        brightness = self.bulb_brightness.get(appliance, 0.0)
        
        bulb_color = self.get_brightness_color(brightness)
        glow_color = self.get_brightness_color(brightness * 0.7)
        
        canvas.create_oval(5, 5, 25, 25, fill=glow_color, outline="")
        
        canvas.create_oval(8, 8, 22, 22, fill=bulb_color, outline="#333333")
        
        canvas.create_rectangle(12, 22, 18, 30, fill="#888888", outline="#333333")
        canvas.create_rectangle(10, 30, 20, 35, fill="#888888", outline="#333333")
    
    def animate_light_bulb(self, appliance, direction):
        if not self.appliance_states[appliance] or appliance not in self.animation_canvases:
            return
        
        current = self.bulb_brightness.get(appliance, 0.0)
        current += direction * 0.05
        
        if current >= 1.0:
            current = 1.0
            direction = -1
        elif current <= 0.4:
            direction = 1
            
        self.bulb_brightness[appliance] = current
        
        self.draw_light_bulb(appliance)
        
        animation_id = self.root.after(100, lambda: self.animate_light_bulb(appliance, direction))
        self.animations[appliance] = animation_id
    
    def get_brightness_color(self, brightness):
        r = 255
        g = 255
        b = int(100 + brightness * 155)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def draw_ac(self, appliance):
        if appliance not in self.animation_canvases:
            return
            
        canvas = self.animation_canvases[appliance]
        canvas.delete("all")
            
        canvas.create_rectangle(5, 5, 20, 25, fill="#cccccc", outline="#333333")
        
        for y in range(8, 23, 5):
            canvas.create_line(20, y, 25, y, fill="#333333")
        
        particles = self.ac_particles.get(appliance, [])
        
        updated_particles = []
        for x, y, size in particles:
            if x < 60:
                canvas.create_oval(x, y, x+size, y+size, fill="#add8e6", outline="")
                updated_particles.append((x+2, y, size))
                
        if random.random() < 0.3:
            for _ in range(random.randint(1, 3)):
                y = random.randint(5, 25)
                size = random.uniform(1, 3)
                updated_particles.append((25, y, size))
                
        self.ac_particles[appliance] = updated_particles
    
    def animate_ac_wind(self, appliance):
        if not self.appliance_states[appliance] or appliance not in self.animation_canvases:
            return
        
        self.draw_ac(appliance)
        
        animation_id = self.root.after(70, lambda: self.animate_ac_wind(appliance))
        self.animations[appliance] = animation_id
    
    def draw_tv(self, appliance):
        if appliance not in self.animation_canvases:
            return
            
        canvas = self.animation_canvases[appliance]
        canvas.delete("all")
            
        canvas.create_rectangle(5, 5, 45, 35, fill="#222222", outline="#000000", width=2)
        
        channel = self.tv_state["channel"]
        frame = self.tv_state["frame"]
        
        if channel == 0:
            canvas.create_rectangle(8, 8, 42, 15, fill="#ff0000", outline="")
            text_pos = 42 - (frame % 50)
            canvas.create_text(text_pos, 12, text="NEWS", fill="white", font=("Arial", 6))
            canvas.create_rectangle(8, 16, 42, 32, fill="#dddddd", outline="")
            for i in range(3):
                canvas.create_line(10, 20+i*4, 40, 20+i*4, fill="#555555")
        
        elif channel == 1:
            if frame % 20 < 10:
                canvas.create_rectangle(8, 8, 42, 32, fill="#0000ff", outline="")
                canvas.create_oval(15, 15, 25, 25, fill="#ffff00", outline="")
            else:
                canvas.create_rectangle(8, 8, 42, 32, fill="#008800", outline="")
                canvas.create_rectangle(25, 15, 35, 25, fill="#ff0000", outline="")
        
        elif channel == 2:
            canvas.create_rectangle(8, 8, 42, 32, fill="#00aa00", outline="")
            ball_x = 25 + 15 * math.cos(frame * 0.2)
            ball_y = 20 + 8 * math.sin(frame * 0.3)
            canvas.create_oval(ball_x-3, ball_y-3, ball_x+3, ball_y+3, fill="white", outline="")
        
        canvas.create_rectangle(20, 35, 30, 38, fill="#444444", outline="#000000")
    
    def animate_tv(self, appliance):
        if not self.appliance_states[appliance] or appliance not in self.animation_canvases:
            return
        
        self.tv_state["frame"] = (self.tv_state["frame"] + 1) % 100
        
        if self.tv_state["frame"] == 0 and random.random() < 0.3:
            self.tv_state["channel"] = (self.tv_state["channel"] + 1) % 3
        
        self.draw_tv(appliance)
        
        animation_id = self.root.after(100, lambda: self.animate_tv(appliance))
        self.animations[appliance] = animation_id
        
    def draw_speaker(self, appliance):
        if appliance not in self.animation_canvases:
            return
            
        canvas = self.animation_canvases[appliance]
        canvas.delete("all")
            
        canvas.create_rectangle(5, 10, 15, 30, fill="#333333", outline="#222222")
        
        canvas.create_oval(8, 15, 12, 25, fill="#666666", outline="#444444")
        
        waves = self.speaker_waves.get(appliance, [])
        
        for radius in waves:
            x = 10 + radius
            canvas.create_arc(
                x-radius, 20-radius, x+radius, 20+radius,
                start=270, extent=180, style="arc", outline="#333333", width=2
            )
        
        updated_waves = [r+1 for r in waves if r < 25]
        
        if random.random() < 0.2 or not updated_waves:
            updated_waves.append(3)
            
        self.speaker_waves[appliance] = updated_waves
    
    def animate_speaker(self, appliance):
        if not self.appliance_states[appliance] or appliance not in self.animation_canvases:
            return
        
        self.draw_speaker(appliance)
        
        animation_id = self.root.after(100, lambda: self.animate_speaker(appliance))
        self.animations[appliance] = animation_id
    
    def draw_radio(self, appliance):
        if appliance not in self.animation_canvases:
            return
            
        canvas = self.animation_canvases[appliance]
        canvas.delete("all")
            
        canvas.create_rectangle(5, 10, 35, 30, fill="#884400", outline="#663300", width=2)
        
        canvas.create_oval(10, 15, 18, 23, fill="#cccccc", outline="#333333")
        canvas.create_line(14, 19, 17, 19, fill="#333333", width=1)
        
        canvas.create_rectangle(20, 13, 32, 27, fill="#222222", outline="#111111")
        
        bars = self.radio_bars.get(appliance, [])
        if not bars:
            bars = [0, 0, 0, 0, 0]
        
        bar_width = 2
        for i, height in enumerate(bars):
            x = 21 + i * (bar_width + 1)
            canvas.create_rectangle(
                x, 26-height, x+bar_width, 26,
                fill="#00ff00", outline=""
            )
        
        updated_bars = []
        for _ in range(5):
            if random.random() < 0.7:
                height = random.randint(2, 12)
            else:
                height = bars[_] if _ < len(bars) else random.randint(2, 12)
            updated_bars.append(height)
            
        self.radio_bars[appliance] = updated_bars
    
    def animate_radio(self, appliance):
        if not self.appliance_states[appliance] or appliance not in self.animation_canvases:
            return
        
        self.draw_radio(appliance)
        
        animation_id = self.root.after(200, lambda: self.animate_radio(appliance))
        self.animations[appliance] = animation_id
    
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'
        
    def update_status(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_var.set(f"{timestamp} - {message}")

    def save_states(self):
        try:
            with open("appliance_states.json", "w") as f:
                json.dump(self.appliance_states, f)
            self.update_status("Configuration saved")
        except Exception as e:
            self.update_status(f"Error saving configuration: {e}")

    def load_states(self):
        try:
            with open("appliance_states.json", "r") as f:
                saved_states = json.load(f)
                self.appliance_states.update(saved_states)
                self.update_status("Configuration loaded")
        except FileNotFoundError:
            self.update_status("No saved configuration found")
        except Exception as e:
            self.update_status(f"Error loading configuration: {e}")
            
        for appliance, state in self.appliance_states.items():
            if appliance in self.buttons:
                text = "ON" if state else "OFF"
                color = self.on_color if state else self.off_color
                self.buttons[appliance].configure(text=text, bg=color)
                
                if state:
                    self.start_animation(appliance)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('clam')
    app = HomeApplianceControl(root)
    root.mainloop() 