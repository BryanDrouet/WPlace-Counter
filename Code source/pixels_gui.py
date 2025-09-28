import tkinter as tk
from tkinter import messagebox
import json
import os, sys

DB_FILE = "data.json"

# ----- Fonctions pour PyInstaller -----
def resource_path(relative_path):
    """ Récupère le chemin absolu du fichier, compatible PyInstaller """
    if hasattr(sys, '_MEIPASS'):  # quand lancé depuis un .exe
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"history": []}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ----- Calcul et affichage -----
def calculer():
    try:
        pixels = int(entry.get())
        if pixels <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erreur", "Merci d'entrer un nombre entier positif.")
        return

    data = load_data()
    history = data["history"]

    total_seconds = pixels * 30
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    result = f"{pixels} pixels * 30 secondes = {total_seconds} sec\n"
    result += f"Converti : {hours}h {minutes}min {seconds}s\n"

    if history:
        last_pixels = history[-1]["pixels"]
        diff = pixels - last_pixels
        if diff > 0:
            result += f"📈 Augmentation de {diff} pixels (dernier : {last_pixels})"
        elif diff < 0:
            result += f"📉 Diminution de {-diff} pixels (dernier : {last_pixels})"
        else:
            result += f"➖ Pas de changement (dernier : {last_pixels})"
    else:
        result += "✅ Premier enregistrement"

    # Sauvegarde
    history.append({"pixels": pixels, "total_seconds": total_seconds})
    save_data(data)

    # Mettre à jour l'affichage du dernier
    if last_label:
        last_label.config(text=f"Dernier max pixels : {pixels} → Temps : {hours}h {minutes}min {seconds}s")

    messagebox.showinfo("Résultat", result)

# ----- Interface -----
root = tk.Tk()
root.title("Calcul Pixels")
root.geometry("450x250")

# Charger icône
icon_path = resource_path("icon.ico")
try:
    root.iconbitmap(icon_path)
except Exception as e:
    print("Impossible de charger l'icone :", e)

# Dernière entrée
data = load_data()
history = data["history"]
last_text = ""
if history:
    last = history[-1]
    h = last["total_seconds"] // 3600
    m = (last["total_seconds"] % 3600) // 60
    s = last["total_seconds"] % 60
    last_text = f"Dernier max pixels : {last['pixels']} → Temps : {h}h {m}min {s}s"

last_label = tk.Label(root, text=last_text, font=("Arial", 12), fg="#ff3838")
last_label.pack(pady=10)

# Question et entrée
label = tk.Label(root, text="Combien de pixels maximum peux-tu poser d'un coup ?", font=("Arial", 12))
label.pack(pady=5)

entry = tk.Entry(root, font=("Arial", 14), justify="center")
entry.pack(pady=5)

btn = tk.Button(root, text="Calculer", command=calculer, font=("Arial", 12))
btn.pack(pady=20)

root.mainloop()
