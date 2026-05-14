from flask import Blueprint, request, jsonify
from app import db
from app.models import Student
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

student_bp = Blueprint('student', __name__)


@student_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    logger.info("Healthcheck endpoint called")
    return jsonify({'status': 'healthy'}), 200


@student_bp.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    logger.info(f"Adding new student: {data}")

    if not data or not data.get('name') or not data.get('email') or not data.get('age'):
        logger.error("Missing required fields")
        return jsonify({'error': 'name, age and email are required'}), 400

    existing = Student.query.filter_by(email=data['email']).first()
    if existing:
        logger.error(f"Email already exists: {data['email']}")
        return jsonify({'error': 'Email already exists'}), 400

    student = Student(
        name=data['name'],
        age=data['age'],
        email=data['email']
    )
    db.session.add(student)
    db.session.commit()
    logger.info(f"Student created successfully with id: {student.id}")
    return jsonify(student.to_dict()), 201


@student_bp.route('/students', methods=['GET'])
def get_students():
    logger.info("Fetching all students")
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students]), 200


@student_bp.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    logger.info(f"Fetching student with id: {id}")
    student = db.session.get(Student, id)
    if not student:
        logger.error(f"Student not found with id: {id}")
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(student.to_dict()), 200


@student_bp.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    logger.info(f"Updating student with id: {id}")
    student = db.session.get(Student, id)
    if not student:
        logger.error(f"Student not found with id: {id}")
        return jsonify({'error': 'Student not found'}), 404

    data = request.get_json()
    if data.get('name'):
        student.name = data['name']
    if data.get('age'):
        student.age = data['age']
    if data.get('email'):
        student.email = data['email']

    db.session.commit()
    logger.info(f"Student updated successfully with id: {id}")
    return jsonify(student.to_dict()), 200


@student_bp.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    logger.info(f"Deleting student with id: {id}")
    student = db.session.get(Student, id)
    if not student:
        logger.error(f"Student not found with id: {id}")
        return jsonify({'error': 'Student not found'}), 404

    db.session.delete(student)
    db.session.commit()
    logger.info(f"Student deleted successfully with id: {id}")
    return jsonify({'message': 'Student deleted successfully'}), 200