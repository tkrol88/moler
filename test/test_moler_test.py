# -*- coding: utf-8 -*-

__author__ = 'Michal Ernst, Marcin Usielski'
__copyright__ = 'Copyright (C) 2018, Nokia'
__email__ = 'michal.ernst@nokia.com, marcin.usielski@nokia.com'

import pytest

from moler.connection_observer import ConnectionObserver
from moler.exceptions import MolerStatusException
from moler.util.moler_test import MolerTest


def test_moler_test_not_raise_exception_when_steps_end(moler_test_se):
    ConnectionObserver.get_unraised_exceptions()
    moler_test_se.test_not_raise_exception_when_steps_end()


def test_moler_test_test_raise_exception_when_not_call_steps_end(moler_test_se):
    ConnectionObserver.get_unraised_exceptions()
    with pytest.raises(MolerStatusException):
        moler_test_se.test_raise_exception_when_not_call_steps_end()


def test_moler_test_raise_exception_when_log_error(moler_test_se):
    ConnectionObserver.get_unraised_exceptions()
    with pytest.raises(MolerStatusException):
        moler_test_se.test_raise_exception_when_log_error()


def test_moler_test_raise_exception_when_log_error_raise_exception_set(moler_test_se):
    ConnectionObserver.get_unraised_exceptions()
    with pytest.raises(MolerStatusException):
        moler_test_se.test_raise_exception_when_log_error_raise_exception_set()


def test_moler_test_not_raise_exception_when_no_steps_end(moler_test):
    ConnectionObserver.get_unraised_exceptions()
    moler_test.test_not_raise_exception_when_no_steps_end()


def test_moler_test_raise_exception_when_no_steps_end_for_global_method():
    with pytest.raises(MolerStatusException):
        moler_test_raise_exception_when_no_steps_end_for_global_method()


# connection observer running in background thread may raise exception
# but such exception is not visible inside MainThread
# However, in all such cases connection observer stores exception via conn_obs.set_exception()


def test_exception_in_observer_is_raised_when_result_is_called_after_set_exception(do_nothing_connection_observer,
                                                                                   ObserverExceptionClass):
    exc = ObserverExceptionClass("some error inside observer")

    def function_using_observer():
        observer = do_nothing_connection_observer
        # for real usage observer should be started to run background thread that will set_exception()
        # but for unit tests we just call it (simulating background thread)
        observer.set_exception(exc)
        print(observer.result())

    with pytest.raises(ObserverExceptionClass) as err:
        function_using_observer()
    assert err.value == exc


def test_exception_in_observer_is_ignored_if_no_result_called_nor_decorator_on_function(do_nothing_connection_observer,
                                                                                        ObserverExceptionClass):
    def function_using_observer():
        observer = do_nothing_connection_observer
        observer.set_exception(ObserverExceptionClass("some error inside observer"))

    function_using_observer()  # should not raise so test should pass


def test_exception_in_observer_is_raised_if_no_result_called_but_decorator_on_function(do_nothing_connection_observer,
                                                                                       ObserverExceptionClass):
    from moler.util.moler_test import MolerTest
    exc = ObserverExceptionClass("some error inside observer")

    @MolerTest.raise_background_exceptions()
    def function_using_observer():
        observer = do_nothing_connection_observer
        observer.set_exception(exc)

    with pytest.raises(MolerStatusException) as err:
        function_using_observer()
    assert exc in err.value.exceptions


def test_exception_in_observer_is_raised_if_no_result_called_but_parameterless_decorator_on_function(
        do_nothing_connection_observer,
        ObserverExceptionClass):
    from moler.util.moler_test import MolerTest
    exc = ObserverExceptionClass("some error inside observer")

    @MolerTest.raise_background_exceptions
    def function_using_observer():
        observer = do_nothing_connection_observer
        observer.set_exception(exc)

    with pytest.raises(MolerStatusException) as err:
        function_using_observer()


def test_exception_in_observer_is_raised_if_no_result_called_but_decorator_on_method(do_nothing_connection_observer,
                                                                                     ObserverExceptionClass):
    from moler.util.moler_test import MolerTest
    exc = ObserverExceptionClass("some error inside observer")

    class MyTest(object):
        @MolerTest.raise_background_exceptions()
        # @MolerTest.raise_background_exceptions  # doesn't work since it is created by python and given class as first argument
        #                                               # compare with syntax of @pytest.fixture  @pytest.yield_fixture
        def method_using_observer(self):
            observer = do_nothing_connection_observer
            observer.set_exception(exc)

    with pytest.raises(MolerStatusException) as err:
        MyTest().method_using_observer()


def test_exception_in_observer_is_raised_if_no_result_called_but_parameterless_decorator_on_method(
        do_nothing_connection_observer,
        ObserverExceptionClass):
    from moler.util.moler_test import MolerTest
    exc = ObserverExceptionClass("some error inside observer")

    class MyTest(object):
        @MolerTest.raise_background_exceptions
        def method_using_observer(self):
            observer = do_nothing_connection_observer
            observer.set_exception(exc)

    with pytest.raises(MolerStatusException) as err:
        MyTest().method_using_observer()


def test_exception_in_observer_is_raised_if_no_result_called_but_decorator_on_classmethod(
        do_nothing_connection_observer,
        ObserverExceptionClass):
    from moler.util.moler_test import MolerTest
    exc = ObserverExceptionClass("some error inside observer")

    with pytest.raises(MolerStatusException) as err:
        class MyTest(object):
            # TODO: Add later
            @MolerTest.raise_background_exceptions()
            @classmethod
            def method_using_observer(cls):
                observer = do_nothing_connection_observer
                observer.set_exception(exc)

        MyTest.method_using_observer()


def test_exception_in_observer_is_raised_if_no_result_called_but_parameterless_decorator_on_classmethod(
        do_nothing_connection_observer,
        ObserverExceptionClass):
    from moler.util.moler_test import MolerTest
    exc = ObserverExceptionClass("some error inside observer")

    with pytest.raises(MolerStatusException) as err:
        class MyTest(object):
            # TODO: Add later support for decorating classmethod and staticmethod
            @MolerTest.raise_background_exceptions
            @classmethod
            def method_using_observer(cls):
                observer = do_nothing_connection_observer
                observer.set_exception(exc)

        MyTest.method_using_observer()


def test_exception_in_observer_is_raised_if_no_result_called_but_decorator_on_staticmethod(
        do_nothing_connection_observer,
        ObserverExceptionClass):
    from moler.util.moler_test import MolerTest
    exc = ObserverExceptionClass("some error inside observer")

    with pytest.raises(MolerStatusException) as err:
        class MyTest(object):
            # TODO: Add later support for decorating classmethod and staticmethod
            @MolerTest.raise_background_exceptions()
            @staticmethod
            def method_using_observer():
                observer = do_nothing_connection_observer
                observer.set_exception(exc)

        MyTest.method_using_observer()


def test_exception_in_observer_is_raised_if_no_result_called_but_parameterless_decorator_on_staticmethod(
        do_nothing_connection_observer,
        ObserverExceptionClass):
    from moler.util.moler_test import MolerTest
    exc = ObserverExceptionClass("some error inside observer")

    with pytest.raises(MolerStatusException) as err:
        class MyTest(object):
            # TODO: Add later
            @MolerTest.raise_background_exceptions
            @staticmethod
            def method_using_observer():
                observer = do_nothing_connection_observer
                observer.set_exception(exc)

        MyTest.method_using_observer()


def test_exception_in_observer_is_raised_if_no_result_called_but_decorator_on_class(do_nothing_connection_observer,
                                                                                    ObserverExceptionClass):
    from moler.util.moler_test import MolerTest
    exc = ObserverExceptionClass("some error inside observer")

    @MolerTest.raise_background_exceptions()
    class MyTest(object):
        def method_using_observer(self):
            observer = do_nothing_connection_observer
            observer.set_exception(exc)

    with pytest.raises(MolerStatusException) as err:
        MyTest().method_using_observer()


def test_exception_in_observer_is_raised_if_no_result_called_but_parameterless_decorator_on_class(
        do_nothing_connection_observer,
        ObserverExceptionClass):
    from moler.util.moler_test import MolerTest
    exc = ObserverExceptionClass("some error inside observer")

    @MolerTest.raise_background_exceptions
    class MyTest(object):
        def method_using_observer(self):
            observer = do_nothing_connection_observer
            observer.set_exception(exc)

    with pytest.raises(MolerStatusException) as err:
        MyTest().method_using_observer()


def test_exception_in_observer_is_raised_if_no_result_called_but_decorator_on_derived_class(
        do_nothing_connection_observer, ObserverExceptionClass):
    from moler.util.moler_test import MolerTest
    exc = ObserverExceptionClass("some error inside observer")

    class MyTestBase(object):
        def method_using_observer(self):
            observer = do_nothing_connection_observer
            observer.set_exception(exc)

    @MolerTest.raise_background_exceptions()
    class MyTest(MyTestBase):
        def method_of_derived_class(self):
            pass

    with pytest.raises(MolerStatusException) as err:
        MyTest().method_using_observer()


def test_exception_in_observer_is_raised_if_no_result_called_but_parameterless_decorator_on_derived_class(
        do_nothing_connection_observer, ObserverExceptionClass):
    from moler.util.moler_test import MolerTest
    exc = ObserverExceptionClass("some error inside observer")

    class MyTestBase(object):
        def method_using_observer(self):
            observer = do_nothing_connection_observer
            observer.set_exception(exc)

    @MolerTest.raise_background_exceptions
    class MyTest(MyTestBase):
        def method_of_derived_class(self):
            pass

    with pytest.raises(MolerStatusException) as err:
        MyTest().method_using_observer()


# --------------------------- resources ---------------------------

@pytest.yield_fixture
def moler_test_se():
    from moler.util.moler_test import MolerTest

    @MolerTest.raise_background_exceptions(check_steps_end=True)
    class MolerTestExampleSE(object):
        def test_not_raise_exception_when_steps_end(self):
            MolerTest.info("Start MolerTest test with log and steps_end")

            MolerTest.steps_end()

        def test_raise_exception_when_not_call_steps_end(self):
            MolerTest.info("Start MolerTest test with log and without steps_end")

        def test_raise_exception_when_log_error(self):
            MolerTest.error("Start MolerTest test with log_error")

        def test_raise_exception_when_log_error_raise_exception_set(self):
            MolerTest.error("Start MolerTest test with log_error and raise_exception", raise_exception=True)

    yield MolerTestExampleSE()


@pytest.yield_fixture
def moler_test():
    from moler.util.moler_test import MolerTest

    @MolerTest.raise_background_exceptions()
    class MolerTestExample(object):
        def test_not_raise_exception_when_no_steps_end(self):
            MolerTest.info("Start MolerTest test with log and steps_end")

    yield MolerTestExample()


@MolerTest.raise_background_exceptions(check_steps_end=True)
def moler_test_raise_exception_when_no_steps_end_for_global_method():
    MolerTest.info("Start global method with log and without steps_end")


@pytest.yield_fixture
def do_nothing_connection_observer():
    from moler.connection_observer import ConnectionObserver

    class DoNothingObserver(ConnectionObserver):
        def data_received(self, data):  # we need to overwrite it since it is @abstractmethod
            pass  # ignore incoming data

    observer = DoNothingObserver()

    ConnectionObserver.get_unraised_exceptions()
    yield observer
    ConnectionObserver.get_unraised_exceptions()


@pytest.fixture
def ObserverExceptionClass():
    class ObserverException(Exception):
        pass

    return ObserverException
