odoo.define('pos_salesperson_app.Orderline', function(require) {
	"use strict";

	const PosComponent = require('point_of_sale.PosComponent');
	const Orderline = require('point_of_sale.Orderline');
	const Registries = require('point_of_sale.Registries');


	const PosSalesOrderline = (Orderline) =>
		class extends Orderline{
			setup() {
            	super.setup();
			}

			addUser(){
				var self = this;
				var sales_user = {};
				for (var i = 0; i < self.env.pos.users.length; i++){
					sales_user[self.env.pos.users[i].id] = self.env.pos.users[i].name
				}
				var current_line = this.props.line
				this.showPopup('SalesPersonPopupWidget', {
					title: this.env._t('Sales Person'),
					startingValue: sales_user,
					list: current_line,
				});
			}

			removeUser(){
				var self = this;
				var order = this.env.pos.get_order();
				this.trigger('select-line', { orderline: this.props.line });
				order.get_selected_orderline().set_sales_person(false, false);
				var add_user = $('.add_salesuser');
				var info_user = $('.user_info');
				for (var i = 0; i < add_user.length; i++){
					if ($(add_user[i]).find('.user_add_id').val() == this.props.line.id){
						$(add_user[i]).show();
					}
				}
				for (var i = 0; i < info_user.length; i++){
					if ($(info_user[i]).find('.user_info_id').val() == this.props.line.id){
						$(info_user[i]).hide();
					}
				}
			}
		};
	Registries.Component.extend(Orderline, PosSalesOrderline);
});
