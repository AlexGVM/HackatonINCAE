"""Zonas adicionales de La Pulpería, 640 x 360, dibujadas con Pygame.

Ninguna imagen externa. Las figuras utilizan píxeles enteros y una paleta
coherente con interior.py. Todas las posiciones están en píxeles lógicos.
"""
import pygame

from fuentes import FuenteTienda

from productos import FRUTAS, VERDURAS, BEBIDAS, ABARROTES, dibujar_producto, tamano

WIDTH, HEIGHT = 640, 360
EXTERIOR_FLOOR_TOP = 150
INVENTARIO_FLOOR_TOP = 96

WALL_RAYA = (100, 111, 69)   # rayas de la pared de la bodega

# Colores compartidos (escenario GBA).
INK = (48, 39, 43)
DARK = (67, 46, 44)
WOOD = (128, 79, 57)
WOOD_LIGHT = (175, 111, 75)
WOOD_TOP = (195, 138, 91)
CREAM = (232, 215, 171)
RED = (184, 94, 83)
RED_DARK = (122, 65, 63)
TEAL = (119, 160, 151)
TEAL_DARK = (72, 116, 114)
GLASS = (175, 209, 207)
GREEN = (100, 145, 83)
GREEN_DARK = (59, 109, 72)
GREEN_LIGHT = (149, 173, 103)
YELLOW = (223, 180, 91)
BLUE = (83, 125, 155)
WALL = (132, 137, 87)
WALL_LIGHT = (160, 165, 106)
FLOOR_A = (155, 163, 145)
FLOOR_B = (116, 133, 121)
FLOOR_LINE = (77, 92, 82)


# Las zonas son independientes de los muebles móviles de la sala.
# Umbrales en coordenadas lógicas 640 x 360. El cambio es automático al cruzarlos.
# Puerta a la calle: centrada en el pasillo entre la góndola de abajo
# (termina en x = 236) y la heladera (empieza en x = 330).
PUERTA_SALA_X = 283
SALA_A_ENTRADA = pygame.Rect(PUERTA_SALA_X - 39, 316, 78, 44)
SALA_A_INVENTARIO = pygame.Rect(591, 100, 49, 97)
ENTRADA_A_SALA = pygame.Rect(281, 151, 78, 42)
INVENTARIO_A_SALA = pygame.Rect(0, 250, 110, 105)


def acceso_actual(zona, player):
    """Indica el destino de la puerta cercana, o None."""
    p = (player.x, player.y)
    if zona == "interior":
        if SALA_A_ENTRADA.collidepoint(p):
            return "entrada"
        if SALA_A_INVENTARIO.collidepoint(p):
            return "inventario"
    elif zona == "entrada" and ENTRADA_A_SALA.collidepoint(p):
        return "interior"
    elif zona == "inventario" and INVENTARIO_A_SALA.collidepoint(p):
        return "interior"
    return None


# Cruces dentro de los pasillos dibujados. Solo importan los pies del personaje.
# Se usan coordenadas anteriores y posteriores para evitar rebotes instantáneos
# al aparecer en la otra pantalla.
SALA_SALIDA_Y = 338
ENTRADA_PUERTA_Y = 192
SALA_BODEGA_X = 611
INVENTARIO_SALIDA_X = 57
# Alto de cada paso, a lo largo del borde de la pantalla (más grande que antes
# para que se cruce aunque el personaje no vaya justo por el centro).
PASO_BODEGA_Y = (100, 196)
PASO_SALA_Y = (258, 350)


def destino_al_cruzar(zona, antes, despues):
    """Devuelve la nueva zona solo si se cruza el umbral en dirección correcta.

    antes y despues: (x, y) del punto de apoyo (pies) en píxeles lógicos.
    No modifica las coordenadas ni consume E.
    """
    x0, y0 = antes
    x1, y1 = despues

    if zona == "interior":
        # Sala -> calle: caminar hacia el borde inferior por la alfombrilla.
        if y0 < SALA_SALIDA_Y <= y1 and PUERTA_SALA_X - 31 <= x1 <= PUERTA_SALA_X + 31:
            return "entrada"
        # Sala -> bodega: cruzar hacia la derecha frente a la puerta.
        if x0 < SALA_BODEGA_X <= x1 and PASO_BODEGA_Y[0] <= y1 <= PASO_BODEGA_Y[1]:
            return "inventario"

    elif zona == "entrada":
        # Calle -> sala: caminar hacia arriba por el sendero central.
        if y0 > ENTRADA_PUERTA_Y >= y1 and 298 <= x1 <= 343:
            return "interior"

    elif zona == "inventario":
        # Bodega -> sala: caminar hacia la izquierda por la puerta baja.
        if x0 > INVENTARIO_SALIDA_X >= x1 and PASO_SALA_Y[0] <= y1 <= PASO_SALA_Y[1]:
            return "interior"

    return None


def _label(surface, text, x, y, size=16, color=CREAM, center=False):
    font = FuenteTienda(None, size)
    letters = font.render(text, False, color)
    rect = letters.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(letters, rect)


def _tile_floor(surface, top=96, size=32):
    pygame.draw.rect(surface, FLOOR_A, (0, top, WIDTH, HEIGHT - top))
    for row in range((HEIGHT - top + size - 1) // size):
        for col in range((WIDTH + size - 1) // size):
            r = pygame.Rect(col * size, top + row * size, size, size)
            pygame.draw.rect(surface, FLOOR_A if (row + col) % 2 == 0 else FLOOR_B, r)
            pygame.draw.rect(surface, FLOOR_LINE, r, 1)
    for x, y in [(92, 201), (271, 341), (587, 296), (351, 141), (456, 250)]:
        pygame.draw.rect(surface, FLOOR_B, (x, y, 4, 2))


def _tree(surface, x, y, crown=1):
    """Árbol con copa de bloques GBA; x/y es la base del tronco."""
    s = crown
    pygame.draw.rect(surface, (75, 67, 51), (x - 10*s, y - 10*s, 26*s, 8*s))
    pygame.draw.rect(surface, WOOD, (x - 5*s, y - 43*s, 12*s, 38*s))
    pygame.draw.rect(surface, WOOD_LIGHT, (x - 3*s, y - 41*s, 3*s, 28*s))
    for dx, dy, w, h, col in [
        (-33, -85, 59, 42, GREEN_DARK),
        (-41, -69, 70, 37, GREEN_DARK),
        (-29, -101, 48, 34, GREEN_DARK),
        (-28, -87, 50, 29, GREEN),
        (-34, -66, 57, 24, GREEN),
        (-20, -96, 32, 22, GREEN_LIGHT),
        (-30, -73, 22, 14, GREEN_LIGHT),
        (4, -83, 15, 12, GREEN_LIGHT),
    ]:
        pygame.draw.rect(surface, col, (x+dx*s, y+dy*s, w*s, h*s))
    # Sombras pixeladas en hojas.
    for ox, oy in [(-19, -54), (8, -48), (-34, -61)]:
        pygame.draw.rect(surface, GREEN_DARK, (x+ox*s, y+oy*s, 10*s, 5*s))


def _bush(surface, x, y):
    pygame.draw.rect(surface, GREEN_DARK, (x, y + 7, 42, 16))
    pygame.draw.rect(surface, GREEN, (x + 5, y, 30, 19))
    pygame.draw.rect(surface, GREEN_LIGHT, (x + 9, y + 2, 10, 5))
    pygame.draw.rect(surface, GREEN_LIGHT, (x + 24, y + 5, 8, 5))
    pygame.draw.rect(surface, YELLOW, (x + 17, y + 13, 4, 4))


def _vidrio(surface, r, que):
    """Interior de la tienda visto por un vidrio, con el vidrio encima."""
    pygame.draw.rect(surface, (126, 134, 98), r)                       # pared de adentro
    pygame.draw.rect(surface, (110, 86, 70), (r.x, r.bottom - 7, r.w, 7))   # piso
    if que == "refris":
        for fx in (r.x + 4, r.x + 34):
            pygame.draw.rect(surface, (70, 76, 84), (fx, r.y + 3, 27, r.h - 5))
            pygame.draw.rect(surface, (196, 210, 214), (fx + 2, r.y + 5, 23, r.h - 10))
            for fila, colores in enumerate(((RED, YELLOW, RED, GREEN), (BLUE, BLUE, RED, YELLOW))):
                for i, c in enumerate(colores):
                    pygame.draw.rect(surface, c, (fx + 4 + i * 5, r.y + 8 + fila * 9, 3, 6))
    elif que == "gondolas":
        pygame.draw.rect(surface, (120, 78, 54), (r.x + 4, r.y + 4, r.w - 8, 6))     # repisa del fondo
        for i, c in enumerate((BLUE, RED, (236, 236, 226), GREEN, BLUE, RED, YELLOW, GREEN, BLUE)):
            pygame.draw.rect(surface, c, (r.x + 7 + i * 6, r.y + 1, 4, 4))
        pygame.draw.rect(surface, (128, 82, 58), (r.x + 6, r.bottom - 15, r.w - 12, 9))   # góndola
        for i, c in enumerate((RED, RED, YELLOW, YELLOW, (232, 140, 50), (232, 140, 50),
                               (130, 70, 150), (130, 70, 150))):
            pygame.draw.circle(surface, c, (r.x + 10 + i * 7, r.bottom - 16), 3)
    else:  # puerta: se ve el mostrador
        pygame.draw.rect(surface, (128, 82, 58), (r.x + 3, r.bottom - 10, r.w - 6, 7))
        pygame.draw.rect(surface, (176, 52, 44), (r.x + 24, r.bottom - 14, 6, 4))
    # El vidrio: un velo celeste translúcido y reflejos.
    velo = pygame.Surface(r.size, pygame.SRCALPHA)
    velo.fill((180, 220, 232, 95))
    for k in range(0, r.w + r.h, 26):
        pygame.draw.line(velo, (255, 255, 255, 110), (k, 0), (k - 10, r.h), 2)
    surface.blit(velo, r.topleft)


def _ventana_tienda(surface, x, que):
    pygame.draw.rect(surface, DARK, (x, 112, 75, 38))
    pygame.draw.rect(surface, WOOD_LIGHT, (x - 2, 148, 79, 4))      # repisita
    _vidrio(surface, pygame.Rect(x + 4, 116, 67, 30), que)
    pygame.draw.line(surface, DARK, (x + 37, 116), (x + 37, 145), 3)


NOMBRE_CARTEL = "LA PULPERIA"      # el del menú (y si no se escogió otro)
CARTEL_MAX = 20                    # letras que caben en el cartel
CARTEL_ANCHO_MIN, CARTEL_ANCHO_MAX = 148, 236


def _lineas_cartel(texto, fuente, ancho):
    """Parte el nombre en 2 renglones parejos (por un espacio si hay)."""
    espacios = [i for i, c in enumerate(texto) if c == " "]
    if espacios:
        mitad = len(texto) / 2
        i = min(espacios, key=lambda k: abs(k - mitad))
        return [texto[:i].strip(), texto[i + 1:].strip()]
    i = (len(texto) + 1) // 2
    return [texto[:i] + "-", texto[i:]]


def medidas_cartel(nombre):
    """(renglones, tamaño de letra, ancho del cartel, alto) para que el
    nombre quepa bien: primero en un renglón (letra más chica si hace falta)
    y si no, en dos."""
    texto = " ".join((nombre or NOMBRE_CARTEL).upper().split())[:CARTEL_MAX] or NOMBRE_CARTEL
    for tam in (25, 23, 21, 19, 17):
        w = FuenteTienda(None, tam).size(texto)[0]
        if w + 14 <= CARTEL_ANCHO_MAX:
            return [texto], tam, max(CARTEL_ANCHO_MIN, w + 18), 29
    for tam in (17, 16, 15, 14, 13, 12):
        f = FuenteTienda(None, tam)
        lineas = _lineas_cartel(texto, f, CARTEL_ANCHO_MAX)
        w = max(f.size(l)[0] for l in lineas)
        if w + 14 <= CARTEL_ANCHO_MAX:
            alto = 2 * f.get_height() + 6
            return lineas, tam, max(CARTEL_ANCHO_MIN, w + 18), max(29, alto)
    f = FuenteTienda(None, 12)
    return _lineas_cartel(texto, f, CARTEL_ANCHO_MAX), 12, CARTEL_ANCHO_MAX, 2 * f.get_height() + 6


def dibujar_cartel(surface, nombre, cx=320, abajo=78):
    """El cartel de madera del techo con el nombre de la pulpería, centrado.
    Crece a lo ancho (y hacia arriba con 2 renglones) según el nombre."""
    lineas, tam, ancho, alto = medidas_cartel(nombre)
    marco = pygame.Rect(0, 0, ancho, alto)
    marco.midbottom = (cx, abajo)
    pygame.draw.rect(surface, DARK, marco)
    pygame.draw.rect(surface, WOOD, marco.inflate(-8, -6))
    fuente = FuenteTienda(None, tam)
    alto_linea = fuente.get_height()
    y0 = marco.centery - alto_linea * len(lineas) / 2
    for i, linea in enumerate(lineas):
        letras = fuente.render(linea, False, CREAM)
        surface.blit(letras, letras.get_rect(center=(cx, round(y0 + alto_linea * (i + 0.5)))))
    return marco


def dibujar_entrada(surface, etiqueta=True, nombre=None):
    """Exterior de la pulpería: fachada, árboles, acera y calle.
    nombre: el que escogió el niño para el cartel (None: LA PULPERIA)."""
    surface.fill((132, 179, 217))

    # Cielo, nubes de bloques y siluetas de cerros.
    for x, y in [(51, 29), (525, 17), (566, 52)]:
        pygame.draw.rect(surface, (244, 237, 205), (x, y + 9, 59, 14))
        pygame.draw.rect(surface, (244, 237, 205), (x + 13, y, 35, 30))
    pygame.draw.polygon(surface, (75, 116, 160),
                        [(0, 133), (0, 95), (71, 62), (130, 105), (198, 76),
                         (260, 120), (377, 73), (480, 124), (574, 68), (640, 105), (640, 145)])

    # Jardín, acera, carretera y pasos de peatones.
    pygame.draw.rect(surface, (118, 152, 93), (0, 144, 640, 99))
    pygame.draw.rect(surface, (91, 124, 78), (0, 230, 640, 13))
    pygame.draw.rect(surface, (176, 178, 154), (0, 200, 640, 45))
    for px in range(0, 640, 34):
        pygame.draw.line(surface, (124, 137, 121), (px, 201), (px, 241), 1)
    pygame.draw.rect(surface, (98, 107, 116), (0, 245, 640, 90))
    pygame.draw.rect(surface, (67, 79, 91), (0, 245, 640, 5))
    pygame.draw.rect(surface, (68, 79, 86), (0, 329, 640, 6))
    for px in range(22, 640, 78):
        pygame.draw.rect(surface, (235, 209, 129), (px, 288, 37, 4))
    pygame.draw.rect(surface, (166, 169, 149), (0, 335, 640, 25))
    for px in range(0, 640, 54):
        pygame.draw.line(surface, (129, 137, 128), (px, 336), (px, 358), 1)
    # Paso peatonal a la pulpería.
    for py in range(252, 327, 17):
        pygame.draw.rect(surface, (224, 220, 199), (292, py, 57, 9))
    # Sendero hacia la puerta y pequeñas piedras.
    pygame.draw.rect(surface, (204, 186, 145), (292, 151, 57, 50))
    for py in (158, 172, 186):
        pygame.draw.line(surface, (155, 137, 111), (295, py), (346, py), 1)

    # Edificio con fachada tejada y ventanas.
    pygame.draw.rect(surface, (63, 54, 50), (172, 83, 299, 80))
    pygame.draw.rect(surface, TEAL_DARK, (178, 86, 287, 74))
    pygame.draw.rect(surface, TEAL, (182, 89, 278, 68))
    for px in range(183, 457, 20):
        pygame.draw.rect(surface, TEAL_DARK, (px, 93, 2, 64))
    # Techo volumétrico sin suavizado.
    pygame.draw.polygon(surface, RED_DARK,
                        [(153, 91), (320, 26), (488, 91), (488, 101), (153, 101)])
    pygame.draw.polygon(surface, RED,
                        [(162, 89), (320, 35), (480, 89), (480, 97), (162, 97)])
    for px in range(166, 478, 21):
        pygame.draw.line(surface, RED_DARK, (px, 91), (px + 9, 97), 2)
    pygame.draw.rect(surface, DARK, (172, 99, 300, 8))

    # Cartel y toldos.
    dibujar_cartel(surface, nombre)
    # Ventanas translúcidas: se ven los muebles de adentro.
    _ventana_tienda(surface, 192, "refris")
    _ventana_tienda(surface, 369, "gondolas")
    # Puerta (coincide con ENTRADA_A_SALA): debajo de la viga del techo,
    # no más alta que la pared.
    pygame.draw.rect(surface, DARK, (289, 110, 64, 50))
    pygame.draw.rect(surface, (118, 83, 59), (294, 114, 54, 42))
    pygame.draw.rect(surface, (90, 62, 46), (294, 114, 54, 2))
    _vidrio(surface, pygame.Rect(301, 118, 40, 22), "puerta")
    pygame.draw.rect(surface, YELLOW, (336, 143, 4, 5))
    pygame.draw.rect(surface, WOOD_LIGHT, (287, 156, 68, 6))
    # Dos macetas en la entrada.
    for x in (270, 360):
        pygame.draw.rect(surface, WOOD, (x, 163, 13, 12))
        pygame.draw.rect(surface, GREEN_DARK, (x + 3, 153, 7, 14))
        pygame.draw.rect(surface, GREEN_LIGHT, (x - 1, 155, 8, 7))

    # Jardines y árboles, dejando libre el pasillo del centro.
    _tree(surface, 87, 194)
    _tree(surface, 548, 195)
    _bush(surface, 192, 180)
    _bush(surface, 415, 180)
    for x, y in [(38, 218), (162, 190), (243, 219), (389, 220), (595, 226)]:
        pygame.draw.rect(surface, (237, 207, 123), (x, y, 3, 3))
        pygame.draw.rect(surface, (211, 109, 108), (x+4, y+3, 3, 3))
    # Nombre de zona sobre etiqueta de madera.
    if etiqueta:
        pygame.draw.rect(surface, DARK, (12, 12, 108, 23))
        pygame.draw.rect(surface, WOOD, (15, 15, 102, 17))
        _label(surface, "ENTRADA", 66, 23, 18, center=True)


# ---------------------------------------------------------
# BODEGA: repisas de varilla de metal (3 pisos), dos refris y una huevera
# ---------------------------------------------------------
# 3 columnas de 3 repisas cada una. Cada piso guarda 8 unidades de un
# producto. Las de frutas y verduras tienen canastos.
SLOTS_POR_PISO = 8
REPISA_W, REPISA_H = 118, 46
PISO_H = 15                      # alto de cada piso de la repisa
COLUMNAS_REPISAS = (120, 262, 404)
FILAS_REPISAS = (140, 214, 288)
# Qué va en cada piso (de arriba a abajo), por columna y fila.
CONTENIDO_REPISAS = {
    0: [["manzana", "banano", "naranja"], ["uvas", "manzana", "banano"],
        ["naranja", "uvas", "manzana"]],
    1: [["zanahoria", "tomate", "brocoli"], ["elote", "zanahoria", "tomate"],
        ["brocoli", "elote", "zanahoria"]],
    2: [["harina", "azucar", "arroz"], ["frijoles", "harina", "azucar"],
        ["arroz", "frijoles", "leche"]],
}
CON_CANASTOS = (0, 1)            # columnas de frutas y verduras

# Dos refris para gaseosas (3 pisos de 8 botellas) y una huevera grande.
REFRIS_BODEGA = [
    (170, 30, ["cola", "naranjada", "limonada"]),
    (246, 30, ["agua", "fresa", "agua"]),
]
REFRI_W, REFRI_H = 66, 82
HUEVERA_BODEGA = (330, 62)       # bandeja de 4 filas x 8 huevos
HUEVERA_W, HUEVERA_H = 110, 50
HUEVERA_FILAS, HUEVERA_COLS = 4, 8
# Congelador de helados: 2 filas de paletas y 2 de conos (8 cada fila).
CONGELADOR_BODEGA = (452, 58)
CONGELADOR_W, CONGELADOR_H = 104, 54
CONGELADOR_FILAS = ["paleta", "paleta", "cono", "cono"]


# Armario de ropa (cosméticos), contra la pared derecha.
ARMARIO = pygame.Rect(584, 150, 46, 66)
ARMARIO_ACTIVO = True       # OPCIONES > EXTRAS > PERSONALIZACIÓN
AVISOS_ACTIVOS = True       # OPCIONES > GRÁFICOS > AVISOS DE ABAJO


def _armario(surface):
    if not ARMARIO_ACTIVO:
        return
    x, y, w, h = ARMARIO
    pygame.draw.rect(surface, (49, 35, 34), (x + 3, y + h, w - 4, 3))
    pygame.draw.rect(surface, DARK, (x, y, w, h))
    pygame.draw.rect(surface, WOOD_TOP, (x + 2, y + 2, w - 4, 6))
    for px in (x + 3, x + w // 2 + 1):
        pygame.draw.rect(surface, WOOD, (px, y + 10, w // 2 - 4, h - 14))
        pygame.draw.rect(surface, WOOD_LIGHT, (px + 2, y + 12, w // 2 - 8, 2))
    pygame.draw.line(surface, DARK, (x + w // 2, y + 10), (x + w // 2, y + h - 4), 2)
    for px in (x + w // 2 - 4, x + w // 2 + 3):
        pygame.draw.rect(surface, YELLOW, (px, y + 34, 2, 5))
    # Ganchito con una camisa en el letrero de arriba
    pygame.draw.rect(surface, CREAM, (x + w // 2 - 9, y - 9, 18, 11))
    pygame.draw.rect(surface, DARK, (x + w // 2 - 9, y - 9, 18, 11), 1)
    cx = x + w // 2
    pygame.draw.polygon(surface, RED, [(cx - 6, y - 5), (cx - 2, y - 7), (cx + 2, y - 7),
                                       (cx + 6, y - 5), (cx + 4, y - 3), (cx + 3, y - 4),
                                       (cx + 3, y), (cx - 3, y), (cx - 3, y - 4), (cx - 4, y - 3)])


def repisas_bodega():
    """[(x, y, columna, [productos por piso])] de las 9 repisas."""
    return [(x, y, c, CONTENIDO_REPISAS[c][f])
            for c, x in enumerate(COLUMNAS_REPISAS) for f, y in enumerate(FILAS_REPISAS)]


def _y_piso(y, piso):
    """Línea donde se apoyan los productos de ese piso (0 = el de arriba)."""
    return y + PISO_H * (piso + 1)


def productos_repisa(x, y, pisos):
    posiciones = []
    paso = (REPISA_W - 12) / SLOTS_POR_PISO
    for piso, tipo in enumerate(pisos):
        pw, ph = tamano(tipo)
        base = _y_piso(y, piso) - 1
        for i in range(SLOTS_POR_PISO):
            px = round(x + 6 + i * paso + (paso - pw) / 2)
            posiciones.append((tipo, px, base - ph))
    return posiciones


def productos_refri(x, y, pisos):
    posiciones = []
    for piso, tipo in enumerate(pisos):
        pw, ph = tamano(tipo)
        base = y + 37 + piso * 15
        for i in range(SLOTS_POR_PISO):
            posiciones.append((tipo, x + 9 + i * 6 + (5 - pw) // 2, base - ph))
    return posiciones


def productos_huevera(x, y):
    pw, ph = tamano("huevos")
    return [("huevos", x + 7 + c * 12 + (9 - pw) // 2, y + 2 + f * 7)
            for f in range(HUEVERA_FILAS) for c in range(HUEVERA_COLS)]


def productos_congelador(x, y):
    posiciones = []
    for fila, tipo in enumerate(CONGELADOR_FILAS):
        pw, ph = tamano(tipo)
        for c in range(8):
            posiciones.append((tipo, x + 6 + c * 12 + (9 - pw) // 2, y + 3 + fila * 10 + (9 - ph)))
    return posiciones


def _congelador(surface, x, y):
    """Congelador horizontal blanco con vidrio escarchado."""
    w, h = CONGELADOR_W, CONGELADOR_H
    pygame.draw.rect(surface, (49, 35, 34), (x + 3, y + h, w - 6, 3))
    pygame.draw.rect(surface, (150, 160, 170), (x, y, w, h))
    pygame.draw.rect(surface, (236, 240, 244), (x + 2, y + 2, w - 4, h - 4))
    pygame.draw.rect(surface, (196, 226, 242), (x + 4, y + 3, w - 8, 41))
    pygame.draw.line(surface, (160, 196, 220), (x + 5, y + 23), (x + w - 6, y + 23), 1)
    pygame.draw.rect(surface, (70, 120, 170), (x + w // 2 - 22, y + h - 9, 44, 6))


def stock_inicial_bodega():
    """Todos los productos que hay en la bodega al empezar el juego."""
    stock = []
    for x, y, _, pisos in repisas_bodega():
        stock += productos_repisa(x, y, pisos)
    for x, y, pisos in REFRIS_BODEGA:
        stock += productos_refri(x, y, pisos)
    stock += productos_huevera(*HUEVERA_BODEGA)
    stock += productos_congelador(*CONGELADOR_BODEGA)
    return stock


# Colores de las repisas de metal y los canastos
METAL = (150, 158, 166)
METAL_CLARO = (204, 210, 216)
METAL_OSCURO = (74, 80, 90)
MIMBRE = (196, 150, 92)
MIMBRE_CLARO = (226, 186, 124)
MIMBRE_OSCURO = (128, 88, 52)


def _repisa(surface, x, y, canastos=False):
    """Repisa de varilla de metal de tres pisos (sin productos)."""
    w, h = REPISA_W, REPISA_H
    pygame.draw.rect(surface, (58, 50, 50), (x + 3, y + h - 2, w - 2, 4))      # sombra
    # Fondo de rejilla (se ve entre los productos)
    for gx in range(x + 6, x + w - 4, 6):
        pygame.draw.line(surface, (96, 104, 112), (gx, y + 2), (gx, y + h - 2), 1)
    for piso in range(3):
        yy = _y_piso(y, piso)
        # Varillas del piso
        pygame.draw.rect(surface, METAL_OSCURO, (x + 2, yy - 1, w - 4, 3))
        pygame.draw.line(surface, METAL_CLARO, (x + 3, yy - 1), (x + w - 4, yy - 1), 1)
        if canastos:
            pygame.draw.rect(surface, MIMBRE_OSCURO, (x + 4, yy - 9, w - 8, 8))
            pygame.draw.rect(surface, MIMBRE, (x + 5, yy - 8, w - 10, 6))
    # Varilla de arriba y postes
    pygame.draw.rect(surface, METAL_OSCURO, (x, y, w, 3))
    pygame.draw.line(surface, METAL_CLARO, (x + 1, y), (x + w - 2, y), 1)
    for px in (x, x + w - 3):
        pygame.draw.rect(surface, METAL_OSCURO, (px, y, 3, h + 2))
        pygame.draw.line(surface, METAL_CLARO, (px + 1, y + 1), (px + 1, y + h), 1)


def _frente_repisa(surface, x, y):
    """Borde delantero de los canastos: tapa la parte de abajo de las frutas."""
    for piso in range(3):
        yy = _y_piso(y, piso)
        pygame.draw.rect(surface, MIMBRE_OSCURO, (x + 4, yy - 5, REPISA_W - 8, 5))
        pygame.draw.rect(surface, MIMBRE_CLARO, (x + 5, yy - 4, REPISA_W - 10, 1))
        for tx in range(x + 7, x + REPISA_W - 6, 5):
            pygame.draw.line(surface, MIMBRE, (tx, yy - 3), (tx + 2, yy - 1), 1)


def _refri(surface, x, y):
    w, h = REFRI_W, REFRI_H
    pygame.draw.rect(surface, (49, 35, 34), (x + 3, y + h, w - 6, 3))
    pygame.draw.rect(surface, DARK, (x, y, w, h))
    pygame.draw.rect(surface, (196, 204, 210), (x + 3, y + 3, w - 6, h - 6))
    pygame.draw.rect(surface, RED_DARK, (x + 5, y + 5, w - 10, 9))
    pygame.draw.rect(surface, RED, (x + 7, y + 7, w - 14, 5))
    pygame.draw.rect(surface, DARK, (x + 5, y + 18, w - 10, h - 24))
    pygame.draw.rect(surface, GLASS, (x + 7, y + 20, w - 14, h - 28))
    for piso in range(3):
        yy = y + 37 + piso * 15
        pygame.draw.rect(surface, (120, 140, 146), (x + 7, yy, w - 14, 2))


def _frente_refri(surface, x, y):
    """Reflejo del vidrio por encima de las botellas."""
    w, h = REFRI_W, REFRI_H
    pygame.draw.line(surface, (236, 246, 246), (x + 10, y + 22), (x + 18, y + 22 + 20), 1)
    pygame.draw.line(surface, (236, 246, 246), (x + 42, y + 22), (x + 52, y + 22 + 24), 1)
    pygame.draw.rect(surface, DARK, (x + 5, y + 18, w - 10, h - 24), 2)
    pygame.draw.rect(surface, DARK, (x + 2, y + h - 6, w - 4, 4))


def _huevera_grande(surface, x, y):
    w, h = HUEVERA_W, HUEVERA_H
    top = 32
    pygame.draw.rect(surface, (49, 35, 34), (x + 3, y + h, w - 6, 3))
    pygame.draw.rect(surface, DARK, (x, y - 2, w, top + 4))
    pygame.draw.rect(surface, (150, 124, 90), (x + 2, y, w - 4, top))
    pygame.draw.rect(surface, (214, 192, 150), (x + 3, y + 1, w - 6, top - 2))
    for f in range(HUEVERA_FILAS):
        for c in range(HUEVERA_COLS):
            pygame.draw.ellipse(surface, (176, 150, 108), (x + 6 + c * 12, y + 5 + f * 7, 10, 6))
    pygame.draw.rect(surface, DARK, (x, y + top, w, h - top))
    pygame.draw.rect(surface, WOOD, (x + 3, y + top + 2, w - 6, h - top - 5))
    pygame.draw.rect(surface, CREAM, (x + w // 2 - 22, y + top + 4, 44, 9))
    for i in range(4):
        pygame.draw.ellipse(surface, (250, 240, 216), (x + w // 2 - 18 + i * 10, y + top + 5, 5, 7))
        pygame.draw.ellipse(surface, (176, 150, 108), (x + w // 2 - 18 + i * 10, y + top + 5, 5, 7), 1)


def dibujar_frente_cajas(surface):
    """Lo que va por delante de los productos: borde de los canastos y vidrio
    de los refris (se dibuja después de los productos de la bodega)."""
    for x, y, columna, _ in repisas_bodega():
        if columna in CON_CANASTOS:
            _frente_repisa(surface, x, y)
    for x, y, _ in REFRIS_BODEGA:
        _frente_refri(surface, x, y)


class paleta_bodega:
    """Colores elegidos en AJUSTES VISUALES, también para la bodega."""

    def __init__(self, *partes):
        self.partes = partes

    def __enter__(self):
        import interior as I
        self.antes = {}
        for parte in self.partes:
            base = I.color_base(parte)
            if base is None:
                continue
            if parte == "paredes":
                tonos = {"WALL": base, "WALL_LIGHT": I._claro(base, 0.18), "WALL_RAYA": I._oscuro(base, 0.2)}
            elif parte == "piso":
                if I.valor_elegido("piso") == "BLANCO Y NEGRO":
                    tonos = {"FLOOR_A": (236, 236, 232), "FLOOR_B": (36, 36, 40), "FLOOR_LINE": (120, 120, 124)}
                else:
                    tonos = {"FLOOR_A": base, "FLOOR_B": I._oscuro(base, 0.22),
                             "FLOOR_LINE": I._oscuro(base, 0.42)}
            else:   # muebles o alfombras: madera
                tonos = {"WOOD": base, "WOOD_LIGHT": I._claro(base, 0.25),
                         "WOOD_TOP": I._claro(base, 0.35), "DARK": I._oscuro(base, 0.5)}
            for nombre, color in tonos.items():
                self.antes.setdefault(nombre, globals()[nombre])
                globals()[nombre] = color
        return self

    def __exit__(self, *args):
        globals().update(self.antes)
        return False


def dibujar_inventario(surface):
    """Almacén con pasillos, cajas, estanterías y piso transitable."""
    with paleta_bodega("paredes"):
        surface.fill(WALL)
    with paleta_bodega("piso"):
        _tile_floor(surface, INVENTARIO_FLOOR_TOP)
    with paleta_bodega("paredes"):
        _pared_bodega(surface)
    with paleta_bodega("muebles"):
        _muebles_bodega(surface)
    with paleta_bodega("alfombras"):
        _alfombra_bodega(surface)


def _pared_bodega(surface):
    pygame.draw.rect(surface, WALL, (0, 0, WIDTH, 96))
    for px in range(0, WIDTH, 16):
        pygame.draw.rect(surface, WALL_RAYA, (px, 0, 2, 68))
        pygame.draw.rect(surface, WALL_LIGHT, (px+5, 0, 1, 65))
    pygame.draw.rect(surface, DARK, (0, 69, 640, 27))
    pygame.draw.rect(surface, WOOD, (0, 73, 640, 19))
    for px in range(0, 640, 36):
        pygame.draw.line(surface, DARK, (px, 73), (px, 92), 2)
    # Ventilación y letrero.
    pygame.draw.rect(surface, DARK, (500, 29, 77, 42))
    pygame.draw.rect(surface, TEAL_DARK, (505, 34, 67, 33))
    for xx in range(511, 570, 10):
        pygame.draw.line(surface, GLASS, (xx, 39), (xx, 61), 2)
    pygame.draw.rect(surface, DARK, (29, 18, 117, 24))
    pygame.draw.rect(surface, WOOD, (33, 22, 109, 16))
    _label(surface, "INVENTARIO", 87, 30, 17, center=True)


def _muebles_bodega(surface):
    # Repisas, refris y huevera vacíos: los productos son objetos que se
    # pueden tomar (ver bodega.py) y se dibujan aparte, encima de este fondo.
    for x, y, _ in REFRIS_BODEGA:
        _refri(surface, x, y)
    _huevera_grande(surface, *HUEVERA_BODEGA)
    _congelador(surface, *CONGELADOR_BODEGA)
    _armario(surface)
    for x, y, columna, _ in repisas_bodega():
        _repisa(surface, x, y, canastos=columna in CON_CANASTOS)


def _alfombra_bodega(surface):
    # Regreso a la sala: alfombrilla en el borde izquierdo, sobre la región
    # de cruce (INVENTARIO_A_SALA). Mismo estilo que CALLE y BODEGA.
    pygame.draw.rect(surface, DARK, (0, 264, 68, 80))
    pygame.draw.rect(surface, WOOD, (0, 267, 64, 74))
    pygame.draw.rect(surface, WOOD_TOP, (0, 269, 59, 3))
    for yy in (290, 318):
        pygame.draw.line(surface, WOOD_TOP, (4, yy), (58, yy), 1)
    _label(surface, "SALA", 32, 305, 15, center=True)


def obstaculos_inventario():
    """Rectángulos que bloquean los muebles de la bodega, no la puerta."""
    rects = [pygame.Rect(x, y, REPISA_W, REPISA_H) for x, y, _, _ in repisas_bodega()]
    rects += [pygame.Rect(x, 96, REFRI_W, y + REFRI_H - 96) for x, y, _ in REFRIS_BODEGA]
    hx, hy = HUEVERA_BODEGA
    rects.append(pygame.Rect(hx, 96, HUEVERA_W, hy + HUEVERA_H - 96))
    cx, cy = CONGELADOR_BODEGA
    rects.append(pygame.Rect(cx, 96, CONGELADOR_W, cy + CONGELADOR_H - 96))
    if ARMARIO_ACTIVO:
        rects.append(ARMARIO.copy())
    return rects


def dibujar_accesos_sala(surface):
    """Alfombrillas que marcan las regiones de paso a otras zonas."""
    # Bodega: alfombrilla en el borde derecho, sobre la región de cruce
    # (SALA_A_INVENTARIO). Mismo estilo que la de la calle.
    pygame.draw.rect(surface, DARK, (572, 106, 68, 84))
    pygame.draw.rect(surface, WOOD, (576, 109, 64, 78))
    pygame.draw.rect(surface, WOOD_TOP, (581, 111, 59, 3))
    for yy in (132, 162):
        pygame.draw.line(surface, WOOD_TOP, (581, yy), (636, yy), 1)
    _label(surface, "BODEGA", 607, 148, 15, center=True)
    # Alfombrilla / umbral de entrada, en el borde inferior del mapa.
    x = PUERTA_SALA_X - 42
    pygame.draw.rect(surface, DARK, (x, 310, 85, 24))
    pygame.draw.rect(surface, WOOD, (x + 4, 313, 77, 18))
    pygame.draw.rect(surface, WOOD_TOP, (x + 9, 315, 67, 3))
    _label(surface, "CALLE", PUERTA_SALA_X + 1, 325, 15, center=True)


def dibujar_hud_zona(surface, zona, destino, mensaje=None):
    """Indicaciones breves: los accesos se cruzan caminando, sin pulsar E."""
    if mensaje is not None:
        message = mensaje
    elif destino == "interior":
        message = ("CAMINA HACIA LA PUERTA PARA ENTRAR"
                   if zona == "entrada" else "CRUZA LA PUERTA IZQUIERDA PARA VOLVER")
    elif zona == "entrada":
        message = "CAMINA HACIA LA SALIDA PARA IR A LA CALLE"
    elif zona == "inventario":
        message = "CRUZA A LA DERECHA PARA IR AL INVENTARIO"
    elif zona == "entrada":
        message = "ENTRADA  |  CAMINA HACIA LA PUERTA CENTRAL"
    else:
        message = "INVENTARIO  |  SAL POR LA PUERTA IZQUIERDA"

    if not AVISOS_ACTIVOS:
        return                           # GRÁFICOS > AVISOS DE ABAJO: NO
    font = FuenteTienda(None, 15)
    label = font.render(message, False, CREAM)
    width = min(WIDTH - 12, label.get_width() + 16)
    rect = pygame.Rect((WIDTH - width) // 2, 336, width, 20)
    pygame.draw.rect(surface, DARK, rect)
    pygame.draw.rect(surface, WOOD_LIGHT, rect, 2)
    surface.blit(label, label.get_rect(center=rect.center))
