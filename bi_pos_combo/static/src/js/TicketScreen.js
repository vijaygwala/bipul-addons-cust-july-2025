odoo.define("bi_pos_combo.TicketScreenInherit", function (require) {
    "use strict";

    const TicketScreen = require("point_of_sale.TicketScreen");
    const Registries = require("point_of_sale.Registries");
    const rpc = require("web.rpc");
    console.log("🔹 Orderlinesssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss:");

    const PosComboTicketScreen = (TicketScreen_) =>
        class extends TicketScreen_ {
            _doesOrderHaveSoleItem(order) {
                // 🔹 Call original method first
                const result = super._doesOrderHaveSoleItem(order);

                const orderlines = order.get_orderlines();
                console.log("🔹 Orderlinessssssssssssss:", orderlines);

                if (orderlines.length === 1) {
                    const theOrderline = orderlines[0];
                    debugger;
                    console.log("🔹 Combo product IDsssssssss:", theOrderline.combo_prod_ids);

                    // 👉 Extra condition: combo products


                    // 🔹 Call backend only once
                    if (!theOrderline.refundCalled) {
                        theOrderline.refundCalled = true;
                        rpc.query({
                            model: "pos.order.line",
                            method: "refund_combo_pro",
                            args: [[theOrderline.id]],
                        })
                            .then((res) => {
                                console.log("✅ Backend refund called:", res);
                            })
                            .catch((err) => {
                                console.error("❌ Backend refund error:", err);
                            });
                    }

                    return true; // Override result for combo

                }

                // 🔹 Fallback to original logic
                return result;
            }
        };

    Registries.Component.extend(TicketScreen, PosComboTicketScreen);

    return TicketScreen;
});

