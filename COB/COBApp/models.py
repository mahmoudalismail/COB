# importing models
from django.db import models
# importing the User model
from django.contrib.auth.models import User

# Member will only be used once we have CMU Authentication
class Member(models.Model):
	# maximum Andrew ID is 8 characters
	andrewID = models.CharField(max_length=8)
	# name of the member
	memberName = models.CharField(max_length=100)

	def __unicode__(self):
		return self.andrewID

# Club model that contains all the clubs
class Club(models.Model):
	clubName = models.CharField(max_length=100)
	logo = models.ImageField(upload_to='receipts', blank=True)
	yearInit = models.CharField(max_length=15)
	description = models.CharField(max_length=200)
	mime_type = models.CharField(max_length=100)
	

	def __unicode__(self):
		return self.clubName

# linking each member with a certain club
class ClubMember(models.Model):
	clubID = models.ForeignKey(Club)
	memberID = models.ForeignKey(User)
	rank = models.CharField(max_length=100)

	def __unicode__(self):
		# returns the member's andrewID
		return self.memberID.username

# table of budgets for each club
class Budget(models.Model):

	# which club this budget points to
	clubID = models.ForeignKey(Club)
	# which year this budget belongs to 
	year = models.CharField(max_length=15)
	allocBudget = models.IntegerField(max_length=100)
	# total expenses in here instead of calculating the total
	# expenses each time for the graph 
	totalExpenses = models.IntegerField(max_length=100)

	# balance is calculated in this way
	# balance = allocBudget = totalExpenses can be calculated on the spot

	def __unicode__(self):
		# return the club's name
		return self.clubID.clubName

# table for the expenses 
class Expenses(models.Model):

	# which member submitted this expense
	memberSubmitted = models.ForeignKey(ClubMember)

	# name of the payer
	nameOfPayer = models.CharField(max_length=100, blank=False)
	# email of the payer
	emailOfPayer = models.CharField(max_length=50, blank=False)
	# which budget does this expense belong to
	budgetID = models.ForeignKey(Budget)	
	# catOfPurchase
	catOfPurchase = models.CharField(max_length=50, blank=False)
	# method of payment
	methodOfPayment = models.CharField(max_length=50, blank=False)
	#vendor or store
	vendorStore = models.CharField(max_length=50, blank=False)
	#purchase amount 
	amount = models.IntegerField(max_length=100, blank=False)
	# purchase date
	date = models.DateField()
	# date of event/program
	timeOfEvent = models.DateField()	
	# what did you buy?
	purchases = models.CharField(max_length=50, blank=False)
	# why did you buy it
	justification = models.CharField(max_length=100, blank=False)	
	# receipt which should be an image 
	receipt = models.ImageField(upload_to='receipts', blank=True)
	# MIME type for the receipt
	mime_type = models.CharField(max_length=200)
	
	# def __unicode__(self):
	# 	# returns the club's name
	# 	return self.budgetID

