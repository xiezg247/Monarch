import unittest
import coverage
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from monarch.app import create_app
from monarch.corelibs.store import db
from monarch.corelibs.mcredis import mc

application = create_app('monarch')
application.config['DEBUG'] = True

manager = Manager(application)

# db
migrate = Migrate(application, db)
manager.add_command('db', MigrateCommand)

# coverage
COV = coverage.coverage(
    branch=True,
    include='monarch/*',
    omit=[
        'tests/*',
    ]
)
COV.start()


@manager.command
def cov():
    """
    Runs the unit tests and generates a coverage report on success.
    While the application is running, you can run the following command in a new terminal:
    'docker-compose run --rm flask python manage.py cov' to run all the tests in the
    'tests' directory. If all the tests pass, it will generate a coverage report.
    :return int: 0 if all tests pass, 1 if not
    """

    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    else:
        return 1


# unittest
@manager.command
def test():
    """
    Runs the unit tests without generating a coverage report.
    Enter 'python manage.py test' to run all the tests in the
    'tests' directory, with no coverage report.
    :return int: 0 if all tests pass, 1 if not
    """

    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


@manager.command
def test_one(test_file):
    """
    Runs the unittest without generating a coverage report.
    Enter 'python manage.py test_one <NAME_OF_FILE>' to run only
    one test file in the 'tests' directory. It provides no coverage report.
    Note that you do not need to put the extension of the test file.
    :return int: 0 if all tests pass, 1 if not
    """

    tests = unittest.TestLoader().discover('tests', pattern=test_file + '.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


# flake8
@manager.command
def flake8():
    """
    Runs the flake8
    Enter 'python manage.py test' to run code
    """
    from subprocess import call
    print('flake8 checking:')
    return call(['flake8',
                 'monarch',
                 '--exclude=__pycache__,',
                 '--show-source',
                 '--ignore=E402,E305,W503'])


@manager.command
def syncdb():
    """
    Enter 'python manage.py syncdb' to sync all tables
    """
    with application.test_request_context():
        from monarch.models.company import Company  # noqa
        from monarch.models.user import User  # noqa
        db.create_all()
        db.session.commit()
        print('Database created.')


@manager.command
def dropdb():
    """
    Enter 'python manage.py dropdb' to drop all tables
    """
    with application.test_request_context():
        from monarch.models.company import Company  # noqa
        from monarch.models.user import User  # noqa
        db.drop_all()
        mc.flushdb()
        print('Database droped.')


if __name__ == '__main__':
    manager.run()
