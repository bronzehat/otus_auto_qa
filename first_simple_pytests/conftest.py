import pytest

@pytest.fixture(scope="function", autouse=True)
def divider_function(request):
    print("\n        --- function %s() start ---" % request.function.__name__)

    def fin():
        print("        --- function %s() done ---" % request.function.__name__)

    request.addfinalizer(fin)


@pytest.fixture(scope="module", autouse=True)
def divider_module(request):
    print("\n    ------- module %s start ---------" % request.module.__name__)

    def fin():
        print("    ------- module %s done ---------" % request.module.__name__)

    request.addfinalizer(fin)


@pytest.fixture(scope="session", autouse=True)
def divider_session(request):
    print("\n----------- session start ---------------")

    def fin():
        print("----------- session done ---------------")

    request.addfinalizer(fin)