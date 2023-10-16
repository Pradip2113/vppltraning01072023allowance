# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import datetime
import frappe
from frappe.model.document import Document
from dateutil import parser
import math

@frappe.whitelist()
def round_val(allo):
	rounded_get = allo // 1
	c=allo-rounded_get
	if c<0.50:
		res=math.floor(allo)
	else:
		res=math.ceil(allo)
	return res

class HRAandMedicalAllowance(Document):
	@frappe.whitelist() 
	def get_Details(self):
		#names_to_filter = ["W-00421"] #"S-00004", "W-00419"
		#emp = frappe.db.get_list("Employee",fields=["name", "last_name", "middle_name", "first_name", "employee_name","basic", "medical_allowance_e","hra_e","dearness_allowance","personal_pay_e","fixed_allowance_e", "designation","grade"],filters={"name": ["in", names_to_filter]})
		emp = frappe.db.get_list("Employee",fields=["name", "last_name", "middle_name", "first_name", "employee_name","basic", "medical_allowance_e","hra_e","dearness_allowance","personal_pay_e","fixed_allowance_e", "designation","grade"])		
		for i in emp:
			temp=str(self.date)
			lst=temp.split('-')
			year=int(lst[0])
			month=int(lst[1])
			date=int(lst[2])
			count=0
			# att=frappe.db.get_list("Attendance",fields=["name","attendance_date","employee","status"],filters={"employee":i.name,"status":"Absent",'attendance_date': ["between", [self.from_date, self.date]]})
			# if att:
			# 	for j in att:
			# 		count+=1
			# present_days=date-count
			# frappe.msgprint("1"+ str(i.name) + " " + str(present_days))

			present_days = frappe.db.count('Attendance', {'status': 'Present','attendance_date': ["between", [self.from_date, self.date]],"employee":i.name})  #,"retation_status":'Not'
			#frappe.msgprint(str(present_days))
			retension_days =   frappe.db.count('Attendance', {'status': 'Present','attendance_date': ["between", [self.from_date, self.date]],"employee":i.name,"retation_status":'On Retation'})  #,"retation_status":'Not'
			#frappe.msgprint(str(retension_days))
			retension_amt_basic = retension_amt_medi = retension_amt_hra  =retension_amt_da=retension_amt_fixed=retension_amt_personal_pay=0
			gra=frappe.db.get_list("Employee Grade",fields=["name","retention_percentage"],filters={"name":i.grade})
			for l in gra:	
				retension_amt_basic = (((float(i.basic)/date)*retension_days)*l.retention_percentage)/100
				retension_amt_medi=(((i.medical_allowance_e/date)*retension_days)*l.retention_percentage)/100
				retension_amt_hra=(((i.hra_e/date)*retension_days)*l.retention_percentage)/100
				if i.dearness_allowance is not None and date != 0:
					retension_amt_da = (((float(i.dearness_allowance) / date) * retension_days) * l.retention_percentage) / 100
				else:
					retension_amt_da = 0  # You can assign a default value or handle this case as needed
				retension_amt_fixed = (((i.fixed_allowance_e/date)*retension_days)*l.retention_percentage)/100
				retension_amt_personal_pay = (((i.personal_pay_e/date)*retension_days)*l.retention_percentage)/100
				
			#frappe.msgprint("retension_amt_basic"+str(retension_amt_basic) + " "+ "date"+str(date) )
				
				# if present_days>0 :
			self.append("hra_and_medical_allowance_details",
								{
									"employee": i.name,
									"employee_name": i.employee_name,
									"grade": i.grade,
									"retention_days":retension_days,
									"retention_amount":retension_amt_medi,
         							"basic":((float(i.basic)/date)*(present_days))+retension_amt_basic if count>20 else ((float(i.basic)/date)*(present_days-retension_days))+retension_amt_basic,
									"medical_allowance":((i.medical_allowance_e/date)*(present_days))+retension_amt_medi if count>20 else ((i.medical_allowance_e/date)*(present_days-retension_days))+retension_amt_medi,
									"hra": ((i.hra_e/date)*(present_days))+retension_amt_hra if count>20 else ((i.hra_e/date)*(present_days-retension_days))+retension_amt_hra,
									"fixed_allowance": ((i.fixed_allowance_e/date)*(present_days))+retension_amt_fixed if count>20 else ((i.fixed_allowance_e/date)*(present_days-retension_days))+retension_amt_fixed,			
									"personal_pay":((float(i.personal_pay_e)/date)*(present_days))+retension_amt_personal_pay if count>20 else ((float(i.personal_pay_e)/date)*(present_days-retension_days))+retension_amt_personal_pay,
									"dearness_allowance":((float(i.dearness_allowance)/date)*(present_days))+retension_amt_da if count>20 else ((float(i.dearness_allowance)/date)*(present_days-retension_days))+retension_amt_da,
									"amount":(retension_amt_basic+retension_amt_medi+retension_amt_hra+retension_amt_da+retension_amt_fixed+retension_amt_personal_pay)
									# "amount": (i.hra_e+retension_amt_hra+i.medical_allowance_e+retension_amt_medi) if count<20 else ((i.hra/date)*present_days)+retension_amt_hra+((i.medical_allowance_e/date)*present_days)+retension_amt_medi,
								},)

	@frappe.whitelist() 
	def calculate_payroll(self,payroll_date):
		frappe.msgprint("this is Payroll method..")
		#emp = frappe.db.get_list("Employee",fields=["name", "last_name", "middle_name", "first_name", "employee_name","basic", "medical_allowance_e","hra_e","dearness_allowance","personal_pay_e","fixed_allowance_e", "designation","grade"])		
		data = frappe.db.sql("""
                      SELECT
    tabemployee.name,
    tabemployee.last_name,
    tabemployee.middle_name,
    tabemployee.first_name,
    tabemployee.employee_name,
    tabemployee.designation,
    tabemployee.grade,
    IFNULL(tabemployeepayroll.basic_c, 0) 'basic',
    IFNULL(tabemployeepayroll.medical_allowance_c, 0) 'medical_allowance_e',
    IFNULL(tabemployeepayroll.hra_c, 0) 'hra_e',
    IFNULL(tabemployeepayroll.dearness_allowance_c, 0) 'dearness_allowance',
    IFNULL(tabemployeepayroll.personal_pay_c, 0) 'personal_pay_e',
    IFNULL(tabemployeepayroll.fixed_allowance_c, 0) 'fixed_allowance_e'
FROM
    `tabEmployee` tabemployee
LEFT JOIN
    `tabEmployee Payroll` tabemployeepayroll
ON
    tabemployeepayroll.parent = tabemployee.name
AND
    tabemployeepayroll.from_date = %(payroll_date)s
    AND tabemployeepayroll.from_date = (
        SELECT MAX(from_date)
        FROM `tabEmployee Payroll`
        WHERE parent in( 'W-00421','S-00162') AND from_date <= %(payroll_date)s
    )
WHERE
    tabemployee.name in( 'W-00421','S-00162')""",{'payroll_date':payroll_date},  as_dict=1)	
		for i in data:
			frappe.msgprint(str(data))
			temp=str(self.date)
			lst=temp.split('-')
			year=int(lst[0])
			month=int(lst[1])
			date=int(lst[2])
			count=0

			present_days = frappe.db.count('Attendance', {'status': 'Present','attendance_date': ["between", [self.from_date, self.date]],"employee":i.name})  #,"retation_status":'Not'
			#frappe.msgprint(str(present_days))
			retension_days =   frappe.db.count('Attendance', {'status': 'Present','attendance_date': ["between", [self.from_date, self.date]],"employee":i.name,"retation_status":'On Retation'})  #,"retation_status":'Not'
			#frappe.msgprint(str(retension_days))
			retension_amt_basic = retension_amt_medi = retension_amt_hra  =retension_amt_da=retension_amt_fixed=retension_amt_personal_pay=0
			gra=frappe.db.get_list("Employee Grade",fields=["name","retention_percentage"],filters={"name":i.grade})
			for l in gra:	
				retension_amt_basic = (((float(i.basic)/date)*retension_days)*l.retention_percentage)/100
				retension_amt_medi=(((i.medical_allowance_e/date)*retension_days)*l.retention_percentage)/100
				retension_amt_hra=(((i.hra_e/date)*retension_days)*l.retention_percentage)/100
				if i.dearness_allowance is not None and date != 0:
					retension_amt_da = (((float(i.dearness_allowance) / date) * retension_days) * l.retention_percentage) / 100
				else:
					retension_amt_da = 0  # You can assign a default value or handle this case as needed
				retension_amt_fixed = (((i.fixed_allowance_e/date)*retension_days)*l.retention_percentage)/100
				retension_amt_personal_pay = (((i.personal_pay_e/date)*retension_days)*l.retention_percentage)/100
				
			#frappe.msgprint("retension_amt_basic"+str(retension_amt_basic) + " "+ "date"+str(date) )
				
				# if present_days>0 :
			self.append("hra_and_medical_allowance_details",
								{
									"employee": i.name,
									"employee_name": i.employee_name,
									"grade": i.grade,
									"retention_days":retension_days,
									"retention_amount":retension_amt_medi,
         							"basic":((float(i.basic)/date)*(present_days))+retension_amt_basic if count>20 else ((float(i.basic)/date)*(present_days-retension_days))+retension_amt_basic,
									"medical_allowance":((i.medical_allowance_e/date)*(present_days))+retension_amt_medi if count>20 else ((i.medical_allowance_e/date)*(present_days-retension_days))+retension_amt_medi,
									"hra": ((i.hra_e/date)*(present_days))+retension_amt_hra if count>20 else ((i.hra_e/date)*(present_days-retension_days))+retension_amt_hra,
									"fixed_allowance": ((i.fixed_allowance_e/date)*(present_days))+retension_amt_fixed if count>20 else ((i.fixed_allowance_e/date)*(present_days-retension_days))+retension_amt_fixed,			
									"personal_pay":((float(i.personal_pay_e)/date)*(present_days))+retension_amt_personal_pay if count>20 else ((float(i.personal_pay_e)/date)*(present_days-retension_days))+retension_amt_personal_pay,
									"dearness_allowance":((float(i.dearness_allowance)/date)*(present_days))+retension_amt_da if count>20 else ((float(i.dearness_allowance)/date)*(present_days-retension_days))+retension_amt_da,
									"amount":(retension_amt_basic+retension_amt_medi+retension_amt_hra+retension_amt_da+retension_amt_fixed+retension_amt_personal_pay)
									# "amount": (i.hra_e+retension_amt_hra+i.medical_allowance_e+retension_amt_medi) if count<20 else ((i.hra/date)*present_days)+retension_amt_hra+((i.medical_allowance_e/date)*present_days)+retension_amt_medi,
								},)
				
				

	@frappe.whitelist()
	def before_save(self):
		# frappe.db.sql("UPDATE `tabEmployee` SET on_retention = 0 WHERE on_retention = 1")

		for i in self.get('hra_and_medical_allowance_details'):
			ssa=frappe.db.get_list("Salary Structure Assignment",fields=["name","employee","medical_allowance","hra","base","da","fixed_allowance","personal_pay"],filters={"employee":i.employee})
			if ssa:
				for j in ssa:
					frappe.db.set_value("Salary Structure Assignment", j.name, "base", round_val(i.basic))
					frappe.db.set_value("Salary Structure Assignment", j.name, "medical_allowance", round_val(i.medical_allowance))
					frappe.db.set_value("Salary Structure Assignment", j.name, "hra", round_val(i.hra))
					frappe.db.set_value("Salary Structure Assignment", j.name, "fixed_allowance", round_val(i.fixed_allowance))
					frappe.db.set_value("Salary Structure Assignment", j.name, "da", round_val(i.dearness_allowance))
					frappe.db.set_value("Salary Structure Assignment", j.name, "personal_pay", round_val(i.personal_pay))

	