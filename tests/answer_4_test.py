import unittest
from datetime import date
from decimal import Decimal
from answer_4 import (
    TerminationBenefits,
    _validate_input,
    _calculate_last_anniversary,
    _calculate_vacation_value,
    _calculate_thirteenth_period_start,
    _calculate_thirteenth_salary_value,
    _calculate_months_worked,
    calculate_termination_benefits,
)
from constants.errors import ERROR_INVALID_DATE_ORDER, ERROR_INVALID_SALARY


class TestTerminationBenefits(unittest.TestCase):
    """Test cases for TerminationBenefits dataclass."""

    def test_termination_benefits_creation(self):
        """Test TerminationBenefits object creation."""
        vacation = Decimal('1000.00')
        thirteenth_salary = Decimal('500.00')
        benefits = TerminationBenefits(vacation, thirteenth_salary)

        self.assertEqual(benefits.vacation, vacation)
        self.assertEqual(benefits.thirteenth_salary, thirteenth_salary)

    def test_total_property(self):
        """Test total property calculation."""
        vacation = Decimal('1000.00')
        thirteenth_salary = Decimal('500.00')
        benefits = TerminationBenefits(vacation, thirteenth_salary)

        expected_total = Decimal('1500.00')
        self.assertEqual(benefits.total, expected_total)

    def test_total_property_zero_values(self):
        """Test total property with zero values."""
        benefits = TerminationBenefits(Decimal('0'), Decimal('0'))
        self.assertEqual(benefits.total, Decimal('0'))

    def test_frozen_dataclass(self):
        """Test that TerminationBenefits is immutable."""
        benefits = TerminationBenefits(Decimal('1000'), Decimal('500'))
        with self.assertRaises(AttributeError):
            benefits.vacation = Decimal('2000')


class TestValidateInput(unittest.TestCase):
    """Test cases for _validate_input function."""

    def test_valid_input(self):
        """Test with valid input parameters."""
        hire_date = date(2023, 1, 1)
        termination_date = date(2023, 12, 31)
        salary = Decimal('3000.00')

        # Should not raise any exception
        _validate_input(hire_date, termination_date, salary)

    def test_invalid_date_order(self):
        """Test with termination date before hire date."""
        hire_date = date(2023, 12, 31)
        termination_date = date(2023, 1, 1)
        salary = Decimal('3000.00')

        with self.assertRaises(ValueError) as context:
            _validate_input(hire_date, termination_date, salary)

        self.assertEqual(str(context.exception), ERROR_INVALID_DATE_ORDER)

    def test_same_dates(self):
        """Test with same hire and termination dates."""
        hire_date = date(2023, 6, 15)
        termination_date = date(2023, 6, 15)
        salary = Decimal('3000.00')

        # Should not raise any exception
        _validate_input(hire_date, termination_date, salary)

    def test_zero_salary(self):
        """Test with zero salary."""
        hire_date = date(2023, 1, 1)
        termination_date = date(2023, 12, 31)
        salary = Decimal('0')

        with self.assertRaises(ValueError) as context:
            _validate_input(hire_date, termination_date, salary)

        self.assertEqual(str(context.exception), ERROR_INVALID_SALARY)

    def test_negative_salary(self):
        """Test with negative salary."""
        hire_date = date(2023, 1, 1)
        termination_date = date(2023, 12, 31)
        salary = Decimal('-1000')

        with self.assertRaises(ValueError) as context:
            _validate_input(hire_date, termination_date, salary)

        self.assertEqual(str(context.exception), ERROR_INVALID_SALARY)

    def test_minimum_salary(self):
        """Test with minimum positive salary."""
        hire_date = date(2023, 1, 1)
        termination_date = date(2023, 12, 31)
        salary = Decimal('0.01')

        # Should not raise any exception
        _validate_input(hire_date, termination_date, salary)


class TestCalculateLastAnniversary(unittest.TestCase):
    """Test cases for _calculate_last_anniversary function."""

    def test_same_year_hire_before_termination(self):
        """Test when hire and termination are in same year, hire before termination."""
        hire_date = date(2023, 3, 15)
        termination_date = date(2023, 8, 20)

        result = _calculate_last_anniversary(hire_date, termination_date)
        self.assertEqual(result, hire_date)

    def test_different_years_termination_after_anniversary(self):
        """Test when termination is after the anniversary in current year."""
        hire_date = date(2020, 3, 15)
        termination_date = date(2023, 8, 20)

        result = _calculate_last_anniversary(hire_date, termination_date)
        expected = date(2023, 3, 15)
        self.assertEqual(result, expected)

    def test_different_years_termination_before_anniversary(self):
        """Test when termination is before the anniversary in current year."""
        hire_date = date(2020, 9, 15)
        termination_date = date(2023, 8, 20)

        result = _calculate_last_anniversary(hire_date, termination_date)
        expected = date(2022, 9, 15)
        self.assertEqual(result, expected)

    def test_exact_anniversary_date(self):
        """Test when termination date is exactly the anniversary."""
        hire_date = date(2020, 6, 15)
        termination_date = date(2023, 6, 15)

        result = _calculate_last_anniversary(hire_date, termination_date)
        self.assertEqual(result, termination_date)


class TestCalculateVacationValue(unittest.TestCase):
    """Test cases for _calculate_vacation_value function."""

    def test_zero_months(self):
        """Test vacation calculation with zero months."""
        salary = Decimal('3000.00')
        result = _calculate_vacation_value(salary, 0)
        self.assertEqual(result, Decimal('0'))

    def test_one_month(self):
        """Test vacation calculation with one month."""
        salary = Decimal('3000.00')
        result = _calculate_vacation_value(salary, 1)
        expected = Decimal('3000.00') / Decimal(9)
        self.assertEqual(result, expected)

    def test_six_months(self):
        """Test vacation calculation with six months."""
        salary = Decimal('3000.00')
        result = _calculate_vacation_value(salary, 6)
        expected = salary * Decimal(6) / Decimal(9)
        self.assertEqual(result, expected)

    def test_twelve_months(self):
        """Test vacation calculation with twelve months."""
        salary = Decimal('3000.00')
        result = _calculate_vacation_value(salary, 12)
        expected = salary * Decimal(12) / Decimal(9)
        self.assertEqual(result, expected)

    def test_fractional_salary(self):
        """Test vacation calculation with fractional salary."""
        salary = Decimal('2850.75')
        result = _calculate_vacation_value(salary, 3)
        expected = salary * Decimal(3) / Decimal(9)
        self.assertEqual(result, expected)


class TestCalculateThirteenthPeriodStart(unittest.TestCase):
    """Test cases for _calculate_thirteenth_period_start function."""

    def test_same_year(self):
        """Test when hire and termination are in the same year."""
        hire_date = date(2023, 5, 15)
        termination_date = date(2023, 11, 20)

        result = _calculate_thirteenth_period_start(hire_date, termination_date)
        self.assertEqual(result, hire_date)

    def test_different_years(self):
        """Test when hire and termination are in different years."""
        hire_date = date(2022, 5, 15)
        termination_date = date(2023, 11, 20)

        result = _calculate_thirteenth_period_start(hire_date, termination_date)
        expected = date(2023, 1, 1)
        self.assertEqual(result, expected)

    def test_hire_in_january_different_years(self):
        """Test when hire was in January but different year."""
        hire_date = date(2022, 1, 10)
        termination_date = date(2023, 11, 20)

        result = _calculate_thirteenth_period_start(hire_date, termination_date)
        expected = date(2023, 1, 1)
        self.assertEqual(result, expected)

    def test_hire_december_termination_january(self):
        """Test when hire was in December and termination in January next year."""
        hire_date = date(2022, 12, 15)
        termination_date = date(2023, 1, 10)

        result = _calculate_thirteenth_period_start(hire_date, termination_date)
        expected = date(2023, 1, 1)
        self.assertEqual(result, expected)


class TestCalculateThirteenthSalaryValue(unittest.TestCase):
    """Test cases for _calculate_thirteenth_salary_value function."""

    def test_zero_months(self):
        """Test 13th salary calculation with zero months."""
        salary = Decimal('3000.00')
        result = _calculate_thirteenth_salary_value(salary, 0)
        self.assertEqual(result, Decimal('0'))

    def test_one_month(self):
        """Test 13th salary calculation with one month."""
        salary = Decimal('3000.00')
        result = _calculate_thirteenth_salary_value(salary, 1)
        self.assertEqual(result, Decimal('250.00'))

    def test_six_months(self):
        """Test 13th salary calculation with six months."""
        salary = Decimal('3000.00')
        result = _calculate_thirteenth_salary_value(salary, 6)
        self.assertEqual(result, Decimal('1500.00'))

    def test_twelve_months(self):
        """Test 13th salary calculation with twelve months."""
        salary = Decimal('3000.00')
        result = _calculate_thirteenth_salary_value(salary, 12)
        self.assertEqual(result, salary)

    def test_fractional_salary(self):
        """Test 13th salary calculation with fractional salary."""
        salary = Decimal('2850.75')
        result = _calculate_thirteenth_salary_value(salary, 3)
        expected = salary / Decimal(4)
        self.assertEqual(result, expected)


class TestCalculateMonthsWorked(unittest.TestCase):
    """Test cases for _calculate_months_worked function."""

    def test_same_day(self):
        """Test calculation for same start and end date."""
        start_date = date(2023, 6, 15)
        end_date = date(2023, 6, 15)
        result = _calculate_months_worked(start_date, end_date)
        self.assertEqual(result, 0)

    def test_less_than_15_days_same_month(self):
        """Test calculation with less than 15 days in the same month."""
        start_date = date(2023, 6, 1)
        end_date = date(2023, 6, 10)
        result = _calculate_months_worked(start_date, end_date)
        self.assertEqual(result, 0)

    def test_less_than_15_days_multiple_months(self):
        """Test calculation with less than 15 days in two months."""
        start_date = date(2023, 6, 18)
        end_date = date(2023, 7, 10)
        result = _calculate_months_worked(start_date, end_date)
        self.assertEqual(result, 0)

    def test_exactly_15_days(self):
        """Test calculation with exactly 15 days."""
        start_date = date(2023, 6, 1)
        end_date = date(2023, 6, 15)
        result = _calculate_months_worked(start_date, end_date)
        self.assertEqual(result, 1)

    def test_more_than_15_days(self):
        """Test calculation with more than 15 days."""
        start_date = date(2023, 6, 1)
        end_date = date(2023, 6, 20)
        result = _calculate_months_worked(start_date, end_date)
        self.assertEqual(result, 1)

    def test_first_month_less_than_15_days(self):
        """Test calculation when first month has less than 15 worked days."""
        start_date = date(2023, 6, 18)
        end_date = date(2023, 8, 16)
        result = _calculate_months_worked(start_date, end_date)
        self.assertEqual(result, 2)

    def test_multiple_months_exact_days(self):
        """Test calculation for multiple months with same day."""
        start_date = date(2023, 1, 15)
        end_date = date(2023, 4, 15)
        result = _calculate_months_worked(start_date, end_date)
        self.assertEqual(result, 4)

    def test_multiple_months_with_partial_days(self):
        """Test calculation for multiple months with partial days."""
        start_date = date(2023, 1, 10)
        end_date = date(2023, 4, 20)
        result = _calculate_months_worked(start_date, end_date)
        self.assertEqual(result, 4)

    def test_year_boundary(self):
        """Test calculation across year boundary."""
        start_date = date(2022, 12, 1)
        end_date = date(2023, 2, 15)
        result = _calculate_months_worked(start_date, end_date)
        self.assertEqual(result, 3)

    def test_maximum_months(self):
        """Test calculation that would exceed 12 months."""
        start_date = date(2020, 1, 1)
        end_date = date(2023, 12, 31)
        result = _calculate_months_worked(start_date, end_date)
        self.assertEqual(result, 12)


class TestCalculateTerminationBenefits(unittest.TestCase):
    """Test cases for calculate_termination_benefits main function."""

    def test_complete_calculation_same_year(self):
        """Test complete calculation within the same year."""
        hire_date = date(2023, 3, 15)
        termination_date = date(2023, 8, 20)
        salary = Decimal('3000.00')

        result = calculate_termination_benefits(hire_date, termination_date, salary)

        self.assertEqual(result.vacation, Decimal('2000.00'))
        self.assertEqual(result.thirteenth_salary, Decimal('1500.00'))
        self.assertEqual(result.total, Decimal('3500.00'))

    def test_complete_calculation_different_years(self):
        """Test complete calculation across different years."""
        hire_date = date(2022, 3, 15)
        termination_date = date(2023, 8, 20)
        salary = Decimal('3000.00')

        result = calculate_termination_benefits(hire_date, termination_date, salary)

        self.assertEqual(result.vacation, Decimal('2000.00'))
        self.assertEqual(result.thirteenth_salary, Decimal('2000.00'))
        self.assertEqual(result.total, Decimal('4000.00'))

    def test_termination_on_hire_date(self):
        """Test calculation when termination is on the same day as hire."""
        hire_date = date(2023, 6, 15)
        termination_date = date(2023, 6, 15)
        salary = Decimal('3000.00')

        result = calculate_termination_benefits(hire_date, termination_date, salary)

        self.assertEqual(result.vacation, Decimal('0'))
        self.assertEqual(result.thirteenth_salary, Decimal('0'))
        self.assertEqual(result.total, Decimal('0'))

    def test_termination_on_anniversary(self):
        """Test calculation when termination is exactly on hire anniversary."""
        hire_date = date(2020, 6, 15)
        termination_date = date(2023, 6, 15)
        salary = Decimal('3000.00')

        result = calculate_termination_benefits(hire_date, termination_date, salary)

        # Should have 0 vacation months (terminated exactly on anniversary)
        self.assertEqual(result.vacation, Decimal('0'))

        # Should have thirteenth salary from January 1st
        self.assertEqual(result.thirteenth_salary, Decimal('1500.00'))

    def test_invalid_input_propagation(self):
        """Test that invalid input errors are properly propagated."""
        hire_date = date(2023, 12, 31)
        termination_date = date(2023, 1, 1)
        salary = Decimal('3000.00')

        with self.assertRaises(ValueError) as context:
            calculate_termination_benefits(hire_date, termination_date, salary)

        self.assertEqual(str(context.exception), ERROR_INVALID_DATE_ORDER)

    def test_high_salary_calculation(self):
        """Test calculation with high salary values."""
        hire_date = date(2023, 1, 1)
        termination_date = date(2023, 12, 31)
        salary = Decimal('15000.00')

        result = calculate_termination_benefits(hire_date, termination_date, salary)

        self.assertEqual(result.vacation, Decimal('20000.00'))
        self.assertEqual(result.thirteenth_salary, Decimal('15000.00'))