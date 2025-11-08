import tkinter as tk
from tkinter import ttk
import json
import os
from pathlib import Path

class CatsUltraHLE:
    def __init__(self, root):
        self.root = root
        self.root.title("Cat's UltraHLE 0.1")
        self.root.geometry("800x600")
        
        # Dummy backend data - ROM database
        self.rom_db = self.load_db()
        self.rom_list = self.scan_roms()  # Initially empty list
        
        self.setup_ui()
        self.refresh_rom_list()
    
    # ─────────────────────────────
    # Database Handling
    # ─────────────────────────────
    def load_db(self):
        """Load ROM database from JSON, or create one if missing."""
        db_path = Path("cats_ultrahle_db.json")
        if db_path.exists():
            try:
                with open(db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("⚠️ Corrupt database file detected; resetting.")
                return {"roms": []}
        return {"roms": []}
    
    def save_db(self):
        """Save ROM database to JSON."""
        with open("cats_ultrahle_db.json", 'w', encoding='utf-8') as f:
            json.dump(self.rom_db, f, indent=2)
    
    # ─────────────────────────────
    # ROM Scanning
    # ─────────────────────────────
    def scan_roms(self):
        """Dummy ROM scanner - returns an empty list."""
        # In a real emulator, you would scan directories for .z64, .n64, .v64, etc.
        return self.rom_db.get("roms", [])
    
    # ─────────────────────────────
    # UI Setup
    # ─────────────────────────────
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Treeview columns
        columns = ("File", "Country", "Size", "Status", "Comments")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=1, column=0, sticky="w", pady=10)
        
        ttk.Button(btn_frame, text="Refresh ROM List", command=self.refresh_rom_list).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Update DB", command=self.update_db).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Load ROM", command=self.load_rom).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Run", command=self.run_emulator).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Pause", command=self.pause_emulator).grid(row=0, column=4, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready - No ROMs Loaded")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, sticky="ew", pady=5)
        
        # Bottom cycle indicators
        cycle_frame = ttk.Frame(main_frame)
        cycle_frame.grid(row=3, column=0, sticky="w", pady=5)
        
        ttk.Label(cycle_frame, text="CPU:").grid(row=0, column=0)
        self.cpu_var = tk.StringVar(value="0%")
        ttk.Label(cycle_frame, textvariable=self.cpu_var).grid(row=0, column=1, padx=10)
        
        ttk.Label(cycle_frame, text="GFX:").grid(row=0, column=2)
        self.gfx_var = tk.StringVar(value="0 FPS")
        ttk.Label(cycle_frame, textvariable=self.gfx_var).grid(row=0, column=3, padx=10)
        
        # Configure grid behavior
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
    
    # ─────────────────────────────
    # Logic Functions
    # ─────────────────────────────
    def refresh_rom_list(self):
        """Populate the ROM list."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        roms = self.scan_roms()
        if roms:
            for rom in roms:
                self.tree.insert("", tk.END, values=(
                    rom.get("file", ""),
                    rom.get("country", ""),
                    rom.get("size", ""),
                    rom.get("status", ""),
                    rom.get("comments", "")
                ))
            self.status_var.set(f"Loaded {len(roms)} ROM(s) from database")
        else:
            self.tree.insert("", tk.END, values=("", "", "", "No ROMs Found", "Scan or add some contraband"))
            self.status_var.set("ROM list refreshed - Vault empty")
    
    def update_db(self):
        """Add a test ROM entry."""
        new_rom = {
            "file": "Phantom Cart (USA).z64",
            "country": "USA",
            "size": "8 MB",
            "status": "Ghost",
            "comments": "Added from shadows"
        }
        self.rom_db.setdefault("roms", []).append(new_rom)
        self.save_db()
        self.refresh_rom_list()
        self.status_var.set("DB seeded with ghost data 🕹️")
    
    def load_rom(self):
        """Simulate ROM loading."""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            rom_file = item['values'][0]
            if rom_file:
                self.status_var.set(f"Loaded: {rom_file}")
            else:
                self.status_var.set("Selected ROM entry invalid.")
        else:
            self.status_var.set("No ROM selected.")
    
    def run_emulator(self):
        """Mock emulator window."""
        self.status_var.set("Emulating void...")
        emu_window = tk.Toplevel(self.root)
        emu_window.title("Emulation Window")
        emu_window.geometry("640x480")
        label = tk.Label(
            emu_window,
            text="N64 Emulation Running!\n(Blank cart - staring into the abyss)",
            bg="black",
            fg="lime",
            font=("Courier", 16)
        )
        label.pack(expand=True, fill="both")
        self.cpu_var.set("∞%")
        self.gfx_var.set("Glitch FPS")
    
    def pause_emulator(self):
        """Pause the mock emulation."""
        self.status_var.set("Paused in the shadows")
        self.cpu_var.set("0%")
        self.gfx_var.set("0 FPS")


if __name__ == "__main__":
    root = tk.Tk()
    app = CatsUltraHLE(root)
    root.mainloop()
