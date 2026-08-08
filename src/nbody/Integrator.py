import numpy as np
from scipy.integrate import solve_ivp
from Dynamik import n_body_equations
from Anfangsbedingungen import initial_conditions_2bp
import matplotlib.pyplot as plt

# solve_ivp(fun, t_span, y0, method='RK45', t_eval=None, dense_output=False, events=None, vectorized=False, args=None, **options)
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html

# Die Variablen aus Anfangsbedingungen.py nach dem Import in diesen zwei Zeilen definiert, so weiter verwenden. noch verallgemeinern!!
y0, m, G = initial_conditions_2bp()

# Zeiten vorher definieren, macht es übersichtlicher
# t_start = 0
# t_end = 100
# frames = 2000 # Wie viele Datenpunkte am Ende
# method='DOP853'
# def run_2bp_simulation(y0, m, G, t_start, t_end, frames, method):
#     sol_2bp = solve_ivp(
#         fun=two_body_equations,
#         t_span=(t_start, t_end),
#         y0=y0_2bp,
#         method=method,
#         args=(m_2bp, G_2bp),
#         rtol=1e-10,
#         atol=1e-10,
#         t_eval=np.linspace(t_start, t_end, frames)
#     )
#     return sol_2bp

# t_start hätte ich fix bei 0 gelassen, t_end und frames im Notebook bei entsprecheneden Sim. definieren, da nicht immer gleich gewünscht
def run_n_body_simulation(y0, m, G, t_start=0, t_end=100, frames=2000):

    # für solve_ivp
    t_eval=np.linspace(t_start, t_end, frames)

    sol = solve_ivp(
        fun=n_body_equations,
        t_span=(t_start, t_end),
        y0=y0, 
        method='DOP853',
        args=(m, G),
        rtol=1e-10, # Könnte auch auf 1e-12
        atol=1e-10, # Könnte auch auf 1e-12
        t_eval=t_eval
    )
    return sol

sol = run_n_body_simulation(y0, m, G, t_start=0, t_end=100, frames=2000)
# Daten auswerten --> solve_ivp.y ist eine Matrix mit 12 Zeilen (2bp) und frames Spalten 
# ersten Zeilen für die Position des ersten Körpers usw. --> 2bp ersten 6 Zeilen für die Pos. und die letzten 6 für die Geschw. 
r1_x = sol.y[0]
r1_y = sol.y[1]
r1_z = sol.y[2]

r2_x = sol.y[3]
r2_y = sol.y[4]
r2_z = sol.y[5]

# --- 3D PLOT ERSTELLEN ---
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Bahnen plotten
ax.plot(r1_x, r1_y, r1_z, label='Körper 1 (Stern)', color='orange')
ax.plot(r2_x, r2_y, r2_z, label='Körper 2 (Planet)', color='blue')

# Startpunkte markieren (Spalte 0)
ax.scatter(r1_x[0], r1_y[0], r1_z[0], color='red', marker='o')
ax.scatter(r2_x[0], r2_y[0], r2_z[0], color='red', marker='o')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()
plt.title("2-Körper-Problem Trajektorien")
plt.show()