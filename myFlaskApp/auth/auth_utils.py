# auth_utils.py

from Bio import SeqIO, Seq
from io import StringIO
import sys
import psycopg2
from collections import defaultdict

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'fa'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_file_with_biopython(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            record = SeqIO.read(file, 'fasta')  # Adjust the format as needed (e.g., 'fasta', 'genbank')
        return record
    except UnicodeDecodeError:
        print("Error decoding file. Trying a different encoding.", file=sys.stderr)
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                record = SeqIO.read(file, 'fasta')
            return record
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)

            raise
def reverse_complement(sequence):
    seq = Seq.Seq(sequence)
    return str(seq.reverse_complement())


def get_headline_and_sequence_length(accession_number, fasta_data):
    full_headline = None
    sequence_length = 0
    
    for record in SeqIO.parse(fasta_data, "fasta"):
        if accession_number in record.id:
            full_headline = record.description
            sequence_length = len(record.seq)  # Count the number of bases in the sequence
            break  # No need to continue searching after finding the record
    
    return full_headline, sequence_length

import logging
from io import StringIO
from Bio import SeqIO

# Add logging configuration
logging.basicConfig(level=logging.INFO)

def get_genomic_region_sequence(accession_number, start_position=None, end_position=None, fasta_data=None):
    sequence = None

    if isinstance(fasta_data, str):
        fasta_data = StringIO(fasta_data)

    for record in SeqIO.parse(fasta_data, "fasta"):
        logging.info("Record ID: %s", record.id)  # Log the record ID for debugging
        logging.info("Record Sequence: %s", record.seq)  # Log the record sequence for debugging

        if accession_number in record.id:
            # If start_position and end_position are provided, extract the specific region
            if start_position is not None and end_position is not None:
                sequence = str(record.seq[start_position - 1:end_position])  # Adjust positions to 0-based indexing
            else:  # If not, get the full sequence
                sequence = str(record.seq)
            logging.info("Extracted Sequence: %s", sequence)  # Log the extracted sequence for debugging
            break  # No need to continue searching after finding the record

    if sequence is None:
        logging.warning("No sequence found for accession number: %s", accession_number)

    return sequence




def parse_genome(file_path):
    records = []

    try:
        with open(file_path, 'r') as file:
            records = list(SeqIO.parse(file, 'fasta'))
    except Exception as e:
        logging.error("Error occurred while parsing genome file: %s", e)

    return records

def get_genome_sequence(accession_number, fasta_data):
    for record in SeqIO.parse(fasta_data, "fasta"):
        if record.id == accession_number:
            return record.seq  # Return the sequence of the record with the matching accession number
    return None  # Return None if no matching record is found

from Bio.Seq import Seq

def find_substring_matches(query_sequence, genome_sequence):
    matches = []
    query_length = len(query_sequence)

    print("Query Sequence Length:", query_length)  # Print length of the query sequence
    print("Genome Sequence Length:", len(genome_sequence))  # Print length of the genome sequence

    # Convert the query sequence to a BioPython Seq object
    query_seq = Seq(query_sequence.upper())  # Convert to uppercase

    # Convert the genome sequence to uppercase
    genome_sequence = genome_sequence.upper()

    # Iterate over the genome sequence and search for matches
    for i in range(len(genome_sequence) - query_length + 1):
        # Extract a substring of the same length as the query from the genome sequence
        substring = genome_sequence[i:i+query_length]

        print("Searching at Index:", i)  # Print the index where substring search begins
        print("Substring:", substring)  # Print the substring for debugging

        # Convert the substring to a BioPython Seq object
        substring_seq = Seq(substring)

        # Check if the substring matches the query sequence or its reverse complement
        if substring_seq == query_seq or substring_seq.reverse_complement() == query_seq:
            # If a match is found, store the indices (start and end positions) of the match
            matches.append((i+1, i+query_length))  # Adjust indices to 1-based indexing
            print("Match found at indices:", i+1, "-", i+query_length)  # Print the indices of the match

    if not matches:
        print("No matches found")  # Log message if no matches are found

    return matches





def parse_file(file_path):
    chromosome_lengths = defaultdict(int)

    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            # Calculate the length of the sequence
            length = len(line.strip())

            # Use the line number as the chromosome identifier
            chromosome = f"Chromosome {i+1}"

            chromosome_lengths[chromosome] = length

    return chromosome_lengths


def insert_file_record(cursor, unique_identifier, filename, file_path):
    try:
        print(f"Inserting values into database: {unique_identifier}, {filename}, {file_path}")

        cursor.execute('INSERT INTO files (filename, file_path, unique_identifier) VALUES (%s, %s, %s)',
                       (filename, file_path, unique_identifier))

    except psycopg2.Error as e:
        print(f"Error inserting record: {e}")
        print(f"Values: {unique_identifier}, {filename}, {file_path}")
        cursor.connection.rollback()
    else:
        print("Record inserted successfully")

def handle_post_request(request):
    # TODO: Implement post request handling logic
    pass

def process_file_upload(request):
    # TODO: Implement file upload processing logic
    pass

def save_file(file):
    # TODO: Implement file saving logic
    pass

def store_file_info_in_db(file):
    # TODO: Implement file info storing logic
    pass

def render_registration_form():
    # TODO: Implement registration form rendering logic
    pass

def get_file_path():
    # TODO: Implement file path retrieval logic
    pass


