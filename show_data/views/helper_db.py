from show_data import db

def insert_into_db(model):
    db.session.add(model)
    db.session.commit()
    return True

def delete_db(model):
    db.session.delete(model)
    db.session.commit()