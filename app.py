import json
from wtforms import SelectField
from flask_wtf import FlaskForm
import string
import random
from flask_admin.contrib.sqla import ModelView
#from flask_restful import Api, Resource
from flask import Flask, jsonify, request
from sqlalchemy import ForeignKey
from model_views import (
    testAdminView, MyModelView, usernameview, testView1, samplep, invoice, report, invoiceDetails, paymentHistory,pickupDetails,
    receiveDetails, sampleStock, Allspecies, Allspecimen, analyticalTest, ourEmployee, invoices, locationViews, clinicalTestViews
)
import forms
import os
from flask import (Flask, url_for, render_template,
                   abort, redirect
                   )
from flask_sqlalchemy import SQLAlchemy
from flask_security import (Security, SQLAlchemyUserDatastore,
                            UserMixin, RoleMixin, login_required, current_user, roles_required
                            )
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin import BaseView, expose
from flask_admin import helpers as admin_helpers
from flask_admin.contrib import sqla
from datetime import datetime


def create_app():
    # The template files will be stored in the [templates] directory
    app = Flask(__name__, template_folder="templates")
    app.debug = True
    app.config.from_pyfile('config.py')
    return app


# Construct an instance of Flask class for our webapp
app = create_app()
# Create database connection object
db = SQLAlchemy(app)
app.app_context().push()
# --------------------------------
# FLASK-SECURITY MODELS
# --------------------------------
user_profiles = db.Table(
    'profile_username',
    db.Column('username_id', db.Integer(), db.ForeignKey('username.id')),
    db.Column('profile_id', db.Integer(), db.ForeignKey('profile.id'))
)


class Profile(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class Username(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True, index=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Profile',
                            secondary=user_profiles,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email


# --------------------------------
# FORMS
# --------------------------------

# --------------------------------
# Setup Flask-Security
# --------------------------------
user_datastore = SQLAlchemyUserDatastore(db, Username, Profile)
security = Security(app, user_datastore,
                    login_form=forms.ExtendedLoginForm)
# register_form=forms.ExtendedRegisterForm)

# --------------------------------
# MODELS
# --------------------------------


# Db for the test


class invoice_details(db.Model):
    invoice_details_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    invoice_id = db.Column(db.Integer, nullable=True)
    test_name = db.Column(db.String(200), nullable=True)
    amount = db.Column(db.Integer, nullable=True)
    created_by = db.Column(db.String(100), nullable=True)
    created_date = db.Column(db.DateTime(timezone=True),
                             default=datetime.utcnow, nullable=True)
    updated_by = db.Column(db.String(100), nullable=True)
    updated_date = db.Column(db.DateTime(timezone=True),
                             default=datetime.utcnow, nullable=True)

    def __str__(self):
        return self.invoice_id
    
    
class payment_history(db.Model):
    payment_history_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    invoice_id = db.Column(db.Integer, nullable=True)
    payment_mode = db.Column(db.String(200), nullable=True)
    total_amount = db.Column(db.Integer, nullable=True)
    paid_amount=db.Column(db.Integer, nullable=True)
    balance_amt = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, nullable=True)
    payment_collected_by = db.Column(db.String(100), nullable=True)
    payment_collected_date = db.Column(db.DateTime(timezone=True),
                                       default=datetime.utcnow, nullable=True)
    def __str__(self):
        return self.payment_mode
    
    
class pickup_details(db.Model):
    pickup_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    sample_id = db.Column(db.Integer, nullable=True)
    picked_by = db.Column(db.String(100), nullable=True)
    picked_date = db.Column(db.DateTime(timezone=True),
                            default=datetime.utcnow, nullable=True)
    remarks = db.Column(db.String(500), nullable=True)
    created_by = db.Column(db.String(100), nullable=True)

    def __str__(self):
        return self.sample_id
    

class location(db.Model):
    location_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    location_name = db.Column(db.String(500), nullable=True)
    sflag = db.Column(db.Integer, nullable=True)
    iflag = db.Column(db.Integer, nullable=True)


class receive_details(db.Model):
    receive_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    sample_id = db.Column(db.Integer, nullable=True)
    received_by = db.Column(db.String(100), nullable=True)
    received_date = db.Column(db.DateTime(timezone=True),
                              default=datetime.utcnow, nullable=True)
    remarks = db.Column(db.String(500), nullable=True)
    created_by=db.Column(db.String(100), nullable=True)
    vet_remarks = db.Column(db.String(500), nullable=True)
    vetremarks_updated_by = db.Column(db.String(100), nullable=True)
    vetremarks_updated_date = db.Column(db.DateTime(timezone=True),
                                        default=datetime.utcnow, nullable=True)

    def __str__(self):
        return self.receive_id
    
    
class sample_stock(db.Model):
    sample_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    sample_code = db.Column(db.String(20), nullable=True)
    sample_name=db.Column(db.String(100), nullable=True)
    sample_description = db.Column(db.String(1000), nullable=True)
    outcome_remarks = db.Column(db.String(1000), nullable=True)
    noof_samples = db.Column(db.Integer, nullable=True)
    customer_name = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(1000), nullable=True)
    mobile_no=db.Column(db.Integer, nullable=True)
    phone_no=db.Column(db.Integer, nullable=True)
    email_id=db.Column(db.String(100), nullable=True)
    created_by = db.Column(db.String(100), nullable=True)
    created_time = db.Column(db.Time(timezone=True),
                             default=datetime.utcnow, nullable=True)
    counciler_status=db.Column(db.Integer, nullable=True)
    customer_status=db.Column(db.Integer, nullable=True)
    pickup_status = db.Column(db.Integer, nullable=True)
    created_date = db.Column(db.DateTime(timezone=True),
                             default=datetime.utcnow, nullable=True)
    total_sample_price=db.Column(db.Integer, nullable=True)
    price_unit = db.Column(db.Integer, nullable=True)
    customer_accepted_by = db.Column(db.String(100), nullable=True)
    customer_accepted_date = db.Column(db.DateTime(timezone=True),
                                       default=datetime.utcnow, nullable=True)
    result_upload_status=db.Column(db.Integer, nullable=True)
    pickup_accepted_status = db.Column(db.Integer, nullable=True)
    receive_accepted_status = db.Column(db.Integer, nullable=True)
    invoice_status = db.Column(db.Integer, nullable=True)
    updated_by = db.Column(db.String(100), nullable=True)
    updated_date = db.Column(db.DateTime(timezone=True),
                             default=datetime.utcnow, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender=db.Column(db.String(25), nullable=True)
    pincode = db.Column(db.Integer, nullable=True)
    location_id = db.Column(db.Integer, nullable=True)
    bread=db.Column(db.String(100), nullable=True)
    # gender = db.Column(db.String(100), nullable=True)
    species_id = db.Column(db.Integer, nullable=True)
    specimen_id = db.Column(db.Integer, nullable=True)

    def __str__(self):
        return self.sample_code
    

class clinicalTest(db.Model):
    clinicalTest_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    clinicalTest_name = db.Column(db.String(500), nullable=True)



class species(db.Model):
    species_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    species_name = db.Column(db.String(100), nullable=True)

    def __str__(self):
        return self.species_id
    
    
class specimen(db.Model):
    specimen_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    specimen_name = db.Column(db.String(500), nullable=True)

    def __str__(self):
        return self.specimen_id


class AnalyticalTestForm(FlaskForm):
    outcome_result = SelectField('Outcome Result', choices=[(
        'positive', 'Positive'), ('negative', 'Negative')])
class analytical_test(db.Model):
    test_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    test_name = db.Column(db.String(200), nullable=True)
    sample_id = db.Column(db.Integer, nullable=True)
    outcome_result = db.Column(db.String(100), nullable=True)
    test_outcome_created_by = db.Column(db.String(100), nullable=True)
    test_outcome_created_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Integer, nullable=True)
    

class employee(db.Model):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    emp_id = db.Column(db.Integer, nullable=True)
    emp_name = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(200), nullable=True)
    designation = db.Column(db.String(200), nullable=True)
    status = db.Column(db.Integer, nullable=True)
    email_id = db.Column(db.String(200), nullable=True)
    phone_no = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(500), nullable=True)
    location = db.Column(db.Integer, nullable=True)
    usercode = db.Column(db.String(20), nullable=True)

    def __str__(self):
        return self.emp_id
    
    
class invoice(db.Model):
    invoice_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    sample_id = db.Column(db.Integer, nullable=True)
    total = db.Column(db.Integer, nullable=True)
    gst = db.Column(db.Integer, nullable=True)
    gst_amount = db.Column(db.Integer, nullable=True)
    created_by = db.Column(db.String(100), nullable=True)
    created_date = db.Column(db.DateTime(timezone=True),
                             default=datetime.utcnow, nullable=True)
    updated_by = db.Column(db.String(100), nullable=True)
    updated_date = db.Column(db.DateTime(timezone=True),
                             default=datetime.utcnow, nullable=True)
    paid_amount = db.Column(db.Integer, nullable=True)
    bal_amt = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, nullable=True)
    others_amt = db.Column(db.Integer, nullable=True)
    others_remarks = db.Column(db.String(500), nullable=True)
    grand_total = db.Column(db.Integer, nullable=True)

    def __str__(self):
        return self.grand_total
    
    
# class sqlite_sequence(db.Model):
#     name = db.Column(db.String(500))
#     seq = db.Column(db.Integer)

#     def __str__(self):
#         return self.name
    
    
    
    
    
    

# --------------------------------
# MODEL VIEW CLASSES
# --------------------------------

# --------------------------------
# FLASK VIEWS / ROUTES
# --------------------------------

@app.route('/')
def index():
    # return render_template('index.html')
    return redirect("/admin")


# creating a class object of testUserView imported from Model_views.py
class testUserView(BaseView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False
    
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        if request.method == 'POST':
            data = request.form
            print(data)
            generate_id(data)
            return jsonify({'success': True})
        # return self.render('admin/usertest.html')
        speciesData = get_species_table_data()
        specimenData = get_specimen_table_data()
        locationData=get_location_table_data()
        clinicalTestData = get_clinicalTest_table_data()
        clinicalTestDatas = json.dumps(clinicalTestData)
        return self.render('admin/usertest.html', speciesData=speciesData, specimenData=specimenData, locationData=locationData, clinicalTestData=clinicalTestDatas, admin_base_template=admin.base_template)
    

def get_species_table_data():
    speciess = db.session.query(species).all()
    data = []
    for spe in speciess:
        row = [spe.species_id, spe.species_name]
        data.append(row)
    return data

def get_specimen_table_data():
    specimens = db.session.query(specimen).all()
    data = []
    for spe in specimens:
        row = [spe.specimen_id, spe.specimen_name]
        data.append(row)
    return data


def get_location_table_data():
    locations = db.session.query(location).all()
    data = []
    for spe in locations:
        row = [spe.location_id, spe.location_name]
        data.append(row)
    return data


def get_clinicalTest_table_data():
    clinicalTests = db.session.query(clinicalTest).all()
    data = []
    for spe in clinicalTests:
        row = [spe.clinicalTest_name]
        data.append(row)
    return data


def generate_id(data):
    id = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    process_data(data, id)
    return

def process_data(data, testId):
    # do something with the data
    defaultDate='0001-01-01 00:00:01'
    defaultTime='00:00:01'
    defaultStatus=0
    try:
        checkTestId = sample_stock.query.filter_by(sample_code=testId).first()
        if (checkTestId != None):
            generate_id(data)
        # 
        # 
        # Backend information
        # 
        # 
        sample_code = testId
        created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(created_date)
        created_by = current_user.username
        created_time='00:00:01'
        print(created_by)
        #
        #
        # Owner and Pet details
        #
        #
        sample_name = data['clinicname']
        sample_description = data['clinicBackground']
        # outcome_remarks = sum of details, like age, canine, owner
        no_of_test = data['no_of_test']
        customer_name = data['username']
        breed = data['breed']
        gender = data['gender']
        age = data['age']
        # 
        # 
        # Address details
        # 
        # 
        state=data['state']
        city=data['city']
        address=data['address']
        pincode=data['pincode']
        phno=data['phno']
        mobileno=phno
        email=data['email']
        # 
        # 
        # Test Details
        # 
        # 
        species = data['species']
        sample = data['sample']
        tests = request.form.getlist('test')
        print(tests)
        return
    except:
        return render_template('admin/usertest.html')


# --------------------------------
# CREATE FLASK ADMIN
# --------------------------------
admin = flask_admin.Admin(
    app,
    '',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# desc = data['address']
        # current_time = datetime.now()
        # clinic = data['clinicname']
        # loaction = data['state']
        # breed = data['breed']
        # sample = data['sample']
        # species = data['species']
        # age = data['age']
        # owner = data['username']
        # mobile = data['phno']
        # tests = data['testBox1']
        # print(testId)
        # # date=current_time,
        # testDb = test(id=testId, desc=desc, date=current_time,
        #               Clinic_ReferralName=clinic, Location=loaction, Breed=breed, Sample=sample, Species=species, Age=age, Owner=owner, Mobile=mobile, Tests=tests)
        # db.session.add(testDb)
        # db.session.commit()
        
        # paymentDb = testPayment(Testid=testId, Owner=owner,Clinic_ReferralName=clinic,Mobile=mobile)
        # db.session.add(paymentDb)
        # db.session.commit()
# visible for users and admin

# manage sample tab
# admin.add_view(testUserView(name="Create Order",
#                endpoint='usertest', category='Manage Orders'))
# admin.add_view(testAdminView(test, db.session,
#                name="Order History", category="Manage Orders"))
# admin.add_view(testView1(name="Legacy Sample Request",category='Manage Orders'))

# Sample Tracking tab
# admin.add_view(samplep(testPayment, db.session, name="Payment / Blue Dart"))


# # Invoice tab
# admin.add_view(invoice(name="Invoice1", category='Inovice'))

# # Report tab
# admin.add_view(report(name="Report1", category="Report"))

###########################################Admin vies for the database table#######################################################
# visible only for admin
admin.add_view(MyModelView(Profile, db.session))
admin.add_view(usernameview(Username, db.session))

# orders
admin.add_view(testUserView(name="Create Order",
               endpoint='usertest', category='Manage Orders'))
admin.add_view(sampleStock(sample_stock, db.session,
               name="Show Orders", category="Manage Orders"))

# payment
admin.add_view(paymentHistory(payment_history, db.session,
               name="Payment History"))

# invoice menu
admin.add_view(invoiceDetails(invoice_details, db.session,
               name="Invoice Details", category="Invoices"))
admin.add_view(invoices(invoice, db.session, name="Final Invoices",
               category="Invoices"))

# pickup and remarks
admin.add_view(pickupDetails(pickup_details, db.session,
               name="Pickup Details", category="Pickup / Remarks"))
admin.add_view(receiveDetails(receive_details, db.session,
               name="Received Details", category="Pickup / Remarks"))

# result
admin.add_view(analyticalTest(analytical_test, db.session,
               name="Result"))

# Function updates (type of test /  required samples)
admin.add_view(Allspecies(species, db.session, name="Species",
               category="Functionality"))
admin.add_view(Allspecimen(specimen, db.session,
               name="Specimen", category="Functionality"))
admin.add_view(locationViews(location, db.session,
               name="Location", category="Functionality"))
admin.add_view(clinicalTestViews(clinicalTest, db.session,
               name="Clinical Tests", category="Functionality"))

# admins and employees
admin.add_view(ourEmployee(employee, db.session,
               name="Employees"))




























##################################################################################################
# --------------------------------
# define a context processor for merging flask-admin's template context
#   into the flask-security views.
# --------------------------------
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

# --------------------------------
# Populate a small db with some example entries.
# --------------------------------


def build_sample_db():
    import string
    import random

    db.drop_all()
    db.create_all()

    with app.app_context():
        profile_user = Profile(name='user')
        profile_super_user = Profile(name='superuser')
        db.session.add(profile_user)
        db.session.add(profile_super_user)
        db.session.commit()

        test_user = user_datastore.create_user(
            first_name='Admin',
            username='admin',
            email='admin@test.com',
            password=encrypt_password('admin'),
            roles=[profile_super_user]
        )

        first_names = [
            'Anand', 'Preethi', 'Jon'
        ]
        last_names = [
            'Choudhary', 'P', 'Snow'
        ]

        for i in range(len(first_names)):
            tmp_email = "{}.{}@test.com".format(first_names[i].lower(),
                                                last_names[i].lower())
            tmp_pass = (str(first_names[i]+last_names[i])).lower()
            user_datastore.create_user(
                first_name=first_names[i],
                last_name=last_names[i],
                username=first_names[i].lower(),
                email=tmp_email,
                password=encrypt_password(tmp_pass),
                roles=[profile_user],
                confirmed_at=datetime.now()

            )
        db.session.commit()
    return


# --------------------------------
# MAIN APP
# --------------------------------
if __name__ == '__main__':
    # Delete the row with the specified primary key
    # db.add(test)
# Commit the changes
    # db.session.commit()
    # db.drop_all()
    # Build a sample db on the fly, if one does not exist yet.
    # db.create_all()
    ##    app_dir = os.path.realpath(os.path.dirname(__file__))
    ##    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    # if not os.path.exists(database_path):
    # build_sample_db()
    app.run()
