import customtkinter as ctk

# --- App Setup ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("700x500")
app.title("Imaginarium Theatre Helper")

# --- Tab View ---
tabview = ctk.CTkTabview(app, width=680, height=460)
tabview.pack(padx=10, pady=10)

tabview.add("This Month")
tabview.add("Your Characters")
tabview.add("Build Recommendations")

# --- Tab Content Placeholders ---
tab1 = tabview.tab("This Month")
tab2 = tabview.tab("Your Characters")
tab3 = tabview.tab("Build Recommendations")

ctk.CTkLabel(tab1, text="This Month's Info Here", font=("Arial", 16)).pack(pady=20)
ctk.CTkLabel(tab2, text="Character Selection Coming Soon", font=("Arial", 16)).pack(pady=20)
ctk.CTkLabel(tab3, text="Build Advice Coming Soon", font=("Arial", 16)).pack(pady=20)

# --- Launch ---
app.mainloop()
