// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('Retention', {
	to_date(frm) {
		frm.call({
		    method:"calculate_total_days",
		    doc:frm.doc,
		})
	},
	// 	from_date(frm) {
	// 	frm.call({
	// 	    method:"calculate_total_days",
	// 	    doc:frm.doc,
	// 	})
	// }
})
