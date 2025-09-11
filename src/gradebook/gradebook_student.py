"""Keep track of data for students in a Student class."""

from statistics import fmean


class Student:
    """Stores grades for individual students."""

    def __init__(self, fname, lname, email, assignment_types):
        self.first_name = fname
        self.last_name = lname
        self.email = email

        self._assignment_types = {}
        for assignment_type in assignment_types:
            self._assignment_types[assignment_type] = []

    def add_grade(self, grade, assignment_type):
        """Adds a grade into the list for a given assignment type."""
        self._assignment_types[assignment_type].append(grade)

    def average(self, assignment_type):
        """Return the rounded mean for an assignment type or "No results"."""
        if not self._assignment_types[assignment_type]:
            return "No results"
        return round(fmean(self._assignment_types[assignment_type]))

    def has_grades(self, assignment_type):
        """Returns whether a given assignment type has any grades."""
        return len(self._assignment_types[assignment_type]) > 0

    def total_average(self, weights_by_assignment_type):
        """Return the rounded mean for all categories or "No results"."""
        summed_average = 0
        summed_weight = 0

        for assignment_type in self._assignment_types:
            assignment_type_average = self.average(assignment_type)
            if assignment_type_average == "No results":
                continue
            summed_average += assignment_type_average * (
                weights_by_assignment_type[assignment_type] / 100
            )
            summed_weight += weights_by_assignment_type[assignment_type] / 100

        if summed_weight == 0:
            return "No results"
        return round(summed_average / summed_weight)
