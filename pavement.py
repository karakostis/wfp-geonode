from paver.easy import sh, task

@task
def run_tests(options):
    """
    Run WFP GeoNode's Unit Test Suite
    """
    sh("python manage.py test wfp.trainings.tests.tests wfp.wfpdocs.tests.tests --settings=wfp.settings.testing --traceback")
    sh('flake8 wfp')
