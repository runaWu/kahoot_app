from app import db

class Users(db.Model):
    __tablename__='users'
    user_id =db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String())
    password=db.Column(db.Integer)
    email=db.Column(db.String())

    def __init__(self,user_id,username,password,email):
        self.user_id=user_id
        self.username=username
        self.password=password
        self.email=email

    def __repr__(self):
        return 'user_id{}>'.format(self.user_id)

    def serialize(self):
        return{
            'user_id':self.user_id,
            'username':self.username,
            'password':self.password,
            'email':self.email
    }    
class Quizzes(db.Model):
    __tablename__='quizzes'
    quiz_id =db.Column(db.Integer, primary_key=True)
    creator_id=db.Column(db.Integer)
    quiz_category=db.Column(db.String())
    quiz_name=db.Column(db.String())
    questions=db.relationship('Question',backref='quizzes',lazy=True)

    def __init__(self,quiz_id,creator_id,quiz_category,quiz_name):
        self.quiz_id=quiz_id
        self.creator_id=creator_id
        self.quiz_category=quiz_category
        self.quiz_name=quiz_name

    def __repr__(self):
        return 'quiz_id{}>'.format(self.quiz_id)

    def serialize(self):
        return{
            'quiz_id':self.quiz_id,
            'creator_id':self.creator_id,
            'quiz_category':self.quiz_category,
            'quiz_name':self.quiz_name,
            'question-list':[{'number':item.question_number,'question':item.question,'answer':item.answer}for item in self.questions]
    }     

class Question(db.Model):
    __tablename__='question'
    question_id =db.Column(db.Integer, primary_key=True)
    quiz_id=db.Column(db.Integer,db.ForeignKey('quizzes.quiz_id'))
    question_number=db.Column(db.Integer)
    question=db.Column(db.String())
    answer=db.Column(db.String())

    def __init__(self,question_id,quiz_id,question_number,question,answer):
        self.question_id=question_id
        self.quiz_id=quiz_id
        self.question_number=question_number
        self.question=question
        self.answer=answer

    def __repr__(self):
        return 'question_id{}>'.format(self.question_id)

    def serialize(self):
        return{
            'question_id':self.question_id,
            'quiz_id':self.quiz_id,
            'question_number':self.question_number,
            'question':self.question,
            'answer':self.answer
    }
class Option(db.Model):
    __tablename__='option'
    option_id =db.Column(db.Integer, primary_key=True)
    quiz_id=db.Column(db.Integer)
    question_id=db.Column(db.Integer)
    a=db.Column(db.String())
    b=db.Column(db.String())
    c=db.Column(db.String())
    d=db.Column(db.String())

    def __init__(self,option_id,quiz_id,question_id,a,b,c,d):
        self.option_id=option_id
        self.quiz_id=quiz_id
        self.question_id=question_id
        self.a=a
        self.b=b 
        self.c=c
        self.d=d 

    def __repr__(self):
        return 'option_id{}>'.format(self.option_id)

    def serialize(self):
        return{
            'option_id':self.option_id,
            'quiz_id':self.quiz_id,
            'question_id':self.question_id,
            'a':self.a,
            'b':self.b,
            'c':self.c,
            'd':self.d
    }    
class Game(db.Model):
    __tablename__='game'
    gamespin =db.Column(db.Integer, primary_key=True)
    quiz_id=db.Column(db.Integer)

    def __init__(self,gamespin,quiz_id):
        self.gamespin=gamespin
        self.quiz_id=quiz_id

    def __repr__(self):
        return 'gamespin{}>'.format(self.gamespin)

    def serialize(self):
        return{
            'gamespin':self.gamespin,
            'quiz_id':self.quiz_id
    }
class Leaderboard(db.Model):
    __tablename__='leaderboard'
    gamespin =db.Column(db.Integer)
    participants=db.Column(db.String(), primary_key=True)
    score =db.Column(db.Integer)

    def __init__(self,gamespin,participants,score):
        self.gamespin=gamespin
        self.participants=participants
        self.score=score

    def __repr__(self):
        return 'gamespin{}>'.format(self.gamespin)

    def serialize(self):
        return{
            'gamespin':self.gamespin,
            'participants':self.participants,
            'score':self.score
    }          