# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
from frappe.utils import nowdate
from dateutil import parser

class BonusAllowance(Document):
	@frappe.whitelist()
	def get_components(self):
		lst=str(nowdate()).split('-')
		year=int(lst[0])
		self.from_date=datetime.date(year-1, 8, 1)
		self.to_date=datetime.date(year, 7, 31)
		lst=['Basic','Fixed Allowance','Personal Pay']
		for i in lst:
			self.append('component_details',{
				"salary_component":i,
			})
	@frappe.whitelist()
	def get_details(self):
		lst=[]
		for k in self.get('component_details'):
			lst.append(str(k.salary_component))
		temp=0
		total=0
		ss=frappe.db.get_list("Salary Slip",fields=['name','employee','employee_name','posting_date','start_date','end_date'],filters={'start_date':["between", [self.from_date, self.to_date]]})
		
		for j in ss:
			doc=frappe.get_doc("Salary Slip",j.name)
			for i in doc.get('earnings'):
				if doc.employee==j.employee and i.salary_component in lst:
					# frappe.msgprint(str(i.amount))
					temp=temp+i.amount
			for k in ss:
				if k.employee==j.employee:
						total=total+temp
			# frappe.msgprint(j.name+'  '+str(temp))
			if not any(d.get("employee") == j.employee for d in self.bonus_allowance_details):
				self.append('bonus_allowance_details',{
				"employee":j.employee,
				"employee_name":j.employee_name,
				"bonus":(total*self.bonus_percentage)/100,
			})
			temp=0
			total=0
