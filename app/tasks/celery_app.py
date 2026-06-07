"""
Background task integration placeholder.

Celery was removed from the production runtime profile. Offline jobs should run
through scripts or a future dedicated worker service with its own dependency
profile and deployment target.
"""

BACKGROUND_TASKS_STATUS = "disabled"
