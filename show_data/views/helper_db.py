from show_data import db

def insert_into_db(model):
    db.session.add(model)
    db.session.commit()
    return True
