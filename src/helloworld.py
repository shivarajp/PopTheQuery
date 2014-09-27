import wsgiref.handlers
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
     
  
global title
   
class Register(db.Model):
    section=db.StringProperty(required="true")
    qtn=db.StringProperty(required="true")
    
   
class visitors(db.Model):
    Name=db.StringProperty(required="true")
    Email=db.StringProperty(required="true")
    
    
class comments(db.Model):
    title=db.StringProperty(required="true")
    comment=db.StringProperty(required="true")
    
   
 
class MainPage(webapp.RequestHandler):
    
   def get(self):
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">SIGN IN WITH GOOGLE ACCOUNT :)</a>.' %
                        users.create_login_url('/'))
            
        

        self.response.out.write('<html><body>%s</body></html>' % greeting)
        
  
        
   
class Homepage(webapp.RequestHandler):

    def get(self):
        self.response.out.write(template.render('index.html',{}))
        

        
class register(webapp.RequestHandler):

    def get(self):
       
        self.response.out.write(template.render('raisequestion.html',{}))
        
    def post(self):
        
        shoutt= Register(section=self.request.get('txt1'),qtn=self.request.get('qtn'))
        shoutt.put()
        
        self.response.out.write(template.render('raisequestion.html',{}))
        
        
class popthequery(webapp.RequestHandler):
    

    def get(self):
        shouts= db.GqlQuery('select * from Register')
        values={'shouts':shouts}
        self.response.out.write(template.render('popthequery.html',values))
   
    def post(self):
        global title
        title=self.request.get('quest')
        self.redirect("/reply")
        


class raisequestion(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('raisequestion.html',{}))
        
    def post(self):
         self.response.out.write(template.render('raisequestion.html',{}))
        
class display(webapp.RequestHandler):

    def get(self):
        self.response.out.write(template.render('display.html',{}))
        
class aboutus(webapp.RequestHandler):

    def get(self):
        self.response.out.write(template.render('aboutus.html',{}))
        
class contactus(webapp.RequestHandler):

    def get(self):
        self.response.out.write(template.render('contactus.html',{}))   
        


class reply(webapp.RequestHandler):
    def get(self):
       
      
        shouts= db.GqlQuery("select * from comments where title = '%s'"  % title)
        
        sh1=db.GqlQuery("select * from Register where section = '%s'"  % title)
        values={'shouts':shouts,'sh1':sh1}

        self.response.out.write(template.render('reply.html',values))
        
    def post(self):
        shoutt= comments(title=self.request.get('ques'),comment=self.request.get('qtn'))
        shoutt.put()
        self.response.out.write(template.render('index.html',{}))
      
    
        
        
application = webapp.WSGIApplication([('/', Homepage),('/MainPage', MainPage),('/register', register),('/popthequery',popthequery),('/reply', reply),('/aboutus', aboutus),('/contactus', contactus)], debug=True)



def main():
    run_wsgi_app(application)
   
    

if __name__ == "__main__":
    main()
