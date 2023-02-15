import string
import random
from flask_admin.contrib.sqla import ModelView
#from flask_restful import Api, Resource
from flask import Flask, request
from sqlalchemy import ForeignKey
from model_views import (
    testAdminView, MyModelView, usernameview, testView1, samplep, invoice, report, invoiceDetails, paymentHistory,
    pickupDetails, receiveDetails, sampleStock, Allspecies, Allspecimen, analyticalTest, ourEmployee, invoices
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


class test(db.Model):
    id = db.Column(db.String, primary_key=True)
    desc = db.Column(db.String(50))
    date = db.Column(db.DateTime(timezone=True),
                     default=datetime.utcnow)
    Clinic_ReferralName = db.Column(db.String(50))
    Location = db.Column(db.String(50))
    Breed = db.Column(db.String(50))
    Sample = db.Column(db.String(50))
    Species = db.Column(db.String(50))
    Age = db.Column(db.Integer)
    Owner = db.Column(db.String(50))
    Mobile = db.Column(db.String(50))
    Tests = db.Column(db.String(50))

    def __str__(self):
        return self.desc
    
class testPayment(db.Model):
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    Testid = db.Column(db.String, ForeignKey("test.id"))
    Owner = db.Column(db.String(50))
    Clinic_ReferralName = db.Column(db.String(50))
    Mobile = db.Column(db.String(50))
    payment=db.Column(db.Boolean,default=False)
    Blue_Dart_booked = db.Column(db.Boolean, default=False)
    def __str__(self):
        return self.id

class usertest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc = db.Column(db.String(50))


# Db for the test


class invoice_details(db.Model):
    invoice_details_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    invoice_id = db.Column(db.Integer)
    test_name = db.Column(db.String(200))
    amount = db.Column(db.Integer)
    created_by = db.Column(db.String(100))
    created_date = db.Column(db.DateTime(timezone=True),
                             default=datetime.utcnow)
    updated_by = db.Column(db.String(100))
    updated_date = db.Column(db.DateTime(timezone=True),
                             default=datetime.utcnow)

    def __str__(self):
        return self.invoice_id
    
    
class payment_history(db.Model):
    payment_history_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    invoice_id = db.Column(db.Integer)
    payment_mode = db.Column(db.String(200))
    total_amount = db.Column(db.Integer)
    paid_amount=db.Column(db.Integer)
    balance_amt = db.Column(db.Integer)
    status = db.Column(db.Integer)
    payment_collected_by = db.Column(db.String(100))
    payment_collected_date = db.Column(db.DateTime(timezone=True),
                             default=datetime.utcnow)
    def __str__(self):
        return self.invoice_id
    
    
class pickup_details(db.Model):
    pickup_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    sample_id = db.Column(db.Integer)
    picked_by = db.Column(db.String(100))
    picked_date = db.Column(db.DateTime(timezone=True),
                             default=datetime.utcnow)
    remarks = db.Column(db.String(500))
    created_by = db.Column(db.String(100))

    def __str__(self):
        return self.sample_id
    

class receive_details(db.Model):
    receive_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    sample_id = db.Column(db.Integer)
    received_by = db.Column(db.String(100))
    received_date = db.Column(db.DateTime(timezone=True),
                                       default=datetime.utcnow)
    remarks = db.Column(db.String(500))
    created_by=db.Column(db.String(100))
    vet_remarks = db.Column(db.String(500))
    vetremarks_updated_by = db.Column(db.String(100))
    vetremarks_updated_date = db.Column(db.DateTime(timezone=True),
                                       default=datetime.utcnow)

    def __str__(self):
        return self.sample_id
    
    
class sample_stock(db.Model):
    sample_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    sample_code = db.Column(db.String(20))
    sample_name=db.Column(db.String(100))
    sample_description = db.Column(db.String(1000))
    outcome_remarks = db.Column(db.String(1000))
    noof_samples = db.Column(db.Integer)
    customer_name = db.Column(db.String(100))
    address = db.Column(db.String(1000))
    mobile_no=db.Column(db.Integer)
    phone_no=db.Column(db.Integer)
    email_id=db.Column(db.String(100))
    created_by = db.Column(db.String(100))
    created_time = db.Column(db.Time(timezone=True),
                             default=datetime.utcnow)
    counciler_status=db.Column(db.Integer)
    customer_status=db.Column(db.Integer)
    pickup_status = db.Column(db.Integer)
    created_date = db.Column(db.DateTime(timezone=True),
                              default=datetime.utcnow)
    total_sample_price=db.Column(db.Integer)
    price_unit = db.Column(db.Integer)
    customer_accepted_by = db.Column(db.String(100))
    customer_accepted_date = db.Column(db.DateTime(timezone=True),
                                        default=datetime.utcnow)
    result_upload_status=db.Column(db.Integer)
    pickup_accepted_status = db.Column(db.Integer)
    receive_accepted_status = db.Column(db.Integer)
    invoice_status = db.Column(db.Integer)
    updated_by = db.Column(db.String(100))
    updated_date = db.Column(db.DateTime(timezone=True),
                                        default=datetime.utcnow)
    age = db.Column(db.Integer)
    gender=db.Column(db.String(25))
    pincode = db.Column(db.Integer)
    location_id = db.Column(db.Integer)
    bread=db.Column(db.String(100))
    # gender = db.Column(db.String(100))
    species_id = db.Column(db.Integer)
    specimen_id = db.Column(db.Integer)

    def __str__(self):
        return self.sample_id
    

class species(db.Model):
    species_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    species_name = db.Column(db.String(100))

    def __str__(self):
        return self.species_id
    
    
class specimen(db.Model):
    specimen_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    specimen_name = db.Column(db.String(500))

    def __str__(self):
        return self.species_id
    
    
class analytical_test(db.Model):
    test_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    test_name = db.Column(db.String(200))
    sample_id = db.Column(db.Integer)
    outcome_result = db.Column(db.String(100))
    test_outcome_created_by = db.Column(db.String(100))
    test_outcome_created_date = db.Column(db.DateTime(timezone=True),
                                       default=datetime.utcnow)
    status = db.Column(db.Integer)
    
    def __str__(self):
        return self.sample_id   
    

class employee(db.Model):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    emp_id = db.Column(db.Integer)
    emp_name = db.Column(db.String(200))
    password = db.Column(db.String(200))
    designation = db.Column(db.String(200))
    status = db.Column(db.Integer)
    email_id = db.Column(db.String(200))
    phone_no = db.Column(db.Integer)
    address = db.Column(db.String(500))
    location = db.Column(db.Integer)
    usercode = db.Column(db.String(20))

    def __str__(self):
        return self.emp_id
    
    
class invoice(db.Model):
    invoice_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    sample_id = db.Column(db.Integer)
    total = db.Column(db.Integer)
    gst = db.Column(db.Integer)
    gst_amount = db.Column(db.Integer)
    created_by = db.Column(db.String(100))
    created_date = db.Column(db.DateTime(timezone=True),
                              default=datetime.utcnow)
    updated_by = db.Column(db.String(100))
    updated_date = db.Column(db.DateTime(timezone=True),
                             default=datetime.utcnow)
    paid_amount = db.Column(db.Integer)
    bal_amt = db.Column(db.Integer)
    status = db.Column(db.Integer)
    others_amt = db.Column(db.Integer)
    others_remarks = db.Column(db.String(500))
    grand_total = db.Column(db.Integer)

    def __str__(self):
        return self.sample_id
    
    
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
        return self.render('admin/usertest.html')
    

def process_data(data, testId):
    # do something with the data
    try:
        checkTestId = test.query.filter_by(id=testId).first()
        if (checkTestId != None):
            generate_id(data)
        desc = data['address']
        current_time = datetime.now()
        clinic = data['clinicname']
        loaction = data['state']
        breed = data['breed']
        sample = data['sample']
        species = data['species']
        age = data['age']
        owner = data['username']
        mobile = data['phno']
        tests = data['testBox1']
        print(testId)
        # date=current_time,
        testDb = test(id=testId, desc=desc, date=current_time,
                      Clinic_ReferralName=clinic, Location=loaction, Breed=breed, Sample=sample, Species=species, Age=age, Owner=owner, Mobile=mobile, Tests=tests)
        db.session.add(testDb)
        db.session.commit()
        
        paymentDb = testPayment(Testid=testId, Owner=owner,Clinic_ReferralName=clinic,Mobile=mobile)
        db.session.add(paymentDb)
        db.session.commit()
        return
    except:
        return render_template('admin/usertest.html')


def generate_id(data):
    id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    process_data(data, id)
    return


# --------------------------------
# CREATE FLASK ADMIN
# --------------------------------
admin = flask_admin.Admin(
    app,
    '',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# visible only for admin
admin.add_view(MyModelView(Profile, db.session))
admin.add_view(usernameview(Username, db.session))

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


#
#
#
#


##
##
# def generate_id(data):
##    id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
##    process_data(data, id)
# return
###
#
#
#
#
###########################################Admin vies for the database table#######################################################

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
admin.add_view(invoices(invoice, db.session, name="Invoices",
               category="Final Invoices"))

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
               name="specimen", category="Functionality"))

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
    # Build a sample db on the fly, if one does not exist yet.
    # db.create_all()
    ##    app_dir = os.path.realpath(os.path.dirname(__file__))
    ##    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    # if not os.path.exists(database_path):
    # build_sample_db()

    app.run()
