#
# Copyright 2018 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
"""Test the expired_endpoint endpoint view."""
from unittest.mock import patch

from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from masu.config import Config
from masu.processor.orchestrator import Orchestrator


@override_settings(ROOT_URLCONF="masu.urls")
class ExpiredDataTest(TestCase):
    """Test Cases for the expired_data endpoint."""

    @patch.object(Orchestrator, "remove_expired_report_data")
    def test_get_expired_data(self, mock_orchestrator):
        """Test the GET expired_data endpoint."""
        mock_response = [{"customer": "acct10001", "async_id": "f9eb2ce7-4564-4509-aecc-1200958c07cf"}]
        expected_key = "Async jobs for expired data removal (simulated)"
        mock_orchestrator.return_value = mock_response
        response = self.client.get(reverse("expired_data"))
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn(expected_key, body)
        self.assertIn(str(mock_response), body.get(expected_key))

    @patch.object(Config, "DEBUG", return_value=False)
    @patch.object(Orchestrator, "remove_expired_report_data")
    def test_del_expired_data(self, mock_orchestrator, mock_debug):
        """Test the DELETE expired_data endpoint."""
        mock_response = [{"customer": "acct10001", "async_id": "f9eb2ce7-4564-4509-aecc-1200958c07cf"}]
        expected_key = "Async jobs for expired data removal"
        mock_orchestrator.return_value = mock_response

        response = self.client.delete(reverse("expired_data"))
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn(expected_key, body)
        self.assertIn(str(mock_response), body.get(expected_key))
