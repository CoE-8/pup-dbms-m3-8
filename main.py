import webapp2
from google.appengine.ext import ndb
import jinja2
import os
import logging
import json


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



class Thesis(ndb.Model):
    Year = ndb.StringProperty(indexed=True)
    Title = ndb.StringProperty(indexed=True)
    Abstract = ndb.StringProperty(indexed=True)
    Adviser = ndb.StringProperty(indexed=True)
    Section = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)



class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('thesisForm.html')
        self.response.write(template.render())

    # def post(self):
    #     thesis = Thesis()
    #     thesis.Year = self.request.get('Year')
    #     thesis.Title = self.request.get('Title')
    #     thesis.Abstract = self.request.get('Abstract')
    #     thesis.Adviser = self.request.get('Adviser')
    #     thesis.Section = self.request.get('Section')
    #     thesis.put()

class ThesisDelete(webapp2.RequestHandler):
    def get(self, thesisId):
        d = Thesis.get_by_id(int(thesisId))
        d.key.delete()
        self.redirect('/')

class ThesisEdit(webapp2.RequestHandler):
    def get(self,thesisId):
        thesis = Thesis.get_by_id(int(thesisId))
        template_data = {
            'thesis': thesis
        }
        template = JINJA_ENVIRONMENT.get_template('editThesis.html')
        self.response.write(template.render(template_data))
    
    def post(self,thesisId):
        thesis = Thesis.get_by_id(int(thesisId))        
        thesis.Year = self.request.get('Year')
        thesis.Title = self.request.get('Title')
        thesis.Abstract = self.request.get('Abstract')
        thesis.Adviser = self.request.get('Adviser')
        thesis.Section = self.request.get('Section')
        thesis.put()
        self.redirect('/')
  
class APIThesisHandler(webapp2.RequestHandler):

    def get(self):
        #get all student
        thesis = Thesis.query().order(-Thesis.date).fetch()
        thesis_list = []

        for th in thesis:
            thesis_list.append({
                    'id' : th.key.id(),
                    'Year' : th.Year,
                    'Title' : th.Title,
                    'Abstract' : th.Abstract,
                    'Adviser' : th.Adviser,
                    'Section' : th.Section
                })
        #return list to client
        response = {
        'result' : 'OK',
        'data' : thesis_list
        }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

    def post(self):
        th = Thesis()
        th.Year = self.request.get('Year')
        th.Title = self.request.get('Title')
        th.Abstract = self.request.get('Abstract')
        th.Adviser = self.request.get('Adviser')
        th.Section = self.request.get('Section')
        th.put()
        
        self.response.headers['Content-Type'] = 'application/json'
        response = {
            'result' : 'OK',
            'data': {
                'id' : th.key.id(),
                'Year' : th.Year,
                'Title' : th.Title,
                'Abstract' : th.Abstract,
                'Adviser' : th.Adviser,
                'Section' : th.Section
            }
        }
        self.response.out.write(json.dumps(response))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/api/thesis', APIThesisHandler),
    ('/thesis/delete/(.*)', ThesisDelete),
    ('/thesis/edit/(.*)', ThesisEdit)
], debug=True)