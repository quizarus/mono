import pytest

from app.quiz.si_importer.pack_loader import load


@pytest.fixture
def si_pack_content():
    return load('.sources/pack.siq')
