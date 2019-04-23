import pytest


def uid(v):
    return f"id{v}"


@pytest.fixture
def id0():
    return uid(0)


@pytest.fixture
def id1():
    return uid(1)


@pytest.fixture
def id2():
    return uid(2)


@pytest.fixture
def id3():
    return uid(3)


@pytest.fixture
def id4():
    return uid(4)
