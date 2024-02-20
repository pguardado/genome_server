from flask_testing import TestCase
from ..myFlaskApp import create_app

class MyTest(TestCase):
    def create_app(self):
        app = create_app()  # Create an instance of your Flask application
        app.config['TESTING'] = True
        return app

    def test_upload(self, client, tmpdir):
        # Create a temporary directory for file uploads
        self.app.config['UPLOAD_FOLDER'] = str(tmpdir)  # Use self.app to access the Flask application instance

        # Create a test file
        test_file = tmpdir.join('test.fa')
        test_file.write('test content')

        # Send a POST request to the /upload route with the test file
        with test_file.open() as f:
            response = client.post('/upload', data={'file': f})

        # Check that the response status code is 200
        assert response.status_code == 200

        # Check that the response data is correct
        assert b'File uploaded successfully' in response.data