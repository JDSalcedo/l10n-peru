# -*- coding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2012 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info@vauxoo.com
############################################################################
#    Coded by: Julio Serna (julio@vauxoo.com)
############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp.osv import fields, osv
from openerp.tools.translate import _

import unicodedata

class account_invoice(osv.Model):
    
    _inherit = 'account.invoice'
    
    def unaccented(self, cadena):
        s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena)) if unicodedata.category(c) != 'Mn'))
        return s.decode()

    def check_ruc_dni(self, cr, uid, ids, context=None):
        country = False
        vat_pe = False
        for inv in self.browse(cr, uid, ids, context=context):
            if inv.type in ('out_invoice', 'out_refund'):
                partner = inv.partner_id.commercial_partner_id
                if inv.user_id.company_id.partner_id.country_id.name:
                    country = self.unaccented(inv.user_id.company_id.partner_id.country_id.name).lower() == 'peru'
                if inv.user_id.company_id.partner_id.vat:
                    if (inv.user_id.company_id.partner_id.vat).lower()[0:2] == 'pr' or \
                        (inv.user_id.company_id.partner_id.vat).lower()[0:2] == 'pd':
                        vat_pe = inv.user_id.company_id.partner_id.vat
                if not ((country and vat_pe) or (country and not vat_pe) or (not country and vat_pe)):
                    return True
                elif partner.vat:
                    return True
                else:
                    return False
        return True

    def check_ruc(self, cr, uid, ids, context=None):
        country = False
        vat_pe = False
        for inv in self.browse(cr, uid, ids, context=context):
            if inv.type in ('out_invoice', 'out_refund'):
                partner = inv.partner_id.commercial_partner_id
                partner_company = partner.is_company
                if inv.user_id.company_id.partner_id.country_id.name:
                    country = self.unaccented(inv.user_id.company_id.partner_id.country_id.name).lower() == 'peru'
                if inv.user_id.company_id.partner_id.vat:
                    if (inv.user_id.company_id.partner_id.vat).lower()[0:2] == 'pr' or \
                        (inv.user_id.company_id.partner_id.vat).lower()[0:2] == 'pd':
                        vat_pe = inv.user_id.company_id.partner_id.vat
                if not ((country and vat_pe) or (country and not vat_pe) or (not country and vat_pe)):
                    return True
                elif (partner_company and partner.vat) or (not partner_company):
                    return True
                else:
                    return False
        return True
    
    def show_message_ruc_dni(self, cr, uid, ids, context=None):
        result = self.check_ruc(cr, uid, ids, context=context)
        if not result:
            raise osv.except_osv(_('Invalid Action!'), _('Not RUC set'))
        return True

    def show_message_ruc_dni2(self, cr, uid, ids, context=None):
        result = self.check_ruc_dni(cr, uid, ids, context=context)
        if not result:
            raise osv.except_osv(_('Invalid Action!'), _('Not RUC or DNI set'))
        return True
