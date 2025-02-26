from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorito = db.relationship("Favoritos", backref="user", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # "favorites": [favorite.id for favorite in self.favorite]
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80))
     temp = db.Column(db.Integer)
     size = db.Column(db.String(80))
     favorito = db.relationship("Favoritos", backref="planet", lazy=True)

     def serialize(self):
         return{
            "id" : self.id,
            "name" : self.name,
            "temp" : self.temp,
            "size" : self.size
         }
     
class Person(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80))
     faccion = db.Column(db.String(80))
     job = db.Column(db.String(80))
     favorito = db.relationship("Favoritos", backref="person", lazy=True)

     def serialize(self):
         return{
            "id" : self.id,
            "name" : self.name,
            "faccion" : self.faccion,
            "job" : self.job
         }
     

class Favoritos(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
     planet_id = db.Column(db.Integer,db.ForeignKey("planet.id"))
     person_id = db.Column(db.Integer,db.ForeignKey("person.id"))

     def serialize(self):
         return{
            "id" : self.id,
            "user_id": self.user_id,
            "planet": self.planet.serialize() if self.planet else None,
            "person": self.person.serialize() if self.person else None

         }



        
     




     