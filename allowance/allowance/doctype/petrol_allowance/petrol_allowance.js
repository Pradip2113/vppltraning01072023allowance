// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('Petrol Allowance', {
	get_details: function (frm) {
		frm.call({
			method:'get_Details',
			doc: frm.doc,
		});
	}
});

// frappe.ui.form.on('Petrol Allowance', {
// 	get_slipboy_details: function (frm) {
// 		frm.call({
// 			method:'get_SlipBoy',
// 			doc: frm.doc,
// 		});
// 	}
// });