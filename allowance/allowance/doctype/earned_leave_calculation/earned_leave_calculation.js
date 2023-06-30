// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('Earned Leave Calculation', {
	get_details: function (frm) {
		frm.clear_table("earned_leave_calculation_details")
		frm.refresh_field('earned_leave_calculation_details')
		frm.call({
			method:'get_Details',
			doc: frm.doc,
		});
	},
	onload: function(frm) {
		frm.clear_table("leave_allocation_permanant")
		frm.refresh_field('leave_allocation_permanant')
		frm.clear_table("leave_allocation_seasonal")
		frm.refresh_field('leave_allocation_seasonal')
		frm.call({
			method:'get_leave_allocation',
			doc: frm.doc,
		});
	}
});
