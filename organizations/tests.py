import json

from django.test import TestCase, RequestFactory

from organizations.views import get_repos


class ReposTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_number_of_repos(self):
        """
        Test repos endpoint
        :return:
        """
        request = self.factory.get('http://127.0.0.1:8000/organizations')
        response = get_repos(request, 'y-luis-organization')

        body = json.loads(response.content.decode())

        # test status code
        self.assertEqual(response.status_code, 200, 'Wrong status code')

        # test JSON well formed and with expected values
        self.assertIn('public_repos', body)
        self.assertEqual(body['public_repos'], 2)
        self.assertIn('biggest_repo', body)
        self.assertIn('name', body['biggest_repo'])
        self.assertIn('size', body['biggest_repo'])
        self.assertEqual(body['biggest_repo']['name'], 'github-api-wrapper')

    def _post_teardown(self):
        pass