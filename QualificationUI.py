import customtkinter as ctk
import json

class QualificationPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.month_file = "data/months.json"
        self.char_file = "data/characters.json"

        self.load_data()

        # Dropdown to select the month
        self.month_option = ctk.CTkOptionMenu(
            self, values=["previous", "current", "next"],
            command=self.update_display
        )
        self.month_option.set("current")
        self.month_option.pack(pady=10)

        # Label for result
        self.result_label = ctk.CTkLabel(self, text="", font=("Arial", 16), wraplength=600, justify="left")
        self.result_label.pack(pady=20)

        self.update_display("current")

    def load_data(self):
        with open(self.month_file, "r", encoding="utf-8") as f:
            self.months = json.load(f)
        with open(self.char_file, "r", encoding="utf-8") as f:
            self.characters = json.load(f)

    def update_display(self, selected_month_key):
        month_data = self.months[selected_month_key]
        trials = set(month_data["trial_characters"])
        featured_elements = set(month_data["featured_elements"])
        off_element_allowed = set(month_data["off_element_characters"])

        total = 6  # Always start with 6 trials

        # Track usable off-element characters
        owned_off_elements = [
            char for char in self.characters
            if char["Name"] in off_element_allowed
            and char.get("owned", False)
            and char.get("Element") not in featured_elements
            and char.get("level", 1) >= 60
        ]
        total += min(len(owned_off_elements), 4)

        # Count additional owned featured-element characters (not trials)
        owned_featured = [
            char for char in self.characters
            if char["Name"] not in trials
            and char.get("owned", False)
            and char.get("Element") in featured_elements
            and char.get("level", 1) >= 60
        ]
        total += len(owned_featured)

        # Determine highest difficulty unlocked
        difficulty = "None"
        if total >= 22 and all(c["level"] >= 70 for c in owned_off_elements + owned_featured):
            difficulty = "Visionary"
        elif total >= 16 and all(c["level"] >= 70 for c in owned_off_elements + owned_featured):
            difficulty = "Hard"
        elif total >= 12:
            difficulty = "Normal"
        elif total >= 8:
            difficulty = "Easy"

        breakdown = (
            f"📅 Month: {month_data['name']}\n\n"
            f"🧪 Trial Characters: 6\n"
            f"🔁 Owned Off-Element Characters: {len(owned_off_elements)} / 4\n"
            f"🌟 Owned Featured-Element Characters (not trials): {len(owned_featured)}\n\n"
            f"🧮 Total Usable: {total}\n\n"
            f"🎯 Highest Qualified Difficulty: {difficulty}"
        )

        self.result_label.configure(text=breakdown)
