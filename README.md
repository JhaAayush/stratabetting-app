# Stratabetting - Kritansh 2024

A comprehensive virtual betting platform for the Kritansh sports festival at IIM Amritsar, developed by the Stratagem Club.

## 🎯 Overview

Stratabetting is a virtual currency betting system where students can bet on various sports events during Kritansh 2024. Students start with 200 virtual coins and can place bets on match outcomes, scores, and other predictions.

## ✨ Features

### For Students
- **User Registration & Authentication** - Secure login with roll numbers
- **Virtual Currency System** - Start with 200 coins, bet and win more
- **Multiple Sports Betting** - Cricket, Football, Basketball, Chess, and more
- **Real-time Balance Tracking** - Monitor your virtual currency
- **Betting History** - View all your past bets and results
- **Personal Analytics** - Track your betting performance

### For Admins (Stratagem Coordinators)
- **Event Management** - Create and manage sports events
- **Question Creation** - Add betting questions with custom odds
- **Result Management** - Settle bets and distribute winnings
- **Data Export** - Download comprehensive betting data
- **User Analytics** - View user performance and statistics
- **User Management** - Monitor student registrations and balances

## 🏆 Competing Teams

The platform supports betting on matches between these four teams:
- **Alpha Wolves**
- **Black Pirates** 
- **Dragon Slayers**
- **Viking Warriors**

*Note: You can bet on any team regardless of whether you're playing or not!*

## 🎮 Sports & Events

The platform supports betting on:
- Cricket (Semi-finals, Finals, Runs, Sixes)
- Football
- Basketball
- Chess
- Futsal
- Table Tennis
- Carrom
- FIFA (Gaming)
- BGMI (Gaming)
- Badminton
- Pool
- Tug of War
- Athletics
- Frisbee

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Stratabetting
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 4: Initial Setup
1. The application automatically creates the database and default admin user
2. Default admin credentials:
   - **Roll Number:** `admin`
   - **Password:** `admin123`

## 📱 Usage Guide

### For Students

1. **Registration**
   - Visit the website
   - Click "Register"
   - Enter your roll number, name, and password
   - Start betting immediately!

2. **Placing Bets**
   - Login to your account
   - Browse active events
   - Click on questions to place bets
   - Select your prediction and bet amount
   - Confirm your bet

3. **Tracking Performance**
   - View your balance on the dashboard
   - Check your betting history
   - Monitor your betting performance

### For Admins

1. **Creating Events**
   - Login as admin
   - Go to "Create Event"
   - Select sport and event type
   - Add description

2. **Adding Betting Questions**
   - Go to event management
   - Click "Add Question"
   - Enter question, options, and odds
   - Activate the question

3. **Settling Bets**
   - After events conclude
   - Mark winning bets
   - System automatically calculates and distributes winnings

4. **Data Export**
   - Use "Export Data" to download CSV files
   - Contains all betting data and user information

## 🏗️ Technical Architecture

### Backend
- **Framework:** Flask (Python)
- **Database:** SQLite (can be upgraded to PostgreSQL/MySQL)
- **Authentication:** Flask-Login
- **ORM:** SQLAlchemy

### Frontend
- **CSS Framework:** Bootstrap 5
- **Icons:** Font Awesome
- **JavaScript:** Vanilla JS with modern features

### Database Schema
- **Users:** Student information and balances
- **Teams:** Team management
- **Sports & Events:** Event organization
- **Betting Questions:** Betting options and odds
- **Bets:** Individual bet records
- **Team Members:** Squad management

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///stratabetting.db
FLASK_ENV=production
```

### Database Migration
For production, consider using Flask-Migrate:
```bash
pip install Flask-Migrate
flask db init
flask db migrate
flask db upgrade
```

## 📊 Admin Features

### Event Management
- Create sports events
- Set event types (Match, Semi-Final, Final, etc.)
- Activate/deactivate events

### Question Management
- Multiple question types
- Custom odds setting
- Option management
- Real-time betting statistics

### Analytics Dashboard
- User registration statistics
- Team performance metrics
- Betting volume analysis
- Revenue tracking (virtual currency)

### Data Export
- CSV export functionality
- Complete betting history
- User performance data
- Team statistics

## 🎨 UI/UX Features

- **Responsive Design** - Works on desktop, tablet, and mobile
- **Modern Interface** - Clean, professional design
- **Real-time Updates** - Live balance and statistics
- **Intuitive Navigation** - Easy-to-use interface
- **Accessibility** - Keyboard navigation and screen reader support

## 🔒 Security Features

- **Password Hashing** - Secure password storage
- **Session Management** - Secure user sessions
- **Input Validation** - Protection against malicious input
- **Admin Authorization** - Role-based access control

## 📈 Future Enhancements

- [ ] Real-time notifications
- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] Social features (team chat)
- [ ] Tournament brackets
- [ ] Live score integration
- [ ] Push notifications
- [ ] Advanced reporting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For technical support or questions:
- Contact Stratagem Club coordinators
- Email: [Your email here]
- Discord: [Your Discord here]

## 📄 License

This project is developed for IIM Amritsar's Kritansh 2024. All rights reserved.

## 🙏 Acknowledgments

- **Stratagem Club** - IIM Amritsar
- **Kritansh Organizing Committee**
- **IIM Amritsar Student Community**

---

**Made with ❤️ for Kritansh 2024**
