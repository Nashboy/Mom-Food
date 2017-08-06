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
import mimetypes
import random
import logging

jinja_environment = jinja2.Environment(loader =
    jinja2.FileSystemLoader(os.path.dirname(__file__)))



class IndexHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        recipe_list = Food.query().fetch()
        if len(recipe_list) >= 3:
            random_val = random.randint(0, (len(recipe_list)-3))
            selfood1 = recipe_list[random_val]
            selfood2 = recipe_list[random_val + 1]
            selfood3 = recipe_list[random_val + 2]
        else:
            selfood1 = "Coming Soon"
            selfood2 = "Coming Soon"
            selfood3 = "Coming Soon"
        temp = {
            "recipe_list": Food.query().fetch(), #all foods
            "featured1": selfood1,
            "featured2": selfood2,
            "featured3": selfood3
        }
        self.response.write(template.render(temp))

class RecipeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/recipe.html')
        # This is unnessary (refering to chosen food list) but I dont know all the commands to go straight
        # to chosen_food off the bat
        chosen_food_list = Food.query().filter(Food.nameFood == self.request.get("foodName")).fetch()
        logging.info(chosen_food_list)
        chosen_food = chosen_food_list[0]
        logging.info(chosen_food)

    # def post(self):
    #     Food.query().filter(Food.nameFood == current_food.nameFood()).get()
        temp = {
            "ingredients" : chosen_food.ingredient_list,

            "methods" : chosen_food.method_list
        }
        logging.info(temp),
        logging.info(chosen_food.ingredient_list[0].get().nameIngredient)
        self.response.write(template.render(temp))

class FoodHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/foods.html')

        temp = {
            "recipe_list": Food.query().fetch(), #all foods
        }
        # logging.warning("=================== ALL Foods ===================")
        #     for k in temp["recipe_list"]:
        #         print k.get()
        # logging.warning("=================== END Foods ===================")
        self.response.write(template.render(temp))

class ContactHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/contact.html')
        temp = {

        }
        self.response.write(template.render(temp))

# class FileUpload(webapp2.RequestHandler):
#
#     def post(self):
#
#         file_upload = self.request.POST.get("file", None)
#         file_name = file_upload.filename
#         image = Images(id=file_name, file_name=file_name, blob=file_upload.file.read())
#         image.put()
#
#         self.response.headers[b'Content-Type'] = mimetypes.guess_type(image.file_name)[0]
#         self.response.write(image.blob)
#
# class ImgServe(webapp2.Requesthandler):
#
#     def get(self, resource):
#
#         image = ndb.Key('Images', resource).get()
#         self.response.headers[b'Content-Type'] = mimetypes.guess_type(image.file_name)[0]
#         self.response.write(image.blob)
# ======== Objects ======
# List of Foods Objects
# class Recipe(ndb.Model):
#     food_list = ndb.KeyProperty("Food", repeated=True)
#     nameRecipe = ndb.StringProperty(required=True)

class Food(ndb.Model):
    nameFood = ndb.StringProperty(required=True)
    ingredient_list = ndb.KeyProperty("Ingredient", repeated=True)
    method_list = ndb.KeyProperty("Method", repeated=True)

# Ingredient Objects
class Ingredient(ndb.Model):
    nameIngredient = ndb.StringProperty(required=True)
    number = ndb.IntegerProperty(required=True)
    unit = ndb.StringProperty(required=True)

# Method Objects
class Method(ndb.Model):
    content = ndb.TextProperty(required=True)

# class Images(ndb.Model):
#     file_name = ndb.StringProperty(required=True)
#     blob = ndb.BlobProperty(required=True)


# Adding entities To work with
flour = Ingredient()
sugar = Ingredient()

sugar.populate(
    nameIngredient = 'sugar',
    number = 5,
    unit = 'teaspoons'
)
sugar_key = sugar.put()

flour.populate(
    nameIngredient = 'flour',
    number = 12,
    unit = 'lbs'
)
flour_key = flour.put()

tip = Method()
tip.populate(
    content = "Method Example"
)
tip_key = tip.put()

cake = Food()
cake.populate(
    nameFood='Cake',
    ingredient_list = [flour_key, sugar_key],
    method_list = [tip_key])

cake_key = cake.put()


# ======== Links =========
app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/food', FoodHandler),
    ('/recipe', RecipeHandler),
    ('/contact', ContactHandler)
], debug=True)
