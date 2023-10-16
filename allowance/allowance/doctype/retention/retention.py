# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from dateutil import parser
from datetime import timedelta, datetime

class Retention(Document):

	@frappe.whitelist()
	def before_save(self):
		emp=frappe.db.get_list("Employee",fields=["name","on_retention"],filters={"name":self.employee})
		for i in emp:
			if str(self.to_date)=="None" or self.to_date=='' or str(self.to_date)=='' or self.to_date=="None":
				frappe.db.set_value("Employee", i.name, "on_retention", 1)
			else:
				frappe.db.set_value("Employee", i.name, "on_retention", 0)

			data = frappe.db.sql("""
									select status,retation_status,name,attendance_date from `tabAttendance` where employee = %(empid)s
         							and attendance_date between %(from_date)s and %(to_date)s
										""",{
							'empid': self.employee	,	'from_date': self.from_date,'to_date': self.to_date
						},  as_dict=1)	
		if data:
			# frappe.msgprint(str(data))
			for row in data:
				frappe.db.set_value('Attendance',row.name , 'retation_status', 'On Retation')
		else:
			start_date = datetime.strptime(self.from_date, "%Y-%m-%d")  # Replace with your start date
			end_date = datetime.strptime(self.to_date, "%Y-%m-%d")    # Replace with your end date

			while start_date <= end_date:
				attendance_doc = {
        			"doctype": "Attendance",
        			"employee": self.employee,
        			"status": "Present",
        			"attendance_date": start_date.date(),
        			"retation_status": "On Retation",
					"company":"VPPL PERIODIC",
					"docstatus":"1",
    			}

				frappe.get_doc(attendance_doc).insert(ignore_permissions=True)
				start_date += timedelta(days=1)

				
    

	@frappe.whitelist()
	def calculate_total_days(self):
		if self.from_date:
			from_date = parser.parse(self.from_date)
			to_date = parser.parse(self.to_date)

			self.total_days = ((to_date - from_date).days)+1
		# else:
		# 	frappe.throw('Please Select From Date First !')

	# def validate(self):
	# 	if self.total_days<=0:
	# 		frappe.throw('Totals Days Must Greater than 0')

