# In dieser Datei wird die Plots für die Erhaltungsgrössen definiert

# --- Funktion für die Animation um Simulation zu visualisieren ---

def create_animation(sol, R_CM, m):
    pass

# # --- 3D PLOT ERSTELLEN ---
# fig = plt.figure(figsize=(10, 8))
# ax = fig.add_subplot(111, projection='3d')

# # Bahnen plotten
# ax.plot(r1_x, r1_y, r1_z, label='Körper 1 (Stern)', color='orange')
# ax.plot(r2_x, r2_y, r2_z, label='Körper 2 (Planet)', color='blue')

# # Startpunkte markieren (Spalte 0)
# ax.scatter(r1_x[0], r1_y[0], r1_z[0], color='red', marker='o')
# ax.scatter(r2_x[0], r2_y[0], r2_z[0], color='red', marker='o')

# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.legend()
# plt.title("2-Körper-Problem Trajektorien")
# plt.show()