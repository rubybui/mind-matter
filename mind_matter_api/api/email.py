from flask import Blueprint, jsonify, request
from mind_matter_api.utils.email import send_email, send_welcome_email, send_password_reset_email

def init_email_routes(app):
    """Initialize email-related API routes."""
    
    @app.route('/test-email', methods=['POST'])
    def test_email():
        """Test endpoint for sending emails."""
        try:
            data = request.get_json()
            email_type = data.get('type', 'general')
            to_email = data.get('to')
            
            if not to_email:
                return jsonify({'error': 'Email address is required'}), 400
                
            if email_type == 'welcome':
                success = send_welcome_email(to=to_email, name='Test User')
            elif email_type == 'reset':
                success = send_password_reset_email(to=to_email, reset_token='test-token-123')
            else:
                # Send general test email
                success = send_email(
                    to=to_email,
                    subject='Test Email from Mind Matter',
                    html='<h1>Test Email</h1><p>This is a test email from Mind Matter API.</p>',
                    text='Test Email\nThis is a test email from Mind Matter API.'
                )
                
            if success:
                return jsonify({'message': f'Test {email_type} email sent successfully'}), 200
            else:
                return jsonify({'error': 'Failed to send email'}), 500
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500 