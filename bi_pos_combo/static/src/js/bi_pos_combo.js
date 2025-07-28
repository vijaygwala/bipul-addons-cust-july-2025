odoo.define('bi_pos_combo.pos', function(require) {
	"use strict";

	var core = require('web.core');
	var utils = require('web.utils');
	var round_pr = utils.round_precision;
	var field_utils = require('web.field_utils');
	const Registries = require('point_of_sale.Registries');
	var { Order, Orderline, PosGlobalState} = require('point_of_sale.models');
	var round_di = utils.round_decimals;

	const POSComboProduct = (PosGlobalState) => class POSComboProduct extends PosGlobalState {

		async _processData(loadedData) {
			await super._processData(...arguments);
			this.product_pack = loadedData['product.pack'] || [];
		}
	}

	Registries.Model.extend(PosGlobalState, POSComboProduct);



	const BiCustomOrderLine = (Orderline) => class BiCustomOrderLine extends Orderline{

		constructor(obj, options){
			super(...arguments);
			this.pos   = options.pos;
			this.order = options.order;
			var self = this;
			if (options.json) {
				this.init_from_JSON(options.json);
				return;
			}
			this.combo_products = this.combo_products;
			var final_data = self.pos.final_products;

			if(final_data){
				for (var i = 0; i < final_data.length; i++) {
					if(final_data[i] == undefined){
						i=i+1;
						if(final_data[i][0] == this.product.id){
							let combo_list = self.prepare_combo_list(final_data[i][1])

							this.combo_products = final_data[i][1];
							self.pos.final_products = null;
						}
					}
					else{
						if(final_data[i][0] == undefined){
							return;
						}
						if(final_data[i][0] == this.product.id){
							this.combo_products = final_data[i][1];
							self.pos.final_products = null;
						}
					}
				}
			}
			this.set_combo_products(this.combo_products);
			this.combo_prod_ids =  this.combo_prod_ids || [];
			this.is_pack = this.is_pack;

		}
		
		clone(){
			const orderline = super.clone(...arguments);
			orderline.is_pack = this.is_pack;
			orderline.price_manually_set = this.price_manually_set;
			orderline.combo_prod_ids = this.combo_prod_ids || [];
			orderline.combo_products = this.combo_products || [];
			return orderline;
		}
		init_from_JSON(json){
			super.init_from_JSON(...arguments);

			this.combo_prod_ids = json.combo_prod_ids;
			if(json.combo_products){
				this.combo_products = json.combo_products && JSON.parse(json.combo_products);
			}
			this.is_pack = json.is_pack;
		}
		export_as_JSON(){

			const json = super.export_as_JSON(...arguments);

			var json_data = JSON.stringify(this.combo_products)
			json.combo_products = this.combo_products && JSON.stringify(this.combo_products);
			json.combo_prod_ids= this.combo_prod_ids;
			json.is_pack=this.is_pack;
			return json;
		}
		export_for_printing(){
			const json = super.export_for_printing(...arguments);
			json.combo_products = this.get_combo_products();
			json.combo_prod_ids= this.combo_prod_ids;
			json.is_pack=this.is_pack;
			return json;
		}
		set_combo_prod_ids(ids){
			this.combo_prod_ids = ids
		}


		prepare_combo_list(list_data){
			var combo_data = [];
			list_data.forEach(function (prod) {
				if(prod != null){

					var prd_data = {
						'active': prod.active,
						'applicablePricelistItems': prod.applicablePricelistItems,
						'attribute_line_ids' : prod.attribute_line_ids,
						'available_in_pos': prod.available_in_pos,
						'barcode': prod.barcode,
						'categ': prod.categ,
						'categ_id': prod.categ_id,
						'cid': prod.cid,
						'combo_qty': prod.combo_qty,
						'combo_limit': prod.combo_limit,
						'optional_limit_qty': prod.optional_limit_qty,
						'default_code': prod.default_code,
						'description': prod.description,
						'description_sale': prod.description_sale,
						'display_name': prod.display_name,
						'id': prod.id,
						'lst_price': prod.lst_price,
						'is_pack': prod.is_pack,
						'pack_ids': prod.pack_ids,
						'standard_price': prod.standard_price,
						'taxes_id': prod.taxes_id,
						'type': prod.type,
						'image_128': prod.image_128,
						'invoice_policy': prod.invoice_policy,
						'optional_product_ids': prod.optional_product_ids,
						'parent_category_ids': prod.parent_category_ids,
						'pos_categ_id': prod.pos_categ_id,
						'product_image_url': prod.product_image_url,
						'product_tmpl_id': prod.product_tmpl_id,
						'to_weight': prod.to_weight,
						'tracking': prod.tracking,
						'uom_id': prod.uom_id,
						"__last_update": prod.__last_update
					}

					combo_data.push(prd_data)
				}
			});

			return combo_data
		}

		set_combo_products(products){
			var ids = [];
			if(this.product.is_pack)
			{	
				if(products)
				{
					products.forEach(function (prod) {
						if(prod != null)
						{
							ids.push(prod.id)
						}
					});
				}
				var list_data = this.prepare_combo_list(products)
				this.combo_products = list_data;
				this.set_combo_prod_ids(ids)
				if(this.combo_prod_ids)
				{
					this.set_combo_price(this.price);
				}
			}

		}
		set_is_pack(is_pack){
			this.is_pack = is_pack
		}
		set_unit_price(price){
			this.order.assert_editable();
			if(this.product.is_pack)
			{
				this.set_is_pack(true);
				var prods = this.get_combo_products()
				var total = price;
			
				this.price = round_di(parseFloat(total) || 0, this.pos.dp['Product Price']);
			}
			else{
				this.price = round_di(parseFloat(price) || 0, this.pos.dp['Product Price']);
			}
		}
		set_combo_price(price){
			var prods = this.get_combo_products()
			var total = 0;
			prods.forEach(function (prod) {
				if(prod)
				{
					total += prod.lst_price	* prod.combo_qty
				}	
			});
			if(self.pos.config.combo_pack_price== 'all_product'){
				this.set_unit_price(total);
			}
			else{
				let prod_price = this.product.lst_price;
				this.set_unit_price(prod_price);
			}
		}
		get_combo_products(){
			self = this;
			if(this.product.is_pack)
			{
				var get_sub_prods = [];
				if(this.combo_products)
				{
					return this.combo_products
				}

				if(this.combo_prod_ids)
				{
					this.combo_prod_ids.forEach(function (prod) {
						var sub_product = self.pos.db.get_product_by_id(prod);
						get_sub_prods.push(sub_product)
					});
					return get_sub_prods;
				}
				
			}
		}


	}
	Registries.Model.extend(Orderline, BiCustomOrderLine);


	const CustomOrder = (Order) => class CustomOrder extends Order{
		constructor(obj, options){
			super(...arguments);
			this.barcode = this.barcode || "";
		}

	}
	Registries.Model.extend(Order, CustomOrder);
});
