
import pytest

from course_registration import (
    can_register,
    waitlist_position,
    late_fee,
)


# Branch tests for can_register()


def test_can_register_valid_status():
    assert can_register("regular", 10, 3, True) == "registered"


def test_can_register_unknown_status():
    with pytest.raises(ValueError):
        can_register("invalid", 10, 3, True)


def test_can_register_valid_credits():
    assert can_register("regular", 10, 3, True) == "registered"


def test_can_register_invalid_credits():
    with pytest.raises(ValueError):
        can_register("regular", 10, 0, True)


def test_prerequisites_met():
    assert can_register("regular", 10, 3, True) == "registered"


def test_prerequisites_not_met():
    assert can_register("regular", 10, 3, False) == "prerequisites missing"


def test_credit_limit_not_exceeded():
    assert can_register("regular", 10, 3, True) == "registered"


def test_credit_limit_exceeded():
    assert can_register("probation", 15, 2, True) == "credit limit exceeded"


# Branch tests for waitlist_position()


def test_invalid_capacity():
    with pytest.raises(ValueError):
        waitlist_position(10, 0, 2)


def test_valid_capacity():
    assert waitlist_position(10, 20, 2) == 0


def test_seats_available():
    assert waitlist_position(10, 20, 2) == 0


def test_no_seats_available():
    assert waitlist_position(20, 20, 2) == 3


def test_waitlist_not_full():
    assert waitlist_position(20, 20, 9) == 10


def test_waitlist_full():
    assert waitlist_position(20, 20, 10) == -1


# Branch tests for late_fee()


def test_days_late_zero():
    assert late_fee(0, 15, False) == 0


def test_days_late_positive():
    assert late_fee(5, 15, False) == 500


def test_waiver_present():
    assert late_fee(5, 15, True) == 0


def test_waiver_absent():
    assert late_fee(5, 15, False) == 500


def test_late_fee_within_seven_days():
    assert late_fee(7, 15, False) == 500


def test_late_fee_after_seven_days():
    assert late_fee(8, 15, False) == 600


def test_credits_above_twenty():
    assert late_fee(5, 21, False) == 750


def test_credits_twenty_or_below():
    assert late_fee(5, 20, False) == 500


def test_fee_exceeds_maximum():
    assert late_fee(30, 21, False) == 2000


def test_fee_does_not_exceed_maximum():
    assert late_fee(5, 15, False) == 500
