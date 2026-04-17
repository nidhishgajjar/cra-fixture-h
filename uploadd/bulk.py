import os
import zipfile
from io import BytesIO
from uploadd.service import UPLOAD_ROOT


def make_archive(user_id, filenames):
    """Zip up the requested files for a user, return bytes."""
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in filenames:
            path = os.path.join(UPLOAD_ROOT, user_id, name)
            if os.path.isfile(path):
                with open(path, "rb") as f:
                    zf.writestr(name, f.read())
    return buf.getvalue()
