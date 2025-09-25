#!/usr/bin/env python3
"""
Stratabetting - Kritansh 2024
Flask Application Startup Script
"""

import os
from app import app, db

def create_app():
    """Create and configure the Flask application."""
    
    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default admin user if it doesn't exist
        from app import User
        if not User.query.filter_by(roll_number='admin').first():
            admin = User(roll_number='admin', name='Admin', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Database initialized with default admin user")
            print("📧 Admin Login: roll='admin', password='admin123'")
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    print("\n🎯 Stratabetting - Kritansh 2024")
    print("=" * 40)
    print("🚀 Starting Flask application...")
    print("🌐 Server will be available at: http://localhost:5000")
    print("👤 Admin login: admin / admin123")
    print("📱 Students can register with their roll numbers")
    print("=" * 40)
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
