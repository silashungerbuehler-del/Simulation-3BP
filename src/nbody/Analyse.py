# In dieser Datei wird die Plots für die Erhaltungsgrössen definiert
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from ipywidgets import interact, IntSlider, Play, jslink, HBox, IntSlider, interactive_output
from IPython.display import display

# Die definierten Funktionen aus Dynamik.py importieren
from nbody.Dynamik import split_condition, calculate_center_of_mass, calculate_total_angular_momentum, calculate_total_energy, calculate_total_momentum

# --- Funktion für die Statische visualisierung der Simulation ---
# Aus Dynamik ist hier split_condition und calculate_center_of_mass relevant

def create_plot(y, m):
    # Die Daten Variablen zuweisen und entpacken
    N, r, v = split_condition(y, m) # r hat die Form (N, 3, T)
    R_CM = calculate_center_of_mass(y, m) # R_CM hat die Form (3, T)

    # figure (Fenster) und axis (3D Koordinatensystem) erstellen
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection="3d")

    # Den max. Abstand der Körper vom Nullpunkt berechnen und mit einem Puffer verhindern, dass sich einer aus dem Frame bewegt
    buffer = 0.2 # 20% Puffer am Rand
    max_val = np.max(np.abs(r)) * (1 + buffer)
    
    # Die Grenzen festlegen dafür vorher max_val def. 
    ax.set_xlim(-max_val, max_val)
    ax.set_ylim(-max_val, max_val)
    ax.set_zlim(-max_val, max_val)

    # Die Achsen benennen und einen Titel setzen
    ax.set_xlabel("X-Achse")
    ax.set_ylabel("Y-Achse")
    ax.set_zlabel("Z-Achse")
    ax.set_title(f"{N}-Körper-Simulation")

    # Die Farben für die Körper definieren
    colors = plt.cm.viridis(np.linspace(0, 1, N)) #plt.cm.jet() ruft die Farbpalette auf und linspace erstellt einen Array mit N Werten zwischen 0 und 1 welche alle den gleichen Abstand haben

    # Die Körper zeichnen:
    for i in range(N):
        # Die Startpunkte in den Plot zeichnen, t=0 und Verblasst zeichnen --> alpha=Deckkraft
        ax.scatter(r[i, 0, 0], r[i, 1, 0], r[i, 2, 0],color=colors[i], alpha=0.6, marker="o", s=40, label=f"Start Körper {i+1}")
        # Die Bahnen zeichnen (Trajektorie)
        ax.plot(r[i, 0, :], r[i, 1, :], r[i, 2, :], color=colors[i], lw=1.5, label=f"Körper {i+1}", alpha=0.6)
        # Die Endpunkte zeichnen
        ax.scatter(r[i, 0, -1], r[i, 1, -1], r[i, 2, -1], color=colors[i], s=80, edgecolors="black")

    # Das Baryzentrum zeichnen
    # Den Startpunkt edes Baryzentrums (CM) zeichnen
    ax.scatter(R_CM[0, 0], R_CM[1, 0], R_CM[2, 0], color="black", alpha=0.6, marker="x", s=60, label="Start Baryzentrum")
    # Trajektorie des CM
    ax.plot(R_CM[0, :], R_CM[1, :], R_CM[2, :], color="black", linestyle="--", lw=1, label="Baryzentrum")
    # Endpunkt CM
    ax.scatter(R_CM[0, -1], R_CM[1, -1], R_CM[2, -1], color="black", marker="x", s=80)

    # Die Legende einblenden
    ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1.0))

    return fig

# --- Funktionen für die Animation um Simulation zu visualisieren ---
# Aus Dynamik ist hier split_condition und calculate_center_of_mass relevant

def create_animation(y, m, interval, step): 
    # Parameter: 
    #   y ist der sol.y Teil, der der Integrator zurück gibt --> 2D-Array (6N, T), enthält r und v
    #   m enthält die Massen der N Körper --> 1D-Array
    #   intervall gibt die Zeit in Millisekunden zwischen den Frames an --> Wiedergabegeschwindigkeit
    #   step führt dazu wie viele Zeitschritte zwischen jedem rendern übersprungen werden sollen --> Auch für Wiedergabegeschwindikeit relevant

    # Die Daten Variablen zuweisen und entpacken
    N, r, v = split_condition(y, m) # r hat die Form (N, 3, T)
    R_CM = calculate_center_of_mass(y, m) # R_CM hat die Form (3, T)

    # T_steps ist die Gesamtzahl der berechneten Zeitpunkte in der Sim
    T_steps = r.shape[2] # greift auf die Anzahl Einträge in r zu, also T

    # Eine Liste erstellen, der Frames die gerendert werden sollen --> Schnellere Wiedergabegeschwindigkeit
    frame_indices = range(0, T_steps, step)

    # figure (Fenster) und axis (3D Koordinatensystem) erstellen
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection="3d")

    # Den max. Abstand der Körper vom Nullpunkt berechnen und mit einem Puffer verhindern, dass sich einer aus dem Frame bewegt
    buffer = 0.2 # 20% Puffer am Rand
    max_val = np.max(np.abs(r)) * (1 + buffer)

    # Die Grenzen festlegen dafür vorher max_val def. 
    ax.set_xlim(-max_val, max_val)
    ax.set_ylim(-max_val, max_val)
    ax.set_zlim(-max_val, max_val)

    # Die Achsen benennen und einen Titel setzen
    ax.set_xlabel("X-Achse")
    ax.set_ylabel("Y-Achse")
    ax.set_zlabel("Z-Achse")
    ax.set_title(f"{N}-Körper-Simulation")

    # Die Farben definieren
    colors = plt.cm.viridis(np.linspace(0, 1, N)) # gleich wie bei statischer visual.
    # Die Startpunkte in den Plot zeichnen, t=0 und Verblasst zeichnen --> alpha=Deckkraft
    for i in range(N):
        ax.scatter(r[i, 0, 0], r[i, 1, 0], r[i, 2, 0], color=colors[i], alpha=0.6, marker="o", s=40, label=f"Start Körper {i+1}")
        
    # Den Startpunkt edes Baryzentrums (CM) zeichnen
    ax.scatter(R_CM[0, 0], R_CM[1, 0], R_CM[2, 0], color="black", alpha=0.6, marker="x", s=60, label="Start Baryzentrum")

    # Platzhalter für Anim. erstellen

    lines = [] # Liste für die Trajektorien 
    points = [] #Liste für die aktuellen Positionen

    # Platzhalter für die N Körper erstellen
    for i in range(N):
        # Leere Linie initialisieren (das Komma entpackt das Plot-Objekt)
        line, = ax.plot([], [], [], color=colors[i], lw=1.5, label=f"Körper {i+1}", alpha=0.4)
        lines.append(line)

        # Leere Punkte initialisieren
        point, = ax.plot([], [], [], marker="o", color=colors[i], ms=8)
        points.append(point)

    # Platzhalter fürs Baryzentrum erstellen
    cm_line, = ax.plot([], [], [], color="black", linestyle="--", lw=1)
    cm_point, = ax.plot([], [], [], marker="x", color="black", ms=10)

    # Die Legende einblenden
    ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1.0))

    # Update definieren; Aktualisiert zu jedem frame die Grafik
    def update(frame):
        # Alle N Körper updaten
        for i in range(N):
            # Trajektorie bis zum jetzigen frame übergeben
            lines[i].set_data(r[i, 0, :frame], r[i, 1, :frame])
            lines[i].set_3d_properties(r[i, 2, :frame])

            # Aktuelle Position nur bei aktuellem frame übergeben
            # Daten müssen für .set_data in Listen verpackt werden.
            points[i].set_data([r[i, 0, frame]], [r[i, 1, frame]])
            points[i].set_3d_properties([r[i, 2, frame]])

        # Das Baryzentrum berechnen
        cm_line.set_data(R_CM[0, :frame], R_CM[1, :frame])
        cm_line.set_3d_properties(R_CM[2, :frame])

        cm_point.set_data([R_CM[0, frame]], [R_CM[1, frame]])
        cm_point.set_3d_properties([R_CM[2, frame]])

        # Die Liste aller veränderten Objekte zurück
        return lines + points + [cm_line, cm_point]

    # Animation laufen lassen
    anim = FuncAnimation(
        fig, 
        update, 
        frames=frame_indices, 
        interval=interval, 
        blit=False,
        repeat=False
    )
    
    return anim, fig

# Hier so definiert, dass man mit dem Schieberegler die Animation spulen kann
def create_scrubber(y, m, step, interval):
    # Parameter:
    #   y ist der sol.y Teil, der der Integrator zurückgibt --> 2D-Array (6N, T), enthält r und v
    #   m enthält die Massen der N Körper --> 1D-Array
    #   step gibt vor, in welchen Schritten der Schieberegler den Zeitindex bewegt
    #         (z.B. step=10 -> Regler bewegt sich in 10er-Schritten durch die Zeitpunkte)

    # Die Daten Variablen zuweisen und entpacken (gleiche Struktur wie in create_animation)
    N, r, v = split_condition(y, m)  # r hat die Form (N, 3, T)
    R_CM = calculate_center_of_mass(y, m)  # R_CM hat die Form (3, T)

    T_steps = r.shape[2]

    # figure (Fenster) und axis (3D Koordinatensystem) erstellen
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Gleiche Grenzenberechnung wie in create_animation, damit die Skalierung konsistent bleibt
    buffer = 0.2
    max_val = np.max(np.abs(r)) * (1 + buffer)
    ax.set_xlim(-max_val, max_val)
    ax.set_ylim(-max_val, max_val)
    ax.set_zlim(-max_val, max_val)

    ax.set_xlabel("X-Achse")
    ax.set_ylabel("Y-Achse")
    ax.set_zlabel("Z-Achse")
    ax.set_title(f"{N}-Körper-Simulation (Scrubber)")

    colors = plt.cm.viridis(np.linspace(0, 1, N))

    # Startpunkte verblasst einzeichnen, wie in create_animation
    for i in range(N):
        ax.scatter(r[i, 0, 0], r[i, 1, 0], r[i, 2, 0], color=colors[i], alpha=0.6, marker="o", s=40, label=f"Start Körper {i+1}")
    ax.scatter(R_CM[0, 0], R_CM[1, 0], R_CM[2, 0], color="black", alpha=0.6, marker="x", s=60, label="Start Baryzentrum")

    # Platzhalter für Trajektorien und aktuelle Positionen, gleiche Struktur wie in create_animation
    lines = []
    points = []
    for i in range(N):
        line, = ax.plot([], [], [], color=colors[i], lw=1.5, label=f"Körper {i+1}", alpha=0.4)
        lines.append(line)

        point, = ax.plot([], [], [], marker="o", color=colors[i], ms=8)
        points.append(point)

    cm_line, = ax.plot([], [], [], color="black", linestyle="--", lw=1)
    cm_point, = ax.plot([], [], [], marker="x", color="black", ms=10)

    ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1.0))

    # scrub() macht dasselbe wie update() in create_animation, wird aber vom
    # Schieberegler aufgerufen statt vom Animations-Timer
    def scrub(frame):
        for i in range(N):
            lines[i].set_data(r[i, 0, :frame], r[i, 1, :frame])
            lines[i].set_3d_properties(r[i, 2, :frame])

            points[i].set_data([r[i, 0, frame]], [r[i, 1, frame]])
            points[i].set_3d_properties([r[i, 2, frame]])

        cm_line.set_data(R_CM[0, :frame], R_CM[1, :frame])
        cm_line.set_3d_properties(R_CM[2, :frame])

        cm_point.set_data([R_CM[0, frame]], [R_CM[1, frame]])
        cm_point.set_3d_properties([R_CM[2, frame]])

        # Bei ipympl-Widgets nötig, da kein automatischer Redraw wie bei FuncAnimation stattfindet
        fig.canvas.draw_idle()

    # Slider für manuelles Scrubben
    slider = IntSlider(min=0, max=T_steps - 1, step=step, value=0, description="Zeitschritt")

    # Play-Button für automatisches Abspielen
    play = Play(min=0, max=T_steps - 1, step=step, interval=interval, value=0, description="Play")

    # Verknüpft beide Widgets: Play treibt den Slider-Wert, Slider zeigt ihn an
    jslink((play, "value"), (slider, "value"))

    # scrub() wird bei jeder Wertänderung des Sliders aufgerufen -- egal ob per
    # Hand gezogen oder durch den Play-Button getrieben
    out = interactive_output(scrub, {"frame": slider})

    ui = HBox([play, slider])
    display(ui, out)

    return fig, ax, slider, play


# --- Plot Funktionen für den Sanity-Check ---

def plot_conservation_of_energy(y, m, G, t):
    # Diese Funktion dient zur visualisierung der Energieerhaltung über die Zeit
    # Es wird der jeweilige relative Energiefehler betrachtet
    E_tot = calculate_total_energy(y, m, G)
    E_0 = E_tot[0]
    E_rel_error = (E_tot - E_0) / np.abs(E_0)
    # Das Resultat plotten
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t, E_rel_error, lw=2, color="red")
    ax.set_title("Energierhaltung") # ; relativer Fehler
    ax.set_xlabel("Zeit t")
    ax.set_ylabel("relativer Fehler")
    ax.grid(True, alpha=0.7, linestyle="--")

    return fig, ax

def plot_conservation_of_momentum(y, m, t):
    # Daten hohlen
    P_tot = calculate_total_momentum(y, m)
    P_tot_0 = P_tot[:, [0]]
    delta_P_tot = P_tot - P_tot_0

    # Figur Plotten
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t, delta_P_tot[0, :], label="Px (X-Komponente)", color="blue", alpha = 0.8)
    ax.plot(t, delta_P_tot[1, :], label="Py (Y-Komponente)", color="green", alpha = 0.8)
    ax.plot(t, delta_P_tot[2, :], label="Pz (Z-Komponente)", color="orange", alpha = 0.8)
    
    ax.set_title("Impulserhaltung")
    ax.set_xlabel("Zeit t")
    ax.set_ylabel("Gesamtimpulsänderung")
    ax.legend(loc="best")
    ax.grid(True, linestyle="--", alpha=0.7)
    
    return fig, ax

def plot_conservation_of_angular_momentum(y, m, t):
    # Daten hohlen
    L_tot = calculate_total_angular_momentum(y, m)
    L_tot_0 = L_tot[:, [0]]
    delta_L_tot = L_tot - L_tot_0
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t, delta_L_tot[0, :], label="Lx (X-Komponente)", color="blue", alpha = 0.8)
    ax.plot(t, delta_L_tot[1, :], label="Ly (Y-Komponente)", color="green", alpha = 0.8)
    ax.plot(t, delta_L_tot[2, :], label="Lz (Z-Komponente)", color="orange", alpha = 0.8)
    
    ax.set_title("Drehimpulserhaltung")
    ax.set_xlabel("Zeit t")
    ax.set_ylabel("Gesamtdrehimpulsänderung")
    ax.legend(loc="best")
    ax.grid(True, linestyle="--", alpha=0.7)
    
    return fig, ax
