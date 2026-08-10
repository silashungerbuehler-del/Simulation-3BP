import numpy as np
from scipy.integrate import solve_ivp
from nbody.Dynamik import n_body_equations

# solve_ivp(fun, t_span, y0, method="RK45", t_eval=None, dense_output=False, events=None, vectorized=False, args=None, **options)
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html

# t_start hätte ich fix bei 0 gelassen, t_end und frames im Notebook bei entsprecheneden Sim. definieren, da nicht immer gleich gewünscht
def run_n_body_simulation(y0, m, G, t_start=0, t_end=100, frames=2000):

    # für solve_ivp
    t_eval=np.linspace(t_start, t_end, frames)

    sol = solve_ivp(
        fun=n_body_equations,
        t_span=(t_start, t_end),
        y0=y0, 
        method="DOP853",
        args=(m, G),
        rtol=1e-10, # Könnte auch auf 1e-12
        atol=1e-10, # Könnte auch auf 1e-12
        t_eval=t_eval
    )
    return sol

# Daten auswerten --> solve_ivp.y ist eine Matrix mit 6n Zeilen (n BP) und frames Spalten 