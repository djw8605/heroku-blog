from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db, models
from app.models import Post

# Initializing the manager
manager = Manager(app)

# Initialize Flask Migrate
migrate = Migrate(app, db)

@manager.command
def periodic():
    from app import periodic
    periodic.periodic()

# Add the flask migrate
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
