import customtkinter as ctk
from PIL import Image
import json
import os

class CharacterSelector(ctk.CTkFrame):
    def __init__(self, master, on_save_callback=None):
        super().__init__(master)
        self.characters_file = "data/characters.json"
        self.on_save_callback = on_save_callback

        with open(self.characters_file, "r", encoding="utf-8") as f:
            self.characters = json.load(f)

        self.sort_mode = "level"  # Default sort
        self.sort_reverse = True  # Descending level

        # --- Sort Controls ---
        sort_frame = ctk.CTkFrame(self)
        sort_frame.pack(pady=10)

        ctk.CTkLabel(sort_frame, text="Sort by:").pack(side="left", padx=(0, 5))

        self.sort_dropdown = ctk.CTkOptionMenu(
            sort_frame,
            values=["name", "element", "level"],
            command=self.change_sort
        )
        self.sort_dropdown.set("level")
        self.sort_dropdown.pack(side="left")

        # --- Scrollable Grid ---
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=1600, height=800)
        self.scrollable_frame.pack(fill="both", expand=True)

        self.checkboxes = {}
        self.level_entries = {}

        self.display_characters()

        # Save Button
        save_button = ctk.CTkButton(self, text="Save Changes", command=self.save_changes)
        save_button.pack(pady=10)

    def change_sort(self, selected):
        if selected == self.sort_mode:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_mode = selected
            self.sort_reverse = selected == "level"
        self.display_characters()

    def display_characters(self):
        # Clear current display
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        def sort_key(char):
            if self.sort_mode == "name":
                return char["Name"]
            elif self.sort_mode == "element":
                return char.get("Element", "")
            elif self.sort_mode == "level":
                return char.get("level", 1)
            return char["Name"]

        sorted_chars = sorted(self.characters, key=sort_key, reverse=self.sort_reverse)

        cols = 10
        card_width = 160
        card_height = 160

        self.checkboxes.clear()
        self.level_entries.clear()

        for i, char in enumerate(sorted_chars):
            col = i % cols
            row = i // cols

            name_key = char["Name"].replace(" ", "_")
            icon_path = os.path.join("character_icons", f"{name_key}_icon.png")

            char_frame = ctk.CTkFrame(
                self.scrollable_frame,
                width=card_width,
                height=card_height,
                fg_color="#2c3e50",  # Darker pale blue
                corner_radius=12
            )
            char_frame.grid(row=row, column=col, padx=8, pady=8)
            char_frame.grid_propagate(False)

            # Icon
            if os.path.exists(icon_path):
                image = Image.open(icon_path).resize((50, 50))
                icon = ctk.CTkImage(light_image=image, size=(50, 50))
                icon_label = ctk.CTkLabel(char_frame, image=icon, text="")
                icon_label.image = icon
                icon_label.grid(row=0, column=0, columnspan=1, pady=(8, 4), sticky="n")
            else:
                icon_label = ctk.CTkLabel(char_frame, text="", width=50, height=50)
                icon_label.grid(row=0, column=0, columnspan=1, pady=(8, 4), sticky="n")

            # Name centered, two-line if contains space
            name = char["Name"]
            if " " in name:
                name = name.replace(" ", "\n")
            name_label = ctk.CTkLabel(
                char_frame,
                text=name,
                justify="center",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            name_label.grid(row=1, column=0, pady=(0, 4), sticky="n")

            # Checkbox centered under name
            owned = char.get("owned", False)
            checkbox = ctk.CTkCheckBox(char_frame, text="", width=20, height=20)
            checkbox.grid(row=2, column=0, pady=(0, 4), sticky="n")
            if owned:
                checkbox.select()
            else:
                checkbox.deselect()

            # Level entry below checkbox
            level = char.get("level", 1)
            level_entry = ctk.CTkEntry(char_frame, width=40, justify="center")
            level_entry.insert(0, str(level))
            level_entry.grid(row=3, column=0, pady=(0, 8), sticky="n")

            # Configure single column to center items horizontally
            char_frame.grid_columnconfigure(0, weight=1)

            self.checkboxes[name_key] = checkbox
            self.level_entries[name_key] = level_entry

        for i in range(cols):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)

    def save_changes(self):
        for char in self.characters:
            name_key = char["Name"].replace(" ", "_")
            checkbox = self.checkboxes.get(name_key)
            level_entry = self.level_entries.get(name_key)

            if checkbox:
                char["owned"] = checkbox.get()

            if level_entry:
                try:
                    level_val = int(level_entry.get())
                    level_val = max(1, min(level_val, 90))  # Clamp between 1 and 90
                except ValueError:
                    level_val = 1
                char["level"] = level_val

        with open(self.characters_file, "w", encoding="utf-8") as f:
            json.dump(self.characters, f, indent=4)

        print("Character data saved!")

        if self.on_save_callback:
            self.on_save_callback()
