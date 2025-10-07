import pytest
from app import app, db, User, Bet, Question, Option, Event

# This is a "fixture", a setup function that Pytest runs before our tests.
@pytest.fixture
def client():
    # Configure the app for testing
    app.config['TESTING'] = True
    # Use an in-memory SQLite database for tests to keep them isolated
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    # Disable CSRF protection in tests
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        # Create all the database tables
        db.create_all()

        # --- Create Test Data ---
        # Create users with scores designed to test ties
        u1 = User(roll_number='U1', name='Alice', points=200)
        u2 = User(roll_number='U2', name='Bob', points=200)
        u3 = User(roll_number='U3', name='Charlie', points=190)
        u4 = User(roll_number='U4', name='Diana', points=190)
        u5 = User(roll_number='U5', name='Eve', points=180)
        u6 = User(roll_number='U6', name='Frank', points=300) # User with no bets
        
        db.session.add_all([u1, u2, u3, u4, u5, u6])

        # Create dummy event/question/option to create bets
        event = Event(name="Test Event")
        question = Question(text="Test Q", event=event)
        option = Option(text="Test Opt", question=question, odds=2.0)
        db.session.add_all([event, question, option])

        # Create bets for users 1-5. Frank (u6) will have no bets.
        b1 = Bet(user_roll_number='U1', question_id=1, option_id=1, amount=10)
        b2 = Bet(user_roll_number='U2', question_id=1, option_id=1, amount=10)
        b3 = Bet(user_roll_number='U3', question_id=1, option_id=1, amount=10)
        b4 = Bet(user_roll_number='U4', question_id=1, option_id=1, amount=10)
        b5 = Bet(user_roll_number='U5', question_id=1, option_id=1, amount=10)
        db.session.add_all([b1, b2, b3, b4, b5])

        db.session.commit()

    # 'yield' the test client to the test functions
    with app.test_client() as client:
        yield client
    
    # Teardown: drop all tables after the test is done
    with app.app_context():
        db.drop_all()


### Test Functions ###

def test_leaderboard_ranking_logic(client):
    """
    Tests the core ranking logic directly by calling the helper function.
    This is a pure "unit test".
    """
    from app import get_ranked_leaderboard
    with app.app_context():
        ranked_players = get_ranked_leaderboard()

    # Expected order: U1/U2 (tie), U3/U4 (tie), U5. U6 is excluded.
    assert len(ranked_players) == 5

    # Check ranks: 1, 1, 3, 3, 5
    assert ranked_players[0]['rank'] == 1
    assert ranked_players[1]['rank'] == 1
    assert ranked_players[2]['rank'] == 3
    assert ranked_players[3]['rank'] == 3
    assert ranked_players[4]['rank'] == 5
    
    # Check that the players are correct
    assert ranked_players[0]['player'].roll_number in ['U1', 'U2']
    assert ranked_players[1]['player'].roll_number in ['U1', 'U2']
    assert ranked_players[2]['player'].roll_number in ['U3', 'U4']
    assert ranked_players[3]['player'].roll_number in ['U3', 'U4']
    assert ranked_players[4]['player'].roll_number == 'U5'


def test_leaderboard_web_route(client):
    """
    Tests the '/leaderboard' web page to ensure it displays the correct data.
    This is an "integration test".
    """
    response = client.get('/leaderboard')
    assert response.status_code == 200

    # Check if the names of our test users appear in the HTML
    assert b'Alice' in response.data
    assert b'Bob' in response.data
    assert b'Eve' in response.data
    
    # Check that the user with no bets does NOT appear
    assert b'Frank' not in response.data

    # Check that the tied rank "1" and the next rank "3" are present
    assert b'>1</span>' in response.data # Rank 1 (Alice & Bob)
    assert b'>3</span>' in response.data # Rank 3 (Charlie & Diana)
    assert b'>5</span>' in response.data # Rank 5 (Eve)


def test_leaderboard_api_route(client):
    """
    Tests the '/api/leaderboard' endpoint to ensure it returns correct JSON.
    This is also an "integration test".
    """
    response = client.get('/api/leaderboard')
    assert response.status_code == 200
    
    data = response.get_json()
    
    # Expected order: U1/U2 (tie), U3/U4 (tie), U5. U6 is excluded.
    assert len(data) == 5

    # Check ranks in the JSON response
    assert data[0]['rank'] == 1
    assert data[1]['rank'] == 1
    assert data[2]['rank'] == 3
    assert data[3]['rank'] == 3
    assert data[4]['rank'] == 5

    # Check that a user's name from the JSON is correct
    assert data[0]['user']['name'] in ['Alice', 'Bob']
    assert data[4]['user']['name'] == 'Eve'