from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import csv
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stratabetting.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    balance = db.Column(db.Integer, default=200)
    is_admin = db.Column(db.Boolean, default=False)
    team = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    members = db.relationship('TeamMember', backref='team', lazy=True)

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(50))  # e.g., 'captain', 'member'

class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    events = db.relationship('Event', backref='sport', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50))  # 'match', 'final', 'semi-final', etc.
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    betting_questions = db.relationship('BettingQuestion', backref='event', lazy=True)

class BettingQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50))  # 'team_winner', 'runs', 'sixes', etc.
    options = db.Column(db.Text)  # JSON string of options
    odds = db.Column(db.Text)  # JSON string of odds for each option
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bets = db.relationship('Bet', backref='question', lazy=True)

class Bet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('betting_question.id'), nullable=False)
    selected_option = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    odds = db.Column(db.Float, nullable=False)
    placed_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_settled = db.Column(db.Boolean, default=False)
    is_winner = db.Column(db.Boolean, default=False)
    winnings = db.Column(db.Integer, default=0)

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        roll_number = request.form['roll_number']
        password = request.form['password']
        user = User.query.filter_by(roll_number=roll_number).first()
        
        if user and user.check_password(password):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid roll number or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        roll_number = request.form['roll_number']
        name = request.form['name']
        password = request.form['password']
        
        if User.query.filter_by(roll_number=roll_number).first():
            flash('Roll number already registered', 'error')
            return render_template('register.html')
        
        user = User(roll_number=roll_number, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! You can now login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    active_events = Event.query.filter_by(is_active=True).all()
    user_bets = Bet.query.filter_by(user_id=current_user.id).all()
    
    return render_template('student_dashboard.html', 
                         events=active_events, 
                         user_bets=user_bets,
                         user=current_user)

@app.route('/student/bet/<int:question_id>', methods=['GET', 'POST'])
@login_required
def place_bet(question_id):
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    question = BettingQuestion.query.get_or_404(question_id)
    
    if not question.is_active:
        flash('This betting question is no longer active', 'error')
        return redirect(url_for('student_dashboard'))
    
    # Check if user already bet on this question
    existing_bet = Bet.query.filter_by(user_id=current_user.id, question_id=question_id).first()
    
    if request.method == 'POST':
        selected_option = request.form['option']
        amount = int(request.form['amount'])
        
        if amount > current_user.balance:
            flash('Insufficient balance', 'error')
            return render_template('place_bet.html', question=question, existing_bet=existing_bet)
        
        if existing_bet:
            flash('You have already placed a bet on this question', 'error')
            return render_template('place_bet.html', question=question, existing_bet=existing_bet)
        
        # Parse odds
        import json
        odds_data = json.loads(question.odds)
        odds_value = odds_data.get(selected_option, 1.0)
        
        # Create bet
        bet = Bet(user_id=current_user.id, question_id=question_id, 
                 selected_option=selected_option, amount=amount, odds=odds_value)
        db.session.add(bet)
        
        # Deduct amount from user balance
        current_user.balance -= amount
        db.session.commit()
        
        flash(f'Bet placed successfully! You bet {amount} coins on {selected_option}', 'success')
        return redirect(url_for('student_dashboard'))
    
    return render_template('place_bet.html', question=question, existing_bet=existing_bet)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('student_dashboard'))
    
    events = Event.query.all()
    users = User.query.filter_by(is_admin=False).all()
    total_bets = Bet.query.count()
    
    # Calculate total questions across all events
    total_questions = sum(len(event.betting_questions) for event in events)
    
    return render_template('admin_dashboard.html', 
                         events=events, 
                         users=users,
                         total_bets=total_bets,
                         total_questions=total_questions)

@app.route('/admin/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    if not current_user.is_admin:
        return redirect(url_for('student_dashboard'))
    
    if request.method == 'POST':
        sport_name = request.form['sport']
        event_name = request.form['event_name']
        description = request.form['description']
        event_type = request.form['event_type']
        
        # Get or create sport
        sport = Sport.query.filter_by(name=sport_name).first()
        if not sport:
            sport = Sport(name=sport_name)
            db.session.add(sport)
            db.session.flush()
        
        event = Event(sport_id=sport.id, name=event_name, 
                     description=description, event_type=event_type)
        db.session.add(event)
        db.session.commit()
        
        flash('Event created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('create_event.html')

@app.route('/admin/event/<int:event_id>/questions')
@login_required
def manage_questions(event_id):
    if not current_user.is_admin:
        return redirect(url_for('student_dashboard'))
    
    event = Event.query.get_or_404(event_id)
    questions = BettingQuestion.query.filter_by(event_id=event_id).all()
    
    return render_template('manage_questions.html', event=event, questions=questions)

@app.route('/admin/create_question/<int:event_id>', methods=['GET', 'POST'])
@login_required
def create_question(event_id):
    if not current_user.is_admin:
        return redirect(url_for('student_dashboard'))
    
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        question_text = request.form['question']
        question_type = request.form['question_type']
        options = request.form['options']  # Comma-separated options
        odds = request.form['odds']  # Comma-separated odds
        
        # Convert options and odds to JSON
        import json
        options_list = [opt.strip() for opt in options.split(',')]
        odds_list = [float(odd.strip()) for odd in odds.split(',')]
        
        if len(options_list) != len(odds_list):
            flash('Number of options and odds must match', 'error')
            return render_template('create_question.html', event=event)
        
        options_json = json.dumps(options_list)
        odds_json = json.dumps(dict(zip(options_list, odds_list)))
        
        question = BettingQuestion(event_id=event_id, question=question_text,
                                 question_type=question_type, options=options_json, odds=odds_json)
        db.session.add(question)
        db.session.commit()
        
        flash('Question created successfully!', 'success')
        return redirect(url_for('manage_questions', event_id=event_id))
    
    return render_template('create_question.html', event=event)

@app.route('/admin/export_data')
@login_required
def export_data():
    if not current_user.is_admin:
        return redirect(url_for('student_dashboard'))
    
    # Create CSV data
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write headers
    writer.writerow(['User Roll Number', 'User Name', 'Team', 'Balance', 
                    'Question', 'Selected Option', 'Amount Bet', 'Odds', 
                    'Placed At', 'Is Settled', 'Is Winner', 'Winnings'])
    
    # Write data
    bets = db.session.query(Bet, User, BettingQuestion).join(User).join(BettingQuestion).all()
    for bet, user, question in bets:
        writer.writerow([
            user.roll_number, user.name, user.team, user.balance,
            question.question, bet.selected_option, bet.amount, bet.odds,
            bet.placed_at, bet.is_settled, bet.is_winner, bet.winnings
        ])
    
    # Create response
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='stratabetting_data.csv'
    )

@app.route('/admin/settle_bet/<int:bet_id>', methods=['POST'])
@login_required
def settle_bet(bet_id):
    if not current_user.is_admin:
        return redirect(url_for('student_dashboard'))
    
    bet = Bet.query.get_or_404(bet_id)
    is_winner = request.form.get('is_winner') == 'true'
    
    if bet.is_settled:
        flash('This bet has already been settled', 'error')
        return redirect(url_for('admin_dashboard'))
    
    bet.is_settled = True
    bet.is_winner = is_winner
    
    if is_winner:
        bet.winnings = int(bet.amount * bet.odds)
        bet.user.balance += bet.winnings
        flash(f'Bet settled! Winner received {bet.winnings} coins', 'success')
    else:
        flash('Bet settled! No winnings', 'info')
    
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/events/<int:event_id>/toggle', methods=['POST'])
@login_required
def toggle_event(event_id):
    if not current_user.is_admin:
        return redirect(url_for('student_dashboard'))
    
    event = Event.query.get_or_404(event_id)
    event.is_active = not event.is_active
    db.session.commit()
    
    status = 'activated' if event.is_active else 'deactivated'
    flash(f'Event {status} successfully', 'success')
    return redirect(url_for('manage_questions', event_id=event_id))

@app.route('/admin/questions/<int:question_id>/toggle', methods=['POST'])
@login_required
def toggle_question(question_id):
    if not current_user.is_admin:
        return redirect(url_for('student_dashboard'))
    
    question = BettingQuestion.query.get_or_404(question_id)
    question.is_active = not question.is_active
    db.session.commit()
    
    status = 'activated' if question.is_active else 'deactivated'
    flash(f'Question {status} successfully', 'success')
    return redirect(url_for('manage_questions', event_id=question.event_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create default admin user
        if not User.query.filter_by(roll_number='admin').first():
            admin = User(roll_number='admin', name='Admin', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Database initialized with default admin user (roll: admin, password: admin123)")
    
    app.run(debug=True)
