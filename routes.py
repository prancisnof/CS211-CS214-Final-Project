from flask import Blueprint, render_template, request, redirect, url_for, make_response
from models import db, Patient, MedicalRecord, Doctor, Appointment, Prescription
from datetime import datetime

main = Blueprint('main', __name__)

# =========================================================
# --- READ: Dashboard ---
# =========================================================

# This is the homepage.
@main.route('/')
def dashboard():
    patients = Patient.query.all()
    # Render the 'dashboard.html' template and pass the list of patients to it for display.
    return render_template('dashboard.html', patients=patients)


# =========================================================
#  --- CREATE: Add Patient ---
# =========================================================

@main.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        # Generate a new case number by counting existing patients and adding 1.
        count = Patient.query.count() + 1
        # Format the case number as a string like "P-01".
        case_no = f"P-{count:02d}"
        
        # Create a new Patient object using data coming from the HTML form.
        new_patient = Patient(
            case_no = case_no,                                
            first_name = request.form['first_name'],         
            last_name = request.form['last_name'],           
            middle_name = request.form.get('middle_name'),   
            gender = request.form['gender'],                
            age = request.form['age'],                       
            contact_no = request.form['contact_no'],      
            address = request.form['address'],             
        # Convert the date string (YYYY-MM-DD) from the form into a Python date object.
            date_of_birth=datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
        )
        # Add the new patient object to the current database session.
        db.session.add(new_patient)
        # Commit the session to save the new patient into the database.
        db.session.commit()
        # Redirect the user back to the main dashboard after successful saving.
        return redirect(url_for('main.dashboard'))
    return render_template('add_patient.html')


# =========================================================
#  --- UPDATE: Edit Patient ---
# =========================================================

# Edit patient route
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    # Fetch the patient or 404 if not found.
    patient = Patient.query.get_or_404(id)

    # Check if the form is being submitted with new data.
    if request.method == 'POST':
        # Update the existing patient object's attributes with the new form data.
        patient.first_name = request.form['first_name']
        patient.last_name = request.form['last_name']
        patient.gender = request.form['gender']
        patient.contact_no = request.form['contact_no']
        
        db.session.commit()
        # Redirect back to the dashboard.
        return redirect(url_for('main.dashboard'))
    return render_template('edit_patient.html', patient=patient)


# =========================================================
#  --- DELETE: Remove Patient ---
# =========================================================

# Deleting patient route
@main.route('/delete/<int:id>')
def delete_patient(id):
    # Fetch the patient or 404 if not found.
    patient = Patient.query.get_or_404(id)
    
    # Mark the patient object for deletion in the database session.
    db.session.delete(patient)
    
    # Commit the transaction to permanently remove the row.
    db.session.commit()
    return redirect(url_for('main.dashboard'))