from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Setting(db.Model):
    __tablename__ = 'settings'

    name = db.Column(db.String(), primary_key=True)
    value = db.Column(db.Boolean, nullable=False, server_default='True')
    category = db.Column(db.String(), nullable=False, server_default='command')
    category_position = db.Column(db.Integer, nullable=False, server_default='0')

    def __init__(self, name, value, category, category_position):
        self.name = name
        self.value = value
        self.category = category
        self.category_position = category_position

    def __repr__(self):
        return f'<Setting {self.name}>'


class GroupmeUser(db.Model):
    __tablename__ = 'groupme_users'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String, nullable=False)
    is_woman = db.Column(db.Boolean, nullable=False, server_default='False')

    def __init__(self, nickname, is_woman):
        self.nickname = nickname
        self.is_woman = is_woman

    def __repr__(self):
        return f'<GroupmeUser {self.id}>'
