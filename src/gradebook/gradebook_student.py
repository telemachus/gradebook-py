"""Keep track of data for students in a Student class."""

from statistics import fmean


class Student:
    """Stores grades for individual students."""

    def __init__(self, fname, lname, email, categories):
        self.first_name = fname
        self.last_name = lname
        self.email = email

        self._categories = {}
        for category in categories:
            self._categories[category] = []

    def add_grade(self, grade, category):
        """Adds a grade into the list for a given category."""
        self._categories[category].append(grade)

    def average(self, category):
        """Return the rounded mean for a category or "No results"."""
        if not self._categories[category]:
            return "No results"
        return round(fmean(self._categories[category]))

    def has_grades(self, category):
        """Returns whether a given category has any grades."""
        return len(self._categories[category]) > 0

    def total_average(self, weights):
        """Return the rounded mean for all categories or "No results"."""
        summed_average = 0
        summed_weight = 0

        for category in self._categories:
            category_average = self.average(category)
            if category_average == "No results":
                continue
            summed_average += category_average * (weights[category] / 100)
            summed_weight += weights[category] / 100

        if not summed_weight:
            return "No results"
        return round(summed_average / summed_weight)
