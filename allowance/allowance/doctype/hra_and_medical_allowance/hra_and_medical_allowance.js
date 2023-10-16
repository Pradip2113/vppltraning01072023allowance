// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt


frappe.ui.form.on('HRA and Medical Allowance', {
	get_details: function (frm) {
		frm.call({
			method:'get_Details',
			doc: frm.doc,
		});
	}
});

frappe.ui.form.on('HRA and Medical Allowance', {
	calculate_payroll: function (frm) {
		frm.clear_table("hra_and_medical_allowance_details")
		frm.refresh_field("hra_and_medical_allowance_details")
		frm.call({
			method:'calculate_payroll',
			doc: frm.doc,
			payroll_date:frm.doc,
		});
	}
});