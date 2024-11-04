class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def day_of_week(self):
        """
        >>> Date(2024, 2, 29).day_of_week()
        5
        >>> Date(2023, 1, 1).day_of_week()
        1
        >>> Date(2023, 5, 1).day_of_week()
        2
        """
        if self.month < 3:
            m = self.month + 12
            y = self.year - 1
        else:
            m = self.month
            y = self.year
        dow = (self.day + (13 * (m + 1)) // 5 + y + y // 4 - y // 100 + y // 400) % 7
        return 7 if dow == 0 else dow

    def __str__(self):
        """
        >>> str(Date(2024, 2, 29))
        'Feb 29, 2024'
        >>> str(Date(2023, 3, 1))
        'Mar 1, 2023'
        >>> str(Date(2020, 12, 31))
        'Dec 31, 2020'
        """
        month_name = "BAD Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()[self.month]
        return f"{month_name} {self.day}, {self.year}"

    def __repr__(self):
        """
        >>> repr(Date(2024, 2, 29))
        'Date(2024, 2, 29)'
        >>> repr(Date(2023, 12, 31))
        'Date(2023, 12, 31)'
        """
        return f"Date({self.year}, {self.month}, {self.day})"

    def is_leap_year(self):
        """
        >>> Date(2020, 2, 29).is_leap_year()
        True
        >>> Date(2023, 2, 28).is_leap_year()
        False
        >>> Date(2000, 2, 29).is_leap_year()
        True
        >>> Date(1900, 2, 28).is_leap_year()
        False
        """
        return self.year % 400 == 0 or (self.year % 4 == 0 and self.year % 100 != 0)

    def days_in_month(self, month=None):
        """
        >>> Date(2024, 2, 29).days_in_month()
        29
        >>> Date(2023, 2, 28).days_in_month()
        28
        >>> Date(2023, 4, 15).days_in_month(4)
        30
        >>> Date(2023, 1, 1).days_in_month(1)
        31
        """
        if month is None:
            month = self.month
        if month in [4, 6, 9, 11]:
            return 30
        elif month == 2:
            return 29 if self.is_leap_year() else 28
        else:
            return 31

    def previous_day(self):
        """
        >>> Date(2024, 3, 1).previous_day()
        Date(2024, 2, 29)
        >>> Date(2024, 1, 1).previous_day()
        Date(2023, 12, 31)
        >>> Date(2023, 1, 1).previous_day()
        Date(2022, 12, 31)
        >>> Date(2024, 2, 2).previous_day()
        Date(2024, 2, 1)
        """
        if self.day > 1:
            return Date(self.year, self.month, self.day - 1)
        else:
            if self.month == 1:
                return Date(self.year - 1, 12, 31)  # Previous year
            else:
                prev_month = self.month - 1
                prev_day = self.days_in_month(prev_month)
                return Date(self.year, prev_month, prev_day)

    def next_day(self):
        """
        >>> Date(2024, 2, 29).next_day()
        Date(2024, 3, 1)
        >>> Date(2024, 12, 31).next_day()
        Date(2025, 1, 1)
        >>> Date(2023, 4, 30).next_day()
        Date(2023, 5, 1)
        """
        if self.day < self.days_in_month():
            return Date(self.year, self.month, self.day + 1)
        else:
            if self.month == 12:
                return Date(self.year + 1, 1, 1)  # Next year
            else:
                return Date(self.year, self.month + 1, 1)

    def equals(self, other):
        """
        >>> Date(2024, 2, 29).equals(Date(2024, 2, 29))
        True
        >>> Date(2024, 2, 29).equals(Date(2024, 2, 28))
        False
        >>> Date(2023, 1, 1).equals(Date(2023, 1, 1))
        True
        """
        return self.year == other.year and self.month == other.month and self.day == other.day

    def before(self, other):
        """
        >>> Date(2024, 2, 28).before(Date(2024, 2, 29))
        True
        >>> Date(2024, 3, 1).before(Date(2024, 2, 29))
        False
        """
        return (self.year, self.month, self.day) < (other.year, other.month, other.day)

    def after(self, other):
        """
        >>> Date(2024, 3, 1).after(Date(2024, 2, 29))
        True
        >>> Date(2024, 2, 28).after(Date(2024, 2, 29))
        False
        """
        return (self.year, self.month, self.day) > (other.year, other.month, other.day)

    def to_days(self):
        """
        >>> Date(1, 12, 31).to_days()
        365
        >>> Date(2023, 1, 1).to_days()
        738521
        >>> Date(2022, 1, 1).to_days()
        738156
        """
        total_days = 0
        for y in range(1, self.year):
            total_days += 365 + (1 if Date(y, 2, 29).is_leap_year() else 0)
        for m in range(1, self.month):
            total_days += self.days_in_month(m)
        total_days += self.day
        return total_days

    def __add__(self, days):
        """
        >>> Date(2023, 1, 1) + 5
        Date(2023, 1, 6)
        >>> Date(2023, 12, 31) + 1
        Date(2024, 1, 1)
        >>> Date(2024, 2, 28) + 1
        Date(2024, 2, 29)
        >>> Date(2024, 2, 29) + 1
        Date(2024, 3, 1)
        """
        current_date = self
        for _ in range(abs(days)):
            current_date = current_date.next_day() if days > 0 else current_date.previous_day()
        return current_date

    def __sub__(self, other):
        """
        >>> Date(2024, 1, 1) - Date(2000, 12, 31)
        8401
        >>> Date(2024, 3, 1) - Date(2024, 2, 29)
        1
        >>> Date(2024, 1, 1) - 1
        Date(2023, 12, 31)
        """
        if isinstance(other, Date):
            return self.to_days() - other.to_days()
        elif isinstance(other, int):
            return self + (-other)

    def __lt__(self, other):
        """
        >>> Date(2024, 2, 28) < Date(2024, 2, 29)
        True
        >>> Date(2024, 3, 1) < Date(2024, 2, 29)
        False
        """
        return self.before(other)

    def __le__(self, other):
        """
        >>> Date(2024, 2, 29) <= Date(2024, 2, 29)
        True
        >>> Date(2024, 2, 28) <= Date(2024, 3, 1)
        True
        """
        return self.before(other) or self.equals(other)

    def __gt__(self, other):
        """
        >>> Date(2024, 3, 1) > Date(2024, 2, 29)
        True
        >>> Date(2024, 2, 29) > Date(2024, 3, 1)
        False
        """
        return self.after(other)

    def __ge__(self, other):
        """
        >>> Date(2024, 2, 29) >= Date(2024, 2, 29)
        True
        >>> Date(2024, 2, 28) >= Date(2024, 3, 1)
        False
        """
        return self.after(other) or self.equals(other)
    
    def __eq__(self, other):
        """
        >>> Date(2024, 2, 29) == Date(2024, 2, 29)
        True
        >>> Date(2024, 2, 29) == Date(2024, 2, 28)
        False
        >>> Date(2023, 1, 1) == Date(2023, 1, 1)
        True
        """
        return self.equals(other)

    def __ne__(self, other):
        """
        >>> Date(2024, 2, 29) != Date(2024, 2, 29)
        False
        >>> Date(2024, 2, 29) != Date(2024, 2, 28)
        True
        >>> Date(2023, 1, 1) != Date(2023, 1, 1)
        False
        """
        return not self.equals(other)
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()