#!/usr/bin/python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import os
import jinja2
from hogwarts_models import Student, Wand, House, Course, Enrollment, Teacher
from seed_hogwarts_db import seed_data

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Welcome to Hogwarts' Online Portal")

class HouseHandler(webapp2.RequestHandler):
    def get(self):
        hogwarts_houses = House.query().order(House.name).fetch()
        start_template = jinja_env.get_template("templates/houselist.html")
        self.response.write(start_template.render({'house_info' : hogwarts_houses}))

class StudentHandler(webapp2.RequestHandler):
    def get(self):
        student_entity_list = Student.query().order(Student.last_name).fetch()
        enrollment_entity_list = Enrollment.query().fetch()
        student_template = jinja_env.get_template("templates/students.html")
        self.response.write(student_template.render(
           {'student_info' : student_entity_list,
            'enrollment_info' : enrollment_entity_list}))

class NewStudentHandler(webapp2.RequestHandler):
    def post(self):
        # Access the user data via the form's input elements' names.
        student_first_name = self.request.get('first-name')
        student_last_name = self.request.get('last-name')
        student_id = self.request.get('student-id')

        new_student_entity = Student(first_name = student_first_name,
                                     last_name = student_last_name,
                                     student_id = int(student_id))
        new_student_entity.put()

        new_student_template = jinja_env.get_template("templates/new_student.html")
        self.response.write(new_student_template.render(
           {'student_info' : new_student_entity}))

class EnrollmentHandler(webapp2.RequestHandler):
    def get(self):
        enrollment_entity_list = Enrollment.query().fetch()
        enrollment_template = jinja_env.get_template("templates/enrollment.html")
        self.response.write(enrollment_template.render(
           {'enrollment_info' : enrollment_entity_list}))

class LoadDataHandler(webapp2.RequestHandler):
    def get(self):
        seed_data()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/houses', HouseHandler),
    ('/enrollment', EnrollmentHandler),
    ('/students', StudentHandler),
    ('/new-student', NewStudentHandler),
    ('/seed-data', LoadDataHandler)
], debug=True)
