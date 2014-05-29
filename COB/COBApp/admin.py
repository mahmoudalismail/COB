from django.contrib import admin
from COBApp.models import Club, Member, ClubMember, Budget, Expenses

class Members(admin.ModelAdmin):
    fieldsets = [
             ('Andrew ID', {'fields': ['andrewID']}),
             ('Member Name', {'fields': ['memberName']})]
             
    list_display = ('andrewID', 'memberName') 
    
    list_filter = ['andrewID']


class Clubs(admin.ModelAdmin):
    fieldsets = [
             ('Club Name', {'fields': ['clubName']}),
             ('Description', {'fields': ['description']}),
             ('Year Initiated', {'fields': ['yearInit']}),
             ('Upload Logo', {'fields': ['logo']})
             ]
             
    list_display = ('clubName', 'description', 'yearInit') 
    
    list_filter = ['clubName']

class ClubMembers(admin.ModelAdmin):
    fieldsets = [
             ('Club ID', {'fields': ['clubID']}),
             ('Member ID', {'fields': ['memberID']}),
             ('Rank', {'fields': ['rank']}),
             ]
             
    list_display = ('clubID', 'memberID', 'rank') 
    
    # list_filter = ['clubName']
class Budgets(admin.ModelAdmin):
    fieldsets = [
             ('Club ID', {'fields': ['clubID']}),
             ('Year', {'fields': ['year']}),
             ('Allocated Budget', {'fields': ['allocBudget']}),
             ('Total Expenses', {'fields': ['totalExpenses']}),
             ]
             
    list_display = ('clubID', 'year', 'allocBudget', 'totalExpenses') 

class Expenses1(admin.ModelAdmin):
    fieldsets = [
             ('Member Submitted', {'fields': ['memberSubmitted']}),
             ('Budget ID', {'fields': ['budgetID']}),
             ('Date', {'fields': ['date']}),
             ('Amount', {'fields': ['amount']}),
             ('Category of Purchase', {'fields': ['catOfPurchase']}),
             ('Receipt', {'fields': ['receipt']}),
             ]
             
    list_display = ('memberSubmitted', 'budgetID', 'date', 'amount', 'catOfPurchase', "receipt")

    list_filter = ['memberSubmitted']


admin.site.register(Member, Members)
admin.site.register(Club, Clubs)
admin.site.register(Budget, Budgets)
admin.site.register(ClubMember, ClubMembers)
admin.site.register(Expenses, Expenses1)