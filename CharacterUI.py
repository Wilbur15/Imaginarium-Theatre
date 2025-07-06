import customtkinter as ctk
from PIL import Image
import json
import os

class CharacterSelector(ctk.CTkFrame):
    def __init__(self, master, on_save_callback=None):
        super().__init__(master)

        self.characters_file = "data/characters.json"
        self.on_save_callback = on_save_callback

        # Load character data
        with open(self.characters_file, "r", encoding="utf-8") as f:
            self.characters = json.load(f)

        # Dicts to hold widget references for state gathering
        self.checkboxes = {}
        self.level_entries = {}

        scrollable_frame = ctk.CTkScrollableFrame(self, width=600, height=400)
        scrollable_frame.pack(fill="both", expand=True)

        cols = 2
        for i, char in enumerate(self.characters):
            col = i % cols
            row = i // cols

            name = char["Name"].replace(" ", "_")
            icon_path = os.path.join("character_icons", f"{name}_icon.png")

            char_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
            char_frame.grid(row=row, column=col, padx=20, pady=10, sticky="w")

            if os.path.exists(icon_path):
                image = Image.open(icon_path).resize((48, 48))
                icon = ctk.CTkImage(light_image=image, size=(48, 48))
                icon_label = ctk.CTkLabel(char_frame, image=icon, text="")
                icon_label.image = icon
                icon_label.grid(row=0, column=0, rowspan=2, padx=5)
            else:
                icon_label = ctk.CTkLabel(char_frame, text="No Icon")
                icon_label.grid(row=0, column=0, rowspan=2, padx=5)

            # Checkbox with initial state from JSON (default False)
            owned = char.get("owned", False)
            checkbox = ctk.CTkCheckBox(char_frame, text=name, command=self.on_state_change)
            checkbox.grid(row=0, column=1, sticky="w", padx=5)
            checkbox.select() if owned else checkbox.deselect()

            # Level entry with initial value from JSON (default 1)
            level = char.get("level", 1)
            level_entry = ctk.CTkEntry(char_frame, width=50)
            level_entry.insert(0, str(level))
            level_entry.grid(row=1, column=1, sticky="w", padx=5)

            # Store references
            self.checkboxes[name] = checkbox
            self.level_entries[name] = level_entry

        # Save button to write updates to JSON
        save_button = ctk.CTkButton(self, text="Save Changes", command=self.save_changes)
        save_button.pack(pady=10)

        for c in range(cols):
            scrollable_frame.columnconfigure(c, weight=1)

    def on_state_change(self):
        # Optional: React immediately on checkbox toggle if needed
        pass

    def save_changes(self):
        # Update self.characters with current checkbox and level states
        for char in self.characters:
            name = char["Name"].replace(" ", "_")
            checkbox = self.checkboxes.get(name)
            level_entry = self.level_entries.get(name)

            if checkbox:
                char["owned"] = checkbox.get()  # True or False

            if level_entry:
                # Validate and clamp level to integer, min 1
                try:
                    level_val = int(level_entry.get())
                    if level_val < 1:
                        level_val = 1
                except ValueError:
                    level_val = 1
                char["level"] = level_val

        # Write updated data back to JSON file
        with open(self.characters_file, "w", encoding="utf-8") as f:
            json.dump(self.characters, f, indent=4)

        print("Character data saved!")

        # Call the callback to update qualification page if provided
        if self.on_save_callback:
            self.on_save_callback()
