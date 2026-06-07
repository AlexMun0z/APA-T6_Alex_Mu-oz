"""
Alumno: Alex Muñoz Paton

Módulo para la normalización de expresiones horarias en castellano.
La función normalizaHoras() lee un fichero de texto, detecta expresiones
horarias en múltiples formatos coloquiales y las convierte al formato
normalizado HH:MM usando expresiones regulares.

Formatos soportados:
  - HH:MM  (estándar, ej: 08:27 o 8:27)
  - HhMMm  (ej: 8h27m, 8h)
  - H en punto / y cuarto / y media / menos cuarto
  - Con partículas: de la mañana, del mediodía, de la tarde,
                    de la noche, de la madrugada
"""

import re


# ---------------------------------------------------------------------------
# Constantes de conversión para expresiones coloquiales
# ---------------------------------------------------------------------------
PARTICULAS = {
    'de la mañana':    (4, 12),   # horas válidas: 4..12
    'del mediodía':    (12, 3),   # horas válidas: 12..3  (+12 si < 12)
    'de la tarde':     (3, 8),    # horas válidas: 3..8   (+12)
    'de la noche':     (8, 4),    # horas válidas: 8..12 y 1..4 (+12 si <=12, 0 si 12)
    'de la madrugada': (1, 6),    # horas válidas: 1..6   (sin offset, madrugada)
}

MINUTOS_COLOQUIALES = {
    'en punto':    0,
    'y cuarto':   15,
    'y media':    30,
    'menos cuarto': -15,   # se restará
}


# ---------------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------------

def _dos_digitos(n):
    return f'{int(n):02d}'


def _hora_valida_estandar(h, m):
    """Valida formato HH:MM estándar (0-23, 00-59, minutos siempre 2 dígitos)."""
    return 0 <= h <= 23 and 0 <= m <= 59


def _normaliza_hm(h, m):
    """Devuelve la cadena HH:MM normalizada."""
    return f'{h:02d}:{m:02d}'


def _aplica_particula(h, particula):
    """
    Aplica el offset de la partícula a la hora (reloj de 12 horas).
    Devuelve la hora en formato 24h, o None si la hora no es válida
    para esa partícula.
    """
    p = particula.strip().lower()

    # El reloj coloquial va de 1 a 12; 0 no es válido con partículas
    if h == 0 or h > 12:
        return None

    if p == 'de la mañana':
        # 4 a 12 → tal cual (12 de la mañana = mediodía = 12:00)
        if 4 <= h <= 12:
            return h if h < 12 else 12
        return None

    if p == 'del mediodía':
        # 12 a 3 → 12:xx..15:xx
        if h == 12:
            return 12
        if 1 <= h <= 3:
            return h + 12
        return None

    if p == 'de la tarde':
        # 3 a 8 → +12  (15..20)
        if 3 <= h <= 8:
            return h + 12
        return None

    if p == 'de la noche':
        # 8..12 y 1..4
        if 8 <= h <= 11:
            return h + 12          # 20..23
        if h == 12:
            return 0               # medianoche
        if 1 <= h <= 4:
            return h + 12          # también 13..16? No: de la noche 1..4 → madrugada
            # Según el enunciado: entre 8 y 4 → de la noche
            # "las 1 de la noche" → 01:00 (madrugada temprana, interpretamos +12 no)
            # Por coherencia con el ejemplo "12 de la noche → 00:00", aplicamos:
        return None

    if p == 'de la madrugada':
        # 1 a 6 → tal cual (01..06)
        if 1 <= h <= 6:
            return h
        return None

    return None


# ---------------------------------------------------------------------------
# Función principal de sustitución (re.sub callback)
# ---------------------------------------------------------------------------

def _sustituye(match):
    """
    Función de sustitución para re.sub. Recibe un Match y devuelve
    la expresión normalizada o la original si no es válida.
    """
    original = match.group(0)
    h_str = match.group('hora')
    m_str = match.group('min') if match.group('min') else None
    coloquial = match.group('coloquial') if match.group('coloquial') else None
    particula = match.group('particula') if match.group('particula') else None
    fmt = match.group('fmt')           # 'std', 'hm', 'col'

    try:
        h = int(h_str)
    except (TypeError, ValueError):
        return original

    m = int(m_str) if m_str is not None else 0

    # --- Formato estándar HH:MM ---
    if fmt == 'std':
        # Minutos deben ser exactamente 2 dígitos en el original
        if len(m_str) != 2:
            return original
        if not _hora_valida_estandar(h, m):
            return original
        return _normaliza_hm(h, m)

    # --- Formato Hh[MMm] ---
    if fmt == 'hm':
        # Horas: 0-23, Minutos: 0-59
        if not (0 <= h <= 23 and 0 <= m <= 59):
            return original
        # Con partícula: el reloj es de 12 h
        if particula:
            h24 = _aplica_particula(h, particula)
            if h24 is None:
                return original
            h = h24
        return _normaliza_hm(h, m)

    # --- Formato coloquial (en punto / y cuarto / y media / menos cuarto) ---
    if fmt == 'col':
        col = coloquial.strip().lower()
        delta = MINUTOS_COLOQUIALES.get(col)
        if delta is None:
            return original
        # Reloj de 1 a 12
        if h == 0 or h > 12:
            return original

        total_min = h * 60 + delta
        h24_base = total_min // 60
        m_final = total_min % 60

        # Normalizar a 0..11h (el enunciado dice devolver en rango 00:00-11:59)
        h_final = h24_base % 12

        if particula:
            h_ajustada = _aplica_particula(h if delta >= 0 else h, particula)
            if h_ajustada is None:
                return original
            # Recalcular con la hora ajustada
            total_min = h_ajustada * 60 + delta
            if total_min < 0:
                total_min += 24 * 60
            h_final = (total_min // 60) % 24
            m_final = total_min % 60
        else:
            h_final = h_final
            # m_final ya calculado

        return _normaliza_hm(h_final, m_final)

    return original


# ---------------------------------------------------------------------------
# Patrón maestro
# ---------------------------------------------------------------------------

# Partículas horarias (orden importante: más largas primero)
_PAT_PARTICULA = (
    r'(?:'
    r'de\s+la\s+ma[ñn]ana'
    r'|del\s+mediod[ií]a'
    r'|de\s+la\s+tarde'
    r'|de\s+la\s+noche'
    r'|de\s+la\s+madrugada'
    r')'
)

# Expresiones coloquiales
_PAT_COLOQUIAL = r'(?:menos\s+cuarto|en\s+punto|y\s+media|y\s+cuarto)'

# Patrón completo (orden: más específico primero)
PATRON = re.compile(
    r'(?:'
    # 1) Formato coloquial con partícula: "8 y media de la tarde"
    r'(?P<fmt>col)'
    r'(?P<hora_col>\d{1,2})\s+(?P<coloquial>' + _PAT_COLOQUIAL + r')'
    r'(?:\s+(?P<particula_col>' + _PAT_PARTICULA + r'))?'
    r'|'
    # 2) Formato Hh[MMm] con o sin partícula: "8h27m de la mañana" / "8h"
    r'(?P<fmt2>hm)'
    r'(?P<hora_hm>\d{1,2})h(?:(?P<min_hm>\d{1,2})m)?'
    r'(?:\s+(?P<particula_hm>' + _PAT_PARTICULA + r'))?'
    r'|'
    # 3) Formato estándar HH:MM
    r'(?P<fmt3>std)'
    r'(?P<hora_std>\d{1,2}):(?P<min_std>\d{2})'
    r')',
    re.IGNORECASE
)


def _sustituye_v2(match):
    """Callback para re.sub con el patrón unificado de grupos nombrados."""
    original = match.group(0)

    if match.group('fmt'):        # coloquial
        h_str = match.group('hora_col')
        col = match.group('coloquial')
        particula = match.group('particula_col')
        fmt = 'col'
    elif match.group('fmt2'):     # Hh[MMm]
        h_str = match.group('hora_hm')
        m_str = match.group('min_hm')
        particula = match.group('particula_hm')
        fmt = 'hm'
        col = None
    elif match.group('fmt3'):     # estándar
        h_str = match.group('hora_std')
        m_str = match.group('min_std')
        particula = None
        fmt = 'std'
        col = None
    else:
        return original

    try:
        h = int(h_str)
    except (TypeError, ValueError):
        return original

    # ---- estándar ----
    if fmt == 'std':
        if len(m_str) != 2:
            return original
        m = int(m_str)
        if not _hora_valida_estandar(h, m):
            return original
        return _normaliza_hm(h, m)

    # ---- Hh[MMm] ----
    if fmt == 'hm':
        m = int(m_str) if m_str else 0
        if not (0 <= h <= 23 and 0 <= m <= 59):
            return original
        if particula:
            h24 = _aplica_particula(h, particula)
            if h24 is None:
                return original
            h = h24
        return _normaliza_hm(h, m)

    # ---- coloquial ----
    if fmt == 'col':
        col_norm = re.sub(r'\s+', ' ', col.strip().lower())
        delta = MINUTOS_COLOQUIALES.get(col_norm)
        if delta is None:
            return original
        if h == 0 or h > 12:
            return original

        if particula:
            # Para "menos cuarto" la hora base real puede ser h-1
            hora_ref = h if delta >= 0 else h
            h24 = _aplica_particula(hora_ref, particula)
            if h24 is None:
                return original
            total = h24 * 60 + delta
        else:
            total = h * 60 + delta

        if total < 0:
            total += 12 * 60
        h_final = (total // 60) % (24 if particula else 12)
        m_final = total % 60
        return _normaliza_hm(h_final, m_final)

    return original


# ---------------------------------------------------------------------------
# Construcción del patrón con grupos simples (más robusta)
# ---------------------------------------------------------------------------

# Usamos un único patrón con alternativas y capturamos todo lo necesario
# mediante un índice de alternativa.

_PAT_PART = (r'de\s+la\s+ma[ñn]ana|del\s+mediod[ií]a|de\s+la\s+tarde'
             r'|de\s+la\s+noche|de\s+la\s+madrugada')

PATRON_FINAL = re.compile(
    r'(?:'
    # --- A: estándar H:MM o HH:MM ---
    r'(\d{1,2}):(\d{2})'
    r'|'
    # --- B: Hh[MMm] + partícula opcional ---
    r'(\d{1,2})h(?:(\d{1,2})m)?'
    r'(?:\s+(' + _PAT_PART + r'))?'
    r'|'
    # --- C: coloquial + partícula opcional ---
    r'(\d{1,2})\s+(menos\s+cuarto|en\s+punto|y\s+media|y\s+cuarto)'
    r'(?:\s+(' + _PAT_PART + r'))?'
    r'|'
    # --- D: número solo + partícula (ej: "12 de la noche") ---
    r'(\d{1,2})\s+(' + _PAT_PART + r')'
    r')',
    re.IGNORECASE
)


def _cb(m):
    """Callback de sustitución para PATRON_FINAL."""
    original = m.group(0)

    g = m.groups()
    # g[0], g[1]        → estándar  H, MM
    # g[2], g[3], g[4]  → Hh[MMm] [partícula]
    # g[5], g[6], g[7]  → coloquial H, expr, [partícula]
    # g[8], g[9]        → número + partícula (ej: "12 de la noche")

    if g[0] is not None:   # estándar
        h, m_s = int(g[0]), g[1]
        if len(m_s) != 2:
            return original
        mm = int(m_s)
        if not _hora_valida_estandar(h, mm):
            return original
        return _normaliza_hm(h, mm)

    if g[2] is not None:   # Hh[MMm]
        h = int(g[2])
        mm = int(g[3]) if g[3] else 0
        if not (0 <= h <= 23 and 0 <= mm <= 59):
            return original
        if g[4]:
            h24 = _aplica_particula(h, g[4])
            if h24 is None:
                return original
            h = h24
        return _normaliza_hm(h, mm)

    if g[5] is not None:   # coloquial
        h = int(g[5])
        col = re.sub(r'\s+', ' ', g[6].strip().lower())
        delta = MINUTOS_COLOQUIALES.get(col)
        if delta is None:
            return original
        if h == 0 or h > 12:
            return original
        particula = g[7]
        if particula:
            h24 = _aplica_particula(h, particula)
            if h24 is None:
                return original
            total = h24 * 60 + delta
            if total < 0:
                total += 24 * 60
            h_f = (total // 60) % 24
        else:
            total = h * 60 + delta
            if total < 0:
                total += 12 * 60
            h_f = (total // 60) % 12
        mm = total % 60
        return _normaliza_hm(h_f, mm)

    if g[8] is not None:   # número + partícula (sin h, sin coloquial)
        h = int(g[8])
        particula = g[9]
        if h == 0 or h > 12:
            return original
        h24 = _aplica_particula(h, particula)
        if h24 is None:
            return original
        return _normaliza_hm(h24, 0)

    return original


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def normalizaHoras(ficText, ficNorm):
    """
    Lee el fichero de texto ficText, busca expresiones horarias en castellano
    y escribe ficNorm con éstas normalizadas al formato HH:MM.

    Las expresiones incorrectas (hora/minuto fuera de rango, formato inválido)
    se dejan tal cual.
    """
    with open(ficText, encoding='utf-8') as f:
        contenido = f.read()

    normalizado = PATRON_FINAL.sub(_cb, contenido)

    with open(ficNorm, 'w', encoding='utf-8') as f:
        f.write(normalizado)


# ---------------------------------------------------------------------------
# Test rápido
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    import os
    test_lines = [
        "La llegada del tren está prevista a las 18:30",
        "Tenía su clase entre las 8h y las 10h30m",
        "Se acaba a las 4 y media de la tarde",
        "Empieza a trabajar a las 7h de la mañana",
        "Es lo mismo 5 menos cuarto que 4:45",
        "Tenemos descanso hasta las 17h5m",
        "Las campanadas son a las 12 de la noche",
        "Son exactamente las 17:5",
        "Cuando llegó, ya eran las 11 de la tarde",
        "El examen es a las 17 de la tarde",
        "Cenamos en las 7 puertas",
        "No llegará antes de las 1h78m",
        "Corrió la maratón en 32h31m, pero no ganó",
        "Quedamos a las 23 en punto",
    ]

    with open('/tmp/horas_test.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(test_lines) + '\n')

    normalizaHoras('/tmp/horas_test.txt', '/tmp/horas_norm.txt')

    with open('/tmp/horas_norm.txt', encoding='utf-8') as f:
        resultado = f.read()

    print("=== Resultado de normalización ===")
    for orig, norm in zip(test_lines, resultado.strip().split('\n')):
        marca = '✓' if orig != norm else '·'
        print(f"{marca} {norm}")
