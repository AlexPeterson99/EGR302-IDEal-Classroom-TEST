from __future__ import absolute_import, unicode_literals

# added by Abanou Farag on 4/14/2020 to allow server to see changes in apps.py
default_app_config = 'ideal_classroom.apps.IdealClassroomConfig'
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
