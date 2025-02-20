import heapq
from collections import Counter
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk
import numpy as np

class HuffmanNode:
    def __init__(self, value, freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq_map):
    heap = []
    for value, freq in freq_map.items():
        heapq.heappush(heap, HuffmanNode(value, freq))

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heapq.heappop(heap)

def generate_codes(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}
    if node is not None:
        if node.value is not None:
            code_map[node.value] = prefix
        generate_codes(node.left, prefix + "0", code_map)
        generate_codes(node.right, prefix + "1", code_map)
    return code_map

def compress_image(image_array, code_map):
    compressed_data = ""
    for row in image_array:
        for pixel in row:
            compressed_data += code_map[pixel]
    return compressed_data

def main_gui():
    def on_compress():
        global gray_image_array
        if gray_image_array is None:
            messagebox.showwarning("Advertencia", "No hay imagen cargada para comprimir.")
            return

        freq_map = Counter(gray_image_array.flatten())
        huffman_tree = build_huffman_tree(freq_map)
        code_map = generate_codes(huffman_tree)
        compressed_data = compress_image(gray_image_array, code_map)
        compressed_text.delete("1.0", tk.END)
        compressed_text.insert(tk.END, compressed_data)

        original_size = gray_image_array.size * 8
        compressed_size = len(compressed_data)
        tasa_de_compresion = (compressed_size / original_size) * 100

        label_stats.config(
            text=f"Tamaño original: {original_size} bits\n"
                 f"Tamaño comprimido: {compressed_size} bits\n"
                 f"Tasa de compresión: {tasa_de_compresion:.2f}%"
        )

    def process_image(image):
        """Procesa la imagen: la redimensiona y convierte a escala de grises si es necesario"""
        image.thumbnail((150, 150))  # Redimensionar para visualización
        
        if image.mode == "L":
            return image, np.array(image), "La imagen ya está en escala de grises."
        else:
            gray_image = image.convert("L")
            return gray_image, np.array(gray_image), "Imagen convertida automáticamente a escala de grises."

    def on_load_image():
        global color_image, gray_image_array
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            try:
                # Cargar la imagen original
                color_image = Image.open(file_path)
                
                # Procesar la imagen (convertir a grises si es necesario)
                gray_image, gray_image_array, message = process_image(color_image)
                
                # Mostrar imagen original
                color_image_tk = ImageTk.PhotoImage(color_image)
                label_original_image.config(image=color_image_tk)
                label_original_image.image = color_image_tk
                
                # Mostrar imagen en escala de grises
                gray_image_tk = ImageTk.PhotoImage(gray_image)
                label_grayscale_image.config(image=gray_image_tk)
                label_grayscale_image.image = gray_image_tk
                
                # Mostrar mensaje informativo
                messagebox.showinfo("Información", message)
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar la imagen: {str(e)}")

    def on_clear():
        global color_image, gray_image_array
        color_image = None
        gray_image_array = None
        label_original_image.config(image="")
        label_grayscale_image.config(image="")
        compressed_text.delete("1.0", tk.END)
        label_stats.config(text="")

    # Crear la ventana principal con scroll
    root = tk.Tk()
    root.title("Compresión de Imágenes con Huffman")
    
    # Crear un canvas con scrollbar
    main_canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
    scrollable_frame = ttk.Frame(main_canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
    )

    main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    main_canvas.configure(yscrollcommand=scrollbar.set)

    # Variables globales para mantener referencias a las imágenes
    color_image = None
    gray_image_array = None

    # Frame principal con padding
    frame_main = ttk.Frame(scrollable_frame, padding="10")
    frame_main.pack(expand=True, fill="both")

    # Contenedor para las imágenes
    images_frame = ttk.Frame(frame_main)
    images_frame.pack(pady=10)

    # Frame para imagen original
    original_frame = ttk.LabelFrame(images_frame, text="Imagen Original", padding="5")
    original_frame.pack(side="left", padx=5)
    label_original_image = ttk.Label(original_frame)
    label_original_image.pack()

    # Frame para imagen en escala de grises
    grayscale_frame = ttk.LabelFrame(images_frame, text="Escala de Grises", padding="5")
    grayscale_frame.pack(side="left", padx=5)
    label_grayscale_image = ttk.Label(grayscale_frame)
    label_grayscale_image.pack()

    # Botones
    buttons_frame = ttk.Frame(frame_main)
    buttons_frame.pack(pady=10)
    
    ttk.Button(buttons_frame, text="Cargar Imagen", command=on_load_image).pack(side="left", padx=5)
    ttk.Button(buttons_frame, text="Comprimir", command=on_compress).pack(side="left", padx=5)
    ttk.Button(buttons_frame, text="Limpiar", command=on_clear).pack(side="left", padx=5)

    # Frame para datos comprimidos
    compressed_frame = ttk.LabelFrame(frame_main, text="Datos comprimidos (binario)", padding="5")
    compressed_frame.pack(fill="x", pady=10)
    compressed_text = tk.Text(compressed_frame, height=6, width=50)
    compressed_text.pack(padx=5, pady=5)

    # Estadísticas
    stats_frame = ttk.LabelFrame(frame_main, text="Estadísticas", padding="5")
    stats_frame.pack(fill="x", pady=10)
    label_stats = ttk.Label(stats_frame, text="")
    label_stats.pack(padx=5, pady=5)

    # Configurar el layout para el scroll
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    main_canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Tamaño inicial de la ventana
    root.geometry("800x600")
    
    root.mainloop()

if __name__ == "__main__":
    main_gui()