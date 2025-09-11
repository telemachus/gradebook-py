"""Keep track of data for students in a Student class."""

from statistics import fmean


class Student:
    """Stores grades for individual students."""

    def __init__(self, fname, lname, email, assignment_categories):
        self.first_name = fname
        self.last_name = lname
        self.email = email

        self._assignment_categories = {}
        for assignment_category in assignment_categories:
            self._assignment_categories[assignment_category] = []

    def add_grade(self, score, assignment_category):
        """Adds a score into the list for a given assignment category."""
        self._assignment_categories[assignment_category].append(score)

    def average(self, assignment_category):
        """Return the rounded mean for an assignment category or "No results"."""
        if not self._assignment_categories[assignment_category]:
            return "No results"
        return round(fmean(self._assignment_categories[assignment_category]))

    def has_grades(self, assignment_category):
        """Returns whether a given assignment type has any grades."""
        return len(self._assignment_categories[assignment_category]) > 0

    def total_average(self, weights_by_assignment_categories):
        """Return the rounded mean for all categories or "No results"."""
        summed_average = 0
        summed_weight = 0

        for assignment_category in self._assignment_categories:
            assignment_category_average = self.average(assignment_category)
            if assignment_category_average == "No results":
                continue
            summed_average += assignment_category_average * (
                weights_by_assignment_categories[assignment_category] / 100
            )
            summed_weight += weights_by_assignment_categories[assignment_category] / 100

        if summed_weight == 0:
            return "No results"
        return round(summed_average / summed_weight)
