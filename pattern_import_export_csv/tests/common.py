# Copyright 2020 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=missing-manifest-dependency

import base64
import csv
import io
from os import path
# pylint: disable=odoo-addons-relative-import
from odoo.addons.pattern_import_export.tests.common import ExportPatternCommon
from odoo.tests.common import SavepointCase

DEBUG_SAVE_EXPORTS = True
CSV_LINE_DELIMITER = "\n"
CSV_VAL_DELIMITER = ","
PATH = path.dirname(__file__)
CELL_VALUE_EMPTY = ""


class ExportPatternCsvCommon(ExportPatternCommon, SavepointCase):

    def _split_csv_str(self, astring):
        result = []
        for line in astring.split(CSV_LINE_DELIMITER):
            result.append([val for val in line.split(CSV_VAL_DELIMITER)])
        return result

    def _helper_get_resulting_csv(self, export, records):
        export._export_with_record(records)
        attachment = self._get_attachment(export)
        self.assertEqual(attachment.name, export.name + ".csv")
        decoded_data = base64.b64decode(attachment.datas).decode("utf-8")
        if DEBUG_SAVE_EXPORTS:
            full_path = PATH + export.name + ".csv"
            with open(full_path, "wt") as out:
                out.write(decoded_data)
        result = []
        for line in decoded_data.split("\r\n"):
            result.append([val for val in line.split(",")])
        return result