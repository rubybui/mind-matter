from flask import jsonify, request, current_app
from marshmallow import ValidationError
from mind_matter_api.schemas import EmergencyContactSchema
from mind_matter_api.services.emergency_contacts import EmergencyContactsService
from mind_matter_api.utils.decorators import require_auth, require_owner
from mind_matter_api.utils.auth import is_user_owner, is_user_admin
import logging

logging.basicConfig(level=logging.DEBUG)

def init_emergency_contacts_routes(app):
    svc: EmergencyContactsService = app.emergency_contacts_service

    @app.route('/emergency-contacts', methods=['GET'])
    @require_auth
    def get_emergency_contacts(user_id):
        """Get all emergency contacts for the current user"""
        try:
            emergency_contacts = svc.get_emergency_contacts(user_id)
            return jsonify(EmergencyContactSchema(many=True).dump(emergency_contacts)), 200
        except Exception as e:
            app.logger.error(f"Error retrieving emergency contacts: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/emergency-contacts', methods=['POST'])
    @require_auth
    def create_emergency_contact(user_id):
        """Create a new emergency contact for the current user"""
        try:
            # Get and validate the request data
            request_data = request.get_json()

            # Add user_id to request data before validation
            request_data['user_id'] = user_id
            
            # Validate the complete data and convert to dict
            validated_data = EmergencyContactSchema().load(request_data)
            contact_data = EmergencyContactSchema().dump(validated_data)
            
            # Create the emergency contact
            new_contact = svc.create_emergency_contacts(user_id, contact_data)
            
            return jsonify(EmergencyContactSchema().dump(new_contact)), 201
        except ValidationError as err:
            app.logger.error(f"Validation error: {err.messages}")
            return jsonify(err.messages), 400
        except Exception as e:
            app.logger.error(f"Unexpected error: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/emergency-contacts/<int:contact_id>', methods=['PUT'])
    @require_auth
    def update_emergency_contact(user_id, contact_id):
        """Update an existing emergency contact"""
        try:
            # First check if the contact exists
            contact = svc.emergency_contacts_repository.get_by_id(contact_id)
            if not contact:
                return jsonify({'error': 'Emergency contact not found'}), 404
                
            # Then check ownership
            if not is_user_owner(user_id, contact) and not is_user_admin(user_id):
                return jsonify({'error': 'Permission denied'}), 403

            # Get and validate the request data
            request_data = request.get_json()

            # Validate the data
            data = EmergencyContactSchema().load(request_data, partial=True)
            # Update the contact
            updated = svc.update_emergency_contacts(contact_id, data)
            return jsonify(EmergencyContactSchema().dump(updated)), 200
        except ValidationError as err:
            app.logger.error(f"Validation error: {err.messages}")
            return jsonify(err.messages), 400
        except Exception as e:
            app.logger.error(f"Unexpected error: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/emergency-contacts/<int:contact_id>', methods=['DELETE'])
    @require_auth
    def delete_emergency_contact(user_id, contact_id):
        """Delete an emergency contact"""
        try:
            # First check if the contact exists
            contact = svc.emergency_contacts_repository.get_by_id(contact_id)
            if not contact:
                return jsonify({'error': 'Emergency contact not found'}), 404
                
            # Then check ownership
            if not is_user_owner(user_id, contact) and not is_user_admin(user_id):
                return jsonify({'error': 'Permission denied'}), 403

            svc.delete_emergency_contacts(contact_id)
            return '', 204
        except Exception as e:
            app.logger.error(f"Error deleting emergency contact: {str(e)}")
            return jsonify({'error': str(e)}), 500
