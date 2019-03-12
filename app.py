from flask import Flask, jsonify,request
from random import randint
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

POSTGRES = {
    'user' :'postgres',
    'pw' : 'adittampan',
    'db' :'kahoot',
    'host' :'localhost',
    'port':'5432'
}
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
#postgresql://username:password@localhost:5432/database
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.init_app(app)
from models import *

#===users===

@app.route("/addUser",methods=['POST'])
def add_user():
    user_id=request.args.get('user_id')
    username=request.args.get('username')
    password=request.args.get('password')
    email=request.args.get('email')

    try:
        users=Users(
            user_id=user_id,
            username=username,
            password=password,
            email=email
        )
        db.session.add(users)
        db.session.commit()
        return "user added, user id {}".format(users.user_id) 

    except Exception as e:
        return (str(e))

@app.route("/login",methods=['POST'])
def login_s():
    body=request.json

    username=body['username']
    password=body['password']
    status=False
    try:
        users=get_all_users().json
        for usr in users:
            if username==usr['username']:
                if password==usr['password']:
                    status=True
    except Exception as e:
        return (str(e))         
    if status:
       return "yay"
    else:
        return "nay"   

@app.route("/getAllUsers",methods=['GET'])
def get_all_users():
    try:
        users=Users.query.order_by(Users.user_id).all()
        return jsonify([usr.serialize() for usr in users])
    except Exception as e:
        return (str(e))

@app.route("/getUser/<id_>",methods=['GET'])
def get_user(id_):
    try:
        users=Users.query.filter_by(user_id=id_).first()
        return jsonify(users.serialize())
    except Exception as e:
        return (str(e))        

@app.route("/deleteUser/<id_>",methods=['DELETE'])
def delete_pelanggan(id_):
    try:
        users=Users.query.filter_by(user_id=id_).delete()
        db.session.commit()
        return "user has been deleted"
    except Exception as e:
        return(str(e)) 

@app.route('/updateUser/<id_>', methods=['POST'])
def update_user(id_):
    user = get_user(id_).json 
    
    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get('email')      

    if username is None:
        username=user['username']

    if password is None:
        password=user['password']

    if email is None:
        email=user['email']           
    try:
        user_ = {
            'username': username,
            'password': password,
            'email': email,
        }
        
        db.session.query(Users).filter_by(user_id=id_).update(user_)
        db.session.commit()
        return 'User updated. user id ={}'.format(id_)
    except Exception as e:
        return(str(e))

#===quizzes===

@app.route("/addQuiz",methods=['POST'])
def add_quiz():
    quiz_id=request.args.get('quiz_id')
    creator_id=request.args.get('creator_id')
    quiz_category=request.args.get('quiz_category')
    quiz_name=request.args.get('quiz_name')

    try:
        quizzes=Quizzes(
            quiz_id=quiz_id,
            creator_id=creator_id,
            quiz_category=quiz_category,
            quiz_name=quiz_name,
        )
        db.session.add(quizzes)
        db.session.commit()
        return "quiz added, quiz id {}".format(quizzes.quiz_id) 

    except Exception as e:
        return (str(e))        

@app.route("/getAllQuizzes",methods=['GET'])
def get_all_quizzes():
    try:
        quizzes=Quizzes.query.order_by(Quizzes.quiz_id).all()
        return jsonify([quiz.serialize() for quiz in quizzes])
    except Exception as e:
        return (str(e))        

@app.route("/getQuiz/<id_>",methods=['GET'])
def get_quiz(id_):
    try:
        quizzes=Quizzes.query.filter_by(quiz_id=id_).first()
        return jsonify(quizzes.serialize())
    except Exception as e:
        return (str(e)) 

@app.route("/deleteQuiz/<id_>",methods=['DELETE'])
def delete_quiz(id_):
    try:
        quizzes=Quizzes.query.filter_by(quiz_id=id_).delete()
        db.session.commit()
        return "quiz has been deleted"
    except Exception as e:
        return(str(e))         

@app.route('/updateQuiz/<id_>', methods=['POST'])
def update_quiz(id_):
    quiz = get_quiz(id_).json 
    
    quiz_category = request.args.get('quiz_category')
    quiz_name = request.args.get('quiz_name')     

    if quiz_category is None:
        quiz_category=quiz['quiz_category']

    if quiz_name is None:
        quiz_name=quiz['quiz_name']
      
    try:
        quiz_ = {
            'quiz_category': quiz_category,
            'quiz_name': quiz_name,
        }
        
        db.session.query(Quizzes).filter_by(quiz_id=id_).update(quiz_)
        db.session.commit()
        return 'quiz updated. quiz id ={}'.format(id_)
    except Exception as e:
        return(str(e))

#===question===

@app.route("/addQuestion",methods=['POST'])
def add_question():
    question_id=request.args.get('question_id')
    quiz_id=request.args.get('quiz_id')
    question_number=request.args.get('question_number')
    question=request.args.get('question')
    answer=request.args.get('answer')

    try:
        question=Question(
            question_id=question_id,
            quiz_id=quiz_id,
            question_number=question_number,
            question=question,
            answer=answer
        )
        db.session.add(question)
        db.session.commit()
        return "question added, quiz id {}".format(question.question_id) 

    except Exception as e:
        return (str(e))                

@app.route("/getAllQuestions",methods=['GET'])
def get_all_questions():
    try:
        questions=Question.query.order_by(Question.question_id).all()
        return jsonify([qst.serialize() for qst in questions])
    except Exception as e:
        return (str(e))        

@app.route("/getQuestion/<id_>",methods=['GET'])
def get_question(id_):
    try:
        questions=Question.query.filter_by(question_id=id_).first()
        return jsonify(questions.serialize())
    except Exception as e:
        return (str(e)) 

@app.route('/updateQuestion/<id_>', methods=['POST'])
def update_question(id_):
    questions = get_question(id_).json 
    
    question_number=request.args.get('question_number')
    question=request.args.get("question")
    answer=request.args.get("answer")     

    if question_number is None:
        question_number=questions['question_number']

    if question is None:
        question=questions['question']

    if answer is None:
        answer=questions['answer']
    try:
        question_ = {
            'question_number': question_number,
            'question': question,
            'answer':answer,
        }
        
        db.session.query(Question).filter_by(question_id=id_).update(question_)
        db.session.commit()
        return 'question updated. question id ={}'.format(id_)
    except Exception as e:
        return(str(e))   

@app.route("/deleteQuestion/<id_>",methods=['DELETE'])
def delete_question(id_):
    try:
        questions=Question.query.filter_by(question_id=id_).delete()
        db.session.commit()
        return "question has been deleted"
    except Exception as e:
        return(str(e)) 

#===option===

@app.route("/addOption",methods=['POST'])
def add_option():
    option_id=request.args.get('option_id')
    quiz_id=request.args.get('quiz_id')
    question_id=request.args.get('question_id')
    a=request.args.get('a')
    b=request.args.get('b')
    c=request.args.get('c')
    d=request.args.get('d')
    try:
        options=Option(
            option_id=option_id,
            quiz_id=quiz_id,
            question_id=question_id,
            a=a,
            b=b,
            c=c,
            d=d,
        )
        db.session.add(options)
        db.session.commit()
        return "option added, option id {}".format(Option.option_id) 

    except Exception as e:
        return (str(e)) 

@app.route("/getAllOptions",methods=['GET'])
def get_all_options():
    try:
        options=Option.query.order_by(Option.option_id).all()
        return jsonify([opt.serialize() for opt in options])
    except Exception as e:
        return (str(e))        

@app.route("/getOption/<id_>",methods=['GET'])
def get_option(id_):
    try:
        options=Option.query.filter_by(option_id=id_).first()
        return jsonify(options.serialize())
    except Exception as e:
        return (str(e))        

@app.route("/deleteOption/<id_>",methods=['DELETE'])
def delete_option(id_):
    try:
        Option.query.filter_by(option_id=id_).delete()
        db.session.commit()
        return "option has been deleted"
    except Exception as e:
        return(str(e))        

@app.route('/updateOption/<id_>', methods=['POST'])
def update_option(id_):
    options = get_option(id_).json 
    
    option_id=request.args.get('option_id')
    quiz_id=request.args.get("quiz_id")
    question_id=request.args.get("question_id")     

    if option_id is None:
        option_id=options['option_id']

    if quiz_id is None:
        quiz_id=options['quiz_id']

    if question_id is None:
        question_id=options['question_id']

    if a is None:
        a=options['a'] 

    if b is None:
        b=options['b'] 
    
    if c is None:
        c=options['c'] 
    
    if d is None:
        d=options['d']                    
    try:
        options_ = {
            'option_id': option_id,
            'quiz_id': quiz_id,
            'question_id':question_id,
            'a':a,
            'b':b,
            'c':c,
            'd':d
        }
        
        db.session.query(Option).filter_by(option_id=id_).update(options_)
        db.session.commit()
        return 'option updated. option id ={}'.format(id_)
    except Exception as e:
        return(str(e))  

#===game===

@app.route("/createGame",methods=['POST'])
def create_game():
    gamespin=randint(100000,999999)
    quiz_id=request.args.get('quiz_id')

    try:
        games=Game(
            gamespin=gamespin,
            quiz_id=quiz_id,
        )
        db.session.add(games)
        db.session.commit()
        return "game created, game pin {}".format(games.gamespin) 

    except Exception as e:
        return (str(e))  

#===create leaderboard/join game=== 
@app.route("/join",methods=['POST'])
def join():
    gamespin=request.args.get('gamespin')
    participants=request.args.get('participants')
    score=0

    try:
        leaderboards=Leaderboard(
            gamespin=gamespin,
            participants=participants,
            score=score,
        )
        db.session.add(leaderboards)
        db.session.commit()
        return "player added, player name {}".format(leaderboards.participants) 

    except Exception as e:
        return (str(e))          

@app.route("/leaderboard",methods=['GET'])
def get_leaderboard():
    try:
        leaderboards=Leaderboard.query.order_by(Leaderboard.gamespin).all()
        return jsonify([leader.serialize() for leader in leaderboards])
    except Exception as e:
        return (str(e))

@app.route("/answer/<gamepin_>",methods=['GET'])
def answer_yay(gamepin_):
    quiz_id_=request.args.get('quiz_id')
    question_id_=request.args.get('quiz_id')
    username_=request.args.get('username')
    answer_=request.args.get('answer')

    try:
        question = Question.query.join( Quizzes , Quizzes.quiz_id==Question.quiz_id).filter(Question.quiz_id==quiz_id_, Question.question_id==question_id_).first()
        answer=question.answer
    except Exception as e:
        return (str(e))

    try:
        leaderboard = Leaderboard.query.filter(Leaderboard.gamespin==gamepin_, Leaderboard.participants==username_).first()
        score=leaderboard.score
    except Exception as e:
        return (str(e))

    if answer==answer_:
        score+=100

    try:
        leaderboards={
            'gamespin':gamepin_,
            'participants':username_,
            'score':score
        }
        db.session.query(Leaderboard).filter(Leaderboard.gamespin==gamepin_, Leaderboard.participants==username_).update(leaderboards)
        db.session.commit()
        return "correct"

    except Exception as e:
        return (str(e))    

