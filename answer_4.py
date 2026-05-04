import calendar
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_UP
from constants.errors import ERROR_INVALID_DATE_ORDER, ERROR_INVALID_SALARY

@dataclass(frozen=True)
class TerminationBenefits:
    """Immutable container for termination benefit values.

    Attributes:
        vacation: Proportional vacation value including constitutional 1/3 bonus,
                 automatically rounded to 2 decimal places with round up.
        thirteenth_salary: Proportional 13th salary value,
                          automatically rounded to 2 decimal places with round up.
    """
    vacation: Decimal
    thirteenth_salary: Decimal

    def __post_init__(self):
        """Round all monetary values to 2 decimal places with round up."""
        object.__setattr__(self, 'vacation',
                        self.vacation.quantize(Decimal('0.01'), rounding=ROUND_UP))
        object.__setattr__(self, 'thirteenth_salary',
                        self.thirteenth_salary.quantize(Decimal('0.01'), rounding=ROUND_UP))

    @property
    def total(self) -> Decimal:
        """Calculate the total sum of all benefits.

        Returns:
            Decimal: Sum of vacation and thirteenth salary values.
        """
        return self.vacation + self.thirteenth_salary


def _validate_input(hire_date: date, termination_date: date, salary: Decimal) -> None:
    """Validate input parameters for benefit calculation.

    Args:
        hire_date: The date when the employee was hired.
        termination_date: The date when the employee was terminated.
        salary: The employee's gross monthly salary.

    Raises:
        ValueError: If termination_date is before hire_date, or if salary is not positive.
    """
    if termination_date < hire_date:
        raise ValueError(ERROR_INVALID_DATE_ORDER)
    if salary <= 0:
        raise ValueError(ERROR_INVALID_SALARY)



def _calculate_last_anniversary(hire_date: date, termination_date: date) -> date:
    """Calculate the most recent hire anniversary before termination.

    Finds the last occurrence of the hire month/day that falls on or before
    the termination date. This marks the start of the current vacation cycle.

    Args:
        hire_date: The original hire date of the employee.
        termination_date: The termination date.

    Returns:
        date: The last hire anniversary date before termination.
    """
    last_anniversary = date(
        termination_date.year,
        hire_date.month,
        hire_date.day
    )
    if last_anniversary > termination_date:
        last_anniversary = date(
            termination_date.year - 1,
            hire_date.month,
            hire_date.day
        )
    return last_anniversary


def _calculate_months_worked(start_date: date, end_date: date) -> int:
    """Calculate the number of months worked between two dates with a limit of 12 months.

    A month is counted if 15 or more days were worked within it.

    Args:
        start_date: The start date of the period.
        end_date: The end date of the period.

    Returns:
        int: Number of months worked.
    """
    total_months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month

    if total_months == 0 and (end_date.day - start_date.day) >= 14:
        total_months += 1
    elif total_months > 0:
        _, start_month_days = calendar.monthrange(start_date.year, start_date.month)
        if (start_month_days - start_date.day) >= 14:
            total_months += 1
        if end_date.day < 15:
            total_months -= 1

    return min(12, total_months)


def _calculate_vacation_value(salary: Decimal, months: int) -> Decimal:
    """Calculate proportional vacation value with constitutional 1/3 bonus.

    Brazilian law mandates a 1/3 bonus on top of proportional vacation.
    Formula: (salary * months / 12) * (4/3) = salary * months / 9

    Args:
        salary: The employee's monthly salary.
        months: Number of months worked in the vacation cycle (0-12).

    Returns:
        Decimal: The vacation value including the constitutional 1/3 bonus.
    """
    return salary * Decimal(months) / Decimal(9)


def _calculate_thirteenth_period_start(
    hire_date: date,
    termination_date: date
) -> date:
    """Determine the start date for 13th salary calculation.

    The 13th salary cycle starts on January 1st of each year, unless the
    employee was hired in the same year as termination, in which case it
    starts from the hire date.

    Args:
        hire_date: The employee's hire date.
        termination_date: The termination date.

    Returns:
        date: The start date of the 13th salary calculation period.
    """
    if hire_date.year == termination_date.year:
        return hire_date
    return date(termination_date.year, 1, 1)


def _calculate_thirteenth_salary_value(salary: Decimal, months: int) -> Decimal:
    """Calculate proportional 13th salary value.

    Formula: salary * months / 12

    Args:
        salary: The employee's monthly salary.
        months: Number of months worked in the current year (0-12).

    Returns:
        Decimal: The proportional 13th salary value.
    """
    return salary * Decimal(months) / Decimal(12)


def calculate_termination_benefits(
    hire_date: date,
    termination_date: date,
    salary: Decimal
) -> TerminationBenefits:
    """Calculate proportional vacation and 13th salary upon contract termination.

    This function computes the benefits due according to Brazilian labor laws:
    - Vacation: Proportional to months worked since the last hire anniversary
      until termination, including the constitutional 1/3 bonus.
    - 13th Salary: Proportional to months worked in the current calendar year
      (from January 1st or hire date until termination).

    Args:
        hire_date: The date when the employee was hired at the company.
        termination_date: The date when the employee's contract was terminated.
        salary: The employee's gross monthly salary as a Decimal.

    Returns:
        TerminationBenefits: An immutable object containing:
            - vacation: Proportional vacation value including 1/3 constitutional bonus
            - thirteenth_salary: Proportional 13th salary value

    Raises:
        ValueError: If termination_date is before hire_date or salary is not positive.
    """
    _validate_input(hire_date, termination_date, salary)

    last_anniversary = _calculate_last_anniversary(hire_date, termination_date)
    vacation_months = _calculate_months_worked(last_anniversary, termination_date)
    vacation_value = _calculate_vacation_value(salary, vacation_months)

    period_start = _calculate_thirteenth_period_start(hire_date, termination_date)
    thirteenth_months = _calculate_months_worked(period_start, termination_date)
    thirteenth_value = _calculate_thirteenth_salary_value(salary, thirteenth_months)

    return TerminationBenefits(
        vacation=vacation_value,
        thirteenth_salary=thirteenth_value
    )