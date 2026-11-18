import json
import os
import jsonpatch
from bundle import MODS_DIR, CONFIG_DIR, CONFIG_PATCH_DIR

__game_config = json.load(open(os.path.join(CONFIG_DIR, "game_config_20120826.json"), 'r', encoding='utf-8'))

def remove_duplicate_items():
    indexes = {}
    items = __game_config["items"]
    num_duplicate = 0

    while True:
        index = 0
        duplicate = False
        for item in items:
            if item["id"] in indexes:
                del items[indexes[item["id"]]]
                indexes.clear()
                duplicate = True
                num_duplicate += 1
                break

            indexes[item["id"]] = index
            index += 1

        if duplicate:
            continue
        
        if num_duplicate:
            print(f" * Removed {num_duplicate} duplicate items from config patches")
        break

def apply_config_patch(filename):
    patch = json.load(open(filename, 'r'))
    jsonpatch.apply_patch(__game_config, patch, in_place=True)

def patch_game_config():

    # Apply patches

    for patch_file in os.listdir(CONFIG_PATCH_DIR):
        if patch_file.endswith(".json"):
            f = os.path.join(CONFIG_PATCH_DIR, patch_file)
            apply_config_patch(f)
            patch = patch_file.replace(".json", "")
            print(" * Patch applied:", patch)

    # Apply mods

    if os.path.exists(MODS_DIR + "/mods.txt"):
        with open(MODS_DIR + "/mods.txt", "r") as f:
            lines = f.readlines()
            f.close()

        for line in lines:
            mod = line.strip()
            if mod.startswith("#"):
                continue
            if mod != "":
                mod.replace(".json", "")
                mod_path = f"{MODS_DIR}/{mod}.json"
                if os.path.exists(mod_path):
                    apply_config_patch(mod_path)
                    print(" * Mod applied:", mod)

    remove_duplicate_items()

print (" [+] Applying config patches and mods...")
patch_game_config()

# The bundled Flash client requests language=es. Translate the base interface strings
# here as well because this server serves one shared game configuration to the client.
SPANISH_LOCALIZATION = {
    "TUTORIAL_INTRO_TITULO": "\u00a1Bienvenido a tu imperio!",
    "TUTORIAL_INTRO_LECCION": "\u00a1Hola, soy #0#! Te ense\u00f1ar\u00e9 a administrar tu imperio.\n\n\u00a1Empecemos!",
    "TUTORIAL_AYTO_TITULO": "Selecciona el ayuntamiento",
    "TUTORIAL_AYTO_LECCION": "Este es tu ayuntamiento. Desde aqu\u00ed puedes entrenar aldeanos.\n\nHaz clic en el ayuntamiento para seleccionarlo.",
    "TUTORIAL_ALDEANO_TITULO": "Entrena un aldeano",
    "TUTORIAL_ALDEANO_LECCION": "El panel inferior muestra las acciones disponibles.\n\nHaz clic en el bot\u00f3n del aldeano para entrenar uno.",
    "TUTORIAL_SELECCIONAR_ALDEANO_TITULO": "Selecciona al aldeano",
    "TUTORIAL_SELECCIONAR_ALDEANO_LECCION": "\u00a1Muy bien! Has entrenado un aldeano.\n\nHaz clic sobre \u00e9l para seleccionarlo.",
    "TUTORIAL_MOVER_ALDEANO_TITULO": "Mueve al aldeano",
    "TUTORIAL_MOVER_ALDEANO_LECCION": "Selecciona una unidad y haz clic en el mapa para moverla al lugar elegido.\n\n\u00a1Prueba a moverla a la zona indicada!",
    "TUTORIAL_ARBOL_TITULO": "Recolecta madera",
    "TUTORIAL_ARBOL_LECCION": "\u00a1Los aldeanos pueden recolectar recursos!\n\nHaz clic en un \u00e1rbol para talarlo.",
    "TUTORIAL_ESPERA_TITULO": "Espera",
    "TUTORIAL_ESPERA_LECCION": "Solo tardar\u00e1 unos segundos...",
    "TUTORIAL_RECOLECCION_TITULO": "Recoge la madera",
    "TUTORIAL_RECOLECCION_LECCION": "Cuando termine la tala, haz clic en el recurso para recoger la madera.",
    "TUTORIAL_CONSTRUIR_TITULO": "Construcci\u00f3n",
    "TUTORIAL_CONSTRUIR_LECCION": "\u00a1Muy bien! Ahora aprender\u00e1s a construir. Primero, haz clic en el bot\u00f3n CONSTRUIR.",
    "TUTORIAL_CASA_TITULO": "Selecciona una casa",
    "TUTORIAL_CASA_LECCION": "Ahora selecciona el edificio que quieres construir. Elige \u00abCasa I\u00bb.",
    "TUTORIAL_COLOCAR_TITULO": "Coloca la casa",
    "TUTORIAL_COLOCAR_LECCION": "Haz clic en el terreno para elegir d\u00f3nde colocar la casa. \u00a1Comenzar\u00e1 la construcci\u00f3n!",
    "TUTORIAL_CABALLERO_TITULO": "Selecciona al caballero",
    "TUTORIAL_CABALLERO_LECCION": "\u00a1Muy bien! Ya est\u00e1s listo para tu primera batalla.\n\nHaz clic en este caballero para seleccionarlo.",
    "TUTORIAL_ATACAR_TITULO": "Ataca al trol",
    "TUTORIAL_ATACAR_LECCION": "\u00a1Los troles son tus enemigos! Derr\u00f3talos antes de que te eliminen.\n\nHaz clic en el trol para atacarlo.",
    "TUTORIAL_BATALLA_TITULO": "Espera a que termine la batalla",
    "TUTORIAL_BATALLA_LECCION": "Las unidades est\u00e1n luchando. Las barras sobre ellas muestran su salud. No te preocupes: esos troles son d\u00e9biles.",
    "TUTORIAL_ENHORABUENA_TITULO": "\u00a1Felicidades!",
    "TUTORIAL_ENHORABUENA_LECCION": "\n\u00a1Muy bien! Ya puedes construir un gran imperio. \u00a1Buena suerte!",
    "TUTORIAL_EI": "\u00a1Eh!",
    "TUTORIAL_EDIFICIO": "Construir",
    "TUTORIAL_CASA": "Selecciona una casa",
    "TUTORIAL_COLOCAR": "Coloca la casa",
    "TUTORIAL_ARTURO": "Haz clic en el rey Arturo",
    "TUTORIAL_OK2": "Haz clic en Aceptar dos veces",
    "TUTORIAL_AYTO": "Haz clic en el ayuntamiento",
    "TUTORIAL_ALDEANO": "Entrena un aldeano",
    "TUTORIAL_FLECHA": "La flecha señala al aldeano",
    "TUTORIAL_GRANJA": "Selecciona una granja",
    "TUTORIAL_ESPERAR": "Espera a que el aldeano recolecte",
    "TUTORIAL_LISTO": "Listo para recolectar",
    "TUTORIAL_OK5": "Haz clic en Aceptar cinco veces",
    "TUTORIAL_SELECCIONA_ALDEANO": "Selecciona al aldeano",
    "TUTORIAL_ARBOL": "Haz clic en el árbol",
    "MISC_SEGURO": "\u00bfEst\u00e1s seguro?",
    "MISC_FAVOR": "\u00bfQuieres aceptar el favor?",
    "STORE_EDIFICIO_EXP": "#0# de experiencia",
    "STORE_EDIFICIO_NIVEL": "Requiere nivel #0#",
    "STORE_EDIFICIO_LIMITE": "Quedan #0# d\u00edas",
    "STORE_EDIFICIO_REFUERZOS": "\n\nPermite recibir refuerzos de tus aliados.",
    "STORE_EDIFICIO_DESBLOQUEO": "Coste de desbloqueo: #0# monedas",
    "STORE_EDIFICIO_SACRIFICIO": "\n\nSacrifica una unidad y recupera algunos recursos.",
    "STORE_EDIFICIO_TESORO": "\n\nDescubre un objeto coleccionable cada d\u00eda.",
    "STORE_EDIFICIO_ESTABLO": "\n\nConvierte espadachines y arqueros en unidades montadas.",
    "STORE_EDIFICIO_CRIADERO": "\n\nColoca dos animales para que se reproduzcan.",
    "STORE_EDIFICIO_ZEPPELIN": "\n\nConstruye un zeppel\u00edn para explorar el Mar Antiguo.",
    "STORE_EDIFICIO_BARCO": "\n\nConstruye un barco para explorar el Gran Mar.",
    "STORE_EDIFICIO_COLISEO": "\n\nAumenta la velocidad de tus aldeanos y la cantidad de recursos que pueden recolectar.",
    "STORE_EDIFICIO_ESTATUA": "\n\nLa estatua aumenta de 3 a 4 el l\u00edmite de ataques diarios.",
    "STORE_EDIFICIO_MINA": "\n\nPermite extraer oro y piedra con mayor rapidez.",
    "STORE_EDIFICIO_SERRADERO": "\n\nPermite talar \u00e1rboles con mayor rapidez.",
    "STORE_EDIFICIO_MERCADO_ALIADOS": "\n\nPermite obtener el recurso que quieras con ayuda de tus aliados.",
    "STORE_EDIFICIO_MAQUINA_DEL_TIEMPO": "\n\nCambia el aspecto del terreno de tu mapa.",
    "STORE_EDIFICIO_RECLUTAMIENTO_ALIADOS": "\n\nConsigue unidades poderosas mediante nuevos reclutas.",
    "STORE_EDIFICIO_MESA_REDONDA": "\n\nObtén recompensas con la ayuda de tus amigos.",
    "STORE_EDIFICIO_HECHICERIA": "\n\nAprende y lanza hechizos.",
    "STORE_EDIFICIO_MARAVILLA_SOCIAL": "\n\nAumenta el l\u00edmite de poblaci\u00f3n hasta en 50 unidades.",
    "STORE_EDIFICIO_DESCONOCIDO": "\n\nNo se encontr\u00f3 la descripci\u00f3n.",
    "STORE_EDIFICIO_IGLESIA_1": "Los sanadores pueden restaurar la salud de tus unidades.",
    "STORE_EDIFICIO_CATEDRAL": "Los monjes convierten unidades enemigas en aliadas.",
    "STORE_EDIFICIO_IGLESIA": "Los sanadores pueden restaurar la salud de tus unidades.",
    "STORE_EDIFICIO_TALLER": "Los ingenieros reparan armas de asedio.",
    "STORE_EDIFICIO_DEMOLICION": "Los kamikazes explotan y da\u00f1an a las unidades y edificios cercanos.",
    "STORE_EDIFICIO_ELEFANTE": "Los elefantes pisan el suelo y aturden a los enemigos cercanos.",
    "STORE_EDIFICIO_CUARTEL1": "El avatar de Anubis crea dos sombras para aniquilar al enemigo.",
    "STORE_EDIFICIO_TAMBORILERO": "Los tambores inspiran a tus tropas y aumentan su velocidad de ataque.",
    "STORE_EDIFICIO_RINOCERONTE": "Los rinocerontes embisten a sus enemigos y los hacen volar.",
    "STORE_EDIFICIO_TORRE_MOVIL": "Torre defensiva m\u00f3vil que tambi\u00e9n puedes usar en los ataques.",
    "STORE_EDIFICIO_PIRAMIDE": "Usa los cuatro ataques especiales de la momia para derrotar a tus enemigos.",
    "STORE_EDIFICIO_TORRE_HIELO": "Congela a las unidades enemigas por un tiempo. Mientras est\u00e1n congeladas, no pueden moverse ni atacar.",
    "STORE_EDIFICIO_TORRE_AGUA": "Desata olas de agua para apartar a los enemigos que se acercan.",
    "STORE_EDIFICIO_FORTALEZA_1": "Guarnece arqueros en su interior para aumentar su poder de ataque.",
    "STORE_EDIFICIO_TORRE_ACEITE": "Crea una barrera de aceite en llamas que prende fuego a los enemigos.",
    "STORE_EDIFICIO_HEROES_ALTAR": "\n\nPermite conseguir h\u00e9roes especiales.",
    "STORE_EDIFICIO_HEROES_CEMENTERIO": "\n\nPermite revivir a tus h\u00e9roes ca\u00eddos.",
    "AUX_ATERRIZANDO": "Aterrizando...",
    "AUX_RECOLECTANDO": "Recolectando...",
    "AUX_ACEPTAR": "Aceptar",
    "AUX_ACELERAR": "\u00bfAcelerar?",
    "AUX_ABSORBER": "#0# absorbido",
    "AUX_PUNTOS": "puntos",
    "AUX_EXP": "Experiencia: #0#",
    "AUX_FUERA_DE_RANGO": "Momia gigante",
    "AUX_ENTRENANDO": "Entrenando...",
    "AUX_CONSTRUYENDO": "Construyendo...",
    "AUX_MODIFICADOR_HORA": "#0# hora",
    "AUX_CARGANDO_TU_IMPERIO": "Cargando tu imperio...",
    "AUX_CARGANDO_IMPERIO": "Cargando el imperio...",
}


def apply_spanish_localization():
    by_name = {item.get("name"): item for item in __game_config.get("localization_strings", []) if isinstance(item, dict)}
    for name, text in SPANISH_LOCALIZATION.items():
        if name in by_name:
            by_name[name]["text"] = text
    with open(os.path.join(CONFIG_DIR, "spanish_localization.json"), encoding="utf-8") as f:
        by_id = json.load(f)
    for item in __game_config.get("localization_strings", []):
        if isinstance(item, dict) and str(item.get("id")) in by_id:
            item["text"] = by_id[str(item["id"])]
    with open(os.path.join(CONFIG_DIR, "spanish_missions.json"), encoding="utf-8") as f:
        translated_missions = json.load(f)
    missions_by_id = {str(item.get("id")): item for item in __game_config.get("missions", [])}
    for mission_id, values in translated_missions.items():
        if mission_id in missions_by_id:
            missions_by_id[mission_id].update(values)
    with open(os.path.join(CONFIG_DIR, "spanish_items.json"), encoding="utf-8") as f:
        translated_items = json.load(f)
    for item in __game_config.get("items", []):
        if str(item.get("id")) in translated_items:
            item["name"] = translated_items[str(item["id"])]
    with open(os.path.join(CONFIG_DIR, "spanish_misc.json"), encoding="utf-8") as f:
        misc = json.load(f)
    for item in __game_config.get("honor_levels", []):
        if str(item.get("id")) in misc["honor_levels"]:
            item["rank"] = misc["honor_levels"][str(item["id"])]
    for collection, fields in (("findable_items", ("title", "description")), ("magics", ("name", "description"))):
        translated = misc[collection]
        for item in __game_config.get(collection, []):
            values = translated.get(str(item.get("id")), {})
            for field in fields:
                if field in values:
                    item[field] = values[field]
    for item in __game_config.get("neighbor_assists", []):
        if misc["neighbor_assists"]:
            values = misc["neighbor_assists"].pop(0)
            item.update(values)
    for item in __game_config.get("social_items", []):
        if str(item.get("id")) in misc["social_items"]:
            item["workers"] = misc["social_items"][str(item["id"])]
    for item, values in zip(__game_config.get("iphone_goals", []), misc["iphone_goals"]):
        item.update(values)


apply_spanish_localization()

def get_game_config() -> dict:
    return __game_config

def game_config() -> dict:
    return get_game_config()

##########
# PLAYER #
##########

def get_xp_from_level(level: int) -> int:
    return __game_config["levels"][int(level)]["exp_required"]

def get_level_from_xp(xp: int) -> int:
    i = 0
    for lvl in __game_config["levels"]:
        if lvl["exp_required"] > int(xp):
            return i
        i += 1
    return 0

#########
# ITEMS #
#########

# ID

items_dict_id_to_items_index = {int(item["id"]): i for i, item in enumerate(__game_config["items"])}

def get_item_from_id(id: int) -> dict:
    items_index = items_dict_id_to_items_index[int(id)] if int(id) in items_dict_id_to_items_index else None
    return __game_config["items"][items_index] if items_index is not None else None

def get_attribute_from_item_id(id: int, attribute_name: str) -> str:
    item = get_item_from_id(id)
    return item[attribute_name] if item and attribute_name in item else None

def get_name_from_item_id(id: int) -> str:
    return get_attribute_from_item_id(id, "name")

# subcat_functional

items_dict_subcat_functional_to_items_index = {int(item["subcat_functional"]): i for i, item in enumerate(__game_config["items"])}

def get_item_from_subcat_functional(subcat_functional: int) -> dict:
    items_index = items_dict_subcat_functional_to_items_index[int(subcat_functional)] if int(subcat_functional) in items_dict_subcat_functional_to_items_index else None
    return __game_config["items"][items_index] if items_index is not None else None

############
# MISSIONS #
############

missions_dict_id_to_missions_index = {int(item["id"]): i for i, item in enumerate(__game_config["missions"])}

def get_mission_from_id(id: int) -> dict:
    items_index = missions_dict_id_to_missions_index[int(id)] if int(id) in missions_dict_id_to_missions_index else None
    return __game_config["missions"][items_index] if items_index is not None else None

def get_attribute_from_mission_id(id: int, attribute_name: str) -> str:
    mission = get_mission_from_id(id)
    return mission[attribute_name] if mission and attribute_name in mission else None