# -*- coding: utf-8 -*-
from openerp import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _get_default_product_code(self):
        return self.env['ir.sequence'].get('product.code')

    product_code = fields.Char("Product Code", index=True, help='Product Code',
                               default=_get_default_product_code, copy=False)

    _sql_constraints = [
        ('product_product__product_code__uniq',
         'unique (product_code)',
         'Product code must be uniq!'),
    ]

    @api.multi
    def action_set_product_code(self):
        for product in self:
            if not product.product_code:
                tmpres = self._get_default_product_code()
                product.write({
                    'product_code': tmpres,
                    'barcode': tmpres,
                })
        return True


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_code = fields.Char('Product Code', store=True, index=True,
                               related='product_variant_ids.product_code',
                               readonly=True, help='Product code')

    @api.multi
    def action_set_product_code(self):
        for tmpl in self.filtered(lambda r: len(r.product_variant_ids) == 1):
            tmpl.product_variant_ids[0].action_set_product_code()
        return True
