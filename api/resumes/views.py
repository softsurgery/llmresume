import os
import re
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404

from .viewsets.resume_view import *


def download_file(request, job_id, filename):
    # Validate job_id
    if not re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', job_id):
        raise Http404("Invalid job ID")

    # Prevent path traversal in filename
    safe_filename = os.path.basename(filename)
    job_dir = Path(settings.MEDIA_ROOT) / "jobs" / job_id

    # Search for the file in the job directory (including subdirectories)
    file_path = None
    for f in job_dir.rglob(safe_filename):
        if f.is_file():
            file_path = f
            break

    if not file_path or not file_path.exists():
        raise Http404("File not found")

    # Ensure the resolved path is within the job directory
    if not str(file_path.resolve()).startswith(str(job_dir.resolve())):
        raise Http404("File not found")

    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=safe_filename)