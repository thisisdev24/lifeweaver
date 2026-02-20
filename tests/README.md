For successfully running tests, first run this command from project root:

>> pip install -e .

You only need to run it once.

Now run tests with:

>> pytest -q

Because pip install -e . registers your package with Python, import app will always work while the editable install is present.