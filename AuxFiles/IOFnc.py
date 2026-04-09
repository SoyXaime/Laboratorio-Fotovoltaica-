import numpy as np
from scipy import stats

def ajuste_VI(I, V):
    """
    Ajuste lineal V = a·I + b con incertidumbres
    
    Parámetros:
        I : array (corriente)
        V : array (voltaje)
    
    Devuelve:
        a, b : parámetros del ajuste
        da, db : incertidumbres
        R2 : coeficiente de determinación
    """
    
    # Ajuste lineal
    slope, intercept, r_value, p_value, std_err = stats.linregress(I, V)
    
    # Parámetros
    a = slope
    b = intercept
    
    # Incertidumbres
    da = std_err
    
    # Error en b
    n = len(I)
    I_mean = np.mean(I)
    Sxx = np.sum((I - I_mean)**2)
    db = std_err * np.sqrt(np.sum(I**2)/ (n * Sxx))
    
    # Coeficiente de determinación
    R2 = r_value**2
    
    return a, da, b, db, R2



def tabla_latex_resultados(resultados):
    """
    resultados: lista de diccionarios con:
        {
            "nombre": "R1",
            "R": valor,
            "dR": incertidumbre,
            "R2": coeficiente
        }
    """
    
    latex = []
    
    latex.append("\\begin{table}[H]")
    latex.append("\\centering")
    latex.append("\\begin{tabular}{ccc}")
    latex.append("\\hline")
    latex.append("Resistencia & $R \\pm \\sigma_R$ (k$\\Omega$) & $R^2$ \\\\")
    latex.append("\\hline")
    
    for r in resultados:
        fila = f"{r['nombre']} & ${r['R']:.3f} \\pm {r['dR']:.3f}$ & {r['R2']:.5f} \\\\"
        latex.append(fila)
    
    latex.append("\\hline")
    latex.append("\\end{tabular}")
    latex.append("\\caption{Resultados del ajuste lineal V-I}")
    latex.append("\\end{table}")
    
    return "\n".join(latex)





def potencia(V,R):
    """
    Calcula la potencia disipada en una resistencia R dada una tensión V.
    
    Parámetros:
        V : array (voltaje)
        R : resistencia (ohmios)
    
    Devuelve:
        P : array (potencia en vatios)
    """
    P = V**2 / R
    return P


def modelo(R, a,b):
    return a / R + b

