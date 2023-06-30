# Copyright (c) 2023, Abhishek Chougule and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
from frappe.utils import nowdate
from dateutil import parser

class EarnedLeaveCalculation(Document):
	@frappe.whitelist()
	def get_Details(self):
		count=0
		trd=0
		emp = frappe.db.get_list("Employee",fields=["name","employee_name", "employment_type"],filters={'employment_type': ['in', ['PERMANENT', 'SEASONAL']]})
		from_date = parser.parse(self.from_date)
		to_date = parser.parse(self.to_date)
		td=(((to_date - from_date).days)+1)
		for i in emp:	
			att=frappe.db.get_list("Attendance",fields=['name','employee','attendance_date','status'],filters={'employee':i.name,'status':'Absent','attendance_date':["between", [self.from_date, self.to_date]]})

			if att:			
				for j in att:
					count+=1
			r=frappe.db.get_list("Retention",fields=['name','employee','total_days','from_date','to_date'],filters={'employee':i.name,'from_date':["between", [self.from_date, self.to_date]],'to_date':["between", [self.from_date, self.to_date]]})
			if r:
				for l in r:
					trd=trd+l.total_days
			
			self.append("earned_leave_calculation_details",
			{
				"employee": i.name,
				"employee_name": i.employee_name,
				"employment_type": i.employment_type,
				"present_days":(td-count)-trd,
				"retention_days":trd,
				"earned_leaves":0,
			},)
			count=0
			trd=0

			for j in self.get('leave_allocation_permanant'):
				for k in self.get('leave_allocation_seasonal'):
					for l in self.get("earned_leave_calculation_details"):
						if l.employment_type =="PERMANENT":
							if l.present_days>=j.days_from and l.present_days<=j.days_to:
								l.earned_leaves=j.no_of_leaves
						else: 
							if l.present_days>=k.days_from and l.present_days<=k.days_to:
								l.earned_leaves=k.no_of_leaves

		
	@frappe.whitelist()
	def get_leave_allocation(self):
		lst=str(nowdate()).split('-')
		year=int(lst[0])
		self.from_date=datetime.date(year-1, 8, 1)
		self.to_date=datetime.date(year, 7, 31)
  
		for_permanant=[[345, 365, 18],[325, 344, 17],[305, 324, 16],[285, 304, 15],[265, 284, 14],[245, 264, 13],[225, 244, 12],[205, 224, 11],[185, 204, 10],[165, 184, 9],[145, 164, 8],[125, 144, 7],[105, 124, 6],[85, 104, 5],[65, 84, 4],[45, 64, 3],[25, 44, 2],[20, 24, 1]]
		for_seasonal=[[120, 365, 9],[107, 119, 8],[94, 106, 7],[81, 93, 6],[68, 80, 5],[55, 67, 4],[42, 54, 3],[29, 41, 2],[20, 28, 1]]

		for i in for_permanant:
			self.append("leave_allocation_permanant",
			{
				"days_from": i[0],
				"days_to": i[1],
				"no_of_leaves": i[2],
			},)	

		for j in for_seasonal:
			self.append("leave_allocation_seasonal",
			{
				"days_from": j[0],
				"days_to": j[1],
				"no_of_leaves": j[2],
			},)
			
