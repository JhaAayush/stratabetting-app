#!/usr/bin/env python3
"""
Simple test script to verify database setup and admin login
"""

from app import app, db, User, Team, Event, BettingQuestion, Bet

def test_database():
    """Test database setup and basic operations."""
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(roll_number='admin').first()
        if admin:
            print(f"✅ Admin user found: {admin.name} (is_admin: {admin.is_admin})")
        else:
            print("❌ Admin user not found")
            
        # Check teams
        teams = Team.query.all()
        print(f"✅ Teams found: {len(teams)}")
        for team in teams:
            print(f"   - {team.name}")
            
        # Check users
        users = User.query.all()
        print(f"✅ Total users: {len(users)}")
        
        # Check events
        events = Event.query.all()
        print(f"✅ Total events: {len(events)}")
        
        # Check questions
        questions = BettingQuestion.query.all()
        print(f"✅ Total questions: {len(questions)}")
        
        # Check bets
        bets = Bet.query.all()
        print(f"✅ Total bets: {len(bets)}")
        
        print("\n🎯 Database test completed successfully!")

if __name__ == '__main__':
    test_database()
