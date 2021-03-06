# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class workshop(models.Model):
#     _name = 'workshop.workshop'
#     _description = 'workshop.workshop'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class MarketCode(models.Model):
    _name = 'product.template.market.code'
    _description = 'Market Code'

    _sql_constraints = [('unique_name',

                         'UNIQUE (name)',

                         'Market code already exists'), ]
    name = fields.Char()
    factor_id = fields.Many2one('product.template.sales.factor', 'Sales Factor')

    
class SalesFactor(models.Model):
    _name = 'product.template.sales.factor'
    _description = 'Pricing Factor'

    name = fields.Char()
    sequence = fields.Integer(default=1)
    factor = fields.Float('Sales Factor', default=1)


class Product(models.Model):
    _inherit = 'product.template'

    # market_code = fields.Char()
    # factor_id = fields.Many2one('market.market_code', 'Market Code', tracking=True, help='Get the products market code', copy=False)
    sales_factor = fields.Many2one('product.template.sales.factor', related='market_code.factor_id', string='Sales Factor', tracking=True)
    market_code = fields.Many2one('product.template.market.code', 'Market Code', tracking=True)
    # list_price: catalog price, user defined
#     list_price = fields.Float(
#         'Sales Price', default=1.0,
#         digits='Product Price',
#         help="Price at which the product is sold to customers.")
    l_price = fields.Float('Compute Sales Price', default=1.0, digits='Product Price')

    @api.onchange('sales_factor', 'market_code')
    def _cal_list_price(self):
        for record in self:
#             record.l_price = record.standard_price * record.sales_factor.factor
            record.list_price = record.standard_price * record.sales_factor.factor
            # record.update({
            #     'list_price': list_price
            # })
            
    def _cal_update_all_list_price(self):
        products = self.env['product.template'].search([('type','=','product')])
        for product in products:
          if product.sales_factor:
            list_price = product.standard_price * product.sales_factor.factor
            product.write({'list_price': list_price})
