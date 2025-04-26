import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from main import generate_password_with_details


def ascii_to_dna_length(ascii_length):
    total_bits = ascii_length * 8
    dna_length = total_bits // 2
    return dna_length


def generate_password():
    ascii_length = password_length_slider.get()
    dna_length = ascii_to_dna_length(ascii_length)
    print(dna_length / 4)
    password, details = generate_password_with_details(dna_length)
    password_var.set(password)
    details_text.delete("1.0", tk.END)
    details_text.insert(tk.END, details)


def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(password_var.get())
    messagebox.showinfo("Skopiowano", "Hasło zostało skopiowane do schowka.")


def toggle_details():
    if details_container.winfo_ismapped():
        details_container.pack_forget()
        toggle_button.config(text="Pokaż szczegóły")
    else:
        details_container.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        toggle_button.config(text="Ukryj szczegóły")


def save_details_as_txt():
    history = details_text.get("1.0", tk.END)
    file = asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file:
        with open(file, "w", encoding="utf-8") as f:
            f.write(history)
        messagebox.showinfo("Zapisano", "Szczegóły zostały zapisane.")


root = tk.Tk()
root.title("Bio-inspirowany Generator Haseł")
root.geometry("900x700")
root.minsize(900, 900)

font_label = ("Helvetica", 16)
font_button = ("Helvetica", 14)

tk.Label(root, text="Kliknij, aby wygenerować SILNE hasło:", font=font_label).pack(pady=20)
tk.Label(root, text="Długość hasła:", font=font_label).pack(pady=5)
password_length_slider = tk.Scale(root, from_=8, to_=32, orient=tk.HORIZONTAL, font=font_label)
password_length_slider.set(8)
password_length_slider.pack(pady=10)

tk.Button(root, text="Generuj hasło", font=font_button, command=generate_password, height=2, width=25).pack(pady=5)

password_var = tk.StringVar()
tk.Entry(root, textvariable=password_var, font=font_label, justify='center', width=32).pack(pady=10)

tk.Button(root, text="Kopiuj do schowka", font=font_button, command=copy_to_clipboard, height=2, width=25).pack(pady=5)

toggle_button = tk.Button(root, text="Pokaż szczegóły", font=font_button, command=toggle_details, height=2, width=25)
toggle_button.pack(pady=5)

details_container = tk.Frame(root)

details_frame = tk.Frame(details_container)
details_text = tk.Text(details_frame, font=("Courier", 12), wrap="word", height=12)
details_scroll = tk.Scrollbar(details_frame, command=details_text.yview)
details_text.config(yscrollcommand=details_scroll.set)

details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
details_scroll.pack(side=tk.RIGHT, fill=tk.Y)
details_frame.pack(fill=tk.BOTH, expand=True)

save_button = tk.Button(details_container, text="Zapisz szczegóły jako TXT", font=font_button,
                        command=save_details_as_txt, height=2, width=30)
save_button.pack(pady=10)

root.mainloop()
