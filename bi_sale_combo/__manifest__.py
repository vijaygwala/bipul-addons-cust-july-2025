{
    "name": "BI Sale Combo Wizard",
    "version": "1.0.0",
    "category": "Sales",
    "summary": "Open a wizard when a combo product is selected on sale order line and add its pack items",
    "description": "When a product with is_pack True is selected in sale.order.line a transient wizard opens allowing selection of required and optional pack items to be added as sale.order.line items.",
    "author": "ChatGPT for Vijay Gwala",
    "depends": ["sale", "product","bi_pos_combo"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_line_combo_wizard_views.xml"
    ],
    "installable": True,
    "application": False
}