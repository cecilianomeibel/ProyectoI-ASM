

# Biblioteca para aplicar mapeos bilineales (Möbius) a círculos y rectas.
# Permite visualizar y validar el efecto geométrico de la transformación.
#
# - Soporta círculos (z = centro + radio * exp(i*theta)) y rectas (y = m x + b).
# - Detección automática de si la imagen es círculo o recta según la singularidad.
# - Muestreo robusto y visualización clara, con referencias geométricas.


import numpy as np
import matplotlib.pyplot as plt

def moebius(z, a, b, c, d):
    """
    Aplica la transformación de Möbius: w = (a z + b) / (c z + d)
    - z: escalar o array de puntos complejos
    - a, b, c, d: coeficientes complejos (ad - bc != 0)
    Retorna la imagen de z bajo el mapeo.
    """
    return (a*z + b) / (c*z + d)

def muestrea_circulo(centro, radio, n=600):
    """
    Genera n puntos equiespaciados sobre un círculo dado (en el plano complejo).
    - centro: centro del círculo (complejo)
    - radio: radio del círculo (real positivo)
    - n: número de muestras
    """
    theta = np.linspace(0, 2*np.pi, n, endpoint=False)
    return centro + radio * np.exp(1j * theta)

def construir_recta(m=None, b_linea=None):
    """
    Construye un punto p0 y un vector dirección v para la recta y = m x + b.
    - Si m es muy grande, se interpreta como recta vertical x = b_linea.
    Retorna (p0, v) ambos complejos.
    """
    if m is not None and b_linea is not None:
        # Si m es muy grande, tratamos la recta como x = const
        if np.isfinite(m) and abs(m) < 1e6:
            x0 = 0.0
            y0 = b_linea
            p0 = x0 + 1j*y0
            v = 1.0 + 1j*m
            return p0, v
        else:
            # Recta vertical: x = x0
            x0 = b_linea  # En este caso, b_linea representa x0
            y0 = 0.0
            p0 = x0 + 1j*y0
            v = 1j  # dirección puramente vertical
            return p0, v
    raise ValueError("Debe proporcionar (m, b_linea) para definir la recta y = m x + b o x = b.")

def contiene_singularidad_circulo(centro, radio, zs, tol=1e-12):
    """
    Indica si la singularidad zs cae dentro (o en el borde) del círculo.
    Si c = 0, zs = None y no hay singularidad en el plano finito.
    """
    if zs is None:
        return False
    return abs(centro - zs) <= radio + tol

def valida_imagen(W, tipo_resultado, verbose=True):
    """
    Valida la imagen: si es línea, ajusta y da ecuación; si es círculo, ajusta y da centro/radio.
    Útil para comprobar el resultado geométrico del mapeo.
    """
    mask = np.isfinite(W)
    X = np.column_stack((W.real[mask], W.imag[mask]))
    if tipo_resultado == "línea":
        # Ajuste de línea por mínimos cuadrados: y = m x + b
        x = X[:,0]
        y = X[:,1]
        A = np.vstack([x, np.ones_like(x)]).T
        m_fit, b_fit = np.linalg.lstsq(A, y, rcond=None)[0]
        if verbose:
            print(f"  Ajuste de línea: y = {m_fit:.4f} x + {b_fit:.4f}")
        return ("línea", m_fit, b_fit)
    else:
        # Ajuste de círculo por mínimos cuadrados
        x = X[:,0]; y = X[:,1]
        A_ls = np.column_stack((2*x, 2*y, np.ones_like(x)))
        b_ls = x**2 + y**2
        sol, *_ = np.linalg.lstsq(A_ls, b_ls, rcond=None)
        a_c, b_c, c_c = sol
        r_c = max(0.0, a_c*a_c + b_c*b_c + c_c)**0.5
        if verbose:
            print(f"  Ajuste de círculo: centro=({a_c:.4f}, {b_c:.4f}), radio={r_c:.4f}")
        return ("círculo", a_c, b_c, r_c)

# Arreglar esto
def mapeo_bilineal():
    """
    Función de ejemplo que aplica un mapeo bilineal a un círculo y muestra el resultado.
    """
    print("Ejemplo de mapeo bilineal: w = (2z + 1) / (z + 1), círculo de centro (1,0) y radio 1.")
    Z, W, zs, pasa, tipo_resultado = mapeo_bilineal_aux(2, 1, 1, 1, 'circulo', centro=1+0j, radio=1.0)
    print("Resultado obtenido:")
    valida_imagen(W, tipo_resultado)
    
def mapeo_bilineal_aux(a, b, c, d, tipo, *, centro=None, radio=None, n=600, mostrar=True, mostrar_referencia=True, ref_factor=3.0, guardar_fig=False, ruta_fig=None, cerrar_fig=True, m=None, b_linea=None, L_plot=10.0, verificar=False):
    """
    Aplica un mapeo de Möbius a un círculo o recta.
    - a, b, c, d: coeficientes del mapeo Möbius (ad-bc != 0)
    - tipo: 'circulo' o 'recta'
    - centro, radio: datos del círculo (si tipo='circulo')
    - m, b_linea: pendiente e intersección (si tipo='recta')
    - n: número de muestras
    - mostrar: si True, muestra la figura
    - mostrar_referencia: si True, dibuja referencia geométrica en la imagen
    - L_plot: longitud visible para rectas
    Retorna: (Z, W, zs, pasa_singularidad, tipo_resultado)
    """
    # Validación básica del mapeo Möbius
    if abs(a*d - b*c) == 0:
        raise ValueError("Transformación inválida: ad - bc = 0 (no es Möbius)")

    # Calcula la singularidad (si existe) en el plano z
    zs = None if abs(c) == 0 else -d / c

    if tipo == "circulo":
        # --- Caso círculo: z = centro + radio * exp(i*theta) ---
        if centro is None or radio is None:
            raise ValueError("Para 'circulo' se requieren centro y radio.")
        Z = muestrea_circulo(centro, radio, n=n)
        pasa = contiene_singularidad_circulo(centro, radio, zs)
        tipo_resultado = "línea" if pasa else "círculo"
    elif tipo == "recta":
        # --- Caso recta: y = m x + b ---
        p0, v = construir_recta(m=m, b_linea=b_linea)
        tol = 1e-12
        # Si es vertical, muestrea y; si no, usa parametrización robusta
        if m is not None and (not np.isfinite(m) or abs(m) >= 1e6):
            y_vals = np.linspace(-L_plot/2.0, L_plot/2.0, n)
            Z = b_linea + 1j * y_vals
            Z_plot = Z.copy()
        else:
            eps = 1e-6
            theta = np.linspace(-np.pi + eps, np.pi - eps, n)
            t = np.tan(theta/2.0)
            Z = p0 + t * v
            v_unit = v / (abs(v) if abs(v) > 0 else 1.0)
            s = np.linspace(-L_plot/2.0, L_plot/2.0, n)
            Z_plot = p0 + s * v_unit
        # Clasificación: ¿la recta pasa por la singularidad?
        if zs is None:
            pasa = False
        elif abs(v) < tol:
            pasa = abs(p0 - zs) < tol
        else:
            t_sing = (zs - p0) / v
            pasa = abs(t_sing.imag) < 1e-9
        tipo_resultado = "línea" if pasa else "círculo"
    else:
        raise ValueError("Opción inválida. Use 'circulo' o 'recta'.")

    # Si algún punto muestreado coincide con la singularidad, desplázalo ligeramente
    if zs is not None:
        mascara = np.abs(Z - zs) < 1e-12
        if np.any(mascara):
            Z = Z.copy()
            Z[mascara] = Z[mascara] + (1e-9 + 0j)

    # Calcula la imagen bajo el mapeo Möbius
    W = moebius(Z, a, b, c, d)
    W_raw = W.copy()
    # Rompe el trazo cerca de la singularidad (evita saltos por infinito)
    denom = c*Z + d
    denom_abs = np.abs(denom)
    W = W.astype(complex)
    mod = np.abs(W)
    finite_both = np.isfinite(denom_abs) & np.isfinite(mod)
    if np.any(finite_both):
        # Umbral relativo para cortar cerca de infinito
        scale = np.nanmedian(denom_abs[finite_both])
        if not np.isfinite(scale) or scale <= 0:
            scale = 1.0
        eps_break = 1e-6 * (1.0 + scale)
        W[~np.isfinite(mod)] = np.nan + 1j*np.nan
        W[denom_abs < eps_break] = np.nan + 1j*np.nan
        # Si quedan muy pocos puntos, relaja el corte y recorta outliers
        min_keep = max(5, int(0.01 * n))
        if np.count_nonzero(np.isfinite(W)) < min_keep:
            W = W_raw.astype(complex)
            W[~np.isfinite(np.abs(W))] = np.nan + 1j*np.nan
            mod2 = np.abs(W)
            fin2 = np.isfinite(mod2)
            if np.any(fin2):
                q99 = np.quantile(mod2[fin2], 0.99)
                thr2 = 10.0 * q99 if np.isfinite(q99) and q99 > 0 else 1e6
                W[mod2 > thr2] = np.nan + 1j*np.nan

    if mostrar:
        fig, ax = plt.subplots(1, 2, figsize=(12, 5))
        # Panel izquierdo (original)
        ax[0].set_title("Original")
        # Usa Z_plot si existe (recta), si no Z
        Z_left = locals().get('Z_plot', Z)
        ax[0].plot(Z_left.real, Z_left.imag, label=tipo)
        if zs is not None:
            ax[0].plot(zs.real, zs.imag, 'ro', label='singularidad')
        # Ajustar límites para mostrar ejes completos
        # Caso especial: recta vertical (m muy grande)
        caso_recta_vertical = (
            tipo == 'recta' and m is not None and (not np.isfinite(m) or abs(m) >= 1e6)
        )
        if caso_recta_vertical:
            ax[0].set_xlim(b_linea - 0.5, b_linea + 0.5)
            ax[0].set_ylim(-L_plot/2.0, L_plot/2.0)
        xlims = ax[0].get_xlim()
        ylims = ax[0].get_ylim()
        ax[0].plot([xlims[0], xlims[1]], [0, 0], color='k', linewidth=0.5)  # eje x
        ax[0].plot([0, 0], [ylims[0], ylims[1]], color='k', linewidth=0.5)  # eje y
        ax[0].set_aspect('equal', adjustable='box')
        ax[0].grid(True)
        ax[0].legend()
        # Panel derecho (mapeado)
        ax[1].set_title("Mapeado bilineal")
        ax[1].plot(W.real, W.imag, label=f"imagen → {tipo_resultado}")
        # Referencias/Verificación
        maskW = np.isfinite(W)
        if mostrar_referencia and np.count_nonzero(maskW) >= 2:
            X = np.column_stack((W.real[maskW], W.imag[maskW]))
            if tipo_resultado == "línea":
                # Ajuste de línea por PCA (dirección principal)
                mu = X.mean(axis=0)
                Y = X - mu
                C = (Y.T @ Y) / max(1, (Y.shape[0] - 1))
                vals, vecs = np.linalg.eigh(C)
                idx = int(np.argmax(vals))
                u = vecs[:, idx]
                s = ref_factor * np.sqrt(max(vals[idx], 1e-12))
                p1 = mu - s * u
                p2 = mu + s * u
                ax[1].plot([p1[0], p2[0]], [p1[1], p2[1]], '--', color='C1', label='referencia línea')
            else:
                # Círculo por mínimos cuadrados: (x-a)^2 + (y-b)^2 = r^2
                x = X[:,0]; y = X[:,1]
                A_ls = np.column_stack((2*x, 2*y, np.ones_like(x)))
                b_ls = x**2 + y**2
                sol, *_ = np.linalg.lstsq(A_ls, b_ls, rcond=None)
                a_c, b_c, c_c = sol
                r_c = max(0.0, a_c*a_c + b_c*b_c + c_c)**0.5
                theta = np.linspace(0, 2*np.pi, 360, endpoint=False)
                xc = a_c + r_c*np.cos(theta)
                yc = b_c + r_c*np.sin(theta)
                ax[1].plot(xc, yc, '--', color='C2', label='referencia círculo')
        # Ajustar límites para mostrar ejes completos
        xlims = ax[1].get_xlim()
        ylims = ax[1].get_ylim()
        # Caso especial: recta y=1 bajo w=1/z, forzar límites para mostrar el círculo imagen
        caso_recta_y1 = (
            tipo == 'recta' and np.isclose(a, 0) and np.isclose(b, 1) and np.isclose(c, 1) and np.isclose(d, 0)
            and m is not None and np.isclose(m, 0.0) and b_linea is not None and np.isclose(b_linea, 1.0)
        )
        if caso_recta_y1:
            ax[0].set_xlim(-50, 50)
            ax[0].set_ylim(0.5, 1.5)
            ax[1].set_xlim(-1.2, 1.2)
            ax[1].set_ylim(-0.2, 1.2)
            xlims = ax[1].get_xlim()
            ylims = ax[1].get_ylim()
        # Si la imagen es una recta, expandir límites y recortar outliers para que no se aplane
        if tipo_resultado == 'línea':
            maskW = np.isfinite(W)
            if np.count_nonzero(maskW) > 0:
                xw = W.real[maskW]
                yw = W.imag[maskW]
                # Recorta outliers usando percentiles 1 y 99
                x1, x99 = np.percentile(xw, [1, 99])
                y1, y99 = np.percentile(yw, [1, 99])
                dx = x99 - x1
                dy = y99 - y1
                if dx > 0 and dy > 0:
                    xpad = 0.2 * dx
                    ypad = 0.2 * dy
                    ax[1].set_xlim(x1 - xpad, x99 + xpad)
                    ax[1].set_ylim(y1 - ypad, y99 + ypad)
                xlims = ax[1].get_xlim()
                ylims = ax[1].get_ylim()
        ax[1].plot([xlims[0], xlims[1]], [0, 0], color='k', linewidth=0.5)  # eje x
        ax[1].plot([0, 0], [ylims[0], ylims[1]], color='k', linewidth=0.5)  # eje y
        ax[1].set_aspect('equal', adjustable='box')
        ax[1].grid(True)
        ax[1].legend()
        plt.tight_layout()
        if guardar_fig:
            import os, time
            base = ruta_fig
            if not base:
                suf = f"{tipo}_{tipo_resultado}_{int(time.time())}.png"
                base = os.path.join(os.getcwd(), f"mapeo_bilineal_{suf}")
            try:
                plt.savefig(base, dpi=160)
                print(f"Figura guardada en: {base}")
            except Exception as e:
                print(f"No se pudo guardar la figura: {e}")
        # Mostrar si hay backend interactivo
        try:
            plt.show(block=True)
        except Exception:
            pass
        if cerrar_fig:
            plt.close(fig)

    return Z, W, zs, pasa, tipo_resultado





