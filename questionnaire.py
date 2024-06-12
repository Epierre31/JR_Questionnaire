import json
import sys
import os
from time import sleep

from loguru import logger

BASE_Q_JSON = "../BD_JSON/"
NB_SEP = 50

TEST_FILE = "animaux_leschats_expert.json"


class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def poser(self, no_question, total_question):
        print(f"QUESTION {no_question}/{total_question}")
        print("  " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i + 1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int - 1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")

        print()
        return resultat_response_correcte

    def demander_reponse_numerique_utlisateur(min, max):
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") :")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)


class Questionnaire:
    categorie = ""
    titre = ""
    difficulte = ""
    questions = []
    filename = ""

    def __init__(self, categorie, titre, difficulte, questions):
        self.categorie = categorie
        self.titre = titre
        self.difficulte = difficulte
        self.questions = questions

    def loadfromFile(filename: str):
        """"
        chargement le fichier json dans un objet questionnaire
        """
        logger.info("chargement de " + filename)
        full_name = BASE_Q_JSON + filename
        if not os.path.exists(full_name):
            return None

        Questionnaire.filename = filename
        with open(full_name, "r", encoding="utf-8") as file:
            qdata = json.load(file)
        logger.info("lecture de " + str(full_name) + " : Done")
        categorie = qdata["categorie"]
        difficulte = qdata["difficulte"]
        titre = qdata["titre"]

        # recup des questions, et identification de la bonne reponse
        question_list = []
        for question in qdata["questions"]:
            titre_question = question["titre"]
            choix=[]
            for ch in question["choix"]:
                choix.append(ch[0])
                if ch[1]:
                    bonne_reponse= ch[0]
            question_list.append(Question(titre=titre_question, choix=choix, bonne_reponse=bonne_reponse))

        logger.info(f"questionnaire chargé : categorie: {categorie} titre: {titre} + difficulté= {difficulte} avec {len(question_list)} questions")
        sleep(2)

        return Questionnaire(categorie=categorie,
                             titre=titre,
                             difficulte=difficulte,
                             questions=question_list)

    def lancer(self):
        score = 0
        nb_questions = len(self.questions)
        print(f"Questionnaire ({nb_questions}): {self.titre}")
        print(f"    categorie : {self.categorie}")
        print(f"    difficulte: {self.difficulte}")
        print(f"-"*NB_SEP + "\n")
        for no_q, question in enumerate(self.questions):
            if question.poser(no_q+1
                    , nb_questions):
                score += 1
        print(f"-"*NB_SEP)
        print("Score final :", score, "sur", len(self.questions))
        print(f"-"*NB_SEP)
        return score

    def choisir_filename():
        if len(sys.argv) > 1:
            #un arg files name ?
            filename = sys.argv[1]
        else:
            filename = input("entrez le nom du fichier json :")
        full_name = BASE_Q_JSON + filename
        if not os.path.exists(full_name):
            print(f"erreur sur filename {filename}")
            file_name= Questionnaire.choisir_filename()
        logger.info("fichier json : " + full_name)
        return filename

pass

logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("../LOG/Questionnaire.log", rotation="500kB", level="WARNING")

if __name__ == '__main__':
    # print(f"arg reçus : {len(sys.argv)}")
    # for i in range(len(sys.argv)):
    #     print (f"arg ({i}): {sys.argv[i]}")
    # print("========================")
    jsonfile =  Questionnaire.choisir_filename()
    questionnaire = Questionnaire.loadfromFile(filename=jsonfile)
    questionnaire.lancer()

