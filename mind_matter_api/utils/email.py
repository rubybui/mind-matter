# -*- coding: utf-8 -*-
"""Email utility functions."""
import logging
from typing import List, Optional, Union
from flask import current_app
from flask_mail import Message
from mind_matter_api.extensions import mail

logger = logging.getLogger(__name__)

def send_email(
    to: Union[str, List[str]],
    subject: str,
    html: str,
    text: Optional[str] = None,
    cc: Optional[Union[str, List[str]]] = None,
    bcc: Optional[Union[str, List[str]]] = None,
    attachments: Optional[List[tuple]] = None
) -> bool:
    """Send an email using Flask-Mail.
    
    Args:
        to: Email address(es) of the recipient(s)
        subject: Subject of the email
        html: HTML content of the email
        text: Plain text content of the email (optional)
        cc: Email address(es) to CC (optional)
        bcc: Email address(es) to BCC (optional)
        attachments: List of attachments as (filename, content_type, data) tuples (optional)
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        msg = Message(
            subject=subject,
            recipients=[to] if isinstance(to, str) else to,
            html=html,
            body=text,
            cc=[cc] if isinstance(cc, str) else cc,
            bcc=[bcc] if isinstance(bcc, str) else bcc,
            attachments=attachments,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        
        mail.send(msg)
        logger.info(f"Email sent successfully to {to}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {to}: {str(e)}")
        return False

def send_password_reset_email(to: str, reset_token: str) -> bool:
    """Send a password reset email.
    
    Args:
        to: Email address of the recipient
        reset_token: Password reset token
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    reset_url = f"{current_app.config.get('FRONTEND_URL', '')}/reset-password?token={reset_token}"
    
    html = f"""
    <h1>Password Reset Request</h1>
    <p>You have requested to reset your password. Click the link below to proceed:</p>
    <p><a href="{reset_url}">Reset Password</a></p>
    <p>If you did not request this, please ignore this email.</p>
    <p>This link will expire in 1 hour.</p>
    """
    
    text = f"""
    Password Reset Request
    
    You have requested to reset your password. Visit the link below to proceed:
    {reset_url}
    
    If you did not request this, please ignore this email.
    This link will expire in 1 hour.
    """
    
    return send_email(
        to=to,
        subject="Password Reset Request",
        html=html,
        text=text
    )

def send_welcome_email(to: str, name: str) -> bool:
    """Send a welcome email to new users.
    
    Args:
        to: Email address of the recipient
        name: Name of the recipient
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    html = f"""
    <h1>Welcome to Mind Matter!</h1>
    <p>Hello {name},</p>
    <p>Thank you for joining Mind Matter. We're excited to have you on board!</p>
    <p>You can now log in to your account and start exploring our features.</p>
    """
    
    text = f"""
    Welcome to Mind Matter!
    
    Hello {name},
    
    Thank you for joining Mind Matter. We're excited to have you on board!
    You can now log in to your account and start exploring our features.
    """
    
    return send_email(
        to=to,
        subject="Welcome to Mind Matter!",
        html=html,
        text=text
    ) 