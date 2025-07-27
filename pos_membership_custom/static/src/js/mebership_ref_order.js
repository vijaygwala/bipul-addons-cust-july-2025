/** @odoo-module **/

import models from 'point_of_sale.models';
import {Order,Orderline} from 'point_of_sale.models';
import  Registries from "point_of_sale.Registries";
const MembershipRef = (Order) => class MembershipRef extends Order {
     constructor() {
     super(...arguments);
     this.membership_card_id = this.membership_card_id || null;
     }
     set_order_membership(membership_card_id){
     this.membership_card_id = membership_card_id
     }
     //send order data to send to the server
     export_as_JSON() {
     const json = super.export_as_JSON(...arguments)
     json.membership_card_id = this.membership_card_id ;
     return json;
     }
     init_from_JSON(json) {
     super.init_from_JSON(...arguments);
      this.membership_card_id = json.membership_card_id;
      }
     };
     Registries.Model.extend(Order, MembershipRef);


     const OrderlineExtended = (Orderline) => class OrderlineExtended extends Orderline {
          constructor() {
          super(...arguments);
          this.association_id = this.association_id || null;
          }
          set_association_id(association_id){
          this.association_id = association_id
          }
          //send order data to send to the server
          export_as_JSON() {
          const json = super.export_as_JSON(...arguments)
          json.association_id = this.association_id ;
          return json;
          }
          init_from_JSON(json) {
          super.init_from_JSON(...arguments);
           this.association_id = json.association_id;
           }
          };
          Registries.Model.extend(Orderline, OrderlineExtended);
