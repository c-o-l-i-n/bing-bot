from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Setting(db.Model):
    __tablename__ = 'settings'

    name = db.Column(db.String(), primary_key=True)
    value = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f'<Setting {self.name}>'


class GroupmeUser(db.Model):
    __tablename__ = 'groupme_users'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String, nullable=False)
    is_woman = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, nickname, is_woman):
        self.nickname = nickname
        self.is_woman = is_woman

    def __repr__(self):
        return f'<GroupmeUser {self.id}>'
