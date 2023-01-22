#!/usr/bin/env python

#Type I.A: Mark if payee total for 1 day is >$10,000. Each transaction is >$10,000 ("CTR")
#Type I.B: Mark if payee total for 1 day is >$10,000. Each transaction is <=$10,000 (“CTR Reportable Small-Check Event”)
#Type II: Mark if payee total for 4 days is >$10,000 where the total for payee for any day is <=$10,000 (“Potential Structuring Event”)
#Author: Anant Raj, Author URI: http://uxanant.com, Reach for support at uxanant@gmail.com
import csv
from dateutil.parser import parse
from datetime import datetime
import time
import operator
import pandas as pd


#1 Date, 6, 8 payee ID
column_date = 1
column_amount = 7
column_payerName = 3
critical_amount = 10000
has_headers = False
input_filename='input.csv'
# Open file

print('Loaded Module: csv, dateutil.parser/parse, datetime/datetime, time, operator, pandas/pd')
print('Input Filename: '+input_filename)
print('Filer Base Column: '+str(column_payerName+1))


temp_rows=[]
with open(input_filename) as file_obj:

    reader_obj = csv.reader(file_obj)
    row_count = 0
    for row in reader_obj:
        if (has_headers and row_count > 0) or not has_headers:
            row[column_date]=parse(row[column_date]).strftime('%m/%d/%Y')
            row[column_date+1]=time.mktime(datetime.strptime(row[column_date], '%m/%d/%Y').timetuple())
            temp_rows.append(row)
        row_count = row_count + 1

pd.DataFrame(temp_rows).to_csv("temp.csv",index=False)

with open('temp.csv') as file_obj:
    sorted_list=[]
    reader_obj = csv.reader(file_obj)
    sorted_list = sorted(reader_obj, key=operator.itemgetter(column_date+1))
    
    type1a_payerName=[]
    type1a_date=[]
    type1b_payerName=[]
    type1b_date=[]
    type1_category=[] # "CTR", "mixed", “CTR Reportable Small-Check Event”
    
    daywise_payerName=[]
    daywise_date=[]
    daywise_amount=[]
    daywise_category=[]
    	
    
    #creating day-wise table
    date=0
    category = []
    payerName = []
    amount = []
    row_count = 0
    for row in sorted_list:
        if (has_headers and row_count > 0) or not has_headers:
            if date != row[column_date]:
                for x in range(len(category)):
                    daywise_payerName.append(payerName[x])
                    daywise_date.append(date)
                    daywise_amount.append(amount[x])
                    daywise_category.append(category[x])
                    if category[x]==1:
                        type1a_payerName.append(payerName[x])
                        type1a_date.append(date)
                    if category[x]==-1 and float(amount[x])>critical_amount:
                        type1b_payerName.append(payerName[x])
                        type1b_date.append(date)
                category = []
                payerName = []
                amount = []
                date=row[column_date]
            if row[column_payerName] in payerName:
                currentIndex = payerName.index(row[column_payerName])
                amount[currentIndex]=(float(amount[currentIndex])+float(row[column_amount]))
                if category[currentIndex] == 1 and float(row[column_amount]) < critical_amount:
                    category[currentIndex] = 0
                if category[currentIndex] == -1 and float(row[column_amount]) > critical_amount:
                    category[currentIndex] = 0
            else:
                payerName.append(row[column_payerName])
                amount.append(row[column_amount])
                if float(row[column_amount]) > critical_amount:
                    category.append(1)
                else:
                    category.append(-1)
                    
        row_count = row_count + 1

df = pd.DataFrame({'Payer Name': type1a_payerName, 'Date': type1a_date})
df.to_csv('output_CTR.csv',index=False)
print('Find output of Type 1 @ ' + 'output_CTR.csv')
df = pd.DataFrame({'Payer Name': type1b_payerName, 'Date': type1b_date})
df.to_csv('output_CTR Reportable Small-Check Event.csv',index=False)
print('Find output of Type 2 @ ' + 'output_CTR Reportable Small-Check Event.csv')
df = pd.DataFrame({'Payer Name': daywise_payerName, 'Date': daywise_date, 'Amount': daywise_amount, 'Category': daywise_category})
df.to_csv('day-wise.csv',index=False, header=False)

type2_payerName=[]
type2_amount=[]
    
with open('day-wise.csv') as file_obj:
	
	# Create reader object by passing the file
	# object to reader method
    reader_obj = csv.reader(file_obj)
    
    icolumn_payerName = 0
    icolumn_date = 1
    icolumn_amount = 2
    icolumn_category = 3
    	
    sorted_list=[]
    reader_obj = csv.reader(file_obj)
    sorted_list = sorted(reader_obj, key=operator.itemgetter(icolumn_amount))
    
    #creating day-wise table
    category = []
    amount = []
    repeat = []
    payerName = []
    
    row_count = 0
    for row in sorted_list:
        if row_count > 0:
            print(row[icolumn_amount])
            if row[icolumn_payerName] in payerName:
                currentIndex = payerName.index(row[icolumn_payerName])
                if repeat[currentIndex] < 4:
                    amount[currentIndex]=(float(amount[currentIndex])+float(row[icolumn_amount]))
                    repeat[x]=repeat[x]+1
                    if category[currentIndex] == 1 and float(row[icolumn_amount]) < critical_amount:
                        category[currentIndex] = 0
                    if category[currentIndex] == -1 and float(row[icolumn_amount]) > critical_amount:
                        category[currentIndex] = 0
            else:
                payerName.append(row[icolumn_payerName])
                amount.append(row[icolumn_amount])
                repeat.append(1)
                if float(row[icolumn_amount]) > critical_amount:
                    category.append(1)
                else:
                    category.append(-1)
        row_count=row_count+1
    for x in range(len(category)):
        if float(amount[x])>10000:
            type2_payerName.append(payerName[x])
            type2_amount.append(amount[x])
    

df = pd.DataFrame({'Payer Name': type2_payerName})
df.to_csv('output_Potential Structuring Event.csv',index=False)

print('Find output of Type 3 @ ' + 'output_Potential Structuring Event.csv')
print('Script completed successfully')

with open(input_filename) as file_obj:

    reader_obj = csv.reader(file_obj)
    row_count = 0
    for row in reader_obj:
        if (has_headers and row_count > 0) or not has_headers:
            row[column_date]=parse(row[column_date]).strftime('%m/%d/%Y')
            row[column_date+1]=time.mktime(datetime.strptime(row[column_date], '%m/%d/%Y').timetuple())
            temp_rows.append(row)
        row_count = row_count + 1

pd.DataFrame(temp_rows).to_csv("temp.csv",index=False)

with open(input_filename,'r') as csvinput:
    with open('output_merged.csv', 'w', newline='') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

        writer = csv.writer(csvoutput)
        
        row_count = 0
        for row in csv.reader(csvinput):
            if (has_headers and row_count > 0) or not has_headers:
                temp_row=row
                if row[column_payerName] in type1a_payerName:
                    temp_row.append("CTR")
                else:
                    temp_row.append("-")
                
                if row[column_payerName] in type1b_payerName:
                    temp_row.append("CTR Reportable Small-Check Event")
                else:
                    temp_row.append("-")
                
                if row[column_payerName] in type2_payerName:
                    temp_row.append("Potential Structuring Event")
                else:
                    temp_row.append("-")
                writer.writerow(temp_row)
            else:
                writer.writerow(row+["CTR","CTR Reportable Small-Check Event","Potential Structuring Event"])
            row_count = row_count + 1
 
print('Find output of Merged @ ' + 'output_merged.csv')
print('Script completed successfully')