class AppointmentsQuery:
    GET_MEDIC_APPOINTMENTS = """
        SELECT * FROM Appointments WHERE medic_id={medic}
    """

    GET_MEDIC_APPOINTMENTS_NUMBER = """
        SELECT COUNT('id') FROM Appointments WHERE medic_id={medic}
    """

    GET_PATIENTS = """
        SELECT * FROM "USER" WHERE "USER"."ID" IN ({pk}) {filters}
    """

    GET_PATIENT_APPOINTMENTS_WITH_STATUS = """
        SELECT * FROM "APPOINTMENTS" WHERE ("APPOINTMENTS"."PATIENT_ID" = {patient_id} AND "APPOINTMENTS"."STATUS" = {status})
    """

    GET_PATIENT_APPOINTMENTS = """
        SELECT * FROM "APPOINTMENTS" WHERE ("APPOINTMENTS"."PATIENT_ID" = {patient_id})
    """

    GET_APPOINTMENT = """
        SELECT * FROM Appointments WHERE id={pk}
    """

    GET_PATIENT_APPOINTMENTS_NUMBER = """
        SELECT COUNT('id') FROM "APPOINTMENTS" WHERE ("APPOINTMENTS"."PATIENT_ID" = {patient_id})
    """

    DELETE_APPOINTMENTS_SYMPTOMS = """
        DELETE FROM "APPOINTMENTS_SYMPTOMS" WHERE "APPOINTMENTS_SYMPTOMS"."APPOINTMENTS_ID" IN ({pk})
    """

    DELETE_APPOINTMENTS = """
        DELETE FROM "APPOINTMENTS" WHERE "APPOINTMENTS"."ID"={pk}
    """

    CHECK_APPOINTMENTS_SCHEDULE = """
        SELECT (1) AS "A" FROM "APPOINTMENTS"
        WHERE ("APPOINTMENTS"."MEDIC_ID"={medic_id} AND "APPOINTMENTS"."PATIENT_ID"={patient_id} AND EXTRACT(DAY FROM "APPOINTMENTS"."SCHEDULED_DATETIME")={day}) FETCH FIRST 1 ROWS ONLY
    """

    UPDATE_APPOINTMENT = """
        UPDATE "APPOINTMENTS" SET "PATIENT_ID"={patient_id}, "MEDIC_ID"={medic_id}, "SCHEDULED_DATETIME"='{scheduled}', "DESCRIPTION"='{description}', "DISEASE_ID" = {disease_id}, "STATUS"={status}, "TREATMENT"='{treatment}'  WHERE "APPOINTMENTS"."ID"={pk}
    """

    INSERT_SYMPTOMS = """
        INSERT INTO "APPOINTMENTS_SYMPTOMS" ("APPOINTMENTS_ID", "SYMPTOMS_ID") VALUES({appointment_pk}, {symptom_pk})
    """

    DELETE_APPOINTMENTS_SYMPTOMS_BY_SYMPTOMS = """
        DELETE FROM "APPOINTMENTS_SYMPTOMS" WHERE "APPOINTMENTS_SYMPTOMS"."APPOINTMENTS_ID"={appointment_pk} AND "APPOINTMENTS_SYMPTOMS"."SYMPTOMS_ID"={symptom_pk}
    """
