from flask import jsonify, request, current_app
from marshmallow import ValidationError
from mind_matter_api.schemas import (
    SurveySchema,
    SurveyQuestionSchema,
    SurveyResponseSchema,
    SurveyAnswerSchema
)
from mind_matter_api.services.surveys import SurveyService


def init_survey_routes(app):
    """
    Initialize survey-related API routes on the Flask app.
    """
    svc: SurveyService = app.survey_service

    @app.route('/surveys', methods=['GET'])
    def get_surveys():
        """Retrieve all surveys"""
        surveys = svc.get_all(
            page=request.args.get('page', type=int, default=1),
            page_size=request.args.get('page_size', type=int, default=10)
        )
        return jsonify(SurveySchema(many=True).dump(surveys)), 200

    @app.route('/surveys/<int:survey_id>', methods=['GET'])
    def get_survey(survey_id):
        """Retrieve a specific survey by ID"""
        survey = svc.get_by_id(survey_id)
        if not survey:
            return jsonify({'error': 'Survey not found'}), 404
        return jsonify(SurveySchema().dump(survey)), 200

    @app.route('/surveys', methods=['POST'])
    def create_survey():
        """Create a new survey"""
        try:
            data = SurveySchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400
        new_survey = svc.create(data)
        return jsonify(SurveySchema().dump(new_survey)), 201

    @app.route('/surveys/<int:survey_id>', methods=['PUT'])
    def update_survey(survey_id):
        """Update an existing survey"""
        try:
            data = SurveySchema().load(request.get_json(), partial=True)
        except ValidationError as err:
            return jsonify(err.messages), 400
        updated = svc.update(survey_id, data)
        return jsonify(SurveySchema().dump(updated)), 200

    @app.route('/surveys/<int:survey_id>', methods=['DELETE'])
    def delete_survey(survey_id):
        """Delete a survey by ID"""
        svc.delete(survey_id)
        return '', 204

    # --- Questions ---
    @app.route('/surveys/<int:survey_id>/questions', methods=['GET'])
    def get_questions(survey_id):
        questions = svc.get_questions(survey_id)
        return jsonify(SurveyQuestionSchema(many=True).dump(questions)), 200

    @app.route('/surveys/<int:survey_id>/questions', methods=['POST'])
    def create_question(survey_id):
        try:
            data = SurveyQuestionSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400
        data['survey_id'] = survey_id
        q = svc.create_question(data)
        return jsonify(SurveyQuestionSchema().dump(q)), 201

    @app.route('/surveys/<int:survey_id>/questions/<int:question_id>', methods=['PUT'])
    def update_question(survey_id, question_id):
        try:
            data = SurveyQuestionSchema().load(request.get_json(), partial=True)
        except ValidationError as err:
            return jsonify(err.messages), 400
        updated = svc.update_question(question_id, data)
        return jsonify(SurveyQuestionSchema().dump(updated)), 200

    @app.route('/surveys/<int:survey_id>/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(survey_id, question_id):
        svc.delete_question(question_id)
        return '', 204

    # --- Responses ---
    @app.route('/surveys/<int:survey_id>/responses', methods=['GET'])
    def get_responses(survey_id):
        responses = svc.get_responses(survey_id)
        return jsonify(SurveyResponseSchema(many=True).dump(responses)), 200

    @app.route('/surveys/<int:survey_id>/responses', methods=['POST'])
    def create_response(survey_id):
        try:
            data = SurveyResponseSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400
        data['survey_id'] = survey_id
        r = svc.create_response(data)
        return jsonify(SurveyResponseSchema().dump(r)), 201

    @app.route('/responses/<int:response_id>', methods=['PUT'])
    def update_response(response_id):
        try:
            data = SurveyResponseSchema().load(request.get_json(), partial=True)
        except ValidationError as err:
            return jsonify(err.messages), 400
        updated = svc.update_response(response_id, data)
        return jsonify(SurveyResponseSchema().dump(updated)), 200

    @app.route('/responses/<int:response_id>', methods=['DELETE'])
    def delete_response(response_id):
        svc.delete_response(response_id)
        return '', 204

    # --- Answers ---
    @app.route('/responses/<int:response_id>/answers', methods=['GET'])
    def get_answers(response_id):
        answers = svc.get_answers(response_id)
        return jsonify(SurveyAnswerSchema(many=True).dump(answers)), 200

    @app.route('/responses/<int:response_id>/answers', methods=['POST'])
    def create_answer(response_id):
        try:
            data = SurveyAnswerSchema().load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400
        data['response_id'] = response_id
        a = svc.create_answer(data)
        return jsonify(SurveyAnswerSchema().dump(a)), 201

    @app.route('/answers/<int:answer_id>', methods=['PUT'])
    def update_answer(answer_id):
        try:
            data = SurveyAnswerSchema().load(request.get_json(), partial=True)
        except ValidationError as err:
            return jsonify(err.messages), 400
        updated = svc.update_answer(answer_id, data)
        return jsonify(SurveyAnswerSchema().dump(updated)), 200

    @app.route('/answers/<int:answer_id>', methods=['DELETE'])
    def delete_answer(answer_id):
        svc.delete_answer(answer_id)
        return '', 204
