# Die Anfangsbedinguen werden in dieser Datei definiert
# Phasenraum, also für jeden Körper (x, y, z, vx, vy, vz)

import numpy as np
from scipy.constants import G as G_real

# Anfangsbedingungen für die Analyse
def initial_conditions_euler(delta_m=(0.0, 0.0, 0.0), delta_r=None, delta_v=None, a=1.0, G=1.0, m_ref=1.0):
    
    # Kollineare Euler-Loesung, gleiche Referenzmasse m_ref für alle drei Körper.
    # Geometrie: P1(-a,0,0), P2(0,0,0) [Zentralkörper], P3(a,0,0).
    # v wird aus m_ref (unveränderten Referenzmasse) berechnet -> bleibt bei delta_m fest, sodass eine Massestörung die exakte periodische Lösung sichtbar wegfällt.

    # delta_m: (dm1, dm2, dm3), Massenstoerung (simulierte Masse)
    # delta_r, delta_v: dict {0,1,2: np.array([dx,dy,dz])}, kinematische Störung
    
    # tatsächlich simulierte Massen (können von m_ref abweichen)
    m = np.array([m_ref + delta_m[0], m_ref + delta_m[1], m_ref + delta_m[2]], dtype=float)

    r = np.array([
        [-a, 0.0, 0.0],
        [ 0.0, 0.0, 0.0],
        [ a, 0.0, 0.0],
    ], dtype=float)

    if delta_r is not None:
        for idx, d in delta_r.items():
            r[idx] += d

    # Geschwindigkeitsbetrag aus m_ref, nicht aus der gestörten Masse
    v_mag = np.sqrt(5.0/4.0 * G * m_ref / a) # = omega * a
    v = np.array([
        [0.0, -v_mag, 0.0], # P1: Gegenuhrzeigersinn
        [0.0,  0.0,   0.0], # P2: Zentralkörper ruht
        [0.0,  v_mag, 0.0], # P3: Gegenuhrzeigersinn
    ], dtype=float)

    if delta_v is not None:
        for idx, d in delta_v.items():
            v[idx] += d

    y0 = np.concatenate((r.flatten(), v.flatten()))
    return y0, m, G, r, v # r, v separat zurückgeben, für die Unit-Berechnung

def initial_conditions_lagrange(m_ref=None, delta_m=(0.0, 0.0, 0.0), delta_r=None, delta_v=None, a=None, G=None):

    # Gleichseitige Lagrange-Loesung für beliebige Massenverhältnisse.
    # m_ref: Referenzmassen, aus denen Geometrie (CM) und omega berechnet werden.
    # delta_m wird erst nach der Positions-/Geschwindigkeitsberechnung addiert -> gleiches Prinzip wie bei Euler.
    # Für Sonne-Jupiter-Trojaner (L4): m_ref=(M_sun, M_jup, ~0), a=Jupiterbahnradius.
    
    m_ref = np.array(m_ref, dtype=float) # Aus m_ref ein Array machen
    M = np.sum(m_ref)

    # Eckpunkte des gleichseitigen Dreiecks (Seite a), noch nicht COM-zentriert
    P = np.array([
        [0.0, 0.0, 0.0],
        [a, 0.0, 0.0],
        [a/2.0, a*np.sqrt(3.0)/2.0, 0.0],
    ], dtype=float)

    # Schwerpunkt aus m_ref, Positionen ins CM-System verschieben
    R_cm = (m_ref[:, None] * P).sum(axis=0) / M
    r = P - R_cm

    if delta_r is not None:
        for idx, d in delta_r.items():
            r[idx] += d

    # omega aus Referenzmasse (Gesamtmasse), Geschwindigkeit über v = omega * e_z x r
    omega = np.sqrt(G * M / a**3)
    v = np.zeros_like(r)
    for i in range(3):
        v[i] = omega * np.array([-r[i, 1], r[i, 0], 0.0])

    if delta_v is not None:
        for idx, d in delta_v.items():
            v[idx] += d

    # tatsächlich simulierte (möglicherweise gestörte) Massen
    m = m_ref + np.array(delta_m)

    y0 = np.concatenate((r.flatten(), v.flatten()))
    return y0, m, G, r, v # r, v separat zurückgeben, für die Unit-Berechnung

def initial_conditions_strong_chaos(delta_m=(0.0, 0.0, 0.0), delta_r=None, delta_v=None):
    # Mit den inputs von delta_m, delta_r und delta_v direkt gestörte systeme berechnen lassen
    # delta_m: delta_m: (dm1, dm2, dm3) - Massenstörung, z.B. (1e-9, 0, 0)
    # delta_r, delta_v: dict {0,1,2: np.array([dx,dy,dz])} - Positions-/Geschw.-Störung
    
    G = 1.0
    m = np.array([1.0 + delta_m[0], 1.0 + delta_m[1], 1.0 + delta_m[2]], dtype=float)

    r = np.array([
        [-1.0, 1.0, 0.0],
        [ 1.0, 0.0, 1.5],
        [ 0.5, 1.0, 0.0],
    ], dtype=float)

    if delta_r is not None:
        for idx, d in delta_r.items():
            r[idx] += d

    v = np.array([
        [0.0,  0.5, 0.0],
        [0.0, -0.5, 0.0],
        [0.0,  0.0, 0.0],
    ], dtype=float)

    if delta_v is not None:
        for idx, d in delta_v.items():
            v[idx] += d

    y0 = np.concatenate((r.flatten(), v.flatten()))
    return y0, m, G, r, v # r, v separat zurückgeben, für die Unit-Berechnung

def initial_conditions_2bp():
    G = 1.0

    # Die Massen der beidne Körper
    m1 = 1000.0
    m2 = 1.0
    m = np.array([m1, m2], dtype=float)

    # Die Startopositionen (x, y, z) der zwei Körper
    r = np.array([
        [0.0, 0.0, 0.0],
        [10.0, 0.0, 0.0]
    ], dtype=float)

    # Die Startgeschwindigkeiten (vx, vy, vz) der zwei Körper
    v = np.array([
        [0.0, 0.0, 0.0],
        [0.0, 10.0, 0.0]
    ], dtype=float)

    y0 = np.concatenate((r.flatten(), v.flatten()))
    return y0, m, G, r, v

# Alte Anfangsbedingungen
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

def pythagorean_problem():
    G = 1
    m1 = 3.0
    m2 = 4.0
    m3 = 5.0
    m = np.array([m1, m2, m3], dtype=float)

    r1 = np.array([1.0, 3.0, 0.0], dtype=float)
    r2 = np.array([-2.0, -1.0, 0.0], dtype=float)
    r3 = np.array([1.0, -1.0, 0.0], dtype=float)

    v1 = np.array([0.0, 0.0, 0.0], dtype=float)
    v2 = np.array([0.0, 0.0, 0.0], dtype=float)
    v3 = np.array([0.0, 0.0, 0.0], dtype=float)

    y0 = np.concatenate((r1, r2, r3, v1, v2, v3), dtype=float)
    return y0, m, G

def initial_conditions_3bp():
    # Die Massen der drei Körper
    m1 = 1.0 # + 10**(-9)
    m2 = 1.0
    m3 = 1.0
    m = np.array([m1, m2, m3], dtype=float)

    # Gravitationskonstante (G=1.0 in N-Körper-Einheiten, später für echte Beispiele in SI-Einheiten angeben)
    G = 1.0

    # Die Startopositionen (x, y, z) der drei Körper
    r1 = np.array([-1.0, 1.0, 0.0], dtype=float)
    r2 = np.array([1.0, 0.0, 1.5], dtype=float)
    r3 = np.array([0.5, 1.0, 0.0], dtype=float)

    # Die Startgeschwindigkeiten (vx, vy, vz) der drei Körper
    v1 = np.array([0.0, 0.5 , 0.0], dtype=float)
    v2 = np.array([0.0, -0.5, 0.0], dtype=float)
    v3 = np.array([0.0, 0.0, 0.0], dtype=float)

    # Der Zustandsvektor y0 (18 Einträge für 3BP --> entspricht den 18 DOF)
    y0 = np.concatenate((r1, r2, r3, v1, v2, v3))
    return y0, m, G
