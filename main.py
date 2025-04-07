import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

# Funkcja do obliczeń Monte Carlo (symulacja wartości pi)
def estimate_pi(num_samples, canvas, figure, alpha_points):
    x_vals = []
    y_vals = []
    inside_circle = 0

    for i in range(1, num_samples + 1):
        # Losowanie punktu w jednostkowym kwadracie (od 0 do 1)
        x, y = np.random.rand(2)
        distance = (x - 0.5)**2 + (y - 0.5)**2  # Dystans do środka koła o promieniu 0.5

        # Sprawdzenie, czy punkt leży w kole
        if distance <= 0.25:  # Równanie okręgu: (x - 0.5)^2 + (y - 0.5)^2 <= r^2
            inside_circle += 1
        x_vals.append(x)
        y_vals.append(y)
        
        # Aktualizacja wykresu w czasie rzeczywistym
        if i % (num_samples // 10) == 0:
            ax = figure.gca()
            ax.clear()
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            # Rysowanie pełnego koła z ciemniejszym kolorem i większym kontrastem
            ax.add_patch(plt.Circle((0.5, 0.5), 0.5, color='darkgray', alpha=0.5))  # Ciemniejsze koło
            ax.scatter(x_vals, y_vals, color='blue', s=1, alpha=alpha_points)  # Ustawienie przezroczystości punktów
            ax.set_title(f"Szacowanie wartości pi: {4 * inside_circle / i:.4f}")
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            canvas.draw()

# Funkcja, która uruchamia symulację w osobnym wątku
def run_simulation():
    num_samples = int(entry_samples.get())
    alpha_points = transparency_slider.get() / 100  # Pobieramy wartość przezroczystości z suwaka
    threading.Thread(target=estimate_pi, args=(num_samples, canvas, figure, alpha_points), daemon=True).start()

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Symulacja Monte Carlo")

# Tworzenie elementów GUI
label_samples = tk.Label(root, text="Liczba próbek:")
label_samples.pack(pady=10)

entry_samples = tk.Entry(root)
entry_samples.pack(pady=10)
entry_samples.insert(0, "10000")  # Domyślna wartość

run_button = tk.Button(root, text="Uruchom symulację", command=lambda: threading.Thread(target=run_simulation).start())
run_button.pack(pady=20)

# Suwak do zmiany przezroczystości punktów
label_transparency = tk.Label(root, text="Przezroczystość punktów:")
label_transparency.pack(pady=5)

transparency_slider = tk.Scale(root, from_=0, to_=100, orient="horizontal", length=300)
transparency_slider.set(50)  # Domyślnie 50% przezroczystości
transparency_slider.pack(pady=10)

# Ustawienia wykresu
figure = plt.Figure(figsize=(6, 6), dpi=100)
ax = figure.add_subplot(111)
ax.set_title("Symulacja Monte Carlo")
ax.set_xlabel('X')
ax.set_ylabel('Y')

# Tworzenie canvasu, na którym będzie wyświetlany wykres
canvas = FigureCanvasTkAgg(figure, master=root)
canvas.get_tk_widget().pack(pady=20)

# Uruchomienie aplikacji
root.mainloop()
