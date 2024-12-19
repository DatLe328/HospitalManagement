from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from app import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(RoleEnum):
    USER = 1
    CASHIER = 2
    NURSE = 3
    DOCTOR = 4
    ADMIN = 5


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class MedicineCategory(BaseModel):
    category_name = Column(String(50), nullable=False)
    medicines = relationship('Medicine', backref='medicine_category', lazy=True)

    def __str__(self):
        return self.category_name


class Medicine(BaseModel):
    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    unit = Column(String(50))
    status = Column(Boolean, default=True)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey(MedicineCategory.id), nullable=False)
    prescription_details = relationship('PrescriptionDetail', backref='medicine', lazy=True)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    full_name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    birth_date = Column(Date, default=datetime.now())
    gender = Column(Boolean, nullable=True)
    phone_number = Column(String(50), nullable=True)
    address = Column(String(100), nullable=True)
    avatar = Column(String(100), nullable=False)
    status = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    prescriptions = relationship("Prescription", backref="user", lazy=True)
    invoices = relationship("Invoice", backref="user", lazy=True)
    appointment_list_details = relationship("AppointmentDetail", backref="user", lazy=True)
    medical_history = relationship("MedicalHistory", backref="user", lazy=True, uselist=False)

    def __str__(self):
        return self.name


class Invoice(BaseModel):
    name = Column(String(50), default="Invoice", nullable=False)
    date = Column(Date, default=datetime.now())
    payment_completed = Column(Boolean, default=False)
    total_amount = Column(Float, nullable=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    def __str__(self):
        return self.name


class Prescription(BaseModel):
    name = Column(String(50), default="Prescription", nullable=False)
    date = Column(Date, default=datetime.now())
    symptoms = Column(String(100), nullable=True)
    diagnosis = Column(String(100), nullable=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    def __str__(self):
        return self.name


class PrescriptionDetail(BaseModel):
    quantity = Column(Integer, nullable=True)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)
    prescription_id = Column(Integer, ForeignKey(Prescription.id), nullable=False)


class AppointmentList(BaseModel):
    name = Column(String(50), default="Appointment List", nullable=True)
    date = Column(Date, default=datetime.now())

    def __str__(self):
        return self.name


class AppointmentDetail(BaseModel):
    appointment_list_id = Column(Integer, ForeignKey(AppointmentList.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)


class Disease(BaseModel):
    name = Column(String(50), nullable=True)
    medical_history_details = relationship("MedicalHistoryDetail", backref="disease", lazy=True)

    def __str__(self):
        return self.name


class MedicalHistory(BaseModel):
    name = Column(String(50), default="Medical History", nullable=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    history_details = relationship("MedicalHistoryDetail", backref="medical_history", lazy=True)

    def __str__(self):
        return self.name


class MedicalHistoryDetail(BaseModel):
    medical_history_id = Column(Integer, ForeignKey(MedicalHistory.id), nullable=False)
    disease_id = Column(Integer, ForeignKey(Disease.id), nullable=False)



if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        import hashlib

        password = "123"
        password_admin = "123456"
        password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
        password_admin = str(hashlib.md5(password_admin.encode('utf-8')).hexdigest())

        # Seed Users
        u1 = User(full_name="Tran Dang Tuan", username="admin", password=password_admin, gender=True,
                  phone_number="0123", address="Ho Chi Minh City",
                  avatar="http://it.ou.edu.vn/asset/ckfinder/userfiles/5/images/giang_vien/Vinh_2.jpg", user_role=UserRole.ADMIN)
        u2 = User(full_name="Nguyen Thi Phuong Trang", username="cashier", password=password, gender=False,
                  phone_number="0124", address="Ho Chi Minh City",
                  avatar="http://it.ou.edu.vn/asset/ckfinder/userfiles/5/images/giang_vien/Vinh_2.jpg", user_role=UserRole.CASHIER)
        u3 = User(full_name="Nguyen Thi Mai Trang", username="nurse", password=password, gender=False,
                  phone_number="0125", address="Ho Chi Minh City",
                  avatar="http://example.com/avatar3.jpg", user_role=UserRole.NURSE)
        u4 = User(full_name="Ho Quang Khai", username="doctor", password=password, gender=True, phone_number="0126",
                  address="Ho Chi Minh City",
                  avatar="http://example.com/avatar4.jpg", user_role=UserRole.DOCTOR)
        u5 = User(full_name="Luu Quang Phuong", username="user", password=password, gender=True, phone_number="0127",
                  address="Ho Chi Minh City",
                  avatar="http://example.com/avatar5.jpg", user_role=UserRole.USER)
        u6 = User(full_name="Dang Sy Tuan", username="user1", password=password, gender=True, phone_number="0128",
                  address="Phu Nhuan",
                  avatar="http://example.com/avatar6.jpg", user_role=UserRole.USER)

        # Seed Medicine Categories
        mc1 = MedicineCategory(category_name="Liquid Medicine")
        mc2 = MedicineCategory(category_name="Tablet Medicine")
        mc3 = MedicineCategory(category_name="Powder Medicine")

        # Seed Medicines
        m1 = Medicine(name="Paracetamol", price=50000, unit="Tablet", description="Oral", category_id=2)
        m2 = Medicine(name="Vitamin C", price=10000, unit="Tablet", description="Oral", category_id=2)
        m3 = Medicine(name="Y", price=5000, unit="Milli", description="Oral", category_id=1)
        m4 = Medicine(name="Sensacool", price=20000, unit="Packet", description="Oral", category_id=3)
        m5 = Medicine(name="Adrenaline", price=30000, unit="Packet", description="Oral", category_id=3)
        m6 = Medicine(name="Probiotic", price=15000, unit="Packet", description="Oral", category_id=3)

        # Seed Prescriptions
        p1 = Prescription(name="Prescription 1", symptoms="Stomachache", diagnosis="Stomach Ulcer", user_id=5)
        p2 = Prescription(name="Prescription 2", symptoms="Back pain", diagnosis="Spinal Degeneration", user_id=3)
        p3 = Prescription(name="Prescription 3", symptoms="Heart pain", diagnosis="Heart Attack", user_id=4)

        # Seed Prescription Details
        pd1_p1 = PrescriptionDetail(quantity=3, medicine_id=3, prescription_id=1)
        pd2_p1 = PrescriptionDetail(quantity=2, medicine_id=5, prescription_id=1)
        pd3_p1 = PrescriptionDetail(quantity=10, medicine_id=6, prescription_id=1)
        pd1_p2 = PrescriptionDetail(quantity=5, medicine_id=6, prescription_id=2)
        pd2_p2 = PrescriptionDetail(quantity=4, medicine_id=4, prescription_id=2)
        pd1_p3 = PrescriptionDetail(quantity=8, medicine_id=2, prescription_id=3)
        pd2_p3 = PrescriptionDetail(quantity=15, medicine_id=6, prescription_id=3)

        # Seed Appointment Lists
        al1 = AppointmentList(name="Appointment List 1", date=datetime.now())
        al2 = AppointmentList(name="Appointment List 2", date=datetime.now())

        # Seed Appointment List Details
        ald1_al1 = AppointmentDetail(appointment_list_id=1, user_id=3)
        ald2_al1 = AppointmentDetail(appointment_list_id=1, user_id=5)
        ald1_al2 = AppointmentDetail(appointment_list_id=2, user_id=4)

        # Seed Diseases
        d1 = Disease(name="Back pain")
        d2 = Disease(name="Headache")
        d3 = Disease(name="Stomachache")
        d4 = Disease(name="Toothache")
        d5 = Disease(name="Heart pain")

        # Seed Medical Histories
        mh1 = MedicalHistory(name="Medical History 1", user_id=3)
        mh2 = MedicalHistory(name="Medical History 2", user_id=5)
        mh3 = MedicalHistory(name="Medical History 3", user_id=4)

        # Seed Medical History Details
        mhd1_mh1 = MedicalHistoryDetail(medical_history_id=1, disease_id=1)
        mhd2_mh1 = MedicalHistoryDetail(medical_history_id=1, disease_id=2)
        mhd3_mh1 = MedicalHistoryDetail(medical_history_id=2, disease_id=3)
        mhd1_mh2 = MedicalHistoryDetail(medical_history_id=2, disease_id=4)
        mhd2_mh2 = MedicalHistoryDetail(medical_history_id=2, disease_id=5)
        mhd1_mh3 = MedicalHistoryDetail(medical_history_id=3, disease_id=5)

        # Seed Invoices
        i1 = Invoice(name="Invoice 1", total_amount=1000000, user_id=3)
        i2 = Invoice(name="Invoice 2", total_amount=2000000, user_id=5)
        i3 = Invoice(name="Invoice 3", total_amount=4000000, user_id=4)
        i4 = Invoice(name="Invoice 4", total_amount=2600000, user_id=2)
        i5 = Invoice(name="Invoice 5", total_amount=1700000, user_id=5)
        i6 = Invoice(name="Invoice 6", total_amount=2000000, user_id=1)
        i7 = Invoice(name="Invoice 7", total_amount=1400000, user_id=3)
        i8 = Invoice(name="Invoice 8", total_amount=2400000, user_id=1)

        # Add all data to the session
        db.session.add_all([u1, u2, u3, u4, u5, u6])
        db.session.add_all([mc1, mc2, mc3])
        db.session.add_all([m1, m2, m3, m4, m5, m6])
        db.session.add_all([d1, d2, d3, d4, d5])
        # db.session.add_all([p1, p2, p3])
        # db.session.add_all([pd1_p1, pd2_p1, pd3_p1, pd1_p2, pd2_p2, pd1_p3, pd2_p3])
        # db.session.add_all([al1, al2])
        # db.session.add_all([ald1_al1, ald2_al1, ald1_al2])
        # db.session.add_all([mh1, mh2, mh3])
        # db.session.add_all([mhd1_mh1, mhd2_mh1, mhd3_mh1, mhd1_mh2, mhd2_mh2, mhd1_mh3])
        # db.session.add_all([i1, i2, i3, i4, i5, i6, i7, i8])

        # Commit the session
        db.session.commit()
