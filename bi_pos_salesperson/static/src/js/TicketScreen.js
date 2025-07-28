odoo.define('bi_pos_salesperson.TicketScreen', function(require) {
	"use strict";

	const Registries = require('point_of_sale.Registries');
	const TicketScreen = require('point_of_sale.TicketScreen');
	const { useListener } = require("@web/core/utils/hooks");

	const BiTicketScreen = (TicketScreen) =>
		class extends TicketScreen {
			setup() {
            	super.setup();
            }
            _getToRefundDetail(orderline) {
                if (orderline.id in this.env.pos.toRefundLines) {
                    return this.env.pos.toRefundLines[orderline.id];
                } else {
                    const partner = orderline.order.get_partner();
                    const orderPartnerId = partner ? partner.id : false;
                    const newToRefundDetail = {
                        qty: 0,
                        orderline: {
                            id: orderline.id,
                            productId: orderline.product.id,
                            price: orderline.price,
                            qty: orderline.quantity,
                            refundedQty: orderline.refunded_qty,
                            orderUid: orderline.order.uid,
                            orderBackendId: orderline.order.backendId,
                            orderPartnerId,
                            tax_ids: orderline.get_taxes().map(tax => tax.id),
                            discount: orderline.discount,
                            pack_lot_lines: orderline.pack_lot_lines ? orderline.pack_lot_lines.map(lot => {
                                return { lot_name: lot.lot_name };
                            }) : false,
                            customer_id: orderline.customer_id,
                            customer_name: orderline.customer_name,
    
                        },
                        destinationOrderUid: false,
                    };
                    this.env.pos.toRefundLines[orderline.id] = newToRefundDetail;
                    return newToRefundDetail;
                }
            }
            _getRefundableDetails(partner) {
                return Object.values(this.env.pos.toRefundLines).filter(
                    ({ qty, orderline, destinationOrderUid ,customer_id ,customer_name }) =>
                        !this.env.pos.isProductQtyZero(qty) &&
                        (partner ? orderline.orderPartnerId == partner.id : true) &&
                        !destinationOrderUid
                );
            }
            _prepareRefundOrderlineOptions(toRefundDetail) {
                const { qty, orderline } = toRefundDetail;
                const draftPackLotLines = orderline.pack_lot_lines ? { modifiedPackLotLines: [], newPackLotLines: orderline.pack_lot_lines} : false;
                return {
                    quantity: -qty,
                    price: orderline.price,
                    extras: { price_automatically_set: true },
                    merge: false,
                    refunded_orderline_id: orderline.id,
                    tax_ids: orderline.tax_ids,
                    discount: orderline.discount,
                    customer_id: orderline.customer_id,
                    customer_name: orderline.customer_name,
                    draftPackLotLines: draftPackLotLines
                };
            }
            async _onDoRefund() {
                const order = this.getSelectedSyncedOrder();
                if (!order) {
                    this._state.ui.highlightHeaderNote = !this._state.ui.highlightHeaderNote;
                    return;
                }
                
                if (this._doesOrderHaveSoleItem(order)) {
                    if (!this._prepareAutoRefundOnOrder(order)) {
                        // Don't proceed on refund if preparation returned false.
                        return;
                    }
                }
    
                const partner = order.get_partner();
    
                const allToRefundDetails = this._getRefundableDetails(partner);
                if (allToRefundDetails.length == 0) {
                    this._state.ui.highlightHeaderNote = !this._state.ui.highlightHeaderNote;
                    return;
                }
    
                // The order that will contain the refund orderlines.
                // Use the destinationOrder from props if the order to refund has the same
                // partner as the destinationOrder.
                const destinationOrder =
                    this.props.destinationOrder &&
                    partner === this.props.destinationOrder.get_partner() &&
                    !this.env.pos.doNotAllowRefundAndSales()
                        ? this.props.destinationOrder
                        : this._getEmptyOrder(partner);
    
                //Add a check too see if the fiscal position exist in the pos
                if (order.fiscal_position_not_found) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Fiscal Position not found'),
                        body: this.env._t('The fiscal position used in the original order is not loaded. Make sure it is loaded by adding it in the pos configuration.')
                    });
                    return;
                }
    
                // Add orderline for each toRefundDetail to the destinationOrder.
                for (const refundDetail of allToRefundDetails) {
                    const product = this.env.pos.db.get_product_by_id(refundDetail.orderline.productId);
                    const options = this._prepareRefundOrderlineOptions(refundDetail);
                    await destinationOrder.add_product(product, options);
                    let dest_order_lines = destinationOrder.orderlines
                    for (let i = 0; i < dest_order_lines.length; i++) {
                        if(dest_order_lines[i].refunded_orderline_id === refundDetail.orderline.id){
                            dest_order_lines[i].customer_id = refundDetail.orderline.customer_id;
                            dest_order_lines[i].customer_name = refundDetail.orderline.customer_name;
                        }
                    }
                    refundDetail.destinationOrderUid = destinationOrder.uid;
                }
                destinationOrder.fiscal_position = order.fiscal_position;
                // Set the partner to the destinationOrder.
                if (partner && !destinationOrder.get_partner()) {
                    destinationOrder.set_partner(partner);
                    destinationOrder.updatePricelist(partner);
                }
    
                if (this.env.pos.get_order().cid !== destinationOrder.cid) {
                    this.env.pos.set_order(destinationOrder);
                }
    
                this._onCloseScreen();
            }
		};
        

	Registries.Component.extend(TicketScreen, BiTicketScreen);

	return TicketScreen;

});
