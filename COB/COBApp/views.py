# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group

# importing the models 
from COBApp.models import Budget, Expenses, ClubMember, Club

# importing json related libraries
from django.utils import simplejson
from django.core import serializers

# authentication libraries
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import logout

# reportlab for generating PDFs
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, cm

# render the index page
def index(request):

	return render(request, 'COBApp/index.html',{});

# renders the dashbaord for user and admin 
@login_required(login_url='/COBApp/login/')
def dashboard(request):

	if not request.user.is_superuser:
		# get the current club from the UserID session
		loggedInClub = ClubMember.objects.get(memberID = request.user)
		
		# get the current budget for the club the user is registered with
		budget = Budget.objects.filter(clubID = loggedInClub.clubID).latest('year')
		
		summary = Expenses.objects.filter(budgetID = budget).order_by('date').reverse().values('date', 'catOfPurchase', 'amount')

		
		return render(request, 'COBApp/dashboard.html', {'allocBudget': budget.allocBudget, 
								'totalExpenses': budget.totalExpenses, 
								'balance': (budget.allocBudget-budget.totalExpenses),
								'username': loggedInClub.memberID.username,
								'clubID': loggedInClub.clubID.id,
								'summary': summary[:3]});
	else:

		return render(request, 'COBApp/admindashboard.html', 
						{'username': request.user.username,
						 'clubs': Club.objects.all()});

# renders the expense form page 
@login_required(login_url='/COBApp/login/')
def expenseform(request):

	if not request.user.is_superuser:
		# get the club for the logged in member
		loggedInClub = ClubMember.objects.filter(memberID = request.user)[0]

		# get the name of the club
		nameOfClub = loggedInClub.clubID.clubName
		
		return render(request, 'COBApp/expenseform.html', {'clubName': nameOfClub, 'username': request.user.username, 'clubID': loggedInClub.clubID.id});
	
	else:
		# get the list of all available clubs 
		all_clubs = Club.objects.all().values('clubName')
		fake_id = 0
		return render(request, 'COBApp/expenseform.html', {'username': request.user.username, 'all_clubs': all_clubs, 'clubID': fake_id});

@login_required(login_url='/COBApp/login/')
# saving the expenses
def submitExpenseForm(request):

	if not request.user.is_superuser:
		# get the club for the current user
		loggedInClub = ClubMember.objects.get(memberID = request.user)
		
		# get the current club's budget 
		clubBudget = Budget.objects.filter(clubID = loggedInClub.clubID).order_by('year').reverse()
		# get the latest club
		clubBudget = clubBudget[0]

	else:

		clubname = request.POST["club_name"]
		# get the club for the user 
		loggedInClub = ClubMember.objects.filter(memberID = request.user)[0]
		# get the current club's budget 

		clubBudget = Budget.objects.filter(clubID = Club.objects.get(clubName = clubname)).order_by('year').reverse()
		# get the latest budget
		clubBudget = clubBudget[0]
	# amount the user entered 
	amountEntered = request.POST['amount']

	# create an Expenses record 
	newExpense = Expenses(memberSubmitted = loggedInClub,
						  nameOfPayer = request.POST['payer'],
						  emailOfPayer = request.POST['email'],
						  budgetID = clubBudget,
						  catOfPurchase = request.POST['catOfPurchase'],
						  methodOfPayment = request.POST['method'],
						  vendorStore = request.POST['store'],
						  amount = amountEntered,
						  date = request.POST['date'],
						  timeOfEvent = request.POST['dateEvent'],
						  purchases = request.POST['purchases'],
						  justification = request.POST['justification'],
						  receipt = request.FILES['receipt'],
						  mime_type = request.FILES['receipt'].content_type)
	newExpense.save()
	print clubBudget.totalExpenses
	# update the total expenses
	clubBudget.totalExpenses = clubBudget.totalExpenses + int(amountEntered)
	clubBudget.save()

	return HttpResponseRedirect(reverse('COBApp.views.expenseform',))

@login_required(login_url='/COBApp/login/')
# AJAX request for receiving the data for the graphs
def getSpending(request, club_id):
	
	if not request.user.is_superuser:
		# get the club for the current user
		loggedInClub = ClubMember.objects.filter(memberID = request.user)[0]

		# get the current budget for the club
		# budget = Budget.objects.filter(clubID = loggedInClub.clubID)[0]
		budget = Budget.objects.filter(clubID = loggedInClub).latest('year')

		# get the club name
		clubName = loggedInClub.clubID.clubName
	else:
		loggedInClub = Club.objects.get(id = club_id)

		budget = Budget.objects.filter(clubID = loggedInClub).latest('year')

		#get the clubName
		clubName = loggedInClub.clubName

	# get expenses for Printing banners, booklets, roll ups
	printing = Expenses.objects.filter(budgetID = budget, 
			catOfPurchase = "Printing banners, booklets, roll ups").values('amount')
	printing =  sum(item['amount'] for item in list(printing))
	
	# get expenses for Supplies for events
	supplies = Expenses.objects.filter(budgetID = budget, 
			catOfPurchase = "Supplies for events").values('amount')
	supplies =  sum(item['amount'] for item in list(supplies))
	
	# get expenses for Giveaways
	giveaways = Expenses.objects.filter(budgetID = budget, 
			catOfPurchase = "Giveaways").values('amount')
	giveaways =  sum(item['amount'] for item in list(giveaways))
	# data_json = serializers.serialize('json', budget, fields=("allocBudget", "totalExpenses"))
	
	# get expenses for Prizes
	prizes = Expenses.objects.filter(budgetID = budget, 
			catOfPurchase = "Prizes").values('amount')
	prizes =  sum(item['amount'] for item in list(prizes))

	# get expenses for Food, snacks, drinks
	food = Expenses.objects.filter(budgetID = budget, 
			catOfPurchase = "Food, snacks, drinks").values('amount')
	food =  sum(item['amount'] for item in list(food))

	# get expenses for transportation 
	transportation = Expenses.objects.filter(budgetID = budget, 
			catOfPurchase = "Transportation").values('amount')
	transportation =  sum(item['amount'] for item in list(transportation))

	# get expenses for Entrance Fees
	fees = Expenses.objects.filter(budgetID = budget, 
			catOfPurchase = "Entrance Fees").values('amount')
	fees =  sum(item['amount'] for item in list(fees))

	# get expenses for Rental Fee (bouncy castles, tents, other equipment)
	rental = Expenses.objects.filter(budgetID = budget, 
		catOfPurchase = "Rental Fee (bouncy castles, tents, other equipment)").values('amount')
	rental =  sum(item['amount'] for item in list(rental))

	# get expenses for Professional Fees (organizational dues)
	prof_fees = Expenses.objects.filter(budgetID = budget, 
		catOfPurchase = "Professional Fees (organizational dues)").values('amount')
	prof_fees =  sum(item['amount'] for item in list(prof_fees))

	# get expenses for Non-capital equipment (camera, rechargeable batteries, portable printer)
	non_capital = Expenses.objects.filter(budgetID = budget, 
		catOfPurchase = "Non-capital equipment (camera, rechargeable batteries, portable printer)").values('amount')
	non_capital =  sum(item['amount'] for item in list(non_capital))

	#return them as json
	data_json = simplejson.dumps([clubName, (budget.allocBudget - budget.totalExpenses),printing, supplies, 
								  giveaways, prizes, food, transportation, fees, rental, prof_fees, non_capital])
	return HttpResponse(data_json, content_type="application/json")


@login_required(login_url='/COBApp/login/')
# logs out the user
def logout_view(request):

	logout(request)
	return HttpResponseRedirect(reverse('COBApp.views.index',))

@login_required(login_url='/COBApp/login/')
# showing the club's dashboards for the admin
def showDashboard(request, clubID):
	if not request.user.is_superuser:
		return "Unauthorized"
	else:
		loggedInClub = Club.objects.get(id = clubID)
		
		# get the current budget for the club the user is registered with
		# budget = Budget.objects.filter(clubID = loggedInClub)[0]
		budget = Budget.objects.filter(clubID = loggedInClub).latest('year')
		
		# get the first latest transactions for the summary
		summary = Expenses.objects.filter(budgetID = budget).order_by('date').reverse().values('date', 'catOfPurchase', 'amount')
		
		return render(request, 'COBApp/dashboard.html', {'allocBudget': budget.allocBudget, 
								'totalExpenses': budget.totalExpenses, 
								'balance': (budget.allocBudget-budget.totalExpenses),
								'username': request.user.username,
								'clubID': loggedInClub.id,
								'summary': summary[:3]});		
def generatePDF(request, clubID):

	# some of the code below I got from 
	# https://docs.djangoproject.com/en/dev/howto/outputting-pdf/
    
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="expenses_report_COB.pdf"'

    # setting up the canvas 
    c = canvas.Canvas(response, pagesize = A4)

    # getting the size of an A4 paper 
    width, height = A4
    
    #start using the text
    textobject = c.beginText()
    
    # set the starting cursor 
    textobject.setTextOrigin(2*cm , height - inch)
    
    # choosing the font 
    textobject.setFont("Helvetica", 12)
    textobject.textLine("COB Budget Generated Report")
    textobject.textLine("Generated by: "+request.user.username)
    # we need to get the expenses for the club

    # normal user, not superuser 
    if not request.user.is_superuser:
    	# get logged in club 
    	loggedInClub = ClubMember.objects.get(memberID = request.user)
    	
    	# get the club name
    	nameOfClub = loggedInClub.clubID.clubName
    	
    	# get the club's budget
    	# budget = Budget.objects.get(clubID = loggedInClub.clubID)
    	budget = Budget.objects.filter(clubID = loggedInClub.clubID).latest('year')

    	# get expenses for the club
    	expenses = Expenses.objects.filter(budgetID = budget).order_by('date')

    else:
    	# get the club
    	loggedInClub = Club.objects.get(id = clubID)

    	# get the club's name
    	nameOfClub = loggedInClub.clubName

    	#get the club's budget
    	# budget = Budget.objects.get(clubID = loggedInClub)
    	budget = Budget.objects.filter(clubID = loggedInClub).latest('year')

    	# get the expenses for the club
    	expenses = Expenses.objects.filter(budgetID = budget).order_by('date')

    # got the needed information, we write the PDF 

    textobject.textLine("Transactions for "+nameOfClub)
    textobject.textLine("")

    # allocated budget
    textobject.textLine("Allocated Budget: QAR "+str(budget.allocBudget))
    # total expenses 
    textobject.textLine("Total Expenses: QAR "+str(budget.totalExpenses))
    # available budget
    textobject.textLine("Available Budget: QAR"+str(budget.allocBudget - budget.totalExpenses))
    textobject.textLine("")

    # get the current coordinates for the cursor 
    x, y = textobject.getCursor()
    # indent the text by 1 cm
    textobject.setTextOrigin(x+cm, y)
    
    # write the all the expenses on the PDF
    for expense in expenses:
    	textobject.textLine("Name: "+expense.nameOfPayer)
    	textobject.textLine("Email: "+expense.emailOfPayer)
    	textobject.textLine("Category Of Purchase: "+expense.catOfPurchase)
    	textobject.textLine("Method Of Payment: "+expense.methodOfPayment)
    	textobject.textLine("Vendor or Store: "+expense.vendorStore)
    	textobject.textLine("Amount: QAR "+str(expense.amount))
    	textobject.textLine("Date of Purchase: "+str(expense.date))
    	textobject.textLine("Date of Event: "+str(expense.timeOfEvent))
    	textobject.textLine("What did you buy?: "+expense.purchases)
    	textobject.textLine("Why did you buy it?: "+expense.justification)
    	textobject.textLine("")

    # draw all the text on the PDF
    c.drawText(textobject)
    c.showPage()
    c.save()
    return response

@login_required(login_url='/COBApp/login/')
# renders the history page 
def history(request, clubID):

	
	if not request.user.is_superuser: 
		# get the current club for the user
		loggedInClub = ClubMember.objects.filter(memberID = request.user)[0]
		# get the current budget
		# Clubbudget = Budget.objects.filter(clubID = loggedInClub.clubID)
		Clubbudget = Budget.objects.filter(clubID = loggedInClub.clubID).latest('year')
		# get all the expenses for the club
		expenses = Expenses.objects.filter(budgetID = Clubbudget)
		# get the history for the specific club
		history = expenses.values('date', 'catOfPurchase', 'amount', 'id')
		# get the club name
		club_name = loggedInClub.clubID.clubName
		# get the clubID
		club_id = loggedInClub.clubID.id

	else:
		# get the current club for the user
		loggedInClub = Club.objects.get(id = clubID)
		# get the current budget
		Clubbudget = Budget.objects.filter(clubID = loggedInClub).latest('year')
		# get all the expenses for the club
		expenses = Expenses.objects.filter(budgetID = Clubbudget)
		# get the history for the specific club
		history = expenses.values('date', 'catOfPurchase', 'amount', 'id')	
		# get the club name
		club_name = loggedInClub.clubName
		# get the club ID
		club_id = clubID

	return render(request, 'COBApp/transactionhistory.html', {'username': request.user.username, 
															  'history': history,
															  'club_name': club_name,
															  'clubID': club_id})
@login_required(login_url='/COBApp/login/')
# get the logo for the club
def decode(request, clubID):
	if request.user.is_superuser:
		loggedInClub = Club.objects.get(id = clubID)
	else:
		memberOfClub = ClubMember.objects.get(memberID = request.user)
		loggedInClub = memberOfClub.clubID
	# no mime_type is being saved because the image is saved through the admin page
	return HttpResponse(loggedInClub.logo.read(), mimetype=loggedInClub.mime_type)

@login_required(login_url='/COBApp/login/')
# shows the transaction details 
def trans(request, transID):
	
	if request.user.is_superuser:
		# get the expense 
		expense = Expenses.objects.get(id = transID)	
		return render(request, 'COBApp/transactiondetails.html', {'username': request.user.username, 
									'details': expense, 'clubID': expense.memberSubmitted.clubID.id})
	else:
		# check if the user is able to view this transaction
		loggedInClub = ClubMember.objects.get(memberID = request.user)
		
		# get the budget
		# budget = Budget.objects.get(clubID = loggedInClub.clubID)
		budget = Budget.objects.filter(clubID = loggedInClub.clubID).latest('year')

		
		expense = Expenses.objects.filter(budgetID = budget, id = transID)

		if len(list(expense)) == 0:
			return "Not authorized"
		else:
			return render(request, 'COBApp/transactiondetails.html', {'username': request.user.username, 
							'details': expense[0], 'clubID': expense[0].memberSubmitted.clubID.id})

@login_required(login_url='/COBApp/login/')
# decodes the receipt
def decode_receipt(request, transID):

	if request.user.is_superuser:
		# get the expense 
		expense = Expenses.objects.get(id = transID)	
		return HttpResponse(expense.receipt.read(), mimetype=expense.mime_type)
	else:
		# check if the user is able to view this transaction
		loggedInClub = ClubMember.objects.get(memberID = request.user)
		
		# get the budget
		budget = Budget.objects.filter(clubID = loggedInClub.clubID).order_by('year').reverse()
		budget = budget[0]
		# filter the budgetID and the trans ID
		expense = Expenses.objects.filter(budgetID = budget, id = transID)

		if len(list(expense)) == 0:
			return "Not authorized"
		else:
			
			return HttpResponse(expense[0].receipt.read(), mimetype=expense[0].mime_type)