import customtkinter as ctk
import math
import os
from typing import Dict, List
from PIL import Image
from OOP import *  # Import semua kelas dari OOP.py

class GeometryCalculator:
    def __init__(self):
        self.icon_path = "icons"
        self.shape_path = "images"
        self.rumus_path = "rumus"
        self.theme = "light"

        self.setup_window()
        self.setup_variables()
        self.create_frames()
        self.create_content()
        self.create_menu()
        self.setup_grid()
        self.app.mainloop()

    def setup_window(self):
        """Initialize main window settings"""
        ctk.set_appearance_mode(self.theme)
        ctk.set_default_color_theme("custom-theme.json")
        self.app = ctk.CTk()
        self.app.title("GEOCAL")
        self.app.geometry("1000x550")

    def setup_variables(self):
        """Initialize variables and constants"""
        self.selection_type = ctk.StringVar(value="Bangun Datar")
        self.entries: Dict[str, ctk.CTkEntry] = {}
        
        # Definisi input fields untuk setiap bangun
        self.input_fields_map = {
            # Bangun Datar
            "Persegi": ["sisi"],
            "Persegi panjang": ["panjang", "lebar"],
            "Segitiga": ["alas", "tinggi", "sisi"],
            "Lingkaran": ["jari_jari"],
            "Jajar Genjang": ["alas", "sisi_miring", "tinggi"],
            "Trapesium": ["sisi_atas", "sisi_bawah", "sisi_kiri", "sisi_kanan", "tinggi"],
            "Belah Ketupat": ["diagonal1", "diagonal2", "sisi"],
            "Layang-Layang": ["diagonal1", "diagonal2", "sisi1", "sisi2"],
            
            # Bangun Ruang
            "Kubus": ["sisi"],
            "Balok": ["panjang", "lebar", "tinggi"],
            "Limas Segiempat": ["sisi_alas", "tinggi"],
            "Limas Segitiga": ["alas", "tinggi_alas", "tinggi"],
            "Prisma Segitiga": ["alas", "tinggi_alas", "tinggi_prisma", "jumlah_sisi_alas"],
            "Tabung": ["jari_jari", "tinggi"],
            "Kerucut": ["jari_jari", "tinggi"],
            "Bola": ["jari_jari"]
        }

        # Map nama bangun ke kelas
        self.shape_class_map = {
            "Persegi": Persegi,
            "Persegi panjang": PersegiPanjang,
            "Segitiga": Segitiga,
            "Lingkaran": Lingkaran,
            "Jajar Genjang": JajarGenjang,
            "Trapesium": Trapesium,
            "Belah Ketupat": BelahKetupat,
            "Layang-Layang": LayangLayang,
            "Kubus": Kubus,
            "Balok": Balok,
            "Limas Segiempat": LimasSegiempat,
            "Limas Segitiga": LimasSegitiga,
            "Prisma Segitiga": Prisma,
            "Tabung": Tabung,
            "Kerucut": Kerucut,
            "Bola": Bola
        }

        self.bangun_datar = [
            "Persegi", "Persegi panjang", "Segitiga", "Lingkaran",
            "Jajar Genjang", "Trapesium", "Belah Ketupat", "Layang-Layang"
        ]
        self.bangun_ruang = [
            "Kubus", "Balok", "Limas Segiempat", "Limas Segitiga",
            "Prisma Segitiga", "Tabung", "Kerucut", "Bola"
        ]

        self.current_shape = None

    def create_frames(self):
        """Create main frames"""
        # Left menu frame
        self.frame_menu = ctk.CTkFrame(self.app, corner_radius=15)
        self.frame_menu.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)
        
        # Right content frame
        self.frame_content = ctk.CTkFrame(self.app, corner_radius=15)
        self.frame_content.grid(row=0, column=1, sticky="nswe", padx=(0, 20), pady=20)

        # Configure weights
        self.app.grid_columnconfigure(0, weight=0)
        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_rowconfigure(0, weight=1)

    def create_input_fields(self, shape_name: str):
        """Create dynamic input fields based on selected shape"""
        # Clear existing fields
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        self.entries.clear()

        # Get required fields for the shape
        fields = self.input_fields_map.get(shape_name, [])

        # Create new fields
        for field in fields:
            field_name = field.replace('_', ' ').title()
            entry = ctk.CTkEntry(self.input_frame, placeholder_text=field_name, height=30)
            entry.pack(pady=5, fill="x")
            self.entries[field] = entry

    def create_content(self):
        """Create right content panel"""
        # Title
        self.label_title = ctk.CTkLabel(
            self.frame_content,
            text="Pilih Bangun",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.label_title.pack(pady=(20, 15), anchor="center")

        # Separator line
        separator = ctk.CTkFrame(self.frame_content, height=2)
        separator.pack(fill="x", padx=20, pady=(0, 20))

        # Main content frame
        content_layout = ctk.CTkFrame(self.frame_content, fg_color="transparent")
        content_layout.pack(fill="both", expand=True, padx=20, pady=0)

        # Theme switch in top-right corner
        self.theme_switch = ctk.CTkSwitch(
            self.frame_content,
            text="",
            command=self.toggle_theme
        )
        self.theme_switch.place(relx=0.9, rely=0.06, anchor="w")  # Pojok kanan atas
        self.theme_switch.select()  # Default ke dark mode
        
        # Left side (Shape image)
        left_frame = ctk.CTkFrame(content_layout, corner_radius=15)
        left_frame.grid(row=0, column=0, sticky="nesw", pady=(5, 0), padx=0)
        
        # Ubah label menjadi container untuk gambar
        self.shape_image_label = ctk.CTkLabel(left_frame, text="")
        self.shape_image_label.grid(row=0, column=0, sticky="nesw", padx=(0, 10))
        
        # Right side (Input fields)
        self.input_frame = ctk.CTkFrame(content_layout, fg_color="transparent")
        self.input_frame.grid(row=0, column=1, sticky="ew", padx=(10, 0))

        # Bottom frame for results
        bottom_frame = ctk.CTkFrame(self.frame_content, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Result 1 displays
        self.result_frame1 = ctk.CTkFrame(bottom_frame, corner_radius=15)
        self.result_frame1.grid(row=0, column=0, sticky="ew", padx=(0, 0))
        
        self.formula_image1 = ctk.CTkLabel(self.result_frame1, text="")
        self.formula_image1.grid(row=0, column=0, columnspan=2, sticky="nesw", pady=(0, 20))

        self.result1_label = ctk.CTkLabel(self.result_frame1, text="          Luas       ", pady=10, text_color=["#517784", "white"])
        self.result1_label.grid(row=1, column=0, sticky="ew", padx=(0, 0))

        self.result1_entry = ctk.CTkEntry(self.result_frame1, height=30, width=210)
        self.result1_entry.grid(row=1, column=1, sticky="e", padx=0)

        # Result 2 displays
        self.result_frame2 = ctk.CTkFrame(bottom_frame, corner_radius=15)
        self.result_frame2.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        
        self.formula_image2 = ctk.CTkLabel(self.result_frame2, text="")
        self.formula_image2.grid(row=0, column=0, columnspan=2, sticky="nesw", pady=(0, 20))

        self.result2_label = ctk.CTkLabel(self.result_frame2, text="          Keliling     ", pady=10, text_color=["#517784", "white"])
        self.result2_label.grid(row=1, column=0, sticky="ew", padx=(0, 0))

        self.result2_entry = ctk.CTkEntry(self.result_frame2, height=30, width=210)
        self.result2_entry.grid(row=1, column=1, sticky="e", padx=0)
        
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=1)

        self.result_frame1.grid_columnconfigure(0, weight=1)
        self.result_frame1.grid_columnconfigure(1, weight=1)

        self.result_frame2.grid_columnconfigure(0, weight=1)
        self.result_frame2.grid_columnconfigure(1, weight=1)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.frame_content, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        calculate_btn = ctk.CTkButton(
            buttons_frame,
            text="Calculate",
            text_color="white",
            height=45,
            command=self.calculate_output
        )
        calculate_btn.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="Clear",
            text_color="white",
            height=45,
            command=self.clear_entries
        )
        clear_btn.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)

        # Configure grid weights for content layout
        content_layout.grid_columnconfigure(0, weight=0)
        content_layout.grid_columnconfigure(1, weight=1)
        content_layout.grid_rowconfigure(0, weight=0)

    def calculate_output(self):
        """Calculate measurements based on input values"""
        try:
            if not self.current_shape:
                return

            # Get values from entries
            values = {field: float(entry.get()) for field, entry in self.entries.items()}
            
            # Create instance of the shape
            shape_class = self.shape_class_map[self.current_shape]
            shape_instance = shape_class(**values)

            # Calculate results based on shape type
            if self.current_shape in self.bangun_datar:
                result1 = shape_instance.luas()
                result2 = shape_instance.keliling()
                self.result1_label.configure(text="          Luas       ")
                self.result2_label.configure(text="          Keliling     ")
            else:
                result1 = shape_instance.volume()
                result2 = shape_instance.luas_permukaan()
                self.result1_label.configure(text="        Volume         ")
                self.result2_label.configure(text="       L.Permukaan   ")

            # Update results
            self.result1_entry.delete(0, "end")
            self.result1_entry.insert(0, f"{result1:.2f}")
            self.result2_entry.delete(0, "end")
            self.result2_entry.insert(0, f"{result2:.2f}")

        except (ValueError, AttributeError) as e:
            self.result1_entry.delete(0, "end")
            self.result1_entry.insert(0, "Error")
            self.result2_entry.delete(0, "end")
            self.result2_entry.insert(0, "Error")

    def clear_entries(self):
        """Clear all input and output fields"""
        for entry in self.entries.values():
            entry.delete(0, "end")
        self.result1_entry.delete(0, "end")
        self.result2_entry.delete(0, "end")

    def update_bangun_list(self, *args):
        """Update shape list based on selected type"""
        for widget in self.frame_buttons.winfo_children():
            widget.destroy()

        bangun_list = self.bangun_datar if self.selection_type.get() == "Bangun Datar" else self.bangun_ruang

        for bangun in bangun_list:
            # Create frame to hold icon and text
            button_frame = ctk.CTkFrame(self.frame_buttons, fg_color="transparent")
            button_frame.pack(pady=5, padx=20, fill="x")

            try:
                # Load icon image
                icon_name = f"icon_{bangun.lower().replace(' ', '_')}_{self.theme}.png"
                icon_full_path = os.path.join(self.icon_path, icon_name)
                icon_image = Image.open(icon_full_path)
                icon = ctk.CTkImage(light_image=icon_image, dark_image=icon_image, size=(15, 15))
                
                # Create button with icon and text
                button = ctk.CTkButton(
                    button_frame,
                    text=bangun,
                    image=icon,
                    compound="left",  # Places icon on the left
                    anchor="w",  # Aligns text to the left
                    fg_color="transparent",
                    height=30,
                    command=lambda b=bangun: self.update_content(b)
                )
                button.pack(fill="x")
                
            except FileNotFoundError:
                # Fallback if icon is not found
                button = ctk.CTkButton(
                    button_frame,
                    text=bangun,
                    anchor="w",  # Aligns text to the left
                    fg_color="transparent",
                    height=30,
                    command=lambda b=bangun: self.update_content(b)
                )
                button.pack(fill="x")

    def update_content(self, bangun: str):
        """Update content when shape is selected"""
        self.current_shape = bangun
        self.label_title.configure(text=bangun)
        self.create_input_fields(bangun)
        
        try:
            # Load shape image (existing code)
            image_name = f"image_{bangun.lower().replace(' ', '_')}.png"
            image_full_path = os.path.join(self.shape_path, image_name)
            shape_image = Image.open(image_full_path)
            shape_ctk_image = ctk.CTkImage(light_image=shape_image, dark_image=shape_image, size=(325, 195))
            self.shape_image_label.configure(image=shape_ctk_image, text="")
            
            # Load formula images
            if bangun in self.bangun_datar:
                # Load luas formula image
                luas_image_name = f"luas_{bangun.lower().replace(' ', '_')}_{self.theme}.png"
                luas_image_path = os.path.join(self.rumus_path, luas_image_name)
                luas_image = Image.open(luas_image_path)
                luas_ctk_image = ctk.CTkImage(light_image=luas_image, dark_image=luas_image, size=(300, 60))
                self.formula_image1.configure(image=luas_ctk_image, text="")
                
                # Load keliling formula image
                keliling_image_name = f"keliling_{bangun.lower().replace(' ', '_')}_{self.theme}.png"
                keliling_image_path = os.path.join(self.rumus_path, keliling_image_name)
                keliling_image = Image.open(keliling_image_path)
                keliling_ctk_image = ctk.CTkImage(light_image=keliling_image, dark_image=keliling_image, size=(300, 60))
                self.formula_image2.configure(image=keliling_ctk_image, text="")
                
                self.result1_label.configure(text="          Luas       ")
                self.result2_label.configure(text="          Keliling     ")
            else:
                # Load volume formula image
                volume_image_name = f"volume_{bangun.lower().replace(' ', '_')}_{self.theme}.png"
                volume_image_path = os.path.join(self.rumus_path, volume_image_name)
                volume_image = Image.open(volume_image_path)
                volume_ctk_image = ctk.CTkImage(light_image=volume_image, dark_image=volume_image, size=(300, 60))
                self.formula_image1.configure(image=volume_ctk_image, text="")
                
                # Load luas permukaan formula image
                lp_image_name = f"lpermukaan_{bangun.lower().replace(' ', '_')}_{self.theme}.png"
                lp_image_path = os.path.join(self.rumus_path, lp_image_name)
                lp_image = Image.open(lp_image_path)
                lp_ctk_image = ctk.CTkImage(light_image=lp_image, dark_image=lp_image, size=(300, 60))
                self.formula_image2.configure(image=lp_ctk_image, text="")
                
                self.result1_label.configure(text="        Volume         ")
                self.result2_label.configure(text="       L.Permukaan   ")

        except FileNotFoundError:
            print("")  # For debugging

    def create_menu(self):
        """Create left menu panel"""
        # Title
        logo_path = os.path.join(self.icon_path, "geocal_logo.png")
        logo_image = Image.open(logo_path)
        # Adjust the size (width, height) as needed
        logo_ctk_image = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(200, 40))
        
        label_menu = ctk.CTkLabel(
            self.frame_menu,
            text="",  # Empty text
            image=logo_ctk_image
        )
        label_menu.pack(pady=(20, 15), )

        # Shape type selector
        self.combo_bangun = ctk.CTkComboBox(
            self.frame_menu,
            values=["Bangun Datar", "Bangun Ruang"],
            variable=self.selection_type,
            width=200,
            height=30
        )
        self.combo_bangun.pack(pady=(5, 15))
        self.selection_type.trace_add("write", self.update_bangun_list)

        # Separator line
        separator = ctk.CTkFrame(self.frame_menu, height=2)
        separator.pack(fill="x", padx=20, pady=5)

        # Buttons frame
        self.frame_buttons = ctk.CTkFrame(self.frame_menu, fg_color="transparent")
        self.frame_buttons.pack(pady=(0, 10), fill="both", expand=True)
        self.update_bangun_list()

    def toggle_theme(self):
        """Toggle between dark and light themes"""
        # Ubah tema
        if self.theme == "dark":
            self.theme = "light"
        else:
            self.theme = "dark"

        # Update mode tampilan
        ctk.set_appearance_mode(self.theme)

        # Perbarui ikon dan gambar rumus
        self.update_icons_and_formulas()

    def update_icons_and_formulas(self):
        """Update icons and formulas based on the current theme"""
        # Update ikon di menu
        self.update_bangun_list()

        # Update gambar rumus untuk bangun yang dipilih saat ini
        if self.current_shape:
            self.update_content(self.current_shape)

    def setup_grid(self):
        """Configure grid weights"""
        self.frame_menu.configure(width=250)

if __name__ == "__main__":
    GeometryCalculator()