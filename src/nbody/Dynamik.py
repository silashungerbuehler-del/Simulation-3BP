import numpy as np

def two_body_equations(t, y0, m, G):
    #Die Vektoren für die Bewegungelichung definieren
    r1 = y0[0:3]
    r2 = y0[3:6]
    v1 = y0[6:9]
    v2 = y0[9:12]

    # Relativvektoren definieren nach dem Prinzip rji = ri - rj (--> F12 mit r21 also r1 - r2)
    # Bei Schriftlichen Teil MA r_vec = r1 - r2 also r21 (für a1)
    r_vec = r1 - r2
    r_mag = np.linalg.norm(r_vec) # "mag" für magnitude, als Betrag

    # Die Vekotren in der Bewegungsgleichung einsetzen
    a1 = -G * m[1]/(r_mag**3) * r_vec
    a2 = G* m[0]/(r_mag**3) * r_vec

    # Den Zustandsvektor anpassen
    return np.concatenate((v1, v2, a1, a2))

# ----------------------------------
# Wird für den Integrator gebraucht:
# ----------------------------------

def n_body_equations(t, y, m, G):
    # ürsprünglicher Zustan aufteilen, nach dem prinzip wie bei split_condition
    N = len(m)

    r = y[0 : 3*N].reshape(N, 3)
    v = y[3*N : 6*N].reshape(N, 3)

    # None = np.newaxis --> fügt eine neue leere Dimension hinzu
    # Durch Broadcasting die Diemensionen: (ri) N,1,3 - (rj)1,N,3 --> N,N,3
    rji = r[:, None, :] - r[None, :, :]

    # Hier ist die Diagonale aber Null, was bei der Division durch rji zu einem Problem wird --> hier angepasst, und Physik stimmt immer noch
    # Zuerst Betrag definieren --> axis = -1 so letzte Achse gewählt hier also die Koordinaten x,y,z von denen wir auch den Betrag wollen
    rji_mag = np.linalg.norm(rji, axis=-1)
    # Division durch Null verhindern
    np.fill_diagonal(rji_mag, 1.0)

    # Die Beschleunigung für alle gleichzeitig ausrechnen 
    # Durch die entsprechenden anpassungen durch slicing erhält man das gewünste Ergebnis, eine Matirx für die Beschleunigungsvektoren aller Körper i mit der Form N,3
    a = -G * np.sum(m[None, :, None] * rji / (rji_mag[:, :, None]**3), axis=1)

    # Der Integrator solve_ivp nimmt nur einen 1D-Array entgegen und ausserdem muss auch noch die Geschwindigkeit angehängt werden
    return  np.concatenate((v.flatten(), a.flatten()))

# ------------------------------------------------
# Wird für den Sanity-Check & Auswertung gebraucht
# ------------------------------------------------

# Erhaltungsgrössen zum Sanity Check
#genauere Infos zu Gedanken in Arbeitsjournal Phase 3 (Könnte man auf allgemeines Projekt anwenden --> in README?)

def split_condition(y, m):
    #Teil die Matrix, die man aus dem Integrator erhält in zwei Teile auf r und v. 
    #Dafür .reshape(layers, rows, collums) das -1 bei collums führt dazu, dass numpy die collums automatisch berechnet und anpasst

    N = len(m)
    r = y[0 : 3*N].reshape(N, 3, -1)
    v = y[3*N : 6*N].reshape(N, 3, -1)

    return N, r, v

def calculate_total_momentum(y, m):
    # Teilt die Matrix auf --> brauchen r nicht
    N, r, v = split_condition(y, m)

    # P = m * v
    momentum_per_body = m.reshape(N, 1, 1) * v

    # Der Gesamtimpuls ist die Summe aller Körper
    P_tot = np.sum(momentum_per_body, axis=0)
    return P_tot # P_tot ist ein 3D Array und die Spalten geben jeweils Px, Py und Pz aus, welche sich über die Zeit verändern.

# Der Schwerpunkt und die Schwerpunktbewegung sind direkte konsequenzen aus der Impulerhaltung --> siehe Arbeitsjournal Phase 3

def calculate_center_of_mass(y, m):
    N, r, v = split_condition(y, m)
    M_tot = np.sum(m)

    # die Multiplikation von der Masse des Körpers mit seiner zusgehörigen Position --> was "im" Summenzeichen der Fromel für arrow(R) steht. 
    r_m = m.reshape(N, 1, 1) * r
    R_CM = np.sum(r_m, axis = 0) / M_tot
    return R_CM

# Im Prinzip eine Unnötige Funktion, ich habe sie einefach noch stehen lassen, falls ich sie mal noch für etwas kleines verwenden möchte.
def calculate_velocity_of_center_of_mass(y, m):
    N, r, v = split_condition(y, m)
    M_tot = np.sum(m)

    # gleiches Prinzip wie bei calculate_center_of_mass(y, m)
    v_m = m.reshape(N, 1, 1) * v
    V_CM = np.sum(v_m, axis = 0) / M_tot
    return V_CM

def calculate_total_angular_momentum(y, m):
    N, r, v = split_condition(y, m)
    momenturm_per_body = m.reshape(N, 1, 1) * v

    # l = m (r x v) = r x mv, also l = r x p
    angular_momentum_per_body = np.cross(r, momenturm_per_body, axis = 1)

    # Gesamtdrehimpuls --> Summe der Drehimpulse der Körper --> ist ein 3D-Array mit Lx, Ly, Lz über die Zeit
    L_tot = np.sum(angular_momentum_per_body, axis=0)
    return L_tot

def calculate_total_energy(y, m, G):
    N, r, v = split_condition(y, m)
    # Die Gesamtenergie setzt sich aus der kinetischen und der potentiellen Energie zusammen

    # kinetische Energie
    v_squared = np.sum(v**2, axis=1)
    E_kin_per_body = 1/2 * m.reshape(N, 1) * v_squared # Broadcasting (bei m.reshape()) ermöglicht wie weiter oben, dass diese Rechnung mit den Arrays funktioniert
    E_kin_tot = np.sum(E_kin_per_body, axis = 0)

    # potentielle Energie 
    E_pot_tot = np.zeros(r.shape[2]) # sonst wäre E_pot_tot nicht definiert
    for i in range(N):
        for j in range(i+1, N):
            #relative Position der Körper berechnen
            r_rel = r[i] - r[j]
            r_reL_mag = np.linalg.norm(r_rel, axis=0) # magnitude also Betrag des Relativvektors berechnen, durch axis = 0 den Betrag entlang der Achse 0 also den Zeilen

            # Einsetzen in Gleichung für Potentielle Energie
            E_pot_tot -= G * m[i] * m[j] / r_reL_mag # So direkt Var. definiert, -= da E_pot negativ ist

    # Gesamtenergie
    E_tot = E_kin_tot + E_pot_tot # ist ein 1D Array der Gesamtenergie über die Zeit
    return E_tot
