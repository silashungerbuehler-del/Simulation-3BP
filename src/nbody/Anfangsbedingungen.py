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
    # Somit bei Positionsstörung v anhand der gestörten position berechnet. Omega aber anhand ungestörten.
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

def initial_conditions_aperiodic(delta_m=(0.0, 0.0, 0.0), delta_r=None, delta_v=None):
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
        [0.0, -m2/m1*10, 0.0],
        [0.0, 10, 0.0]
    ], dtype=float)

    y0 = np.concatenate((r.flatten(), v.flatten()))
    return y0, m, G, r, v
