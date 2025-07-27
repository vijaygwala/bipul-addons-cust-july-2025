odoo.define('pos_salesperson_app.pos', function(require) {
	"use strict";

	const { PosGlobalState, Orderline } = require('point_of_sale.models');
	const Registries = require('point_of_sale.Registries');

	const PosCustomPosGlobalState = (PosGlobalState) => class PosCustomPosGlobalState extends PosGlobalState {
	    async _processData(loadedData) {
	        await super._processData(...arguments);
            this.users = loadedData['users'];
	    }
    }
    Registries.Model.extend(PosGlobalState, PosCustomPosGlobalState);

    const PosOrderline = (Orderline) => class PosOrderline extends Orderline {
    	constructor() {
        	super(...arguments);
			this.sales_person_id;
			this.image;
    	}

		set_sales_person(sales_person_id, user_name){
			this.sales_person_id = sales_person_id;
			if (sales_person_id){
				this.image = `/web/image?model=res.users&field=image_128&id=${sales_person_id}`;
			}
			this.sales_person_name = user_name;
		}

		export_as_JSON(){
	        const json = super.export_as_JSON(...arguments);
			json.sales_person_id = this.sales_person_id || false;
	        return json;
	    }
	}
    Registries.Model.extend(Orderline, PosOrderline);
});
