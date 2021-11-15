"""Keep track of data for students in a Student class."""
from statistics import fmean


class Student:
    def __init__(self, fname, lname, email, categories):
        self.first_name = fname
        self.last_name = lname
        self.email = email

        self._categories = {}
        for category in categories:
            self._categories[category] = []


    def add_grade(self, grade, category):
        self._categories[category].append(grade)


    def average(self, category):
        if not self._categories[category]:
            return "No results"
        return round(fmean(self._categories[category]))


    def total_average(self, weights):
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

