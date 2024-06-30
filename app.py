import os
import tkinter as tk
from tkinter import filedialog, messagebox
import imageio
import imageio.core.util

def split_dds(input_file, output_base_dir):
    try:
        img = imageio.imread(input_file)

        height, width, _ = img.shape

        part_size = 256

        if height % part_size != 0 or width % part_size != 0:
            raise ValueError("Размеры изображения должны быть кратны 256.")

        num_parts_vertical = height // part_size
        num_parts_horizontal = width // part_size
        num_parts = num_parts_vertical * num_parts_horizontal

        base_filename = os.path.splitext(os.path.basename(input_file))[0]
        output_dir = os.path.join(output_base_dir, base_filename)
        os.makedirs(output_dir, exist_ok=True)

        part_number = 1
        for i in range(num_parts_vertical):
            for j in range(num_parts_horizontal):
                top = i * part_size
                bottom = top + part_size
                left = j * part_size
                right = left + part_size

                part_img = img[top:bottom, left:right]

                part_filename = os.path.join(output_dir, f"{part_number}.dds")

                imageio.imwrite(part_filename, part_img, format='DDS')
                
                part_number += 1

        return True

    except Exception as e:
        messagebox.showerror("Ошибка", f"Неожиданная ошибка при обработке файла {input_file}:\n{e}")
        return False

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        entry.delete(0, tk.END)
        entry.insert(0, directory)

def start_splitting():
    directory = entry.get()
    if directory:
        dds_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith('.dds')]
        if not dds_files:
            messagebox.showwarning("Предупреждение", "В выбранной директории нет файлов DDS.")
            return

        parent_dir = os.path.dirname(directory)
        output_base_dir = os.path.join(parent_dir, "out")

        success_count = 0
        for dds_file in dds_files:
            if split_dds(dds_file, output_base_dir):
                success_count += 1

        messagebox.showinfo("Успех", f"Успешно обработано {success_count} файлов DDS.")
    else:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите директорию, содержащую файлы DDS для разделения.")

root = tk.Tk()
root.title("DDS Splitter")

icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Logo.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
else:
    messagebox.showwarning("Предупреждение", f"Иконка не найдена: {icon_path}")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

label = tk.Label(frame, text="Выберите директорию с DDS файлами для разделения:")
label.grid(row=0, column=0, sticky=tk.W)

entry = tk.Entry(frame, width=50)
entry.grid(row=0, column=1, padx=10)

browse_button = tk.Button(frame, text="Обзор", command=browse_directory)
browse_button.grid(row=0, column=2, padx=10)

split_button = tk.Button(frame, text="Разделить DDS", command=start_splitting)
split_button.grid(row=1, columnspan=3, pady=10)

root.mainloop()
