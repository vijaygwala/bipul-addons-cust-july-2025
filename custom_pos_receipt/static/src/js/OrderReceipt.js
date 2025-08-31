odoo.define("custom_pos_receipt.maiOrderReceipt", function (require) {
  "use strict";

  const OrderReceipt = require("point_of_sale.OrderReceipt");
  const Registries = require("point_of_sale.Registries");
  const { onMounted } = owl;
  const rpc = require("web.rpc");

  const maiOrderReceipt = (OrderReceipt) =>
    class extends OrderReceipt {
      setup() {
        super.setup();
        onMounted(() => {
          let order = this.env.pos.get_order();
          let barcode = order.order_barcode.toString();
          if ($("#order_barcode").length > 0) {
            JsBarcode("#order_barcode", barcode);
          }
        });

        const currorder = this.props.order;
        // ensure every line has custom combo products
        for (let line of currorder.get_orderlines()) {
          if (
            !line.combo_prod_custom_ids ||
            !line.combo_prod_custom_ids.length
          ) {
            // fetch from server
            rpc
              .query({
                model: "product.combo.custom",
                method: "get_combo_products_by_order_line",
                args: [line.id || 0],
              })
              .then(function (result) {
                line.combo_prod_custom_ids = result || [];
                console.log(result);
              });
          }
        }
      }
    };

  Registries.Component.extend(OrderReceipt, maiOrderReceipt);
  return OrderReceipt;
});
