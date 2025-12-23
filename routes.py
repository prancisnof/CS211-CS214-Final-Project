from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Patient, MedicalRecord, Doctor, Appointment, Prescription
from datetime import datetime

main = Blueprint('main', __name__)

# =========================================================
# --- READ: Dashboard (Patients) ---
# =========================================================
@main.route('/')
def dashboard():
    patients = Patient.query.all()
    return render_template('dashboard.html', patients=patients)

# =========================================================
# --- CREATE: Add Patient ---
# =========================================================
@main.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        count = Patient.query.count() + 1
        case_no = f"P-{count:02d}"

        new_patient = Patient(
            case_no=case_no,
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            middle_name=request.form.get('middle_name'),
            gender=request.form['gender'],
            age=request.form['age'],
            contact_no=request.form['contact_no'],
            address=request.form['address'],
            date_of_birth=datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
        )
        db.session.add(new_patient)
        db.session.commit()
        flash("Patient added successfully!", "success")
        return redirect(url_for('main.dashboard'))
    return render_template('add_patient.html')

# =========================================================
# --- UPDATE: Edit Patient ---
# =========================================================
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)

    if request.method == 'POST':
        patient.first_name = request.form['first_name']
        patient.middle_name = request.form.get('middle_name')
        patient.last_name = request.form['last_name']
        patient.gender = request.form['gender']
        patient.age = request.form['age']
        patient.contact_no = request.form['contact_no']
        patient.address = request.form['address']
        patient.date_of_birth = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()

        db.session.commit()
        flash("Patient updated successfully!", "info")
        return redirect(url_for('main.dashboard'))
    return render_template('edit_patient.html', patient=patient)

# =========================================================
# --- DELETE: Remove Patient (POST safer) ---
# =========================================================
@main.route('/delete/<int:id>', methods=['POST'])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash("Patient deleted successfully!", "danger")
    return redirect(url_for('main.dashboard'))

# =========================================================
# --- VIEW: Patient Details ---
# =========================================================
@main.route('/patient/<int:id>')
def patient_details(id):
    patient = Patient.query.get_or_404(id)

    # Related records
    medical_records = MedicalRecord.query.filter_by(patient_id=id).all()
    prescriptions = Prescription.query.join(MedicalRecord).filter(MedicalRecord.patient_id == id).all()
    appointments = Appointment.query.filter_by(patient_id=id).all()

    return render_template(
        'patient_details.html',
        patient=patient,
        medical_records=medical_records,
        prescriptions=prescriptions,
        appointments=appointments
    )

# =========================================================
# --- VIEW: Doctors ---
# =========================================================
@main.route('/doctors')
def doctors():
    doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors)

# =========================================================
# --- VIEW: Medical Records ---
# =========================================================
@main.route('/records')
def records():
    records = MedicalRecord.query.all()
    return render_template('records.html', records=records)

# =========================================================
# --- VIEW: Prescriptions ---
# =========================================================
@main.route('/prescriptions')
def prescriptions():
    prescriptions = Prescription.query.all()
    return render_template('prescriptions.html', prescriptions=prescriptions)

# =========================================================
# --- VIEW: Appointments ---
# =========================================================
@main.route('/appointments')
def appointments():
    appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=appointments)