import pytest

from roboscript import execute
from syntax import highlight


def test_highlight():
    assert highlight("F3RF5LF7") == '<span style="color: pink">F</span><span style="color: orange">3</span><span style="color: green">R</span><span style="color: pink">F</span><span style="color: orange">5</span><span style="color: red">L</span><span style="color: pink">F</span><span style="color: orange">7</span>'
    assert highlight("FFFR345F2LL") == '<span style="color: pink">FFF</span><span style="color: green">R</span><span style="color: orange">345</span><span style="color: pink">F</span><span style="color: orange">2</span><span style="color: red">LL</span>'


def test_rs1():
    assert execute("") == "*"
    assert execute("FFFFF") == "******"
    assert execute("FFFFFLFFFFFLFFFFFLFFFFFL") == "******\r\n*    *\r\n*    *\r\n*    *\r\n*    *\r\n******"
    assert execute("LFFFFFRFFFRFFFRFFFFFFF") == "    ****\r\n    *  *\r\n    *  *\r\n********\r\n    *   \r\n    *   "
    assert execute("LF5RF3RF3RF7") == "    ****\r\n    *  *\r\n    *  *\r\n********\r\n    *   \r\n    *   "


def test_rs2():
    assert execute("LF5(RF3)(RF3R)F7") == "    ****\r\n    *  *\r\n    *  *\r\n********\r\n    *   \r\n    *   "
    assert execute("(L(F5(RF3))(((R(F3R)F7))))") == "    ****\r\n    *  *\r\n    *  *\r\n********\r\n    *   \r\n    *   "
    assert execute("F4L(F4RF4RF4LF4L)2F4RF4RF4") == "    *****   *****   *****\r\n    *   *   *   *   *   *\r\n    *   *   *   *   *   *\r\n    *   *   *   *   *   *\r\n*****   *****   *****   *"
    assert execute("F4L((F4R)2(F4L)2)2(F4R)2F4") == "    *****   *****   *****\r\n    *   *   *   *   *   *\r\n    *   *   *   *   *   *\r\n    *   *   *   *   *   *\r\n*****   *****   *****   *"


def assert_path_equals(actual, expected):
    try:
        assert actual == expected
    except AssertionError:
        print("You returned:")
        print(actual)
        print("Expected path of MyRobot:")
        print(expected)
        raise


def expect_error(why, code):
    with pytest.raises(Exception, message=why):
        execute(code)


@pytest.mark.parametrize("message,assertions", [
    ('should work for RS2-compliant programs', [
        lambda: assert_path_equals(execute('(F2LF2R)2FRF4L(F2LF2R)2(FRFL)4(F2LF2R)2'), "    **   **      *\r\n    **   ***     *\r\n  **** *** **  ***\r\n  *  * *    ** *  \r\n***  ***     ***  "),
    ]),
    ('should properly parse a pattern definition and not cause any side effects', [
        lambda: assert_path_equals(execute('p0(F2LF2R)2q'), '*'),
        lambda: assert_path_equals(execute('p312(F2LF2R)2q'), '*'),
    ]),
    ('should execute a given pattern when it is invoked', [
        lambda: assert_path_equals(execute('p0(F2LF2R)2qP0'), "    *\r\n    *\r\n  ***\r\n  *  \r\n***  "),
        lambda: assert_path_equals(execute('p312(F2LF2R)2qP312'), "    *\r\n    *\r\n  ***\r\n  *  \r\n***  "),
    ]),
    ('should always parse pattern definitions first before attempting to invoke them', [
        lambda: assert_path_equals(execute('P0p0(F2LF2R)2q'), "    *\r\n    *\r\n  ***\r\n  *  \r\n***  "),
        lambda: assert_path_equals(execute('P312p312(F2LF2R)2q'), "    *\r\n    *\r\n  ***\r\n  *  \r\n***  "),
    ]),
    ('should allow other forms of RoboScript code alongside pattern definitions and invocations', [
        lambda: assert_path_equals(execute('F3P0Lp0(F2LF2R)2qF2'), "       *\r\n       *\r\n       *\r\n       *\r\n     ***\r\n     *  \r\n******  "),
    ]),
    ('should allow a pattern to be invoked multiple times', [
        lambda: assert_path_equals(execute('(P0)2p0F2LF2RqP0'), "      *\r\n      *\r\n    ***\r\n    *  \r\n  ***  \r\n  *    \r\n***    ")
    ]),
    ('should throw an error when a non-existing pattern is invoked', [
        lambda: expect_error('Your interpreter should throw an error because pattern "P1" does not exist', 'p0(F2LF2R)2qP1'),
        lambda: expect_error('Your interpreter should throw an error because pattern "P0" does not exist', 'P0p312(F2LF2R)2q'),
        lambda: expect_error('Your interpreter should throw an error because pattern "P312" does not exist', 'P312'),
    ]),
    ('should properly parse multiple pattern definitions', [
        lambda: assert_path_equals(execute('P1P2p1F2Lqp2F2RqP2P1'), "  ***\r\n  * *\r\n*** *"),
        lambda: assert_path_equals(execute('p1F2Lqp2F2Rqp3P1(P2)2P1q(P3)3'), "  *** *** ***\r\n  * * * * * *\r\n*** *** *** *"),
    ]),
    ('should throw an error when a pattern is defined more than once', [
        lambda: expect_error('Your interpreter should throw an error since pattern "P1" is defined twice', 'p1F2Lqp1(F3LF4R)5qp2F2Rqp3P1(P2)2P1q(P3)3'),
    ]),
    ('should throw an error when any form of infinite recursion is detected', [
        lambda: expect_error('should throw an error when any form of infinite recursion is detected', 'p1F2RP1F2LqP1'),
        lambda: expect_error('Your interpreter should throw an error since pattern "P1" invokes "P2" which then again invokes "P1", creating an infinite cycle', 'p1F2LP2qp2F2RP1qP1'),
    ])
])
def test_rs3(message, assertions):
    for assertion in assertions:
        assertion()
