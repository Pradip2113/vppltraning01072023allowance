# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DA(Document):
	@frappe.whitelist()
	def get_Details(self):
		emp = frappe.db.get_list("Employee", fields=["name","is_da_aplicable","employee_name","designation"],filters={"is_da_aplicable":1})
		for i in emp:
			if not any(d.get("employee") == i.name for d in self.da_details):
						self.append("da_details",
							{
								"employee": i.name,
								"employee_name": i.employee_name,
								"designation": i.designation,
								"da": self.da_amount,
							},)

	@frappe.whitelist()
	def before_save(self):
		for i in self.get('da_details'):
			ssa=frappe.db.get_list("Salary Structure Assignment",fields=["name","employee","petrol_allowance","da"],filters={"employee":i.employee})
			if ssa:
				for j in ssa:
					frappe.db.set_value("Salary Structure Assignment", j.name, "da", i.da)
