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
		emp = frappe.db.get_list("Employee",fields=["name", "last_name", "middle_name", "first_name", "employee_name", "hra", "designation","grade"])
		for i in emp:
			temp=str(self.date)
			lst=temp.split('-')
			year=int(lst[0])
			month=int(lst[1])
			date=int(lst[2])
			count=0
			att=frappe.db.get_list("Attendance",fields=["name","attendance_date","employee","status"],filters={"employee":i.name,"status":"Absent",'attendance_date': ["between", [datetime.date(year, month, 1), self.date]]})
			if att:
				for j in att:
					count+=1
			present_days=date-count

			if not any(d.get("employee") == i.name for d in self.hra_and_medical_allowance_details):
				retemp=frappe.db.get_list("Employee",fields=['name',"on_retention"],filters={'name':i.name})
				for j in retemp:
					ret=frappe.db.get_list("Retention",fields=["name","from_date","employee","to_date","total_days"],filters={"employee":i.name})
					retension_days=0
					if j.on_retention==1:
						for k in ret:
							from_date = parser.parse(str(k.from_date))
							to_date = parser.parse(self.date)
							retension_days = ((to_date - from_date).days)+1
					else:
						
						if ret:
							# frappe.msgprint(str(ret))
							for k in ret:
								if str(k.to_date)!="None":
									from_date = parser.parse(str(k.from_date))
									to_date = parser.parse(self.date)
									
									if ((to_date - from_date).days)>0:
										# change 
										retension_days = retension_days+k.total_days
										# retension_days = ((to_date - from_date).days)
									else:
										pass
						else:
							pass


				gra=frappe.db.get_list("Employee Grade",fields=["name","retention_percentage"],filters={"name":i.grade})
				for l in gra:	
					retension_amt_medi=(((self.medical_allowance/date)*retension_days)*l.retention_percentage)/100
					retension_amt_hra=(((i.hra/date)*retension_days)*l.retention_percentage)/100
				
				# if present_days>0 :
				self.append("hra_and_medical_allowance_details",
								{
									"employee": i.name,
									"employee_name": i.employee_name,
									"grade": i.grade,
									"retention_days":retension_days,
									"retention_amount":retension_amt_medi,
									"hra": ((i.hra/date)*(present_days))+retension_amt_hra if count>20 else ((i.hra/date)*(present_days-retension_days))+retension_amt_hra,
									"medical_allowance":((self.medical_allowance/date)*(present_days))+retension_amt_medi if count>20 else ((self.medical_allowance/date)*(present_days-retension_days))+retension_amt_medi,
									# "hra": i.hra+retension_amt_hra if count<20 else ((i.hra/date)*present_days)+retension_amt_hra ,
									# "medical_allowance":self.medical_allowance+retension_amt_medi if count<20 else ((self.medical_allowance/date)*present_days)+retension_amt_medi,
									"amount": (i.hra+retension_amt_hra+self.medical_allowance+retension_amt_medi) if count<20 else ((i.hra/date)*present_days)+retension_amt_hra+((self.medical_allowance/date)*present_days)+retension_amt_medi,
								},)
				break
				

	@frappe.whitelist()
	def before_save(self):
		# frappe.db.sql("UPDATE `tabEmployee` SET on_retention = 0 WHERE on_retention = 1")

		for i in self.get('hra_and_medical_allowance_details'):
			ssa=frappe.db.get_list("Salary Structure Assignment",fields=["name","employee","medical_allowance","hra"],filters={"employee":i.employee})
			if ssa:
				for j in ssa:
					frappe.db.set_value("Salary Structure Assignment", j.name, "medical_allowance", round_val(i.medical_allowance))
					frappe.db.set_value("Salary Structure Assignment", j.name, "hra", round_val(i.hra))

	