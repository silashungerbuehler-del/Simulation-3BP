# Die Anfangsbedinguen werden in dieser Datei definiert, also auch hier später bei der Anylse angepasst.
# Phasenraum, also für jeden Körper (x, y, z, vx, vy, vz)
# Jetzt noch alle Zahlen als Platzhalter --> bei der Analyse später anpassen

import numpy as np

def initial_conditions_2bp():
    # Die Massen der beidne Körper
    m1 = 1000.0
    m2 = 1.0
    m = np.array([m1, m2], dtype=float)
    
    # Gravitationskonstante (G=1.0 in N-Körper-Einheiten, später für echte Beispiele in SI-Einheiten angeben)
    G = 1.0

    # Die Startopositionen (x, y, z) der zwei Körper
    r1 = np.array([0.0, 0.0, 0.0], dtype=float)
    r2 = np.array([10.0, 0.0, 0.0], dtype=float)

    # Die Startgeschwindigkeiten (vx, vy, vz) der zwei Körper
    v1 = np.array([0.0, 0.0, 0.0], dtype=float)
    v2 = np.array([0.0, 10.0, 0.0], dtype=float)

    # Der Zustandsvektor y0 (12 Einträge für 2BP --> entspricht den 12 DOF)
    y0 = np.concatenate((r1, r2, v1, v2))

    return y0, m, G

def initial_conditions_3bp():
    # Die Massen der drei Körper
    m1 = 1.0
    m2 = 1.0
    m3 = 1.0
    m = np.array([m1, m2, m3], dtype=float)

    # Gravitationskonstante (G=1.0 in N-Körper-Einheiten, später für echte Beispiele in SI-Einheiten angeben)
    G = 1.0

    # Die Startopositionen (x, y, z) der drei Körper
    r1 = np.array([-1.0, 0.0, 0.0], dtype=float)
    r2 = np.array([1.0, 0.0, 0.0], dtype=float)
    r3 = np.array([0.0, 1.0, 0.0], dtype=float)

    # Die Startgeschwindigkeiten (vx, vy, vz) der drei Körper
    v1 = np.array([0.0, 0.5, 0.0], dtype=float)
    v2 = np.array([0.0, -0.5, 0.0], dtype=float)
    v3 = np.array([0.0, 0.0, 0.0], dtype=float)

    # Der Zustandsvektor y0 (18 Einträge für 3BP --> entspricht den 18 DOF)
    y0 = np.concatenate((r1, r2, r3, v1, v2, v3))
    return y0, m, G

def figure_eight():
    G = 1
    m1 = 1.0
    m2 = 1.0
    m3 = 1.0
    m = np.array([m1, m2, m3], dtype=float)

    r1 = np.array([0.97000436, -0.24308753, 0], dtype=float)
    r2 = -r1
    r3 = np.array([0.0, 0.0, 0])

    v3 = np.array([-0.93240737, -0.86473146, 0], dtype=float)
    v1 = -v3 / 2
    v2 = -v3 / 2

    y0 = np.concatenate((r1, r2, r3, v1, v2, v3), dtype=float)
    return y0, m, G