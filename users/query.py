class UserQuery:
    GET_USER = """
        SELECT * FROM "USER" WHERE "USER"."ID"={pk}
    """