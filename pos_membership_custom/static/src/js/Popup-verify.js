odoo.define('pos_membership_custom.MembershipPopupVerify', function (require) {
    'use strict';
    const { Gui } = require('point_of_sale.Gui');
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { _t } = require('web.core');
    var rpc = require('web.rpc');
    const { useState, useRef, onMounted ,EventBus,useEffect} = owl;
    
    const bus = new EventBus();

    //Creates a pop up for membership
    class MembershipPopupVerify extends AbstractAwaitablePopup {
        setup() {
            super.setup();
            this.gifts = useState([])
            this.verify_state = useState({ card: false, code: '', selected_gift: false, discount_msg: '' })
            this.env.pos.card = false;
            let customer = this.env.pos.get_order().get_partner()
            let self = this
            var code = rpc.query({
                model: 'res.partner',
                method: 'get_membership_code',
                args: [[customer.id]]
            }).then(function (code) {

                self.verify_state.code = code

            })

            // bus.on("Membership_check", this, this.Membership_check);
            // this.pbc = this.Membership_check.bind(this);
            onMounted(async () => {
                this.do_check();
            });

         
        
            

        }
        async getGiftProduct(event) {

            this.verify_state.selected_gift = event.target.value



        }

        do_check() {
            return new Promise((resolve) => {
                setTimeout(() => {
                    this.Membership_check();
                    resolve(); // Ensure the promise resolves after calling Membership_check()
                }, 2000); // Simulated async delay
            });
        }
      

        // This is used to check the customer has membership
        async Membership_check() {
            var customer_details = []
            const customerInput = $('.card_code').val();
            var order = this.env.pos.get_order()
            var customer = order.get_partner().id
            customer_details.push({
                'customerInput': customerInput,
                'customer': customer
            })
            var self = this
            //This is used to retrieve the customers membership details
            var cardd = await rpc.query({
                model: 'membership.card',
                method: 'membership_card_check',
                args: [, customer_details]
            }).then(function (card) {

                console.log(card)

                self.verify_state.card = card
                self.env.pos.card = card
                if (card.is_discount_applied) {
                    self.verify_state.discount_msg = ""
                }
                else {
                    
                    self.verify_state.discount_msg = "Discount is only aaplicable in event month"
                }

                console.log(self.verify_state.card)
                if (self.verify_state.card == 0) {
                    $("#cnfm-btn").prop("disabled", true);
                    Gui.showPopup('ErrorPopup', {
                        title: _t('Membership'),
                        body: _t('Your Card is Expired/Invalid Please check you have membership.')
                    });

                    return 0
                }
                self.verify_state.card.gifts.forEach((gift, index, array) => {

                    self.gifts.push({
                        product_id: gift.product_id,
                        name: gift.name,
                        qty: gift.qty,
                        association_id: gift.association_id,
                        visible: true
                    })

                    self.verify_state[gift.product_id.toString() + "-" + gift.association_id.toString()] = gift.qty

                });
                order.get_orderlines().forEach(function (t) {
                    self.gifts.forEach((gift, index, array) => {


                        if (gift.product_id == t.product.id || gift.association_id == t.association_id) {
                            if (gift.product_id == t.product.id) {
                                gift.qty = gift.qty - t.quantity

                                if (gift.qty <= 0) {
                                    gift.visible = false
                                }

                            }
                            else {
                                gift.visible = false
                            }
                        }

                        self.verify_state[gift.product_id.toString() + "-" + gift.association_id.toString()] = gift.qty


                    });

                })

                let temp_lst = self.gifts.filter(item => item.visible === true)

                if (temp_lst.length != 0) {
                    self.verify_state.selected_gift = temp_lst[0].product_id.toString() + "-" + temp_lst[0].association_id.toString()

                }


                if (self.verify_state.card.purchase_amount < self.verify_state.card.membership_limit_amount) {
                    // $("#fields-div").css("display", "none !important");
                    // $("#verified-info-div").css("display", "none !important");
                    $("#msg-display-div").css("display", "inline-block !important");
                }
                else {
                    $("#msg-display-div").css("display", "none");
                }

            })
        }
        //Confirms the membership
        async confirm() {
            var order = this.env.pos.get_order();
            var lines = order.get_orderlines();
            var self = this
            if (this.env.pos.card) {
                var product = this.env.pos.db.get_product_by_id(this.env.pos.card.product_id);
            }
            else {
                var product = 'undefined'
                await this.showPopup('ErrorPopup', {
                    title: this.env._t("No Membership discount product found"),
                    body: this.env._t("The discount product seems misconfigured.Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'.Also confirm the customer has membership card."),
                });
                return;
            }
            // Remove existing discounts and add new discount
            if (this.env.pos.card.is_discount_applied) {
                lines.filter(line => line.get_product() === product)
                    .forEach(line => order.remove_orderline(line));
                let linesByTax = order.get_orderlines_grouped_by_tax_ids();
                for (let [tax_ids, lines] of Object.entries(linesByTax)) {
                    // Note that tax_ids_array is an Array of tax_ids that apply to these lines
                    // That is, the use case of products with more than one tax is supported.
                    let tax_ids_array = tax_ids.split(',').filter(id => id !== '').map(id => Number(id));
                    let baseToDiscount = order.calculate_base_amount(tax_ids_array, lines.filter(ll => !ll.reward_id && (!this.env.pos.config.tip_product_id || ll.product.id !== this.env.pos.config.tip_product_id[0])));
                    // We add the price as manually set to avoid re computation when changing customer.
                    let discount = - parseFloat(this.env.pos.card.discount) / 100.0 * baseToDiscount;
                    console.log(discount)
                    if (discount < 0) {

                        order.add_product(product, {
                            price: discount,
                            lst_price: discount,
                            tax_ids: tax_ids_array,
                            merge: false,
                            description:
                                `${this.env.pos.card.discount}%, ` +
                                (tax_ids_array.length ?
                                    _.str.sprintf(
                                        this.env._t('Tax: %s'),
                                        tax_ids_array.map(taxId => this.env.pos.taxes_by_id[taxId].amount + '%').join(', ')
                                    ) :
                                    this.env._t('No tax')),
                            extras: {
                                price_automatically_set: true,
                            },
                        });
                        //add gift products

                    }

                }
            }
            if (this.verify_state.selected_gift) {
                console.log(self.verify_state.selected_gift)

                let gift_item = this.env.pos.db.get_product_by_id(parseInt(this.verify_state.selected_gift.split("-")[0]));
                order.add_product(gift_item, {
                    price: 0.0,
                    lst_price: 0.0,
                    quantity: this.verify_state[this.verify_state.selected_gift],
                    association_id: parseInt(this.verify_state.selected_gift.split("-")[1]),
                    merge: false,
                    extras: {
                        price_automatically_set: true,
                    },
                });

                order.get_orderlines().forEach(function (t) {
                    if (t.get_product() === gift_item) {
                        t.set_association_id(parseInt(self.verify_state.selected_gift.split("-")[1]))
                    }
                })




            }
            console.log("outside XXXX")

            order.set_order_membership(this.env.pos.card.card_id);
            this.env.posbus.trigger('close-popup', {
                popupId: this.props.id,
                response: { confirmed: true, payload: null },
            });


            // // remove the or items for the added product
            // let selected_prod = parseInt(this.verify_state.selected_gift.split("-")[0])
            // let assoc_id = parseInt(this.verify_state.selected_gift.split("-")[1])



        }
    }
    //Create membership popup
    MembershipPopupVerify.template = 'MembershipPopupVerify';
    MembershipPopupVerify.defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
        title: 'Membership Card',
        body: '',
    };
    Registries.Component.add(MembershipPopupVerify);
    return MembershipPopupVerify;
});
