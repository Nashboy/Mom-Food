#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2
from google.appengine.ext import ndb
import random
import logging

jinja_environment = jinja2.Environment(loader =
    jinja2.FileSystemLoader(os.path.dirname(__file__)))



class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/main.html')

        self.response.write('Hello world!')

class RecipeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/recipe.html')
        ing_list = Ingredient.query().filter()
        self.response.write(template.render(temp))

class FoodHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/foods.html')
        temp = {

        }
        self.response.write(template.render(temp))


# ======== Objects ======
# List of Foods Objects
class Food(ndb.Model):
    name = ndb.StringProperty(required=True)
    ingredient_list = ndb.KeyProperty(required=True)
    method_list = ndb.KeyProperty(required=True)

# Ingredient Objects
class Ingredient(ndb.Model):
    name = ndb.StringProperty(required=True)
    number = ndb.IntegerProperty(required=True)
    unit = ndb.StringProperty(required=True)

# Method Objects
class Method(ndb.Model):
    content = ndb.StringProperty(repeating=True)

# ======== Links =========
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/food', FoodHandler),
    ('/recipe', RecipeHandler),
    ('/contact', ContactUs)
], debug=True)
