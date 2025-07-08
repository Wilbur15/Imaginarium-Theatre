import customtkinter as ctk
from CharacterUI import CharacterSelector
from QualificationUI import QualificationPage

# --- App Setup ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.after(0, lambda: app.wm_state('zoomed'))
app.title("Imaginarium Theatre Helper")


# --- Tab View ---
tabview = ctk.CTkTabview(app)
tabview.pack(padx=20, pady=20, fill="both", expand=True)

tabview.add("This Month")
tabview.add("Your Characters")
tabview.add("Build Recommendations")

# --- Tab References ---
tab1 = tabview.tab("This Month")
tab2 = tabview.tab("Your Characters")
tab3 = tabview.tab("Build Recommendations")

# --- Load Qualification Page into Tab 1 ---
qualification_page = QualificationPage(master=tab1)
qualification_page.pack(pady=20, padx=20, fill="both", expand=True)

# Callback to refresh qualification page on character save
def refresh_qualification():
    qualification_page.load_data()
    qualification_page.update_display(qualification_page.month_option.get())

# --- Load Character Selector into Tab 2 ---
character_selector = CharacterSelector(master=tab2, on_save_callback=refresh_qualification)
character_selector.pack(pady=10, padx=20, fill="both", expand=True)

# --- Placeholder for Tab 3 ---
ctk.CTkLabel(tab3, text="Build Advice Coming Soon", font=("Arial", 16)).pack(pady=40)

# --- Launch App ---
app.mainloop()
