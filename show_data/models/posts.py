from show_data import db

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    post_text = db.Column(db.String(128))
    post_date = db.Column(db.DateTime)
    eng_rate = db.Column(db.Integer)
    imp = db.Column(db.Integer)
    reach = db.Column(db.Integer)
    good = db.Column(db.Integer)
    comment = db.Column(db.Integer)
    save_cnt = db.Column(db.Integer)
    play_cnt = db.Column(db.Integer)

    def __init__(self, id, post_text, post_date, eng_rate, imp, reach, good, comment, save_cnt, play_cnt):
        self.id = id
        self.post_text = post_text
        self.post_date = post_date
        self.eng_rate = eng_rate
        self.imp = imp
        self.reach = reach
        self.good = good
        self.comment = comment
        self.save_cnt = save_cnt
        self.play_cnt = play_cnt
