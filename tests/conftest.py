"""Scaffold tests use an in-memory kit tarball, not GitHub main."""

from __future__ import annotations

import io
import tarfile

import pytest

_KIT_FILES = {
    "pixeltable-starter-kit-main/chat-agent/app.py": "agent = True\n",
    "pixeltable-starter-kit-main/chat-agent/pyproject.toml": '[project]\nname = "chat-agent"\n',
    "pixeltable-starter-kit-main/chat-agent/pixeltable.toml": "[[pixeltable.database]]\n",
    "pixeltable-starter-kit-main/video-search/app.py": "videointel = True\n",
    "pixeltable-starter-kit-main/video-search/pyproject.toml": '[project]\nname = "video-search"\n',
    "pixeltable-starter-kit-main/video-search/pixeltable.toml": "[[pixeltable.database]]\n",
}


def _kit_tarball() -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        for name, content in _KIT_FILES.items():
            data = content.encode()
            info = tarfile.TarInfo(name=name)
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))
    return buf.getvalue()


@pytest.fixture(autouse=True)
def _local_starter_kit(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _kit_tarball()
    monkeypatch.setattr("pixeltable_new.new.fetch_tarball", lambda url="": payload)
