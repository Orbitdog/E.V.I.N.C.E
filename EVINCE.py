'''
EVINCE - Earned Value INtegrating Calculator

'''
import csv
import collections
import pprint
import plotly.graph_objs as go
import pandas as pd
import plotly.offline as offline

# Earned Value Engine Calculations - captures the basic calculations in atomic functions

pv_plannedValue = 0.0 
# the cumulative amount planned to be spent for all the work planned to be done up to the period of analysis 

ac_actualValue = 0.0
# the cumulative amount actually spent for all work completed up to the period of analysis

ev_earnedValue = 0.0
# the cumulative amount planned to be spent for all the work completed up to the period of analysis
 
bac_budgetaryCostAtCompletion = 0.0
# the amount planned to be spent for the total project

# functions for derivaive indices
def CPI(EV,AC): 	# return cost performance index calculation
	cpi = EV / AC
	return cpi
	
def SPI(EV,PV):	# return schedule performance index calculation
	spi = EV / PV
	return spi
	
def TCPI(BAC,PV,AC): # return  total cost performance index calculation
	tcpi = (BAC - PV) / (BAC - AC)
	return tcpi

# functions for derivative values
def SV(EV,PV):		# return schedule variance
	sv = EV - PV
	return sv
	
def CV(AC,EV):		# return cost variance
	cv = AC - EV
	return cv
	
def EAC(BAC,CPI):	# return predicted ("estimated") total project cost	
	eac = BAC / CPI
	return eac
	
def ETC(EAC,AC):	# return amount balance needed to complete the project
	etc = EAC - AC
	return etc
	
def VAC(BAC,EAC):	# return total variance at completion
	vac = BAC - EAC
	return vac
	
# functions for derivative percentages
def PCS(EV,BAC):	# return percentage of total budget planned for work completed to date
	pcs = EV / BAC
	return pcs\
	
def PSB(AC,BAC):	# return percentage of the total budget spent for work completed to date
	psb = AC / BAC
	return psb
	
def PCV(CV,EV):		# return percentage variance from budget for work completed to date
	pcv = CV / EV
	return pcv
	
def PSV(SV,PV):		# return percentage variance of the rate of spending for work completed to date
	psv = SV / PV
	return psv
	
def PPCWI(AC,PV):	# return percentage of planned rate of spending actually for work completed to date
	ppcwi = AC / PV
	return ppcwi

def separator(stars,dashes):
	 print(*['*']*stars, sep='-'*dashes)
 
def tab(ntabs):
	return "\t"*ntabs
	
def PrintDatasetCSV(filename):
	with open(filename, mode='r') as csv_file:
		csv_reader = csv.DictReader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				print(f'\t{tab(1).join(row)}')
				line_count += 1
			print(f'\t{row["PERIOD"]}\t{row["PV"]}\t{row["AC"]}\t{row["EV"]}') # how to improve this w/ tab fn
			line_count += 1
		print(f'Processed {line_count} line/s. \nProcessed {line_count - 1} record/s.')
		return True
 
	 
def loadDatasetCSV(filename):
	
	dlist = []
	with open(filename, mode='r') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for line in csv_reader:
			dlist.append(line)

	return dlist
		
def execCalcs(dataSet):
	pointer1 = 1 # skip the first element(0)in list as these are the labels. assume data structure is maintained that way
	resultsSet = []					
	for pointer1 in range(1, len(dataSet)):						
		subdataSet = dataSet[pointer1] 	# this is pointing to the list within the list
		# load values passed into dataSet for calcs: PV,AC,EV,BAC
		pv = subdataSet[1]				# skip again the first element(0) which is the period value 
		ac = subdataSet[2]
		ev = subdataSet[3]
		bac= subdataSet[4]
		cpi= str(CPI(float(ev),float(ac)))
		subdataSet.append(cpi)
		spi= str(SPI(float(ev),float(pv)))
		subdataSet.append(spi)
		tcpi= str(TCPI(float(bac),float(pv),float(ac)))
		subdataSet.append(tcpi)
		sv= str(SV(float(ev),float(pv)))
		subdataSet.append(sv)
		cv = str(CV(float(ac),float(ev)))
		subdataSet.append(cv)
		resultsSet.append(subdataSet)	
	return resultsSet
	
def plotResults(resultsTable):  # let's code this to be  little more generic to specify which data to plot
	
	pointer1 = 0
	plotResultsX=[]
	plotResultsY1=[]
	plotResultsY2=[]
	plotResultsY3=[]
	for pointer1 in range(0,len(resultsTable)):
		subdataSet = resultsTable[pointer1]
		xaxis = float(subdataSet[0])
		plotResultsX.append(xaxis)
		yaxis1 = float(subdataSet[1])
		plotResultsY1.append(yaxis1)
		yaxis2 = float(subdataSet[2])
		plotResultsY2.append(yaxis2)
		yaxis3 = float(subdataSet[3])
		plotResultsY3.append(yaxis3)
		
	trace1 = go.Scatter(
		 x=plotResultsX, y=plotResultsY1,mode='lines',
		name = 'PV')
	trace2 = go.Scatter(
		 x=plotResultsX, y=plotResultsY2,mode='lines',
		 name = 'AC',)
	trace3 = go.Scatter(
		 x=plotResultsX, y=plotResultsY3,mode='lines',
		 name = 'EV',)
		 
	data = [trace1 , trace2, trace3]
	
	layout =  go.Layout(title = "Combines PV & AC & EV", showlegend = True) # legend = dict( x = 0.00, y= 0.00))

	figure = go.Figure(data=data, layout=layout)

	offline.plot(figure)

	return False 
	
# Main Execution Loop starts here including break and error capture control

datasetFile = "d01.csv"
# PrintDatasetCSV(datasetFile)
dataSet = loadDatasetCSV(datasetFile)
# pprint.pprint(dataSet)
# print(dataSet)

resultsTable = execCalcs(dataSet)
# pprint.pprint(resultsTable)

plotResults(resultsTable)

# state = plotResults(resultsTable)

'''
# Test Bench - exercise all functions and modules
pv_plannedValue = float(input('PLANNED VALUE TO BE COMPLETED: '))
ac_actualValue = float(input('ACTUAL VAUE COMPLETED: '))
ev_earnedValue = float(input('EARNED VALUE OF COMPLETED: '))
bac_budgetaryCostAtCompletion = float(input('BUDGETARY COST AT COMPLETION: '))
separator(10,4)
print('PLANNED VALUE = ', pv_plannedValue)
print('ACTUAL VALUE = ', ac_actualValue)
print('EARNED VALUE = ', ev_earnedValue)
separator(10,4)
print('PERFORMANCE INDICES')
separator(10,4)	
print('COST PERFORMANCE INDEX = ', str(CPI(ev_earnedValue,ac_actualValue)))
print('SCHED PERFORMANCE INDEX = ',str(SPI(ev_earnedValue,pv_plannedValue)))
print('TOTAL COST PERFORMANCE INDEX = ',str(TCPI(bac_budgetaryCostAtCompletion, pv_plannedValue, ac_actualValue)))
separator(10,4)
print('DERIVATIVE VALUES CALCULATED')
separator(10,4)
print('SCHEDULE VARIANCE = ', str(SV(ev_earnedValue,pv_plannedValue)))
print('COST VARIANCE = ', str(CV(ac_actualValue,ev_earnedValue)))
CPI = CPI(ev_earnedValue,ac_actualValue)
EAC = EAC(bac_budgetaryCostAtCompletion,CPI)
ETC = ETC(EAC,ac_actualValue)
VAC = VAC(bac_budgetaryCostAtCompletion,EAC)
print('PREDICTED TOTAL COST = ',str(EAC))
print('BALANCE REQUIRED TO COMPLETE = ',str(ETC))
print('VARIANCE AT COMPLETION = ' , str(VAC))
separator(10,4)
print('PERCENTAGES')
separator(10,4)
print('% of TOTAL BUDGET PLANNED = {0} %'.format(PCS(ev_earnedValue,bac_budgetaryCostAtCompletion)*100))
print('% of TOTAL BUDGET SPENT = {0} %'.format(PSB(ac_actualValue,bac_budgetaryCostAtCompletion)*100))
print('% VARIANCE FROM BUDGET = {0} % '.format(PCV(CV(ac_actualValue,ev_earnedValue),ev_earnedValue)*100))
print('% VARIANCE FROM SPEND RATE = {0} %'.format(PSV(SV(ev_earnedValue,pv_plannedValue), pv_plannedValue)*100))
print('% PLANNED SPEND RATE = {0} %'.format(PPCWI(ac_actualValue,pv_plannedValue)*100))
separator(10,4); print('TEST BENCH DONE...............')
'''
