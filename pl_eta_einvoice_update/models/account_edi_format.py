# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.l10n_eg_edi_eta.models.account_edi_format import AccountEdiFormat
import logging

_logger = logging.getLogger(__name__)

class AccountEdiFormatCustom(models.Model):
    _inherit = 'account.edi.format'

    @api.model
    def _l10n_eg_eta_prepare_address_data(self, partner, invoice, issuer=False):
        address = {
            'address': {
                'country': partner.country_id.code,
                'governate': partner.state_id.name or '',
                'regionCity': partner.city or '',
                'street': partner.street or '',
                'buildingNumber': partner.l10n_eg_building_no or '',
                'postalCode': partner.zip or '',
            },
            'name': partner.name,
        }
        if issuer:
            address['address']['branchID'] = invoice.journal_id.l10n_eg_branch_identifier or ''
        individual_type = self._l10n_eg_get_partner_tax_type(partner, issuer)
        address['type'] = individual_type or ''
        address['id'] = ''
        if invoice.amount_total >= invoice.company_id.l10n_eg_invoicing_threshold or individual_type != 'P':
            address['id'] = partner.vat
        _logger.info('Address Data: %s' % address)
        return address

    @api.model
    def _l10n_eg_validate_info_address(self, partner_id, issuer=False, invoice=False):
        fields = ["country_id"]
        if (invoice and invoice.amount_total >= invoice.company_id.l10n_eg_invoicing_threshold):
            fields = ["country_id",
                      "state_id", "city", "street",
                      "l10n_eg_building_no", "vat"]
        return all(partner_id[field] for field in fields)


AccountEdiFormat._l10n_eg_eta_prepare_address_data = AccountEdiFormatCustom._l10n_eg_eta_prepare_address_data
AccountEdiFormat._l10n_eg_validate_info_address = AccountEdiFormatCustom._l10n_eg_validate_info_address