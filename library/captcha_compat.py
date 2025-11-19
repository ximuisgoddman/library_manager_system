"""
Compatibility helpers for third-party apps.

django-simple-captcha<=0.5 expects Pillow's ``ImageFont`` objects to expose the
``getsize`` method. Pillow 10 removed it in favour of ``getlength`` /
``getbbox``, which leads to ``AttributeError: 'FreeTypeFont' object has no
attribute 'getsize'`` while rendering captcha images.  This module monkey
patches ``captcha.views.getsize`` to compute the character box via ``getbbox``
when necessary so that older captcha versions keep working on newer Pillow
releases.
"""

from __future__ import annotations

import logging
from typing import Tuple

logger = logging.getLogger(__name__)
_PATCHED = False


def _patched_getsize(font, text) -> Tuple[int, int]:
    """
    Replacement for captcha.views.getsize that tolerates Pillow>=10.

    Uses ``getbbox`` if ``getsize`` no longer exists and keeps the legacy
    behaviour of adding ``getoffset`` (when available) so the upstream code
    does not need to change.
    """

    width = height = 0

    if hasattr(font, "getsize"):
        width, height = font.getsize(text)
    elif hasattr(font, "getbbox"):
        left, top, right, bottom = font.getbbox(text)
        width = right - left
        height = bottom - top
    else:  # pragma: no cover
        logger.debug("Unknown font object for captcha rendering: %s", font)

    if hasattr(font, "getoffset"):
        offset_x, offset_y = font.getoffset(text)
        width += offset_x
        height += offset_y

    return int(width), int(height)


def patch_captcha_getsize(force: bool = False) -> bool:
    """
    Attempt to patch ``captcha.views.getsize``.

    Returns True if the patch was applied, False otherwise.
    """

    global _PATCHED
    if _PATCHED and not force:
        return True

    try:
        from captcha import views as captcha_views  # pylint: disable=import-outside-toplevel
    except Exception as exc:  # pragma: no cover - captcha optional in some envs
        logger.debug("captcha compatibility patch skipped: %s", exc)
        return False

    original = getattr(captcha_views, "getsize", None)
    if original is None:
        logger.debug("captcha.views has no getsize function to patch")
        return False

    if getattr(original, "__module__", "") == __name__ and not force:
        _PATCHED = True
        return True

    captcha_views.getsize = _patched_getsize
    _PATCHED = True
    logger.info("Patched captcha.views.getsize for Pillow >= 10 compatibility")
    return True


try:  # Best-effort patch during module import; silent failure if settings not ready.
    patch_captcha_getsize()
except Exception:  # pragma: no cover
    logger.debug("Initial captcha patch attempt failed; will retry later.", exc_info=True)

