from odoo import models ,fields
import xlwt
import base64
from io import BytesIO

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    employee_id = fields.Many2one('employee.info', string="Employee ID")
    
    display_employee_name = fields.Char(
        string="Employee Name",
        related="employee_id.emp_name",
        readonly=True,
        store=False
    )
    def action_print_sales_excel(self):
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("Sales Report")

        sheet.col(0).width = 4000
        sheet.col(1).width = 3500
        sheet.col(2).width = 3500
        sheet.col(3).width = 4500
        sheet.col(4).width = 4000
        sheet.col(5).width = 9000
        sheet.row(0).height = 500
        sheet.row(1).height = 300

        title_style = xlwt.XFStyle()

        title_font = xlwt.Font()
        title_font.bold = True
        title_font.height = 320
        title_style.font = title_font

        title_align = xlwt.Alignment()
        title_align.horz = xlwt.Alignment.HORZ_CENTER
        title_align.vert = xlwt.Alignment.VERT_CENTER
        title_style.alignment = title_align

        title_pattern = xlwt.Pattern()
        title_pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        title_pattern.pattern_fore_colour = xlwt.Style.colour_map['olive_ega']
        title_style.pattern = title_pattern

        subtitle_style = xlwt.XFStyle()

        subtitle_font = xlwt.Font()
        subtitle_font.bold = True
        subtitle_font.italic = True
        subtitle_style.font = subtitle_font

        subtitle_style.alignment = title_align
        subtitle_style.pattern = title_pattern

        header_style = xlwt.XFStyle()

        header_font = xlwt.Font()
        header_font.bold = True
        header_font.colour_index = xlwt.Style.colour_map['white']
        header_style.font = header_font

        header_align = xlwt.Alignment()
        header_align.horz = xlwt.Alignment.HORZ_CENTER
        header_align.vert = xlwt.Alignment.VERT_CENTER
        header_style.alignment = header_align

        header_pattern = xlwt.Pattern()
        header_pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        header_pattern.pattern_fore_colour = xlwt.Style.colour_map['indigo']
        header_style.pattern = header_pattern

        header_borders = xlwt.Borders()
        header_borders.left = header_borders.right = header_borders.top = header_borders.bottom = xlwt.Borders.THIN
        header_style.borders = header_borders

        data_style = xlwt.XFStyle()

        data_align = xlwt.Alignment()
        data_align.vert = xlwt.Alignment.VERT_CENTER
        data_style.alignment = data_align

        data_borders = xlwt.Borders()
        data_borders.left = data_borders.right = data_borders.top = data_borders.bottom = xlwt.Borders.THIN
        data_style.borders = data_borders

        amount_style = xlwt.XFStyle()
        amount_style.num_format_str = '#,##0.000'
        amount_style.borders = data_borders

        sheet.write_merge(
            0, 0, 0, 5,
            self.company_id.name,
            title_style
        )

        sheet.write_merge(
            1, 1, 0, 5,
            "SALES REPORT 01-01-2026 To 06-01-2026",
            subtitle_style
        )

        headers = ["Order", "Customer", "Total", "Owner", "Untaxed Amount", "Payment Transactions Amount"]

        row = 3
        for col, header in enumerate(headers):
            sheet.write(row, col, header, header_style)

        row += 1
        total = 0.0

        for order in self:
            sheet.write(row, 0, order.name, data_style)
            sheet.write(row, 1, str(order.date_order.date()), data_style)
            sheet.write(row, 2, order.partner_id.id, data_style)
            sheet.write(row, 3, order.partner_id.name, data_style)
            sheet.write(row, 4, order.amount_total, amount_style)
            sheet.write(row, 5, order.user_id.name or '', data_style)
            total += order.amount_total
            row += 1

        sheet.write_merge(row, row, 0, 3, "Total", header_style)
        sheet.write(row, 4, total, amount_style)

        buffer = BytesIO()
        workbook.save(buffer)
        buffer.seek(0)

        attachment = self.env['ir.attachment'].create({
            'name': 'sales_report.xls',
            'type': 'binary',
            'datas': base64.b64encode(buffer.read()),
            'mimetype': 'application/vnd.ms-excel'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }