from django.conf.urls import patterns, include, url
from COBApp import views
from django.contrib.auth import authenticate, login


urlpatterns = patterns('',
	# the index login page 
	url(r'^$', views.index, name='index'),
	# dashboard for the admin 
	url(r'^dashboard/$', views.dashboard, name='dashboard'),

	# new expense form for the user/admin to enter expenses
	url(r'^expenseform/$', views.expenseform, name='expenseform'), #add new entry of image and caption
	# getting the spending for the displaying the graph (through an AJAX request)
	url(r'^getSpending/(?P<club_id>\d+)/$', views.getSpending, name='getSpending'),

	# temporary login URL, leads to authentication page
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'COBApp/login.html'}, name="login"),

	# temporary logout URL
	url(r'^logout/$', 'COBApp.views.logout_view', name='logout'),

	# onlick submit on Expense Form
	url(r'^submitExpenseForm/$', views.submitExpenseForm, name='submitExpenseForm'),

	# showing the clubs' dashboards for the admin
	url(r'^showDashboard/(?P<clubID>\w+)/$', views.showDashboard, name='showDashboard'),

	# showing the history for the clubs
	url(r'^history/(?P<clubID>\d+)/$', views.history, name='history'),

	# decode for loading the logos from the database
	url(r'^decode/(?P<clubID>\d+)/$', views.decode, name='decode'),

	# generates a PDF with the transactions 
	url(r'^generatePDF/(?P<clubID>\d+)/$', views.generatePDF, name='generatePDF'),

	# transaction details 
	url(r'^details/(?P<transID>\d+)/$', views.trans, name='trans'),

	# decoding the receipt
	url(r'^decode_receipt/(?P<transID>\d+)/$', views.decode_receipt, name='decode_receipt'),	
	)