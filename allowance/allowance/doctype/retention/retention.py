# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from dateutil import parser

class Retention(Document):

	@frappe.whitelist()
	def before_save(self):
		emp=frappe.db.get_list("Employee",fields=["name","on_retention"],filters={"name":self.employee})
		for i in emp:
			if str(self.to_date)=="None" or self.to_date=='' or str(self.to_date)=='' or self.to_date=="None":
				frappe.db.set_value("Employee", i.name, "on_retention", 1)
			else:
				frappe.db.set_value("Employee", i.name, "on_retention", 0)

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

