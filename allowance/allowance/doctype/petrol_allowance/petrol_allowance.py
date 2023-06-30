# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import datetime
import frappe
from frappe.model.document import Document
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

class PetrolAllowance(Document):
	@frappe.whitelist()
	def get_Details(self):
		designation_items = [d.designation for d in self.select_designation]
		designationslst = "{}".format(",".join(["{}".format(name) for name in designation_items]))
		designations=designationslst.split(',')

		query = """
			SELECT name, last_name, middle_name, first_name, employee_name, designation, petrol_allowance_in_ltr
			FROM `tabEmployee`
			WHERE designation IN ({})
		""".format(", ".join(["%s"] * len(designations)))
  
		emp = frappe.db.sql(query, tuple(designations), as_dict=True)
  
		for i in emp:
			if not any(d.get("employee") == i.name for d in self.petrol_allowance_details):
				des=frappe.db.get_list("Designation",fields=["name","season_rate","off_season_rate"],filters={"name":"SLIP BOY"})
				for k in des:
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
					if ((( ((i.petrol_allowance_in_ltr*self.petrol_rate*self.season_percentage)/100)/date)*present_days if self.season else ((((self.petrol_rate*self.off_season_percentage)/100)*i.petrol_allowance_in_ltr)/date)*present_days) if i.designation=="FIELD MAN" else (k.season_rate if self.season else k.off_season_rate))!=0:
						self.append("petrol_allowance_details",
							{
								"employee": i.name,
								"employee_name": i.employee_name,
								"designation": i.designation,
								"ltr": i.petrol_allowance_in_ltr if i.designation=="FIELD MAN" else 0,
								"amount": (( ((i.petrol_allowance_in_ltr*self.petrol_rate*self.season_percentage)/100)/date)*present_days if self.season else ((((self.petrol_rate*self.off_season_percentage)/100)*i.petrol_allowance_in_ltr)/date)*present_days) if i.designation=="FIELD MAN" else (k.season_rate if self.season else k.off_season_rate)
							},)
					


	@frappe.whitelist()
	def before_save(self):
		for i in self.get('petrol_allowance_details'):
			ssa=frappe.db.get_list("Salary Structure Assignment",fields=["name","employee","petrol_allowance"],filters={"employee":i.employee})
			if ssa:
				for j in ssa:
					frappe.db.set_value("Salary Structure Assignment", j.name, "petrol_allowance", round_val(i.amount))

	def validate(self):
		if self.petrol_rate<=0:
			frappe.throw('Please Enter Valid Petrol Rate !')
					


