
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from run import app
from exts import db
from app.model import User, Comment, Posts


manage = Manager(app)


# bonding Migrate and app, db
migrate = Migrate(app, db)

# add migrate script to manager
manage.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manage.run()
