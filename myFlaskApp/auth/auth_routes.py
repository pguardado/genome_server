import os
import sys
import uuid
import logging
from io import StringIO
from flask import current_app as app, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from Bio import SeqIO
from . import auth_bp
from .auth_utils import (
    handle_post_request, process_file_upload, save_file, render_registration_form, 
    get_file_path, find_substring_matches, 
    get_genomic_region_sequence, allowed_file, parse_genome, 
    read_file_with_biopython, parse_file, reverse_complement, 
    get_headline_and_sequence_length, get_genome_sequence
)
from ..models import FileRecord
from ..utils import store_file_info_in_session, get_file_info_from_session, get_file_record
from ..db import db

# Define a route for file upload
@auth_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('upload.html', message='No file part in the request'), 400

    unique_id_from_form = request.form.get('unique_id')
    print(f"Unique ID from form: {unique_id_from_form}")  # Log the unique_id from form

    if not unique_id_from_form:
        unique_id_from_form = str(uuid.uuid4()).replace("-", "")
        print(f"Generated UUID: {unique_id_from_form}")  # Log the generated UUID

    unique_identifier = unique_id_from_form
    print(f"Final unique identifier: {unique_identifier}")  # Log the final unique identifier

    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            print(f"Creating directory: {app.config['UPLOAD_FOLDER']}")
            os.makedirs(app.config['UPLOAD_FOLDER'])

        file.save(file_path)

        if os.path.exists(file_path):
            try:
                chromosome_lengths = parse_file(file_path)
            except Exception as e:
                print(f"Error parsing file: {e}", file=sys.stderr)
                chromosome_lengths = {}

            print(f"File saved successfully: {file_path}")

            # Store file info in session
            store_file_info_in_session({
                'unique_identifier': unique_identifier,
                'filename': filename,
                'file_path': file_path
            })

            # Create a new FileRecord instance
            file_record = FileRecord(
                unique_identifier=unique_identifier,
                filename=filename,
                file_path=file_path
            )

            # Add the new record to the session
            db.session.add(file_record)

            try:
                # Commit the session to save the new record
                db.session.commit()
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                db.session.rollback()
                return render_template('upload.html', message='Error uploading file')

            return render_template('summary.html', unique_identifier=unique_identifier, message='File uploaded successfully', num_chromosomes=len(chromosome_lengths), chromosome_lengths=chromosome_lengths)
        else:
            print(f"Error saving file: {file_path}")
            return render_template('upload.html', message='Error saving file')
    else:
        return render_template('upload.html', message='Invalid file or file type')

@auth_bp.route('/download', methods=['GET', 'POST'])
def download_file():
    if request.method == 'POST':
        unique_identifier = request.form['unique_identifier']

        file_info = get_file_info_from_session()
        if file_info is not None and file_info['unique_identifier'] == unique_identifier:
            file_path = file_info['file_path']

            try:
                record = read_file_with_biopython(file_path)
                return render_template('display_sequence.html', record=record)
            except Exception as e:
                print(f"Error reading file: {e}", file=sys.stderr)
                return render_template('download.html', message='Error reading file')
        else:
            return render_template('download.html', message='File not found with the given identifier')

    return render_template('download.html')

@auth_bp.route('/parse_genome', methods=['POST'])
def parse_genome_page():
    file_info = get_file_info_from_session()
    if not file_info:
        return jsonify({'message': 'No file uploaded'}), 400
    file_path = file_info['file_path']
    records = parse_genome(file_path)
    return jsonify(records)

@auth_bp.route('/summary/<unique_identifier>', methods=['GET'])
def summary(unique_identifier):
    file_record = get_file_record(unique_identifier)  # Use your function here
    if file_record is not None:
        file_path = file_record.file_path

        try:
            chromosome_lengths = parse_file(file_path)
            num_chromosomes = len(chromosome_lengths)
            return render_template('summary.html', num_chromosomes=num_chromosomes, chromosome_lengths=chromosome_lengths)
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            return render_template('upload.html', message='Error reading file')
    else:
        return render_template('upload.html', message='File not found with the given identifier')

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if request.method == 'POST':
        try:
            logging.info('Received POST request')
            unique_id = request.form.get('unique_id')  # Retrieve unique_id from form data
            logging.info(f'unique_id: {unique_id}')

            analysis_type = request.form.get('analysis_type')  # Retrieve the analysis type from the form data
            logging.info(f'analysis_type: {analysis_type}')  # Log the analysis type

            # Redirect to the appropriate analysis route
            if analysis_type == 'genome_summary':
                return redirect(url_for('genome_summary', unique_id=unique_id))
            elif analysis_type == 'genome_region':
                return redirect(url_for('genomic_region', unique_id=unique_id))
            elif analysis_type == 'genome_string_match':
                return redirect(url_for('genome_string_match', unique_id=unique_id))
        except Exception as e:
            logging.error(f'Error occurred during analysis: {e}')
            return "An error occurred during analysis", 500  # Return generic error message

    logging.info('Rendering analysis.html')
    return render_template('analysis.html')


@app.route('/genome_summary', methods=['GET', 'POST'])
def genome_summary():
    if request.method == 'POST':
        accession_number = request.form.get('accession_number')
        unique_id = request.args.get('unique_id')  # Retrieve unique_id from query parameters

        if not unique_id:
            return "No unique ID found in request", 400

        file_record = FileRecord.query.filter_by(unique_identifier=unique_id).first()

        if not file_record:
            return "Invalid unique identifier", 400

        fasta_data = StringIO(file_record.get_contents())
        headline, length = get_headline_and_sequence_length(accession_number, fasta_data)

        return render_template('genome_summary_results.html', headline=headline, length=length)

    return render_template('genome_summary.html')

@app.route('/genomic_region', methods=['GET', 'POST'])
def genomic_region():
    if request.method == 'POST':
        accession_number = request.form.get('accession_number')
        start_position = int(request.form.get('start_position'))
        end_position = int(request.form.get('end_position'))
        unique_id = request.args.get('unique_id')  # Retrieve unique_id from query parameters

        if not unique_id:
            return "No unique ID found in request", 400

        file_record = FileRecord.query.filter_by(unique_identifier=unique_id).first()

        if not file_record:
            return "Invalid unique identifier", 400

        fasta_data = StringIO(file_record.get_contents())
        sequence = get_genomic_region_sequence(accession_number, start_position, end_position, fasta_data)

        if sequence is None:
            return "Sequence not found for the specified genomic region", 404

        print("Sequence Length:", len(sequence))  # Print sequence length for debugging

        return render_template('genomic_region_results.html', sequence=sequence)

    return render_template('genomic_region.html')

import logging

# Add logging configuration
logging.basicConfig(level=logging.INFO)

@app.route('/genome_string_match', methods=['GET', 'POST'])
def genome_string_match():
    if request.method == 'POST':
        query_sequence = request.form.get('query_sequence')
        accession_number = request.form.get('accession_number')
        unique_id = request.args.get('unique_id')  # Retrieve unique_id from query parameters

        if not unique_id:
            logging.error("No unique ID found in request")
            return "No unique ID found in request", 400

        file_record = FileRecord.query.filter_by(unique_identifier=unique_id).first()

        if not file_record:
            logging.error("Invalid unique identifier")
            return "Invalid unique identifier", 400

        fasta_data = file_record.get_contents()
        genome_sequence = get_genomic_region_sequence(accession_number, 0, None, fasta_data)

        if genome_sequence is None:
            logging.error("No genome sequence found for the given accession number")
            return "No genome sequence found for the given accession number", 400

        logging.info("Genome Sequence: %s", genome_sequence[:100])  # Log the first 100 characters of the genome sequence for debugging

        matches = find_substring_matches(query_sequence, genome_sequence)

        if not matches:
            logging.info("No matches found")
        else:
            logging.info("Matches found: %s", matches)

        return render_template('genome_string_match_results.html', matches=matches)

    return render_template('genome_string_match.html')
