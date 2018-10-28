# -*- coding: utf-8 -*-
from canvasapi import Canvas
from datetime import datetime, timedelta


class MyAssignment:
    def __init__(self, name, dueDate):
        self._name = name
        self._dueDate = dueDate

    def name(self):
        return self._name

    def due_date(self):
        return self._dueDate


# Canvas API URL
API_URL = "https://canvas.ubc.ca"
# Canvas API key
API_KEY = "11224~vJnLZIH77OBrFKZETSXds7mNy8ONE1xXnAYtGjoONJkc0tAA7IuCi3Op028ryI4U"

# initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

courses = []

for course in canvas.get_courses():
    if course.attributes.get("course_code") is not None:
        courses.append(course)

# each course has a list of assignments that are sorted by due date
course_dict = {}

for course in courses:
    theirAssignments = course.get_assignments()
    print(course)

    myAssignments = []

    for theirAssignment in theirAssignments:
        if theirAssignment.due_at is not None:
            datetime_object = datetime.strptime(theirAssignment.due_at, '%Y-%m-%dT%H:%M:%SZ')
            if datetime.now() - timedelta(days=1) < datetime_object:
                a = MyAssignment(theirAssignment.name, datetime_object)
                myAssignments.append(a)

    # now sort
    allSorted = sorted(myAssignments, key=lambda assignment: assignment._dueDate)
    for assignment in allSorted:
        print(assignment.name())
        print(assignment.due_date())

    course_dict[course] = allSorted
