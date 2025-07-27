odoo.define('bi_pos_salesperson.OrderlineDetails', function(require) {
    'use strict';

   const PosComponent = require('point_of_sale.PosComponent');
   const Registries = require("point_of_sale.Registries");
   const OrderlineDetails = require("point_of_sale.OrderlineDetails");
   const { useListener } = require("@web/core/utils/hooks");


   const PosOrderlineDetails = (OrderlineDetails) =>
        class extends OrderlineDetails {
            setup() {
                super.setup();
			}
            imageUrl(id) {
			    return '/web/image?model=res.users&id='+id+'&field=image_1920';
            }
           
        };

    Registries.Component.extend(OrderlineDetails, PosOrderlineDetails);
    return OrderlineDetails;

    });
