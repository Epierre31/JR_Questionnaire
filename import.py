import sys
import os

import requests
import json
import unicodedata
from loguru import logger

BASE_Q_JSON = "../BD_JSON/"

# ====> REMARQUE : Les Url ci-dessous sont différentes que celles affichées dans la vidéo.
# C'est normal, continuez bien avec les url de ce fichier
open_quizz_db_data = (
    ("Animaux", "Les chats", "https://www.codeavecjonathan.com/res/mission/openquizzdb_50.json"),
    ("Arts", "Musée du Louvre", "https://www.codeavecjonathan.com/res/mission/openquizzdb_86.json"),
    ("Bande dessinnée", "Tintin", "https://www.kiwime.com/oqdb/files/2124627384/OpenQuizzDB_124/openquizzdb_124.json"),
    ("Bande dessinnée", "Tintin", "https://www.codeavecjonathan.com/res/mission/openquizzdb_124.json"),
    ("Cinéma", "Alien", "https://www.codeavecjonathan.com/res/mission/openquizzdb_241.json"),
    ("Cinéma", "Star wars", "https://www.codeavecjonathan.com/res/mission/openquizzdb_90.json"),
)


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def get_quizz_filename(categorie, titre, difficulte):
    return strip_accents(categorie).lower().replace(" ", "") + "_" + strip_accents(titre).lower().replace(" ",
                                                                                                          "") + "_" + strip_accents(
        difficulte).lower().replace(" ", "") + ".json"


def generate_json_file(categorie, titre, url):
    out_questionnaire_data = {"categorie": categorie, "titre": titre, "questions": []}
    out_questions_data = []
    logger.info(f"Conversion de : {str(url)}")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.warning(f"erreur acces sur : {str(url)}\n ==> {e}")
        return

    data = json.loads(response.text)
    all_quizz = data["quizz"]["fr"]
    for quizz_title, quizz_data in all_quizz.items():
        out_filename = get_quizz_filename(categorie, titre, quizz_title)
        # logger.info("generation de " + str(out_filename) + " Start")
        out_questionnaire_data["difficulte"] = quizz_title
        for question in quizz_data:
            question_dict = {}
            question_dict["titre"] = question["question"]
            question_dict["choix"] = []
            for ch in question["propositions"]:
                question_dict["choix"].append((ch, ch == question["réponse"]))
            out_questions_data.append(question_dict)
        out_questionnaire_data["questions"] = out_questions_data
        out_json = json.dumps(out_questionnaire_data)

        full_name = BASE_Q_JSON + out_filename
        if not os.path.isdir(BASE_Q_JSON):
            os.mkdir(BASE_Q_JSON)
        else:
            if os.path.exists(full_name):
                os.remove(full_name)

        file = open(full_name, "w")
        file.write(out_json)
        file.close()
        logger.info("generation de " + str(full_name) + " : Done")

logger.remove()
logger.add(sys.stderr,level="INFO")
logger.add("../LOG/Import.log",rotation="500kB",level="WARNING")


for quizz_data in open_quizz_db_data:
    generate_json_file(quizz_data[0], quizz_data[1], quizz_data[2])
