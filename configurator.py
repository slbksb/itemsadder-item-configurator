import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import yaml
import webbrowser

class ConfigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EnderAzure's ItemsAdder Configurator")
        self.root.geometry("1800x900")  # Set initial window size to be larger

        self.previous_state = ""
        self.lore_list = []

        # Paned window to allow resizing between settings and config display
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=1)

        # Left frame for settings
        self.settings_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.settings_frame, minsize=200)

        # Canvas and vertical scrollbar for scrolling
        self.canvas = tk.Canvas(self.settings_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.scrollbar = ttk.Scrollbar(self.settings_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.second_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.second_frame, anchor="nw")

        # Bind mouse wheel to scroll everywhere
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind_all("<Button-4>", self._on_mouse_wheel)
        self.canvas.bind_all("<Button-5>", self._on_mouse_wheel)

        # Right frame for config display
        self.config_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.config_frame, minsize=200)

        # Set the initial split ratio (3/4 for settings, 1/4 for config)
        self.paned_window.paneconfig(self.settings_frame, minsize=900)
        self.paned_window.paneconfig(self.config_frame, minsize=300)

        # Text widget to display the config
        self.config_text = tk.Text(self.config_frame, height=40, width=80)
        self.config_text.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

        # Add all other widgets to self.second_frame instead of root
        self.setup_widgets()

        # Initial update
        self.update_config_if_changed()

    def _on_mouse_wheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units")
        if event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units")

    def setup_widgets(self):
        # Type Selection
        tk.Label(self.second_frame, text="Type:").grid(row=0, column=0, padx=10, pady=10)
        self.type_var = tk.StringVar(self.second_frame)
        self.type_var.set("Tool")
        self.type_menu = tk.OptionMenu(self.second_frame, self.type_var, "Tool", "Armor", command=self.update_type)
        self.type_menu.grid(row=0, column=1, padx=10, pady=10)

        # Item ID
        tk.Label(self.second_frame, text="Item ID:").grid(row=1, column=0, padx=10, pady=10)
        self.item_id_entry = tk.Entry(self.second_frame, width=50)
        self.item_id_entry.grid(row=1, column=1, padx=10, pady=10)

        # Display name
        tk.Label(self.second_frame, text="Display Name:").grid(row=2, column=0, padx=10, pady=10)
        self.display_name_entry = tk.Entry(self.second_frame, width=50)
        self.display_name_entry.grid(row=2, column=1, padx=10, pady=10)
        self.color_codes_button = tk.Button(self.second_frame, text="Minecraft Color Codes", command=self.open_color_codes)
        self.color_codes_button.grid(row=2, column=2, padx=10, pady=10)

        # Lore
        tk.Label(self.second_frame, text="Lore:").grid(row=3, column=0, padx=10, pady=10)
        self.lore_entry = tk.Entry(self.second_frame, width=50)
        self.lore_entry.grid(row=3, column=1, padx=10, pady=10)
        self.add_lore_button = tk.Button(self.second_frame, text="+", command=self.add_lore)
        self.add_lore_button.grid(row=3, column=2, padx=10, pady=10)

        # Material
        tk.Label(self.second_frame, text="Material:").grid(row=4, column=0, padx=10, pady=10)
        self.material_entry = tk.Entry(self.second_frame, width=50)
        self.material_entry.grid(row=4, column=1, padx=10, pady=10)

        # Texture Path
        self.texture_label = tk.Label(self.second_frame, text="Texture Path:")
        self.texture_label.grid(row=5, column=0, padx=10, pady=10)
        self.texture_entry = tk.Entry(self.second_frame, width=50)
        self.texture_entry.grid(row=5, column=1, padx=10, pady=10)

        # Model Path
        self.model_label = tk.Label(self.second_frame, text="Model Path:")
        self.model_label.grid(row=6, column=0, padx=10, pady=10)
        self.model_entry = tk.Entry(self.second_frame, width=50)
        self.model_entry.grid(row=6, column=1, padx=10, pady=10)

        # Enchants
        self.enchants = []
        self.enchant_var = tk.StringVar(self.second_frame)
        self.enchant_var.set("Select Enchant")
        self.enchantments = [
            ("aqua_affinity", "Aqua Affinity (Helmet)"),
            ("bane_of_arthropods", "Bane of Arthropods (Sword)"),
            ("blast_protection", "Blast Protection (Armor)"),
            ("channeling", "Channeling (Trident)"),
            ("curse_of_binding", "Curse of Binding (Armor)"),
            ("curse_of_vanishing", "Curse of Vanishing (All)"),
            ("depth_strider", "Depth Strider (Boots)"),
            ("efficiency", "Efficiency (Tools)"),
            ("feather_falling", "Feather Falling (Boots)"),
            ("fire_aspect", "Fire Aspect (Sword)"),
            ("fire_protection", "Fire Protection (Armor)"),
            ("flame", "Flame (Bow)"),
            ("fortune", "Fortune (Tools)"),
            ("frost_walker", "Frost Walker (Boots)"),
            ("impaling", "Impaling (Trident)"),
            ("infinity", "Infinity (Bow)"),
            ("knockback", "Knockback (Sword)"),
            ("looting", "Looting (Sword)"),
            ("loyalty", "Loyalty (Trident)"),
            ("luck_of_the_sea", "Luck of the Sea (Fishing Rod)"),
            ("lure", "Lure (Fishing Rod)"),
            ("mending", "Mending (All)"),
            ("multishot", "Multishot (Crossbow)"),
            ("piercing", "Piercing (Crossbow)"),
            ("power", "Power (Bow)"),
            ("projectile_protection", "Projectile Protection (Armor)"),
            ("protection", "Protection (Armor)"),
            ("punch", "Punch (Bow)"),
            ("quick_charge", "Quick Charge (Crossbow)"),
            ("respiration", "Respiration (Helmet)"),
            ("riptide", "Riptide (Trident)"),
            ("sharpness", "Sharpness (Sword)"),
            ("silk_touch", "Silk Touch (Tools)"),
            ("smite", "Smite (Sword)"),
            ("soul_speed", "Soul Speed (Boots)"),
            ("sweeping_edge", "Sweeping Edge (Sword)"),
            ("thorns", "Thorns (Armor)"),
            ("unbreaking", "Unbreaking (All)")
        ]

        self.enchant_label = tk.Label(self.second_frame, text="Select Enchant:")
        self.enchant_label.grid(row=7, column=0, padx=10, pady=10)
        self.enchant_menu = tk.OptionMenu(self.second_frame, self.enchant_var, *[desc for code, desc in self.enchantments])
        self.enchant_menu.grid(row=7, column=1, padx=10, pady=10)

        self.enchant_level_label = tk.Label(self.second_frame, text="Enchant Level:")
        self.enchant_level_label.grid(row=8, column=0, padx=10, pady=10)
        self.enchant_level_entry = tk.Entry(self.second_frame, width=50)
        self.enchant_level_entry.grid(row=8, column=1, padx=10, pady=10)

        self.add_enchant_button = tk.Button(self.second_frame, text="Add Enchant", command=self.add_enchant)
        self.add_enchant_button.grid(row=9, columnspan=2, pady=10)

        # Custom Enchants
        tk.Label(self.second_frame, text="Custom Enchant:").grid(row=10, column=0, padx=10, pady=10)
        self.custom_enchant_entry = tk.Entry(self.second_frame, width=50)
        self.custom_enchant_entry.grid(row=10, column=1, padx=10, pady=10)

        self.add_custom_enchant_button = tk.Button(self.second_frame, text="Add Custom Enchant", command=self.add_custom_enchant)
        self.add_custom_enchant_button.grid(row=11, columnspan=2, pady=10)

        # Unbreakable checkbox
        self.unbreakable_var = tk.BooleanVar()
        self.unbreakable_check = tk.Checkbutton(self.second_frame, text="Unbreakable", variable=self.unbreakable_var, command=self.update_config_if_changed)
        self.unbreakable_check.grid(row=12, columnspan=2, pady=10)

        # Max Custom Durability
        self.durability_label = tk.Label(self.second_frame, text="Max Custom Durability:")
        self.durability_label.grid(row=13, column=0, padx=10, pady=10)
        self.durability_entry = tk.Entry(self.second_frame, width=50)
        self.durability_entry.grid(row=13, column=1, padx=10, pady=10)

        # Custom Durability
        self.custom_durability_label = tk.Label(self.second_frame, text="Custom Durability:")
        self.custom_durability_label.grid(row=14, column=0, padx=10, pady=10)
        self.custom_durability_entry = tk.Entry(self.second_frame, width=50)
        self.custom_durability_entry.grid(row=14, column=1, padx=10, pady=10)

        # Disappear When Broken
        self.disappear_when_broken_var = tk.BooleanVar()
        self.disappear_when_broken_check = tk.Checkbutton(self.second_frame, text="Disappear When Broken", variable=self.disappear_when_broken_var, command=self.update_config_if_changed)
        self.disappear_when_broken_check.grid(row=15, columnspan=2, pady=10)

        # Armor specific properties (initially hidden)
        self.armor_properties_frame = tk.Frame(self.second_frame)

        # Armor Slot Selection
        tk.Label(self.armor_properties_frame, text="Armor Slot:").grid(row=0, column=0, padx=10, pady=10)
        self.armor_slot_var = tk.StringVar(self.armor_properties_frame)
        self.armor_slot_var.set("chest")
        self.armor_slot_menu = tk.OptionMenu(self.armor_properties_frame, self.armor_slot_var, "chest", "head", "legs", "feet")
        self.armor_slot_menu.grid(row=0, column=1, padx=10, pady=10)

        # Armor Value
        tk.Label(self.armor_properties_frame, text="Armor Value:").grid(row=1, column=0, padx=10, pady=10)
        self.armor_value_entry = tk.Entry(self.armor_properties_frame, width=50)
        self.armor_value_entry.grid(row=1, column=1, padx=10, pady=10)

        # Armor Toughness
        tk.Label(self.armor_properties_frame, text="Armor Toughness:").grid(row=2, column=0, padx=10, pady=10)
        self.armor_toughness_entry = tk.Entry(self.armor_properties_frame, width=50)
        self.armor_toughness_entry.grid(row=2, column=1, padx=10, pady=10)

        # Attribute Modifiers
        self.attribute_modifiers = {}
        self.attribute_modifier_var = tk.StringVar(self.second_frame)
        self.attribute_modifier_var.set("Select Modifier")
        self.attribute_modifiers_options = [
            "attackDamage", "attackSpeed", "maxHealth", "movementSpeed", 
            "armor", "armorToughness", "attackKnockback", "luck"
        ]

        self.attribute_modifier_label = tk.Label(self.second_frame, text="Select Modifier:")
        self.attribute_modifier_label.grid(row=16, column=0, padx=10, pady=10)
        self.attribute_modifier_menu = tk.OptionMenu(self.second_frame, self.attribute_modifier_var, *self.attribute_modifiers_options)
        self.attribute_modifier_menu.grid(row=16, column=1, padx=10, pady=10)

        self.attribute_modifier_value_label = tk.Label(self.second_frame, text="Modifier Value:")
        self.attribute_modifier_value_label.grid(row=17, column=0, padx=10, pady=10)
        self.attribute_modifier_value_entry = tk.Entry(self.second_frame, width=50)
        self.attribute_modifier_value_entry.grid(row=17, column=1, padx=10, pady=10)

        # Slot selection for modifiers
        self.modifier_slot_var = tk.StringVar(self.second_frame)
        self.modifier_slot_var.set("mainhand")
        self.modifier_slot_label = tk.Label(self.second_frame, text="Modifier Slot:")
        self.modifier_slot_label.grid(row=18, column=0, padx=10, pady=10)
        self.modifier_slot_menu = tk.OptionMenu(self.second_frame, self.modifier_slot_var, "mainhand", "head", "chest", "legs", "feet")
        self.modifier_slot_menu.grid(row=18, column=1, padx=10, pady=10)

        self.add_attribute_modifier_button = tk.Button(self.second_frame, text="Add Modifier", command=self.add_attribute_modifier)
        self.add_attribute_modifier_button.grid(row=19, columnspan=2, pady=10)

        # Bind change events to inputs
        self.bind_change_events()

    def bind_change_events(self):
        self.item_id_entry.bind("<KeyRelease>", lambda event: self.update_config_if_changed())
        self.display_name_entry.bind("<KeyRelease>", lambda event: self.update_config_if_changed())
        self.lore_entry.bind("<KeyRelease>", lambda event: self.update_config_if_changed())
        self.material_entry.bind("<KeyRelease>", lambda event: self.update_config_if_changed())
        self.texture_entry.bind("<KeyRelease>", lambda event: self.update_config_if_changed())
        self.model_entry.bind("<KeyRelease>", lambda event: self.update_config_if_changed())
        self.enchant_level_entry.bind("<KeyRelease>", lambda event: self.update_config_if_changed())
        self.durability_entry.bind("<KeyRelease>", lambda event: self.update_config_if_changed())
        self.custom_durability_entry.bind("<KeyRelease>", lambda event: self.update_config_if_changed())
        self.custom_enchant_entry.bind("<KeyRelease>", lambda event: self.update_config_if_changed())
        self.armor_value_entry.bind("<KeyRelease>", lambda event: self.update_config_if_changed())
        self.armor_toughness_entry.bind("<KeyRelease>", lambda event: self.update_config_if_changed())
        self.attribute_modifier_value_entry.bind("<KeyRelease>", lambda event: self.update_config_if_changed())
        self.enchant_var.trace("w", lambda *args: self.update_config_if_changed())
        self.armor_slot_var.trace("w", lambda *args: self.update_config_if_changed())
        self.type_var.trace("w", lambda *args: self.update_type())
        self.disappear_when_broken_var.trace("w", lambda *args: self.update_config_if_changed())

    def add_lore(self):
        lore_text = self.lore_entry.get().strip()
        if lore_text:
            self.lore_list.append(lore_text)
            self.lore_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Lore '{lore_text}' added.")
            self.update_config_if_changed()
        else:
            messagebox.showerror("Error", "Please enter valid lore text.")

    def add_enchant(self):
        enchant_desc = self.enchant_var.get()
        level = self.enchant_level_entry.get()
        enchant = next((code for code, desc in self.enchantments if desc == enchant_desc), None)
        if enchant and level.isdigit():
            self.enchants.append(f"{enchant}:{level}")
            self.enchant_var.set("Select Enchant")
            self.enchant_level_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Enchant {enchant_desc} level {level} added.")
            self.update_config_if_changed()
        else:
            messagebox.showerror("Error", "Please select a valid enchant and enter a numeric level.")

    def add_custom_enchant(self):
        custom_enchant = self.custom_enchant_entry.get().strip()
        if custom_enchant:
            self.enchants.append(custom_enchant)
            self.custom_enchant_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Custom Enchant '{custom_enchant}' added.")
            self.update_config_if_changed()
        else:
            messagebox.showerror("Error", "Please enter a valid custom enchant.")

    def add_attribute_modifier(self):
        modifier = self.attribute_modifier_var.get()
        value = self.attribute_modifier_value_entry.get().strip()
        slot = self.modifier_slot_var.get()
        if modifier != "Select Modifier" and self.is_valid_number(value):
            if slot not in self.attribute_modifiers:
                self.attribute_modifiers[slot] = {}
            self.attribute_modifiers[slot][modifier] = value
            self.attribute_modifier_var.set("Select Modifier")
            self.attribute_modifier_value_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Attribute Modifier '{modifier}' with value {value} added to {slot}.")
            self.update_config_if_changed()
        else:
            messagebox.showerror("Error", "Please select a valid modifier and enter a numeric value.")

    def is_valid_number(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def get_current_state(self):
        return {
            "type": self.type_var.get(),
            "item_id": self.item_id_entry.get(),
            "display_name": self.display_name_entry.get(),
            "lore": self.lore_list,
            "material": self.material_entry.get(),
            "texture": self.texture_entry.get(),
            "model": self.model_entry.get().strip(),
            "enchants": self.enchants,
            "custom_enchants": self.custom_enchant_entry.get(),
            "unbreakable": self.unbreakable_var.get(),
            "max_custom_durability": self.durability_entry.get(),
            "custom_durability": self.custom_durability_entry.get(),
            "disappear_when_broken": self.disappear_when_broken_var.get(),
            "armor_slot": self.armor_slot_var.get() if self.type_var.get() == "Armor" else "",
            "armor_value": self.armor_value_entry.get() if self.type_var.get() == "Armor" else "",
            "armor_toughness": self.armor_toughness_entry.get() if self.type_var.get() == "Armor" else "",
            "attribute_modifiers": self.attribute_modifiers,
        }

    def update_type(self, *args):
        if self.type_var.get() == "Armor":
            self.armor_properties_frame.grid(row=19, columnspan=2, padx=10, pady=10)
        else:
            self.armor_properties_frame.grid_forget()

    def update_config_if_changed(self):
        current_state = str(self.get_current_state())
        if current_state != self.previous_state:
            self.previous_state = current_state
            self.create_config()

    def create_config(self):
        item_id = self.item_id_entry.get()
        display_name = self.display_name_entry.get()
        lore = self.lore_list
        material = self.material_entry.get()
        texture = self.texture_entry.get().strip()
        model = self.model_entry.get().strip()
        max_custom_durability = self.durability_entry.get()
        custom_durability = self.custom_durability_entry.get()
        disappear_when_broken = self.disappear_when_broken_var.get()

        lore_config = '\n'.join([f'      - \'{line.strip()}\'' for line in lore])
        enchants_config = '\n'.join([f'      - {enchant}' for enchant in self.enchants])

        unbreakable = self.unbreakable_var.get()
        durability_config = f"      max_custom_durability: {max_custom_durability}\n      custom_durability: {custom_durability}\n      disappear_when_broken: {str(disappear_when_broken).lower()}" if max_custom_durability.isdigit() else f"      disappear_when_broken: {str(disappear_when_broken).lower()}"

        attribute_modifiers_config = '\n'.join([f'        {slot}:\n' + '\n'.join([f'          {mod}: {val}' for mod, val in mods.items()]) for slot, mods in self.attribute_modifiers.items()])

        config = f'''{item_id}:
    display_name: "{display_name}"
    lore:
{lore_config}
    resource:
      material: {material}
      generate: {'false' if model else 'true'}'''

        if model:
            config += f'\n      model_path: "{model}"'
        else:
            config += f'\n      textures:\n      - {texture}'

        config += f'''
    enchants:
{enchants_config}
    durability:
      unbreakable: {str(unbreakable).lower()}
{durability_config}'''

        if self.type_var.get() == "Armor":
            armor_slot = self.armor_slot_var.get()
            armor_value = self.armor_value_entry.get()
            armor_toughness = self.armor_toughness_entry.get()
            armor_properties = f'''    specific_properties:
      armor:
        slot: {armor_slot}
    attribute_modifiers:
        {armor_slot}:
          armor: {armor_value}
          armorToughness: {armor_toughness}'''
            config += f'\n{armor_properties}'

        if self.attribute_modifiers:
            config += f'\n    attribute_modifiers:\n{attribute_modifiers_config}'

        self.config_text.delete(1.0, tk.END)  # Clear the text widget
        self.config_text.insert(tk.END, config)  # Insert the new config

        with open("config.yml", "w") as file:
            file.write(config)

    def open_color_codes(self):
        webbrowser.open("https://www.digminecraft.com/lists/color_list_pc.php")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigApp(root)
    root.mainloop()