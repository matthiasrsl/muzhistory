from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone as tz

from requests.exceptions import ConnectionError

from .models import *
from deezerdata.models.deezer_objects import DeezerTrack


class ExceptionLogTest(TestCase):
    def setUp(self):
        self.connection_error_album_patch = patch(
            "deezerdata.models.deezer_objects.DeezerAlbum.download_data",
            new=MagicMock(side_effect=ZeroDivisionError()),
        )

    def test_logs_connection_error(self):
        """
        Tests that if a requests.exceptions.ConnectionError occurs
        during a retrieval process, a corresponding ExceptionLog
        entry is created.
        """
        self.connection_error_album_patch.start()
        logs_before = ExceptionLog.objects.all().order_by("-occured_on")
        nb_logs_before = len(logs_before)
        with self.assertRaises(ZeroDivisionError):
            track = DeezerTrack.get_or_retrieve(
                67238735
            )  # Daft Punk's Get Lucky.
        logs_after = ExceptionLog.objects.all().order_by("-occured_on")
        nb_logs_after = len(logs_after)
        last_log = logs_after[0]
        self.assertEqual(
            nb_logs_after - nb_logs_before, 2
        )  # One exception happened during the retrieval of the album and was then transmitted to DeezerTrack.get_or_retrieve() and was therefore logged twice, which is the expected behavior.
        self.assertEqual(last_log.exception_name, "ZeroDivisionError")
        self.assertEqual(last_log.function_name, "DeezerTrack.get_or_retrieve")
        self.assertEqual(last_log.exception_module, "builtins")
        self.connection_error_album_patch.stop()


class ExceptionLogDisplayTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        normal_user = User.objects.create_user(
            "normaluser", "foo@bar.com", "pwd"
        )
        staff_user = User.objects.create_user(
            "staffuser", "foo@bar.com", "pwd"
        )
        superuser = User.objects.create_superuser(
            "superuser", "foo@bar.com", "pwd"
        )
        staff_user.is_staff = True
        normal_user.save()
        staff_user.save()
        superuser.save()
        exception_log = ExceptionLog.objects.create(
            exception_name = "name",
            exception_module = "module",
            exception_value = "value",
            function_name = "name",
            traceback = "traceback",
            occured_on = tz.now()
        )
        exception_log.save()

    def setUp(self):
        self.client = Client()

    def test_restricted_access(self):
        """
        Tests that only a superuser can access exception logs.
        """
        log_id = ExceptionLog.objects.get().id
        self.client.login(username='normaluser', password='pwd')
        response = self.client.get(reverse("tools:log_display", args=[log_id]))
        self.assertEqual(response.status_code, 403)

        self.client.login(username='staffuser', password='pwd')
        response = self.client.get(reverse("tools:log_display", args=[log_id]))
        self.assertEqual(response.status_code, 403)

        self.client.login(username='superuser', password='pwd')
        response = self.client.get(reverse("tools:log_display", args=[log_id]))
        self.assertEqual(response.status_code, 200)

    

class ExceptionLogListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        normal_user = User.objects.create_user(
            "normaluser", "foo@bar.com", "pwd"
        )
        staff_user = User.objects.create_user(
            "staffuser", "foo@bar.com", "pwd"
        )
        superuser = User.objects.create_superuser(
            "superuser", "foo@bar.com", "pwd"
        )
        staff_user.is_staff = True
        normal_user.save()
        staff_user.save()
        superuser.save()
        exception_log = ExceptionLog.objects.create(
            exception_name = "name",
            exception_module = "module",
            exception_value = "value",
            function_name = "name",
            traceback = "traceback",
            occured_on = tz.now()
        )
        exception_log.save()

    def setUp(self):
        self.client = Client()

    def test_restricted_access(self):
        """
        Tests that only a superuser can access exception logs.
        """
        self.client.login(username='normaluser', password='pwd')
        response = self.client.get(reverse("tools:log_list"))
        self.assertEqual(response.status_code, 403)

        self.client.login(username='staffuser', password='pwd')
        response = self.client.get(reverse("tools:log_list"))
        self.assertEqual(response.status_code, 403)

        self.client.login(username='superuser', password='pwd')
        response = self.client.get(reverse("tools:log_list"))
        self.assertEqual(response.status_code, 200)
