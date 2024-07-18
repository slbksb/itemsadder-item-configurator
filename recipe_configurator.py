import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk

class RecipeConfigurator:
    def __init__(self, root):
        self.root = root
        self.root.title("ItemsAdder Recipe Configurator")

        self.crafting_grid = [['' for _ in range(3)] for _ in range(3)]
        self.ingredients = {}
        self.create_widgets()

    def create_widgets(self):
        # Left frame for crafting grid and input
        left_frame = ttk.Frame(self.root)
        left_frame.grid(row=0, column=0, padx=10, pady=10)

        # Crafting grid
        self.entries = []
        for i in range(3):
            row_entries = []
            for j in range(3):
                entry = ttk.Entry(left_frame, width=10)
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.bind("<KeyRelease>", self.update_display)  # Update on key release
                row_entries.append(entry)
            self.entries.append(row_entries)
        
        # Custom item result entry
        tk.Label(left_frame, text="Custom Item Result:").grid(row=3, column=0, pady=10, columnspan=3)
        self.result_entry = ttk.Entry(left_frame, width=20)
        self.result_entry.grid(row=4, column=0, pady=10, columnspan=3)
        self.result_entry.bind("<KeyRelease>", self.update_display)  # Update on key release

        # Copy button
        copy_button = ttk.Button(left_frame, text="Copy Config", command=self.copy_config)
        copy_button.grid(row=5, column=0, columnspan=3, pady=10)

        # Right frame for config display
        right_frame = ttk.Frame(self.root)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')

        # Config display
        self.config_display = tk.Text(right_frame, width=40, height=20, wrap='word')
        self.config_display.grid(row=0, column=0, padx=5, pady=5)
        self.config_display.config(state=tk.DISABLED)

    def copy_config(self):
        self.extract_crafting_grid()
        custom_item = self.result_entry.get().strip()
        if not custom_item:
            messagebox.showerror("Error", "Custom item result cannot be empty!")
            return

        ingredients, pattern = self.construct_ingredients_and_pattern()
        config = self.construct_config(custom_item, ingredients, pattern)

        self.root.clipboard_clear()
        self.root.clipboard_append(f"    {self.get_item_name(custom_item)}:\n{config}")
        messagebox.showinfo("Success", "Config copied to clipboard!")

    def extract_crafting_grid(self):
        for i in range(3):
            for j in range(3):
                self.crafting_grid[i][j] = self.entries[i][j].get().strip()

    def construct_ingredients_and_pattern(self):
        ingredients = {}
        pattern = []
        current_letter = ord('B')  # Start from 'B'
        
        for row in self.crafting_grid:
            pattern_row = ''
            for item in row:
                if item:
                    if item not in ingredients:
                        if current_letter > ord('Z'):
                            messagebox.showerror("Error", "Too many unique items in the recipe.")
                            return None, None
                        ingredients[item] = chr(current_letter)
                        current_letter += 1
                    pattern_row += ingredients[item]
                else:
                    pattern_row += 'X'
            pattern.append(pattern_row)
        return ingredients, pattern

    def construct_config(self, custom_item, ingredients, pattern):
        ingredients_config = "\n".join([f"        {value}: {key}" for key, value in ingredients.items()])
        pattern_config = "\n".join([f"      - {row}" for row in pattern])
        config = f"""      permission: rangemc.crafting
      enabled: true
      pattern:
{pattern_config}
      ingredients:
{ingredients_config}
      result:
        item: {custom_item}
        amount: 1"""
        return config

    def get_item_name(self, custom_item):
        if ":" in custom_item:
            return custom_item.split(":")[1]
        return custom_item

    def update_display(self, event=None):
        self.extract_crafting_grid()
        custom_item = self.result_entry.get().strip()
        ingredients, pattern = self.construct_ingredients_and_pattern()
        if ingredients is None or pattern is None:
            return  # Stop update if there is an error
        config = self.construct_config(custom_item, ingredients, pattern)
        
        self.config_display.config(state=tk.NORMAL)
        self.config_display.delete(1.0, tk.END)
        self.config_display.insert(tk.END, f"    {self.get_item_name(custom_item)}:\n{config}")
        self.config_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeConfigurator(root)
    root.mainloop()