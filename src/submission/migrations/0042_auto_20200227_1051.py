# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-02-27 10:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0040_article_projected_issue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='stage',
            field=models.CharField(choices=[('Unsubmitted', 'Unsubmitted'), ('Unassigned', 'Unassigned'), ('Assigned', 'Assigned to Editor'), ('Under Review', 'Peer Review'), ('Under Revision', 'Revision'), ('Rejected', 'Rejected'), ('Accepted', 'Accepted'), ('Editor Copyediting', 'Editor Copyediting'), ('Author Copyediting', 'Author Copyediting'), ('Final Copyediting', 'Final Copyediting'), ('Typesetting', 'Typesetting'), ('Proofing', 'Proofing'), ('pre_publication', 'Pre Publication'), ('Published', 'Published'), ('preprint_review', 'Preprint Review'), ('preprint_published', 'Preprint Published'), ('typesetting_plugin', 'Typesetting Plugin')], default='Unsubmitted', max_length=200),
        ),
    ]
