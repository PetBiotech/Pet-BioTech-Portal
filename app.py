import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template
import json
from wtforms import SelectField
from flask_wtf import FlaskForm
import string
import random
from flask_admin.contrib.sqla import ModelView

from flask import Flask, jsonify, request, session
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from model_views import (
    finalTestTableView,MyModelView, usernameview, pickupDetails,
    receiveDetails, Allspecies, Allspecimen, ourEmployee, locationViews, clinicalTestViews
)
import forms
import os
from flask_admin.actions import action
from flask import (Flask, url_for, render_template,
                   abort, redirect
                   )
from flask_sqlalchemy import SQLAlchemy
from flask_security import (Security, SQLAlchemyUserDatastore,
                            UserMixin, RoleMixin, login_required, current_user, roles_required
                            )
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin import BaseView, expose, AdminIndexView
from flask_admin import helpers as admin_helpers
# from flask_admin.contrib import sqlasql
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

class sampleStock(MyModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False
    column_list = ('sample_id', 'sample_code', 'sample_name', 'sample_description', 'outcome_remarks', 'customer_name', 'address', 'mobile_no',
                       'email_id', 'age', 'gender', 'pincode', 'breed', 'location_name', 'species_name', 'specimen_name','created_date')
    column_searchable_list = ['sample_id', 'sample_code', 'sample_name', 'sample_description', 'outcome_remarks', 'noof_samples', 'customer_name', 'address', 'mobile_no',
                                  'email_id', 'age', 'gender', 'pincode', 'breed', 'location_name', 'species_name', 'specimen_name','created_date']
    column_filters = ['sample_id', 'sample_code', 'sample_name', 'sample_description', 'outcome_remarks', 'noof_samples', 'customer_name', 'address', 'mobile_no',
                          'email_id', 'age', 'gender', 'pincode', 'breed', 'location_name', 'species_name', 'specimen_name','created_date']
    column_editable_list = ['sample_code','sample_name', 'sample_description', 'outcome_remarks', 'noof_samples', 'customer_name',
                                'address', 'mobile_no', 'email_id', 'age', 'gender', 'pincode', 'location_name', 'breed', 'species_name', 'specimen_name']
    # other functions
    column_display_pk = True
    column_default_sort = ('sample_id', True)
    #form_columns = ['id', 'desc']
    # can_create = False
    can_edit = True
    can_view_details = True
    page_size = 50
    create_modal = True
    edit_modal = True
    can_export = True
    can_delete = True

    @property
    def can_create(self):
        return False
    form_columns = ('sample_code','sample_name', 'sample_description', 'outcome_remarks', 'noof_samples', 'customer_name', 'address',
                    'mobile_no', 'email_id', 'age', 'gender', 'pincode', 'location_id', 'breed', 'species_id', 'specimen_id')

    def on_model_delete(self, model):
        # Delete all related invoices_details
        try:
            find_invoice = invoice.query.filter_by(
                sample_id=model.sample_id).first()
            if (find_invoice != None):
                find_invoice_id = find_invoice.invoice_id
            related_invoices = db.session.query(invoice_details).filter_by(
                invoice_id=find_invoice_id).all()
            for invoiceRow in related_invoices:
                db.session.delete(invoiceRow)
            db.session.commit()
            # Delete all related payment data
            related_invoices = db.session.query(payment_history).filter_by(
                invoice_id=find_invoice_id).all()
            for invoiceRow in related_invoices:
                db.session.delete(invoiceRow)
            # Delete all related invoices
            related_invoices = db.session.query(
                invoice).filter_by(sample_id=model.sample_id).all()
            for invoiceRow in related_invoices:
                db.session.delete(invoiceRow)
            db.session.commit()
            # Delete all related analytical_test
            related_invoices = db.session.query(
                analytical_test).filter_by(sample_id=model.sample_id).all()
            for invoiceRow in related_invoices:
                db.session.delete(invoiceRow)
            # Delete all related picked up data
            related_invoices = db.session.query(
                pickup_details).filter_by(sample_id=model.sample_id).all()
            for invoiceRow in related_invoices:
                db.session.delete(invoiceRow)
            # Delete all related receive data
            related_invoices = db.session.query(
                receive_details).filter_by(sample_id=model.sample_id).all()
            for invoiceRow in related_invoices:
                db.session.delete(invoiceRow)
             # Delete all related summary data
            related_invoices = db.session.query(
                FinalTestView).filter_by(sample_id=model.sample_id).all()
            for invoiceRow in related_invoices:
                db.session.delete(invoiceRow)
            db.session.commit()
        except:
            print("Error")


# invoice update class

class invoiceDetails(MyModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    column_display_pk = False
    column_default_sort = ('invoice_id', True)
    #form_columns = ['id', 'desc']
    column_searchable_list = ['invoice_id', 'sample_id', 'test_name', 'amount',
                               'created_date', 'updated_by', 'updated_date']
    column_filters = ['invoice_id', 'sample_id', 'test_name', 'amount',
                       'created_date', 'updated_by', 'updated_date']
    can_create = True
    can_edit = True

    column_editable_list = ['test_name', 'amount']
    column_list = ('invoice_id','sample_id', 'test_name', 'amount',
                   'created_date', 'updated_by', 'updated_date')
    can_view_details = True
    page_size = 50
    create_modal = True
    edit_modal = False
    can_export = False
    # Remove invoice_id from form_columns
    form_columns = ['invoice_id','sample_id','test_name', 'amount']

    @property
    def can_delete(self):
        if (current_user.has_role('superuser')):
            return True
        return False

    # on edit

    def after_model_change(self, form, model, is_created):
        try:
            print(str(model.invoice_id))
        except TypeError:
            print("Failed to convert to string")
        if not is_created:
            invoice_id_edited = model.invoice_id
            related_invoices = db.session.query(invoice_details).filter_by(
                invoice_id=invoice_id_edited).all()
            amount = 0
            c_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            updated_date = datetime.strptime(c_date, '%Y-%m-%d %H:%M:%S')
            for invoiceRow in related_invoices:
                amount += invoiceRow.amount
                invoiceRow.updated_by = current_user.username
                invoiceRow.updated_date = updated_date
            invoiceDb = db.session.query(invoice).filter_by(
                invoice_id=invoice_id_edited).first()
            invoiceAmount = 0
            balanceAmount = 0
            if (invoiceDb is not None):
                invoiceAmount = amount+invoiceDb.gst_amount+invoiceDb.others_amt
                balanceAmount = invoiceAmount-invoiceDb.paid_amount
                invoiceDb.total = amount
                invoiceDb.grand_total = invoiceAmount
                invoiceDb.bal_amt = balanceAmount
                invoiceDb.updated_by = current_user.username
                invoiceDb.updated_date = updated_date
            else:
                print("An Error has occured")
            paymentDb = db.session.query(payment_history).filter_by(
                invoice_id=invoice_id_edited).first()
            if (paymentDb is not None):
                paymentDb.total_amount = invoiceAmount
                paymentDb.balance_amt = balanceAmount
            else:
                print("An Error has occured")
            db.session.commit()
            print("Data has been edited")
            
            # 
        if is_created:
            c_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            created_date = datetime.strptime(c_date, '%Y-%m-%d %H:%M:%S')
            test_id = analytical_test.query.order_by(
                analytical_test.test_id.desc()).first().test_id+1
            analytical_testDb = analytical_test(test_id=test_id, test_name=model.test_name, sample_id=model.sample_id,
                                                outcome_result='null', test_outcome_created_by='', test_outcome_created_date=created_date, status=0)
            db.session.add(analytical_testDb)
            sample_stock_details=db.session.query(sample_stock).filter_by(sample_id=model.sample_id).first()
            customer_name=''
            cityName=''
            customer_code=''
            # sample_stock_details.sample_code
            # sample_stock_details.customer_name
            if( sample_stock_details):
                customer_name = sample_stock_details.customer_name
                customer_code = sample_stock_details.sample_code
                if (sample_stock_details.location_id):
                    cityName=db.session.query(location).filter_by(location_id=sample_stock_details.location_id).first().location_name
            summaryTableDb = FinalTestView(test_id=test_id, test_name=model.test_name, sample_id=model.sample_id,
                                               outcome_result='null', client_name=customer_name, sample_code=customer_code, created_date=created_date, city_name=cityName)
            db.session.add(summaryTableDb)
            db.session.commit()
            
class invoices(MyModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    column_display_pk = True
    column_default_sort = ('invoice_id', True)
    #form_columns = ['id', 'desc']
    column_searchable_list = ['invoice_id', 'sample_id', 'total', 'gst', 'gst_amount', 'created_date',
                              'updated_by', 'updated_date', 'paid_amount', 'bal_amt',  'others_amt', 'others_remarks', 'grand_total']
    column_filters = ['invoice_id', 'sample_id', 'total', 'gst', 'gst_amount', 'created_date',
                      'updated_by', 'updated_date', 'paid_amount', 'bal_amt',  'others_amt', 'others_remarks', 'grand_total']
    column_editable_list = ['gst', 'gst_amount',
                            'paid_amount',  'others_amt', 'others_remarks']
    can_create = False
    can_edit = True
    column_list = ('invoice_id', 'sample_id', 'total', 'gst', 'gst_amount', 'others_amt', 'grand_total', 'paid_amount', 'bal_amt','created_date', 'updated_by',
                   'updated_date', 'others_remarks')
    can_view_details = True
    page_size = 50
    create_modal = True
    edit_modal = True
    can_export = True
    
    form_columns = ['gst', 'gst_amount','paid_amount',  'others_amt', 'others_remarks']

    def after_model_change(self, form, model, is_created):
        try:
            # print("after_model_change called", str(model))
            print(str(model.invoice_id))
        except TypeError:
            print("Failed to convert to string")
        if not is_created:
            invoice_id_edited = model.invoice_id
            c_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            updated_date = datetime.strptime(c_date, '%Y-%m-%d %H:%M:%S')
            invoiceDb = db.session.query(invoice).filter_by(
                invoice_id=invoice_id_edited).first()
            invoiceAmount = 0
            balanceAmount = 0
            paidAmount = 0
            if (invoiceDb is not None):
                invoiceAmount = invoiceDb.total+invoiceDb.gst_amount+invoiceDb.others_amt
                balanceAmount = invoiceAmount-invoiceDb.paid_amount
                paidAmount = invoiceDb.paid_amount
                invoiceDb.grand_total = invoiceAmount
                invoiceDb.bal_amt = balanceAmount
                invoiceDb.updated_by = current_user.username
                invoiceDb.updated_date = updated_date
            else:
                print("An Error has occured")
            paymentDb = db.session.query(payment_history).filter_by(
                invoice_id=invoice_id_edited).first()
            if (paymentDb is not None):
                paymentDb.total_amount = invoiceAmount
                paymentDb.paid_amount = paidAmount
                paymentDb.balance_amt = balanceAmount
            else:
                print("An Error has occured")
            db.session.commit()
            print("Data has been edited")
            # refresh code
            pyautogui.hotkey('f5')
        if is_created:
            print("New Data has been added")

class paymentHistory(MyModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    column_display_pk = False
    column_default_sort = ('invoice_id', True)
    #form_columns = ['id', 'desc']
    column_searchable_list = ['invoice_id', 'sample_id', 'payment_mode', 'total_amount', 'paid_amount',
                              'balance_amt', 'status', 'payment_collected_by', 'payment_collected_date']
    column_filters = ['invoice_id', 'sample_id', 'payment_mode', 'total_amount', 'paid_amount',
                      'balance_amt', 'status', 'payment_collected_by', 'payment_collected_date']
    column_editable_list = ['payment_mode', 'status']
    can_create = False
    can_edit = True
    column_list = ('invoice_id','sample_id', 'payment_mode', 'total_amount', 'paid_amount',
                   'balance_amt', 'status', 'payment_collected_by', 'payment_collected_date')
    can_view_details = True
    page_size = 50
    create_modal = True
    edit_modal = True
    can_export = True

    form_columns = ['payment_mode', 'status']
    
    @property
    def can_delete(self):
        if (current_user.has_role('superuser')):
            return True
        return False
    
    def after_model_change(self, form, model, is_created):
        if not is_created:
            invoice_id_edited = model.invoice_id
            c_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            updated_date = datetime.strptime(c_date, '%Y-%m-%d %H:%M:%S')
            paymentDb = db.session.query(payment_history).filter_by(
                invoice_id=invoice_id_edited).first()
            if (paymentDb is not None):
                if(paymentDb.status != 0):
                    paymentDb.payment_collected_by = current_user.username
                    paymentDb.payment_collected_date = updated_date
            else:
                print("An Error has occured")
            db.session.commit()
            print("Data has been edited")
            # refresh code
            pyautogui.hotkey('f5')
        if is_created:
            print("New Data has been added")
            
            
class analyticalTest(MyModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    @action('generate_result', 'Generate Resultsheet', 'Are you sure you want to generate a result sheet?')
    @expose('/generate-result', methods=['POST'])
    def generate_result(self, ids):
        # Get the selected records
        records = analytical_test.query.filter(
            analytical_test.test_id.in_(ids)).all()

        # Get the data for the selected records
        selected_ids = [record.sample_id for record in records]

        data = analytical_test.query.filter(
            analytical_test.sample_id.in_(selected_ids)).all()
        dataCount=analytical_test.query.filter(
            analytical_test.sample_id.in_(selected_ids)).count()
        # Create a list of dictionaries with the necessary attributes
        form_data = []
        showRemarks="False"
        allRemarks = [[]]*dataCount
        t=0
        for d in data:
            sample = sample_stock.query.get(d.sample_id)
            allRemarks[t]=d.remarks  
            t+=1          
            form_data.append({
                'sample_id': sample.sample_id,
                'remarks': d.remarks,
                'test_name': d.test_name,
                'outcome_result': d.outcome_result,
            })
        for i in allRemarks:
            if(i):
                showRemarks="True"
        remarkData=({
            'showRemark':showRemarks,
            'remarks':allRemarks
        })
        r_data = []
        row_data = sample_stock.query.filter(
            sample_stock.sample_id.in_(selected_ids)).all()
        for r in row_data:
            trimDate=str(r.created_date)[:10]
            speciesName='Unavailable'
            speciesNameCheck=db.session.query(species).filter_by(species_id=r.species_id).first()
            if (speciesNameCheck != None):
                speciesName = speciesNameCheck.species_name
            email = r.email_id
            phone = r.phone_no
            customerName=r.customer_name
            petName=r.sample_name
            petAge=r.age
            if (email == '' or email == 'NA@NA.com' or email==None):
                email = 'Unavailable'
            if (str(phone) == '' or phone==None):
                phone = 'Unavailable'
            if (speciesName=='' or speciesName==None):
                speciesName = 'Unavailable'
            if (customerName == '' or customerName == None):
                customerName = 'Unavailable'
            if (petName == '' or petName == None):
                petName = 'Unavailable'
            if (petAge == '' or petAge == None):
                petAge = 'Unavailable'
            r_data.append({
                'sample_id':selected_ids,
                'date': trimDate,
                'customer_name': customerName,
                'age': petAge,
                'email': email,
                'phno': phone,
                'pet_name': petName,
                'species': speciesName})
        # Render the template with the form data
        return self.render('my_action.html', data=form_data, r_data=r_data, remarkData=remarkData)

    column_display_pk = True
    column_default_sort = ('test_id', True)
    #form_columns = ['id', 'desc']
    column_searchable_list = ['sample_id',
                              'status', 'outcome_result', 'test_name']
    column_filters = ['test_id', 'test_name', 'sample_id', 'outcome_result',
                      'remarks', 'status']
    column_editable_list = ['test_name', 'outcome_result', 'remarks','status']
    can_create = True
    can_edit = True
    column_list = ('test_id', 'sample_id', 'test_name', 'outcome_result','remarks')
    can_view_details = True
    page_size = 50
    create_modal = True
    edit_modal = True
    can_export = True

    def after_model_change(self, form, model, is_created):
        if not is_created:
            test_id = model.test_id
            c_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            updated_date = datetime.strptime(c_date, '%Y-%m-%d %H:%M:%S')
            resultDb = db.session.query(
                analytical_test).filter_by(test_id=test_id).first()
            if (resultDb is not None):
                if(resultDb.outcome_result=='Positive' or resultDb.outcome_result=='positive' or resultDb.outcome_result=='Pos' or resultDb.outcome_result=='pos'):
                    resultDb.status=1
                else:
                    resultDb.status=0
                summaryTest = db.session.query(
                    FinalTestView).filter_by(test_id=test_id).first()
                summaryTest.outcome_result = resultDb.outcome_result
                resultDb.test_outcome_created_by = current_user.username
                resultDb.test_outcome_created_date = updated_date
            else:
                print("An Error has occured")
            db.session.commit()
            print("Data has been edited")
            # refresh code
            pyautogui.hotkey('f5')
        if is_created:
            print("New Data has been added")


######################################################################################################


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


# --------------------------------
# MODELS
# --------------------------------


# Db for the test


class invoice_details(db.Model):
    invoice_details_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    invoice_id = db.Column(db.Integer, nullable=True)
    sample_id = db.Column(db.Integer, nullable=True)
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
    sample_id = db.Column(db.Integer, nullable=True)
    payment_mode = db.Column(db.String(200), nullable=True)
    total_amount = db.Column(db.Integer, nullable=True)
    paid_amount = db.Column(db.Integer, nullable=True)
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
    created_by = db.Column(db.String(100), nullable=True)
    vet_remarks = db.Column(db.String(500), nullable=True)
    vetremarks_updated_by = db.Column(db.String(100), nullable=True)
    vetremarks_updated_date = db.Column(db.DateTime(timezone=True),
                                        default=datetime.utcnow, nullable=True)

    def __str__(self):
        return self.receive_id


class sample_stock(db.Model):
    sample_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    sample_code = db.Column(db.String(100), nullable=True)
    sample_name = db.Column(db.String(100), nullable=True)
    sample_description = db.Column(db.String(1000), nullable=True)
    outcome_remarks = db.Column(db.String(1000), nullable=True)
    noof_samples = db.Column(db.Integer, nullable=True)
    customer_name = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(1000), nullable=True)
    mobile_no = db.Column(db.Integer, nullable=True)
    phone_no = db.Column(db.Integer, nullable=True)
    email_id = db.Column(db.String(100), nullable=True)
    created_by = db.Column(db.String(100), nullable=True)
    created_time = db.Column(db.Time(timezone=True),
                             default=datetime.utcnow, nullable=True)
    counciler_status = db.Column(db.Integer, nullable=True)
    customer_status = db.Column(db.Integer, nullable=True)
    pickup_status = db.Column(db.Integer, nullable=True)
    created_date = db.Column(db.DateTime(timezone=True),
                             default=datetime.utcnow, nullable=True)
    total_sample_price = db.Column(db.Integer, nullable=True)
    price_unit = db.Column(db.Integer, nullable=True)
    customer_accepted_by = db.Column(db.String(100), nullable=True)
    customer_accepted_date = db.Column(db.DateTime(timezone=True),
                                       default=datetime.utcnow, nullable=True)
    result_upload_status = db.Column(db.Integer, nullable=True)
    pickup_accepted_status = db.Column(db.Integer, nullable=True)
    receive_accepted_status = db.Column(db.Integer, nullable=True)
    invoice_status = db.Column(db.Integer, nullable=True)
    updated_by = db.Column(db.String(100), nullable=True)
    updated_date = db.Column(db.DateTime(timezone=True),
                             default=datetime.utcnow, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(25), nullable=True)
    pincode = db.Column(db.Integer, nullable=True)
    location_id = db.Column(db.Integer, nullable=True)
    breed = db.Column(db.String(100), nullable=True)
    # gender = db.Column(db.String(100), nullable=True)
    species_id = db.Column(db.Integer, nullable=True)
    specimen_id = db.Column(db.Integer, nullable=True)
    
    species_name=db.Column(db.String(100),nullable=True)
    specimen_name=db.Column(db.String(1000),nullable=True)
    location_name=db.Column(db.String(100),nullable=True)
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
    remarks=db.Column(db.String(1000),nullable=True)


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


class FinalTestView(db.Model):
    __tablename__ = 'FinalTestView'
    test_id = db.Column(db.Integer, db.ForeignKey(
        'analytical_test.test_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey(
        'analytical_test.sample_id'), unique=False)
    test_name = db.Column(db.String(250), nullable=True)
    created_date = db.Column(db.DateTime, nullable=True)
    outcome_result = db.Column(db.String(100), nullable=True)
    city_name = db.Column(db.String(100), nullable=True)
    client_name = db.Column(db.String(250), nullable=True)
    sample_code = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<FinalTestView(test_id={self.test_id}, sample_id={self.sample_id}, test_name='{self.test_name}', created_date='{self.created_date}', outcome_result='{self.outcome_result}', city_name='{self.city_name}', client_name='{self.client_name}')>"

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

class hometab(AdminIndexView):
    @expose('/', methods=["GET","POST"])
    def home(self):
        dashBoardCountData=[]
        totalTests = analytical_test.query.count()
        totalOrders= sample_stock.query.count()
        positiveResults = analytical_test.query.filter_by(outcome_result="Positive").count()
        positiveResults += analytical_test.query.filter_by(outcome_result="positive").count()
        dashBoardCountData={
            'totalTests':totalTests,
            'totalOrders':totalOrders,
            'positiveResults':positiveResults
        }
        location_data = db.session.query(
            FinalTestView.city_name,
            db.func.count(
                db.case(
                    (FinalTestView.outcome_result == 'Positive', 1),
                    (FinalTestView.outcome_result == 'Negative', None),
                    else_=None
                )
            ).label('positive_tests'),
            db.func.count(
                db.case(
                    (FinalTestView.outcome_result == 'Negative', 1),
                    (FinalTestView.outcome_result == 'Positive', None),
                    else_=None
                )
            ).label('negative_tests'),
            db.func.count(
                db.case(
                    (FinalTestView.outcome_result == 'null', 1),
                    else_=None
                )
            ).label('null_tests'),
            db.func.count(FinalTestView.outcome_result).label('total_outcome_results')
        ).group_by(FinalTestView.city_name).order_by(db.desc('total_outcome_results')).all()

        orderDateDataRows = db.session.query(
            db.func.DATE(sample_stock.created_date),
            db.func.count()
        ).filter(
            sample_stock.created_date >= '2018-01-01 00:00:01'
        ).group_by(
            db.func.DATE(sample_stock.created_date)
        ).all()

        orderDateData = [tuple(row) for row in orderDateDataRows]
        return self.render(
            'admin/index.html',
            dashBoardCountData=dashBoardCountData,
            location_data=location_data,
            orderDateData=orderDateData
        )
    
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
            # print(data)
            # generate_id(data)
            process_data(data)
            return jsonify({'success': True})
        # return self.render('admin/usertest.html')
        speciesData = get_species_table_data()
        specimenData = get_specimen_table_data()
        locationData = get_location_table_data()
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


# def generate_id(data):
#     id = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
#     process_data(data, id)
#     return


def process_data(data):
    # do something with the data
    c_date = '0001-01-01 00:00:01'
    defaultDate = datetime.strptime(c_date, '%Y-%m-%d %H:%M:%S')
    defaultStatus = 0
    try:
        # checkTestId = sample_stock.query.filter_by(sample_code=testId).first()
        # if (checkTestId != None):
        #     generate_id(data)
        #
        #
        # Backend information
        #
        #
        c_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        created_date = datetime.strptime(c_date, '%Y-%m-%d %H:%M:%S')
        created_by = current_user.username
        # time_str = '00:00:01'
        time_str = datetime.now()
        new_time_str = time_str.strftime('%H:%M:%S')
        created_time = datetime.strptime(new_time_str, '%H:%M:%S').time()
        # print("***********************")
        # print(created_time)
        # print(created_date)
        #
        #
        # Owner and Pet details
        #
        #
        sample_code = data['sampleCode']
        sample_name = data['clinicname']
        sample_description = data['clinicBackground']
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
        state = data['state']
        city = data['city']
        OtherCity = data['otherCity']
        if(OtherCity==''):
            OtherCity='None'
        if(city=='Other' and OtherCity!='None'):
            otherOptionBelow = location.query.order_by(location.location_id.desc()).first()
            otherOptionBelow.location_name=OtherCity
            newCity = location(location_name='Other')
            db.session.add(newCity)
            db.session.commit()
            city=OtherCity
        city_code = location.query.order_by(location.location_id.desc()).first()
        address = data['address']
        pincode = data['pincode']
        phno = data['phno']
        mobileno = phno
        email = data['email']
        if(city != '' ):
            city_code=db.session.query(location).filter_by(location_name=city).first().location_id
        address += "\n"+city+" - "+pincode+"\n"+state
        #
        #
        # Test Details
        #
        #
        species_name = data['species']
        OtherSpecies=data['otherSpecies']
        if(OtherSpecies==''):
            OtherSpecies = 'None'
        if (species_name == 'Other' and OtherSpecies != 'None'):
            otherOptionBelow = species.query.order_by(species.species_id.desc()).first()
            otherOptionBelow.species_name = OtherSpecies
            newSpecies= species(species_name='Other')
            db.session.add(newSpecies)
            db.session.commit()
            species_name = OtherSpecies
        species_id = species.query.order_by(species.species_id.desc()).first()
        if (species_name != ''):
            species_id = db.session.query(species).filter_by(species_name=species_name).first().species_id
        #
        # 
        # Sample
        sample = data['sample']
        OtherSample=data['otherSpecimen']
        if(OtherSample==''):
            OtherSample = 'None'
        if (sample == 'Other' and OtherSample!='None'):
            otherOptionBelow = specimen.query.order_by(specimen.specimen_id.desc()).first()
            otherOptionBelow.specimen_name = OtherSample
            newSpecimen = specimen(specimen_name='Other')
            db.session.add(newSpecimen)
            db.session.commit()
            sample = OtherSample
        specimen_id = specimen.query.order_by(specimen.specimen_id.desc()).first()
        if (sample != ''):
            specimen_id = db.session.query(specimen).filter_by(specimen_name=sample).first().specimen_id
        tests = request.form.getlist('selectTest')
        outcome_remarks = ''
        i = 1
        for test in tests:
            index = str(i)
            outcome_remarks += index + "."+test+'\n'
            i += 1
        #
        #
        # Creation of Id's
        #
        #
        sample_id = sample_stock.query.order_by(
            sample_stock.sample_id.desc()).first().sample_id+1
        invoice_id = invoice.query.order_by(
            invoice.invoice_id.desc()).first().invoice_id+1
        test_id = analytical_test.query.order_by(
            analytical_test.test_id.desc()).first().test_id
        sample_code = sample_code.upper()+"/" + str(created_date)[2:4] + "/" + str(created_date)[5:7]+"/"+str(sample_id)
        #
        #
        # Storing in Database
        #
        #
        sampleStockDb = sample_stock(sample_id=sample_id, sample_code=sample_code, sample_name=sample_name, sample_description=sample_description, outcome_remarks=outcome_remarks, noof_samples=no_of_test, customer_name=customer_name, address=address, mobile_no=mobileno, phone_no=phno, email_id=email, created_by=created_by, created_time=created_time, counciler_status=defaultStatus, customer_status=defaultStatus,
                                     pickup_status=defaultStatus, created_date=created_date, total_sample_price='', price_unit='', customer_accepted_by='', customer_accepted_date=defaultDate, result_upload_status=0, pickup_accepted_status=0, receive_accepted_status=0, invoice_status=0, updated_by='', updated_date=defaultDate, age=age, gender=gender, pincode=pincode, location_id=city_code, breed=breed, species_id=species_id, specimen_id=specimen_id, species_name=species_name, specimen_name=sample, location_name=city)
        db.session.add(sampleStockDb)
        invoiceDb = invoice(invoice_id=invoice_id, sample_id=sample_id, total=0, gst=0, gst_amount=0, created_by=created_by, created_date=created_date,
                            updated_by=0, updated_date=defaultDate, paid_amount=0, bal_amt=0, status=0, others_amt=0, others_remarks='', grand_total=0)
        db.session.add(invoiceDb)
        for test in tests:
            test_id += 1
            invoice_detailsDb = invoice_details(invoice_id=invoice_id, test_name=test, amount=0,
                                                created_by=created_by, created_date=created_date, updated_by='', updated_date=defaultDate,sample_id=sample_id)
            db.session.add(invoice_detailsDb)
            analytical_testDb = analytical_test(test_id=test_id, test_name=test, sample_id=sample_id,
                                                outcome_result='null', test_outcome_created_by='', test_outcome_created_date=defaultDate, status=0)
            db.session.add(analytical_testDb)
            summaryTableDb = FinalTestView(test_id=test_id, test_name=test, sample_id=sample_id,
                                           outcome_result='null', client_name=customer_name, sample_code=sample_code, created_date=created_date, city_name=city)
            db.session.add(summaryTableDb)
        pickupDb = pickup_details(sample_id=sample_id, picked_by='', picked_date=defaultDate,
                                  remarks='', created_by=created_by)
        db.session.add(pickupDb)
        receiveDb = receive_details(sample_id=sample_id, received_by='', received_date=defaultDate,
                                    remarks='', created_by=created_by, vet_remarks='', vetremarks_updated_by='', vetremarks_updated_date=defaultDate)
        db.session.add(receiveDb)
        paymentDb = payment_history(invoice_id=invoice_id, payment_mode='', total_amount='', paid_amount='',
                                    balance_amt='', status=0, payment_collected_by='', payment_collected_date=defaultDate,sample_id=sample_id)
        db.session.add(paymentDb)
        db.session.commit()
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
    index_view=hometab(name="Dashboard"),
)


    


########################################### Admin vies for the database table#######################################################
# orders
admin.add_view(testUserView(name="Create Order",
               endpoint='usertest', menu_icon_type='glyph', menu_icon_value='glyphicon glyphicon-plus'))
admin.add_view(sampleStock(sample_stock, db.session,
               name="Show Orders",menu_icon_type='glyph', menu_icon_value='glyphicon glyphicon-search'))

# invoice menu
admin.add_view(invoiceDetails(invoice_details, db.session,
               name="Create Invoice", category="Invoice"))
admin.add_view(invoices(invoice, db.session, name="Final Invoices",
               category="Invoice"))

# payment, pickup and receive
admin.add_view(paymentHistory(payment_history, db.session,
               name="Payment History", category="Others"))
admin.add_view(pickupDetails(pickup_details, db.session,
               name="Pickup Details", category="Others"))
admin.add_view(receiveDetails(receive_details, db.session,
               name="Received Details", category="Others"))

# result
admin.add_view(analyticalTest(analytical_test, db.session,
               name="Result",menu_icon_type='glyph', menu_icon_value='glyphicon glyphicon-list-alt'))

# Function updates (type of test /  required samples)
admin.add_view(Allspecies(species, db.session, name="Species",
               category="Functionality"))
admin.add_view(Allspecimen(specimen, db.session,
               name="Specimen", category="Functionality"))
admin.add_view(locationViews(location, db.session,
               name="Location", category="Functionality"))
admin.add_view(clinicalTestViews(clinicalTest, db.session,
               name="Clinical Tests", category="Functionality"))

# final table
admin.add_view(finalTestTableView(FinalTestView, db.session,
               name="Summary",menu_icon_type='glyph', menu_icon_value='glyphicon glyphicon-plus'))

# admins and employees
admin.add_view(MyModelView(Profile, db.session,
               name="Profiles", category="Employees"))
admin.add_view(usernameview(Username, db.session,
               name="New Employees", category="Employees"))
admin.add_view(ourEmployee(employee, db.session,
               name="Old Employees", category="Employees"))


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

def update_sample_id():
    resultTest=db.session.query(invoice).all()
    for eachTest in resultTest:
        if(eachTest.invoice_id):
            print(eachTest.sample_id)
            in_det=db.session.query(payment_history).filter_by(invoice_id=eachTest.invoice_id).all()
            for iDetails in in_det:
                iDetails.sample_id=eachTest.sample_id
    db.session.commit()


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
    db.create_all()
    ##    app_dir = os.path.realpath(os.path.dirname(__file__))
    ##    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    # if not os.path.exists(database_path):
    build_sample_db()
    # sql = "ALTER TABLE invoice ADD CONSTRAINT fk_invoice_sample FOREIGN KEY (sample_id) REFERENCES sample_stock(sample_id) ON DELETE CASCADE;"
    # db.session.execute(sql)
    # db.session.commit()
    app.run()
