from django.db import connection


def load_data():
    diases = [
        "INSERT INTO Diseases (name) VALUES ('COVID-19')",
        "INSERT INTO Diseases (name) VALUES ('Anemie')",
        "INSERT INTO Diseases (name) VALUES ('Gripa')",
        "INSERT INTO Diseases (name) VALUES ('Viroze')",
        "INSERT INTO Diseases (name) VALUES ('Diabet')",
        "INSERT INTO Diseases (name) VALUES ('Hipertensiune arteriala')"
    ]
    symptoms = [
        "INSERT INTO Symptoms (name) VALUES ('Dureri de cap')",
        "INSERT INTO Symptoms (name) VALUES ('Febra')",
        "INSERT INTO Symptoms (name) VALUES ('Tuse')",
        "INSERT INTO Symptoms (name) VALUES ('Oboseala')",
        "INSERT INTO Symptoms (name) VALUES ('Gat inflamat')",
        "INSERT INTO Symptoms (name) VALUES ('Durere de cap')",
        "INSERT INTO Symptoms (name) VALUES ('Pierderea simtului mirosului si al gustului')",
    ]

    specializations = [
        "INSERT INTO Users_Specialization (name) VALUES ('Pediatru')",
        "INSERT INTO Users_Specialization (name) VALUES ('Medic de familie')",
        "INSERT INTO Users_Specialization (name) VALUES ('Cardiolog')"
    ]

    with connection.cursor() as cursor:
        print("------LOAD DISEASES DATA----")
        try:
            for d in diases:
                cursor.execute(d)
        except Exception as ex:
            print(f"------ERROR LOAD DISEASES DATA---- {ex}")
        print("------LOAD SYMPTOMS DATA----")
        try:
            for s in symptoms:
                cursor.execute(s)
        except Exception as ex:
            print(f"------ERROR LOAD SYMPTOMS DATA---- {ex}")
        print("------LOAD SPECIALIZATION DATA----")
        try:
            for s in specializations:
                cursor.execute(s)
        except Exception as ex:
            print(f"------ERROR LOAD SPECIALIZATION DATA---- {ex}")
        print("------FINISH----")
