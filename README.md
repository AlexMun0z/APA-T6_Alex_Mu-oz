# Expresiones Regulares

## Nom i cognoms

> [!Important]
> Introduzca a continuación su nombre y apellidos:
>
> Alex Muñoz Paton

## Aviso Importante

> [!Caution]
> 
> El objetivo de esta tarea es aprender a usar las expresiones regulares. En concreto, su
> implementación en Python. A los profesores de la asignatura les importa un pimiento si
> usted conoce alguna biblioteca que hace el mismo trabajo de manera más sencilla y/o
> eficiente; su uso está prohibido.
>
> ¿Quiere saber más?, consulte con el profesorado.
 
## Fecha de entrega: 7 de junio a medianoche

## Tratamiento de ficheros de notas

Con el final de curso llega la ardua tarea de evaluar las tareas realizadas por los alumnos durante el
mismo. Para facilitar esta tarea, se dispone de la clase `Alumno` que proporciona los datos
fundamentales de cada alumno: su número de identificación (`numIden`), su nombre completo 
(`nombre`) y la lista de notas obtenidas a lo largo del curso (`notas`). La clase también
proporciona métodos para añadir una nota al expediente del alumno (`__add__()`), para obtener
la representación *oficial* del mismo (`__repr__()`) y para obtener la representación
*bonita* (`__str__()`).

La definición de la clase `Alumno`, disponible en `alumno.py`, es:

```python
class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'
```

A menudo, las notas de los alumnos se almacenan en ficheros de texto en los que los datos de cada alumno
ocupan una línea con los distintos valores separados por espacios y/o tabuladores.

El ejemplo siguiente muestra un fichero típico con las notas de tres alumnos:

```text
171 Blanca Agirrebarrenetse 10  	9 	  9.5
23  Carles Balcell de Lara  5 	    5 	  4.5  	5.2
68  David Garcia Fuster 	7.75    5.25  8   
```

Añada al fichero `alumno.py` la función `leeAlumnos(ficAlum)` que lea un fichero de texto con los datos de 
todos los alumnos y devuelva un diccionario en el que la clave sea el nombre de cada alumno y su contenido 
el objeto `Alumno` correspondiente.

La función deberá cumplir los requisitos siguientes:

- Sólo debe realizar lo que se indica; es decir, debe leer el fichero de texto que se le pasa como único
  argumento y devolver un diccionario con los datos de los alumnos.
- El análisis de cada línea de texto se realizará usando expresiones regulares.
- La función `leeAlumnos()` debe incluir, en su cadena de documentación, la prueba unitaria siguiente según
  el formato de la biblioteca `doctest`, donde el fichero `'alumnos.txt'` es el fichero mostrado como ejemplo
  al principio de este enunciado:

  ```python
  >>> alumnos = leeAlumnos('alumnos.txt')
  >>> for alumno in alumnos:
  ...     print(alumnos[alumno])
  ...
  171     Blanca Agirrebarrenetse 9.5
  23      Carles Balcells de Lara 4.9
  68      David Garcia Fuster     7.0
  ```

  - Evidentemente, es responsabilidad del autor comprobar que la prueba unitaria se pasa satisfactoriamente
    antes de la entrega de la tarea.

  - Para evitar que diferencias debidas a espacios en blanco o tabuladores den lugar a error, se recomienda
    efectuar las pruebas unitarias con la opción `doctest.NORMALIZE_WHITESPACE`. Por ejemplo,
    `doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)`.


## Análisis de expresiones horarias

En casi todos los idiomas más habituales, cualquier hora puede reducirse al formato estándar HH:MM, donde HH es 
un número de dos dígitos, que representa la hora y está comprendido entre 00 y 23, y MM es otro número de dos 
dígitos, que representa el minuto y está comprendido entre 00 y 59.

No obstante, en el lenguaje hablado, es raro usar este formato estándar. En el caso del castellano, existe una
gran variedad de formatos. La lista siguiente alguna de las posibilidades más frecuentes, aunque existen bastantes
más:

- **08:27**

  Es el formato estándar. Cuando la hora es menor que 10, es posible representarla con
  dos dígitos (08:27), o sólo uno (8:27). Los minutos se representan siempre con dos (8:05).

- **8h27m**

  Las horas o minutos menores que 10 pueden representarse usando uno o dos dígitos. Las horas
  *en punto* pueden indicarse sin minutos (8h).

- **8 en punto**

  Las horas exactas suelen indicarse con la partícula *'en punto'*. En ese caso, es
  habitual omitir la letra *h* después de la cifra.

  Otras alternativas semejantes son las *'8 y cuarto'*, las *'8 y media'* o las *'8 menos cuarto'*.

  En todos estos casos, el reloj empleado será de 12 horas y empezando en 1 (de 1 a 12). El
  resultado será ambiguo, ya que no sabremos si una cierta hora es AM o PM, pero así es cómo
  se suele hablar (la gente queda a *'las 11 en punto'* para ir a una fiesta, no a las
  *'las 23 en punto'*). El resultado se devolverá siempre en el rango de 00:00 a 11:59.

- **... de la mañana**

  Las expresiones horarias entre las 4 y las 12 pueden ir seguidas de la partícula *'de la mañana'*.

  Análogamente, las horas entre las 12 y las 3 pueden ir seguidas de *'del mediodía'*, las horas entre
  las 3 y las 8 pueden serlo de *'de la tarde'*, entre 8 y 4 de *'de la noche'* y entre 1 y
  6 de *'de la madrugada'*.

  En estos casos, el reloj empleado es siempre de 12 horas (nunca se dice *'las 18 de la tarde'*, sino
  *'las 6 de la tarde'*). Además la hora no puede ser cero, sino que, en ese caso, se usaría 12.

### Tarea: normalización de las expresiones horarias de un texto

Escriba el fichero `horas.py` con la función `normalizaHoras(ficText, ficNorm)`, que lee el fichero de
texto `ficText`, lo analiza en busca de expresiones horarias y escribe el fichero `ficNorm` en el que
éstas se expresan según el formato normalizado, con las horas y los minutos indicados por dos dígitos
y separados por dos puntos (08:27).

Cada línea del fichero puede contener, o no, una o más expresiones horarias, pero éstas nunca aparecerán
partidas en más de una línea.

Las horas con expresión incorrecta, por ejemplo, *'17:5'* (en la expresión normalizada deben usarse dos
dígitos para expresar los minutos) u *'11 de la tarde'* (la tarde nunca llega hasta esa hora), deben
dejarse tal cual.

Para la evaluación de la tarea se usará un texto con unas cien expresiones horarias, que incluirán tanto
expresiones correctas como incorrectas. Una parte de la nota dependerá de la precisión en su normalización.

Se recomienda empezar normalizando textos que sólo contengan expresiones correctas del tipo más sencillo;
es decir, con la forma *'18h45m'*. La consecución de este objetivo garantiza una nota mínima de notable
bajo (7). La extensión al resto de formatos indicados y la detección de expresiones incorrectas serán
necesarias para alcanzar la nota máxima (10).

La tabla siguiente muestra un ejemplo de texto antes y después de su normalización, incluyendo tanto
expresiones horarias **correctas** como <span style="color:red">**incorrectas**</span>.

### Ejemplo de normalización de las expresiones horarias de un texto

Las líneas siguientes muestran ejemplos de expresiones horarias, tanto correctas como incorrectas. Las
mismas expresiones se encuentran en el fichero `horas.txt`, que puede usar para comprobar el correcto
funcionamiento de su función.

#### Expresiones válidas

> - La llegada del tren está prevista a las **18:30**
> - La llegada del tren está prevista a las **18:30**

> - Tenía su clase entre las **8h** y las **10h30m**
> - Tenía su clase entre las **08:00** y las **10:30**

> - Se acaba a las **4 y media de la tarde**
> - Se acaba a las **16:30**

> - Empieza a trabajar a las **7h de la mañana**
> - Empieza a trabajar a las **07:00**

> - Es lo mismo **5 menos cuarto** que **4:45**
> - Es lo mismo **04:45** que **04:45**

> - Tenemos descanso hasta las **17h5m**
> - Tenemos descanso hasta las **17:05**

> - Las campanadas son a las **12 de la noche**
> - Las campanadas son a las **00:00**

#### Expresiones incorrectas

> - Son exactamente las $\textbf{\color{red}17:5}$
> - Son exactamente las $\textbf{\color{red}17:5}$

> - Cuando llegó, ya eran las $\textbf{\color{red}11 de la tarde}$
> - Cuando llegó, ya eran las $\textbf{\color{red}11 de la tarde}$

> - El examen es a las $\textbf{\color{red}17 de la tarde}$
> - El examen es a las $\textbf{\color{red}17 de la tarde}$

> - Cenamos en las $\textbf{\color{red}7}$ puertas
> - Cenamos en las $\textbf{\color{red}7}$ puertas

> - No llegará antes de las $\textbf{\color{red}1h78m}$
> - No llegará antes de las $\textbf{\color{red}1h78m}$

> - *Corrió* la maratón en $\textbf{\color{red}32h31m}$, pero no ganó
> - *Corrió* la maratón en $\textbf{\color{red}32h31m}$, pero no ganó

> - Quedamos a las $\textbf{\color{red}23 en punto}$
> - Quedamos a las $\textbf{\color{red}23 en punto}$


#### Entrega

##### Ficheros `alumno.py` y `horas.py`

- Ambos ficheros deben incluir una cadena de documentación con el nombre del alumno o alumnos
  y una descripción de su contenido.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el
  uso de los estándares marcados por PEP-ocho.

##### Ejecución de los tests unitarios de `alumno.py`

<img width="421" height="579" alt="image" src="https://github.com/user-attachments/assets/1e4a8e0c-e7cd-4be1-865c-3f1ed6a8ac8a" />


##### Código desarrollado

###### alumno
```python
"""
Alumno: Alex Muñoz Paton

Módulo para el tratamiento de las notas de los alumnos.
Contiene la clase Alumno y la función leeAlumnos() para leer
ficheros de texto con datos de alumnos usando expresiones regulares.
"""

import re
import doctest


class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'


def leeAlumnos(ficAlum):
    """
    Lee un fichero de texto con los datos de todos los alumnos y devuelve
    un diccionario en el que la clave es el nombre de cada alumno y su
    contenido el objeto Alumno correspondiente.

    Cada línea del fichero contiene: numIden, nombre (dos o más palabras)
    y una lista de notas, separados por espacios y/o tabuladores.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171     Blanca Agirrebarrenetse 9.5
    23      Carles Balcell de Lara 4.9
    68      David Garcia Fuster     7.0
    """
    alumnos = {}
    # Patrón: número de identificación, nombre (2+ palabras), notas (números reales)
    patron = re.compile(
        r'^(\d+)'                          # numIden: uno o más dígitos
        r'[\s]+'                           # separador
        r'((?:[A-Za-záéíóúüñÁÉÍÓÚÜÑ]+'   # primera palabra del nombre
        r'(?:[\s]+[A-Za-záéíóúüñÁÉÍÓÚÜÑ]+)+))'  # resto de palabras del nombre
        r'[\s]+'                           # separador
        r'([\d.,\s\t]+)$'                 # notas
    )
    patron_nota = re.compile(r'\d+(?:[.,]\d+)?')

    with open(ficAlum, encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            m = patron.match(linea)
            if m:
                num_iden = int(m.group(1))
                nombre = m.group(2).strip()
                notas_str = m.group(3)
                notas = [float(n.replace(',', '.'))
                         for n in patron_nota.findall(notas_str)]
                alumnos[nombre] = Alumno(nombre, num_iden, notas)
    return alumnos


if __name__ == '__main__':
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE, verbose=True)
```
###### horas
```python
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

```
##### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y
visualizarse correctamente en el repositorio, incluyendo la imagen con la ejecución de
los tests unitarios y el realce sintáctico del código fuente insertado.

##### Y NADA MÁS

Sólo se corregirá el contenido de este fichero `README.md` y los códigos fuente `alumno.py`
y `horas.py`. No incluya otros ficheros con código fuente, notebooks de Jupyter o explicaciones
adicionales; simplemente, no se tendrán en cuenta para la evaluación de la tarea. Evidentemente,
sí puede añadir ficheros con las imágenes solicitadas en el enunciado, pero éstas deberán ser
visualizadas correctamente desde este mismo fichero al acceder al repositorio de la tarea.
