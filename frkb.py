import tkinter as tk
from PIL import Image, ImageTk

class ColorPickerApp:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("Color Picker")

        # Görüntü dosya yolunu kaydet
        self.image_path = image_path
        
        self.image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.image)

        # Canvas oluştur ve görüntüyü yerleştir
        self.canvas = tk.Canvas(root, width=self.image.width, height=self.image.height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Seçilen noktanın bilgilerini gösterecek etiketi oluştur
        self.label = tk.Label(root, text="", anchor=tk.W, font=("Helvetica", 20))
        self.label.pack()

        # Seçilen noktaların bilgilerini tutacak liste
        self.selected_points = []  
        self.point_counter = 1

        # Canvas'a tıklama ve fare hareketi olaylarını bağla
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_mouse_motion)

        # Kaydırma çubuklarını içeren pencere oluştur
        self.selected_points_window = tk.Toplevel(self.root)
        self.selected_points_window.title("Seçilen Noktalar")

        # Canvas ve scrollbar'ı pencereye ekle
        self.selected_points_canvas = tk.Canvas(self.selected_points_window, width=400, height=300)
        self.selected_points_scrollbar = tk.Scrollbar(self.selected_points_window, orient="vertical", command=self.selected_points_canvas.yview)
        self.selected_points_canvas.configure(yscrollcommand=self.selected_points_scrollbar.set)
        self.selected_points_scrollbar.pack(side="right", fill="y")
        self.selected_points_canvas.pack(side="left", fill="both", expand=True)

        # Seçilen noktaların bilgilerini listeleyecek etiketleri tutacak frame
        self.selected_points_frame = tk.Frame(self.selected_points_canvas)
        self.selected_points_canvas.create_window((0, 0), window=self.selected_points_frame, anchor="nw")

    def on_canvas_click(self, event):
        x = event.x
        y = event.y

        # Tıklanan Piksel'in rengini al
        pixel_color = self.get_pixel_color(x, y)

        if pixel_color is not None:
            # Pixel rengini hex formatına dönüştür
            hex_color = "#{:02x}{:02x}{:02x}".format(*pixel_color)
            # Kontrol
            print(f"Seçilen konumdaki renk (Hex): {hex_color}")
        else:
            # Kontrol
            print("Renk alınamadı.")

        # İşaretlenen noktayı kırmızı bir daire ile göster
        self.show_selected_point(x, y)

        # Seçilen noktanın bilgilerini listeye ve pencereye ekleyin
        self.add_point_info(x, y, hex_color)

    def on_mouse_motion(self, event):
        x = event.x
        y = event.y

        # Fare konumundaki pikselin rengini al
        pixel_color = self.get_pixel_color(x, y)

        if pixel_color is not None:
            # Piksel rengini hex formatında görüntüle
            hex_color = "#{:02x}{:02x}{:02x}".format(*pixel_color)
            info_text = f"X: {x}, Y: {y}\nRenk: {hex_color}"
            self.label.config(text=info_text)
        else:
            self.label.config(text=f"X: {x}, Y: {y}\nRenk alınamadı.")

    def get_pixel_color(self, x, y):
        # Verilen konumdaki piksel rengini alın
        try:
            pixel_color = self.image.getpixel((x, y))
            return pixel_color
        except Exception as e:
            print(f"Hata: {e}")
            return None

    def show_selected_point(self, x, y):
        # Yeni noktayı işaretle
        point_id = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="red", width=2)

        # Noktanın yanına sıra numarasını ve rengini yaz
        label_text = f"{self.point_counter}"
        label_id = self.canvas.create_text(x + 10, y, text=label_text, anchor=tk.W, font=("Helvetica", 12), fill="red")

        # Seçilen noktanın bilgilerini listeye ekle
        self.selected_points.append({"X": x, "Y": y, "Renk": f"#{point_id} ({label_id})"})

        # Pencereye ekledikten sonra sayacı arttır
        self.point_counter += 1

    def add_point_info(self, x, y, hex_color):
        # Seçilen noktanın bilgilerini pencereye ekleyin
        point_info_text = f"{self.point_counter - 1}. X: {x}, Y: {y}, Renk: {hex_color}"
        tk.Label(self.selected_points_frame, text=point_info_text, font=("Helvetica", 14)).pack(pady=5)

        # Canvas boyutunu güncelle ve scrollbar'ı ayarla
        self.selected_points_canvas.update_idletasks()
        self.selected_points_canvas.config(scrollregion=self.selected_points_canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()

    # Görüntü dosyasının yolu
    image_path = "cat.jpg"  # Değişmesi gereken yer "burasıdır." uzantısını eklemeyi de unutmayın lütfen!

    app = ColorPickerApp(root, image_path)

    root.mainloop()
