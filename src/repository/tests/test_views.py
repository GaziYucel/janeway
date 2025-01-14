__copyright__ = "Copyright 2017 Birkbeck, University of London"
__author__ = "Andy Byers, Mauro Sanchez & Joseph Muller"
__license__ = "AGPL v3"
__maintainer__ = "Birkbeck Centre for Technology and Publishing"

from django.test import TestCase, override_settings
from django.shortcuts import reverse
from django.utils import timezone
from django.core import mail
from django.urls.base import clear_script_prefix

from utils.testing import helpers
from utils.install import update_settings
from core import models as cm
from repository import models as rm, install


class TestModels(TestCase):
    def setUp(self):
        self.press = helpers.create_press()
        self.press.save()
        self.request = helpers.Request()
        self.request.press = self.press
        self.repo_manager = helpers.create_user(
            'repo_manager@janeway.systems'
        )
        self.repo_manager.is_active = True
        self.repo_manager.save()
        self.reviewer = helpers.create_user(
            'repo_reviewer@janeway.systems',
        )
        self.repository, self.subject = helpers.create_repository(
            self.press,
            [self.repo_manager],
            [],
            domain='repo.test.com',
        )
        install.load_settings(self.repository)
        role = cm.Role.objects.create(name='Reviewer', slug='reviewer')
        rm.RepositoryRole.objects.create(
            repository=self.repository,
            user=self.reviewer,
            role=role,
        )
        self.preprint_author = helpers.create_user(
            username='repo_author@janeway.systems',
        )
        self.preprint_one = helpers.create_preprint(
            self.repository,
            self.preprint_author,
            self.subject,
            title='Preprint Number One',
        )
        self.server_name = "repo.test.com"
        update_settings()
        clear_script_prefix()

    @override_settings(URL_CONFIG='domain')
    def test_invite_reviewer(self):
        data = {
            'reviewer': self.reviewer.pk,
            'date_due': '2022-01-01',
        }
        path = reverse(
            'repository_new_review',
            kwargs={
                'preprint_id': self.preprint_one.pk,
            }
        )
        self.client.force_login(self.repo_manager)
        response = self.client.post(
            path,
            data=data,
            SERVER_NAME=self.server_name,
        )
        self.assertEqual(
            1,
            self.preprint_one.review_set.count(),
        )

    @override_settings(URL_CONFIG='domain')
    def test_notify_reviewer(self):
        review = rm.Review.objects.create(
            reviewer=self.reviewer,
            preprint=self.preprint_one,
            manager=self.repo_manager,
            date_due=timezone.now(),
        )
        data = {
            'message': 'This is a test email',
        }
        path = reverse(
            'repository_notify_reviewer',
            kwargs={
                'preprint_id': self.preprint_one.pk,
                'review_id': review.pk,
            }
        )
        self.client.force_login(
            self.repo_manager,
        )
        response = self.client.post(
            path,
            data=data,
            SERVER_NAME=self.server_name,
        )
        self.assertEqual(
            'Preprint Review Invitation',
            mail.outbox[0].subject
        )

    @override_settings(URL_CONFIG='domain')
    def test_do_review(self):
        review = rm.Review.objects.create(
            reviewer=self.reviewer,
            preprint=self.preprint_one,
            manager=self.repo_manager,
            date_due=timezone.now(),
            status='new',
        )
        data = {
            'body': 'This is my review.',
            'anonymous': True,
        }
        path = reverse(
            'repository_submit_review',
            kwargs={
                'review_id': review.pk,
                'access_code': review.access_code,
            }
        )
        self.client.post(
            path,
            data=data,
            SERVER_NAME=self.server_name,
        )
        comment = rm.Comment.objects.get(
            author=review.reviewer,
            preprint=self.preprint_one,
        )
        self.assertEqual(
            comment.body,
            'This is my review.',
        )

    @override_settings(URL_CONFIG='domain')
    def test_publish_review_comment(self):
        comment = rm.Comment.objects.create(
            author=self.reviewer,
            preprint=self.preprint_one,
            body='This is my review',
        )
        review = rm.Review.objects.create(
            reviewer=self.reviewer,
            preprint=self.preprint_one,
            manager=self.repo_manager,
            date_due=timezone.now(),
            status='complete',
            comment=comment
        )
        path = reverse(
            'repository_review_detail',
            kwargs={
                'preprint_id': self.preprint_one.pk,
                'review_id': review.pk,
            }
        )
        self.client.force_login(self.repo_manager)
        self.client.post(
            path,
            data={
                'publish': True,
            },
            SERVER_NAME=self.server_name,
        )
        self.assertEqual(
            1,
            self.preprint_one.comment_set.filter(
                review__isnull=False,
                is_public=True,
            ).count()
        )

    @override_settings(URL_CONFIG='domain')
    def test_unpublish_review_comment(self):
        comment = rm.Comment.objects.create(
            author=self.reviewer,
            preprint=self.preprint_one,
            body='This is my review',
            is_public=True,
            is_reviewed=True,
        )
        review = rm.Review.objects.create(
            reviewer=self.reviewer,
            preprint=self.preprint_one,
            manager=self.repo_manager,
            date_due=timezone.now(),
            status='complete',
            comment=comment
        )
        path = reverse(
            'repository_review_detail',
            kwargs={
                'preprint_id': self.preprint_one.pk,
                'review_id': review.pk,
            }
        )
        self.client.force_login(self.repo_manager)
        self.client.post(
            path,
            data={
                'unpublish': True,
            },
            SERVER_NAME=self.server_name,
        )
        self.assertEqual(
            0,
            self.preprint_one.comment_set.filter(
                review__isnull=False,
                is_public=True,
            ).count()
        )

    @override_settings(URL_CONFIG='domain')
    def test_edit_review_comment(self):
        comment = rm.Comment.objects.create(
            author=self.reviewer,
            preprint=self.preprint_one,
            body='This is my review',
            is_public=True,
            is_reviewed=True,
        )
        review = rm.Review.objects.create(
            reviewer=self.reviewer,
            preprint=self.preprint_one,
            manager=self.repo_manager,
            date_due=timezone.now(),
            status='complete',
            comment=comment
        )
        path = reverse(
            'repository_edit_review_comment',
            kwargs={
                'preprint_id': self.preprint_one.pk,
                'review_id': review.pk,
            }
        )
        self.client.force_login(self.repo_manager)
        self.client.post(
            path,
            data={
                'body': 'This is my slightly different review.',
                'anonymous': False,
            },
            SERVER_NAME=self.server_name,
        )
        comment = rm.Comment.objects.get(
            author=review.reviewer,
            preprint=self.preprint_one,
        )
        self.assertEqual(
            comment.body,
            'This is my slightly different review.',
        )
