odoo.define('bi_pos_salesperson.pos', function(require) {
	"use strict";

	const Registries = require('point_of_sale.Registries');
	var { Order, Orderline, PosGlobalState} = require('point_of_sale.models');
	var utils = require('web.utils');
	var round_di = utils.round_decimals;
	var round_pr = utils.round_precision;
	

	const PoSSalePerson = (PosGlobalState) => class PoSSalePerson extends PosGlobalState {
		async _processData(loadedData) {
			await super._processData(...arguments);
			var self = this;
			this.users = loadedData['res.users'];
			this.pos_salesperson_record = [];
			_.each(this.config.allow_user_ids, function(allow_user){
                _.each( loadedData['users'], function(user){
                    if (allow_user == user.id){
                        self.pos_salesperson_record.push(user);
                    }
                });
            });
		}
	}

	Registries.Model.extend(PosGlobalState, PoSSalePerson);


	const PosOrderLine = (Orderline) => class PosOrderLine extends Orderline {
		constructor(obj, options) {
			super(...arguments);
			this.customer_name = this.customer_name || '';
			this.customer_id = this.customer_id || '';
		}
		clone(){
			const orderline = super.clone(...arguments);
			orderline.customer_name = this.customer_name;
	        orderline.customer_id = this.customer_id;
			return orderline;
		}
		set_customer_name(customer_name){
			this.customer_name = customer_name;
		}
		get_customer_name(){
			return this.customer_name;
		}
		set_customer_id(customer_id){
			this.customer_id = customer_id;
		}
		get_customer_id(){
			return this.customer_id;
		}
		export_as_JSON() {			
			const json = super.export_as_JSON(...arguments);
			json.customer_name = this.get_customer_name();
			json.customer_id = this.get_customer_id();
            return json;
		}
		init_from_JSON(json){
			super.init_from_JSON(...arguments);	
			this.set_customer_id(json.customer_id);
			this.set_customer_name(json.customer_name);
		}
		export_for_printing(){
			const json = super.export_for_printing(...arguments);
			json.customer_name = this.get_customer_name();
			json.customer_id = this.get_customer_id();
			return json;
		}
		can_be_merged_with(orderline){
			var price = parseFloat(round_di(this.price || 0, this.pos.dp['Product Price']).toFixed(this.pos.dp['Product Price']));
			var order_line_price = orderline.get_product().get_price(orderline.order.pricelist, this.get_quantity());
			order_line_price = round_di(orderline.compute_fixed_price(order_line_price), this.pos.currency.decimal_places);
			if( this.get_product().id !== orderline.get_product().id){    //only orderline of the same product can be merged
				return false;
			}else if(!this.get_unit() || !this.get_unit().is_pos_groupable){
				return false;
			}else if(this.get_discount() > 0){             // we don't merge discounted orderlines
				return false;
			}else if(!utils.float_is_zero(price - order_line_price - orderline.get_price_extra(),
						this.pos.currency.decimal_places)){
				return false;
			}else if(this.product.tracking == 'lot' && (this.pos.picking_type.use_create_lots || this.pos.picking_type.use_existing_lots)) {
				return false;
			}else if (this.description !== orderline.description) {
				return false;
			}else if (orderline.get_customer_note() !== this.get_customer_note()) {
				return false;
			}else if (orderline.get_customer_name() !== this.get_customer_name()) {
				return false;
			}else if (orderline.get_customer_id() !== this.get_customer_id()) {
				return false;
			} else if (this.refunded_orderline_id) {
				return false;
			}else{
				return true;
			}
		}
	}
	Registries.Model.extend(Orderline, PosOrderLine);




});
