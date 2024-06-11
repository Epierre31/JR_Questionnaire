import json
import sys
import os
from loguru import logger

BASE_Q_JSON = "../BD_JSON/"

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

    def __init__(self, categorie, titre, difficulte, questions):
        self.categorie = categorie
        self.titre = titre
        self.difficulte = difficulte
        self.questions = questions

    def loadfromFile(filename: str):
        logger.info("chargement de " + filename)
        full_name = BASE_Q_JSON + filename
        if not os.path.exists(full_name):
            return None

        with open(full_name, "r", encoding="utf-8") as file:
            qdata = json.load(file)
        logger.info("lecture de " + str(full_name) + " : Done")
        categorie = qdata["categorie"]
        difficulte = qdata["difficulte"]
        titre = qdata["titre"]
        question_list = []
        for question in qdata["questions"]:
            titre_question = question["titre"]
            choix=[]
            for ch in question["choix"]:
                choix.append(ch[0])
                if ch[1]:
                    bonne_reponse= ch[0]
            question_list.append(Question(titre=titre_question, choix=choix, bonne_reponse=bonne_reponse))
        logger.info("questionnaire chargé :")
        logger.info(f"  ==> categrorie: {categorie} titre: {titre} + difficulté= {difficulte}")
        logger.info(f"  ==> avec {len(question_list)} questions")
        return Questionnaire(categorie=categorie,
                             titre=titre,
                             difficulte=difficulte,
                             questions=question_list)

    def lancer(self):
        score = 0
        nb_questions = len(self.questions)
        print(f"Questionnaire dans la categorie: {self.categorie}")
        print(f"    titre     : {self.titre}")
        print(f"    difficulte: {self.difficulte}")
        print(f"    avec {nb_questions} questions")
        print(f"-"*30 + "\n")
        for no_q, question in enumerate(self.questions):
            if question.poser(no_q+11
                    , nb_questions):
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score


logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("../LOG/Questionnaire.log", rotation="500kB", level="WARNING")

if __name__ == '__main__':
    questionnaire = Questionnaire.loadfromFile(filename=TEST_FILE)
    questionnaire.lancer()

