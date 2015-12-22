import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from api import app, db

app.config.from_pyfile('config.py')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

db.create_all()

if __name__ == '__main__':
    manager.run()