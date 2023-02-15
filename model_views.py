import datetime
import gettext
from pyexpat import model
from flask_admin.contrib import sqla
from flask_security import current_user
from flask import Flask, abort, redirect, render_template, url_for, request
from flask_admin import BaseView, expose
import sqlite3
import string
import random
from flask_admin.model import typefmt

from flask_sqlalchemy import SQLAlchemy
from markupsafe import Markup
# from app import generate_id,process_data

# from app import generate_id

app = Flask(__name__)


class MyModelView(sqla.ModelView):

    # @expose("/submit",methods=["POST"])
    # def submit(self):
    #     data=request.form
    #     print(data)
    #     print("Here I am")
    #     return redirect("/successForm")

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser'):
            return True
        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users
          when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


# @app.route("/successForm")
# def successForm():
#     print("Happy Stores")


class usernameview(MyModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser'):

            if current_user.has_role('superuser'):
                self.can_create = True
                self.can_edit = True
                self.can_delete = True
                self.can_export = True

            return True
        return False

    column_list = ('id', 'first_name', 'last_name', 'username',
                   'email', 'active', 'roles', 'confirmed_at')


# class testUserView(BaseView):

# def is_accessible(self):
# if not current_user.is_active or not current_user.is_authenticated:
# return False
# if current_user.has_role('superuser') or current_user.has_role('user'):
# return True
# return False
##
# @expose('/', methods=['GET', 'POST'])
# def index(self):
# data=request.form
# print(data)
# return self.render('admin/usertest.html')

    # column_display_pk = True
    # form_columns = ['id', 'desc']
    # column_searchable_list = ['desc']
    # column_filters = ['id']
    # can_create = True
    # can_edit = True
    # can_delete = False  # disable model deletion
    # can_view_details = True
    # page_size = 50  # pagination
    # create_modal = True
    # edit_modal = True
    # can_export = True


class testAdminView(MyModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            if current_user.has_role('user'):
                self.can_create = False
                self.can_edit = True
                self.can_delete = False
                self.can_export = True
            else:
                self.can_create = False
                self.can_edit = True
                self.can_delete = True
                self.can_export = True
            return True
        return False
    column_display_pk = True
    #form_columns = ['id', 'desc']
    column_searchable_list = ['id', 'Owner', 'Clinic_ReferralName', 'Mobile','Tests','Species','Location','date']
    column_filters = ['id', 'Owner', 'Clinic_ReferralName',
                      'Mobile', 'Tests', 'Species', 'Location', 'date']
    column_editable_list = ['desc']
    can_create = False
    can_edit = True

    can_view_details = True
    page_size = 50
    create_modal = True
    edit_modal = True
    can_export = True


class testView1(BaseView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    @expose('/')
    def index(self):
        return self.render('admin/legacysr.html')



class samplep(MyModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    
    column_display_pk = False
    column_default_sort = ('id', True)
    #form_columns = ['id', 'desc']
    column_searchable_list = ['Testid']
    column_filters = ['Testid', 'payment', 'Blue_Dart_booked']
    column_editable_list = ['payment', 'Blue_Dart_booked']
    can_create = False
    can_edit = True
    column_list = ('Testid', 'Owner', 'Clinic_ReferralName',
                   'Mobile', 'payment', 'Blue_Dart_booked')
    can_view_details = True
    page_size = 50
    create_modal = True
    edit_modal = True
    can_export = True


# invoice section

class invoice(BaseView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    @expose('/')
    def index(self):
        return self.render('admin/invoice.html')


# invoice section


class report(BaseView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    @expose('/')
    def index(self):
        return self.render('admin/report.html')

    @expose('/')
    def index(self):
        return self.render('admin/hi.html')
    
    
###############################################################################################
# 1
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
    column_searchable_list = ['invoice_id', 'test_name', 'amount',
                              'created_by', 'created_date', 'updated_by', 'updated_date']
    column_filters = ['invoice_id', 'test_name', 'amount',
                      'created_by', 'created_date', 'updated_by', 'updated_date']
    column_editable_list = ['test_name', 'amount']
    can_create = False
    can_edit = True
    column_list = ('invoice_id','test_name','amount','created_by','created_date','updated_by','updated_date')
    can_view_details = True
    page_size = 50
    create_modal = True
    edit_modal = True
    can_export = True


# 2
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
    column_searchable_list = ['invoice_id', 'payment_mode', 'total_amount', 'paid_amount',
                              'balance_amt', 'status', 'payment_collected_by', 'payment_collected_date']
    column_filters = ['invoice_id', 'payment_mode', 'total_amount', 'paid_amount',
                      'balance_amt', 'status', 'payment_collected_by', 'payment_collected_date']
    column_editable_list = ['payment_mode', 'total_amount', 'paid_amount',
                            'balance_amt', 'status', 'payment_collected_by', 'payment_collected_date']
    can_create = False
    can_edit = True
    column_list = ('invoice_id','payment_mode','total_amount','paid_amount','balance_amt','status','payment_collected_by','payment_collected_date')
    can_view_details = True
    page_size = 50
    create_modal = True
    edit_modal = True
    can_export = True

# 3
class pickupDetails(MyModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    column_display_pk = True
    column_default_sort = ('pickup_id', True)
    #form_columns = ['id', 'desc']
    column_searchable_list = ['pickup_id', 'sample_id',
                              'picked_by', 'picked_date', 'remarks', 'created_by']
    column_filters = ['pickup_id', 'sample_id',
                      'picked_by', 'picked_date', 'remarks', 'created_by']
    column_editable_list = ['picked_by', 'picked_date', 'remarks', 'created_by']
    can_create = False
    can_edit = True
    column_list = ('pickup_id','sample_id','picked_by','picked_date','remarks','created_by')
    can_view_details = True
    page_size = 50
    create_modal = True
    edit_modal = True
    can_export = True

# 4
class receiveDetails(MyModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    column_display_pk = True
    column_default_sort = ('receive_id', True)
    #form_columns = ['id', 'desc']
    column_searchable_list = ['receive_id', 'sample_id', 'received_by', 'received_date',
                              'remarks', 'created_by', 'vet_remarks', 'vetremarks_updated_by', 'vetremarks_updated_date']
    column_filters = ['receive_id', 'sample_id', 'received_by', 'received_date', 'remarks',
                      'created_by', 'vet_remarks', 'vetremarks_updated_by', 'vetremarks_updated_date']
    column_editable_list = ['remarks','vet_remarks']
    can_create = False
    can_edit = True
    column_list = ('receive_id','sample_id','received_by','received_date','remarks','created_by','vet_remarks','vetremarks_updated_by','vetremarks_updated_date')
    can_view_details = True
    page_size = 50
    create_modal = True
    edit_modal = True
    can_export = True

# 5
class sampleStock(MyModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    column_display_pk = True
    column_default_sort = ('sample_id', True)
    #form_columns = ['id', 'desc']
    column_searchable_list = ['sample_id','sample_code','sample_name','sample_description','outcome_remarks','noof_samples','customer_name','address','mobile_no','phone_no','email_id','created_by','created_time','counciler_status','customer_status','pickup_status','created_date','total_sample_price','price_unit','customer_accepted_by','customer_accepted_date','result_upload_status','pickup_accepted_status','receive_accepted_status','invoice_status','updated_by','updated_date','age','gender','pincode','location_id','bread','species_id','specimen_id']
    column_filters = ['sample_id','sample_code','sample_name','sample_description','outcome_remarks','noof_samples','customer_name','address','mobile_no','phone_no','email_id','created_by','created_time','counciler_status','customer_status','pickup_status','created_date','total_sample_price','price_unit','customer_accepted_by','customer_accepted_date','result_upload_status','pickup_accepted_status','receive_accepted_status','invoice_status','updated_by','updated_date','age','gender','pincode','location_id','bread','species_id','specimen_id']
    column_editable_list = ['sample_code','sample_name','sample_description','outcome_remarks','noof_samples','customer_name','address','mobile_no','phone_no','email_id','created_by','created_time','counciler_status','customer_status','pickup_status','created_date','total_sample_price','price_unit','customer_accepted_by','customer_accepted_date','result_upload_status','pickup_accepted_status','receive_accepted_status','invoice_status','updated_by','updated_date','age','gender','pincode','location_id','bread','species_id','specimen_id']
    can_create = False
    can_edit = True
    column_list = ('sample_id','sample_code','sample_name','sample_description','outcome_remarks','noof_samples','customer_name','address','mobile_no','phone_no','email_id','created_by','created_time','counciler_status','customer_status','pickup_status','created_date','total_sample_price','price_unit','customer_accepted_by','customer_accepted_date','result_upload_status','pickup_accepted_status','receive_accepted_status','invoice_status','updated_by','updated_date','age','gender','pincode','bread','location_id','species_id','specimen_id')
    can_view_details = True
    page_size = 50
    create_modal = True
    edit_modal = True
    can_export = True

# 6


class Allspecies(MyModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    column_display_pk = True
    column_default_sort = ('species_id', True)
    #form_columns = ['id', 'desc']
    column_searchable_list = ['species_id', 'species_name']
    column_filters = ['species_id', 'species_name']
    column_editable_list = [ 'species_name']
    can_create = True
    can_edit = True
    column_list = ('species_id','species_name')
    can_view_details = True
    page_size = 50
    create_modal = True
    edit_modal = True
    can_export = True

# 7


class Allspecimen(MyModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    column_display_pk = True
    column_default_sort = ('specimen_id', True)
    #form_columns = ['id', 'desc']
    column_searchable_list = ['specimen_id', 'specimen_name']
    column_filters = ['specimen_id', 'specimen_name']
    column_editable_list = [ 'specimen_name']
    can_create = True
    can_edit = True
    column_list = ('specimen_id', 'specimen_name')
    can_view_details = True
    page_size = 50
    create_modal = True
    edit_modal = True
    can_export = True

# 8
class analyticalTest(MyModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    column_display_pk = True
    column_default_sort = ('test_id', True)
    #form_columns = ['id', 'desc']
    column_searchable_list = ['test_id', 'status']
    column_filters = ['test_id', 'test_name', 'sample_id', 'outcome_result',
                      'test_outcome_created_by', 'test_outcome_created_date', 'status']
    column_editable_list = ['test_name', 'sample_id', 'outcome_result',
                            'test_outcome_created_by', 'test_outcome_created_date', 'status']
    can_create = False
    can_edit = True
    column_list = ('test_id','test_name','sample_id','outcome_result','test_outcome_created_by','test_outcome_created_date','status')
    can_view_details = True
    page_size = 50
    create_modal = True
    edit_modal = True
    can_export = True

# 9
class ourEmployee(MyModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser') or current_user.has_role('user'):
            return True
        return False

    column_display_pk = True
    column_default_sort = ('id', True)
    #form_columns = ['id', 'desc']
    column_searchable_list = ['id', 'emp_id', 'emp_name', 'password', 'designation',
                              'status', 'email_id', 'phone_no', 'address', 'location', 'usercode']
    column_filters = ['id', 'emp_id', 'emp_name', 'password', 'designation',
                      'status', 'email_id', 'phone_no', 'address', 'location', 'usercode']
    column_editable_list = [ 'emp_id', 'emp_name', 'password', 'designation',
                            'status', 'email_id', 'phone_no', 'address', 'location', 'usercode']
    can_create = False
    can_edit = True
    column_list = ('id','emp_id','emp_name','password','designation','status','email_id','phone_no','address','location','usercode')
    can_view_details = True
    page_size = 50
    create_modal = True
    edit_modal = True
    can_export = True

# 10
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
    column_searchable_list = ['invoice_id','sample_id','total','gst','gst_amount','created_by','created_date','updated_by','updated_date','paid_amount','bal_amt','status','others_amt','others_remarks','grand_total']
    column_filters = ['invoice_id','sample_id','total','gst','gst_amount','created_by','created_date','updated_by','updated_date','paid_amount','bal_amt','status','others_amt','others_remarks','grand_total']
    column_editable_list = ['sample_id','total','gst','gst_amount','created_by','created_date','updated_by','updated_date','paid_amount','bal_amt','status','others_amt','others_remarks','grand_total']
    can_create = False
    can_edit = True
    column_list = ('invoice_id','sample_id','total','gst','gst_amount','created_by','created_date','updated_by','updated_date','paid_amount','bal_amt','status','others_amt','others_remarks','grand_total')
    can_view_details = True
    page_size = 50
    create_modal = True
    edit_modal = True
    can_export = True
