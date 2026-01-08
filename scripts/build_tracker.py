#!/usr/bin/env python3
"""
LinkedIn Hand-Raiser Engagement Tracker Builder
Generates production-grade Excel workbook with formulas, formatting, and sample data pre-built
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, FormulaRule
from datetime import datetime, timedelta
import os

def create_tracker_workbook():
    """Create the complete LinkedIn engagement tracker workbook"""

    # Create workbook
    wb = Workbook()

    # Remove default sheet
    if 'Sheet' in wb.sheetnames:
        wb.remove(wb['Sheet'])

    # Create the three main sheets
    create_post_performance_sheet(wb)
    create_dashboard_sheet(wb)
    create_response_tracker_sheet(wb)

    # Save to tracking folder
    output_path = os.path.expanduser('~/tk_projects/linkedin-hand-raiser-system/tracking/linkedin_engagement_tracker.xlsx')
    wb.save(output_path)
    print(f"✅ Tracker created successfully: {output_path}")
    return output_path

def create_post_performance_sheet(wb):
    """TAB 1: Post Performance Tracker"""
    ws = wb.create_sheet("Post Performance Tracker", 0)

    # Define headers
    headers = [
        'Post ID', 'Date Posted', 'Vertical', 'Pain Point', 'Post Type',
        'Impressions', 'Likes', 'Comments', 'Shares', 'DMs Received',
        'Videos Sent', 'Demos Booked', 'Notes',
        'Total Engagement', 'Engagement %', 'Conversion %',
        'Video→Demo %', 'Cost/Engage', 'Tier', 'Status'
    ]

    # Write headers (Row 1)
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num, value=header)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="4A90E2", end_color="4A90E2", fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # Sample data (6 posts)
    sample_data = [
        ['EC-001', datetime(2025, 1, 13), 'Electrical', 'Material Cost Overruns', 'Hand-Raiser',
         1247, 63, 8, 2, 5, 5, 2, 'High engagement on copper price spike'],
        ['EC-002', datetime(2025, 1, 15), 'Electrical', 'Labor Burden', 'Hand-Raiser',
         892, 34, 3, 1, 2, 2, 0, 'Lower engagement, may need refinement'],
        ['HV-001', datetime(2025, 1, 15), 'HVAC', 'Labor Burden Blindness', 'Hand-Raiser',
         1583, 87, 12, 4, 8, 7, 3, 'Strong resonance on "80% done" angle'],
        ['PL-001', datetime(2025, 1, 17), 'Plumbing', 'Admin Time Waste', 'Hand-Raiser',
         1129, 56, 6, 2, 4, 4, 1, 'Office manager empathy angle worked'],
        ['HV-002', datetime(2025, 1, 20), 'HVAC', 'Material Cost Overruns', 'Hand-Raiser',
         743, 28, 2, 0, 1, 1, 0, 'Cross-tested electrical pain point, lower fit'],
        ['EC-003', datetime(2025, 1, 22), 'Electrical', 'Cash Flow Delays', 'Educational',
         1034, 41, 5, 1, 3, 3, 1, 'Testing new pain point angle']
    ]

    # Write sample data (Rows 2-7)
    for row_num, row_data in enumerate(sample_data, 2):
        for col_num, value in enumerate(row_data, 1):
            ws.cell(row=row_num, column=col_num, value=value)

    # Add formulas for calculated columns
    for row in range(2, 8):  # Rows 2-7
        # Column N: Total Engagement (SUM of Likes + Comments + Shares)
        ws[f'N{row}'] = f'=SUM(G{row}:I{row})'

        # Column O: Engagement % (Total Engagement / Impressions * 100)
        ws[f'O{row}'] = f'=IF(F{row}>0,N{row}/F{row}*100,0)'
        ws[f'O{row}'].number_format = '0.0"%"'

        # Column P: Conversion % ((Comments + DMs) / Impressions * 100)
        ws[f'P{row}'] = f'=IF(F{row}>0,(H{row}+J{row})/F{row}*100,0)'
        ws[f'P{row}'].number_format = '0.0"%"'

        # Column Q: Video→Demo % (Demos / Videos * 100)
        ws[f'Q{row}'] = f'=IF(K{row}>0,L{row}/K{row}*100,0)'
        ws[f'Q{row}'].number_format = '0.0"%"'

        # Column R: Cost/Engage (placeholder for future paid spend)
        ws[f'R{row}'] = 0

        # Column S: Performance Tier (based on Engagement %)
        ws[f'S{row}'] = f'=IF(O{row}>=5,"🟢 High",IF(O{row}>=2,"🟡 Medium","🔴 Low"))'

        # Column T: Status (pipeline stage indicator)
        ws[f'T{row}'] = f'=IF(L{row}>0,"✅ Closed",IF(K{row}>0,"📹 Video Sent",IF(J{row}>0,"💬 Engaged","👀 Posted")))'

    # Apply conditional formatting
    # Engagement % heatmap (Column O)
    ws.conditional_formatting.add(
        'O2:O100',
        ColorScaleRule(
            start_type='num', start_value=0, start_color='EA4335',
            mid_type='num', mid_value=5, mid_color='FBBC04',
            end_type='num', end_value=10, end_color='34A853'
        )
    )

    # Performance Tier highlighting (Column S)
    ws.conditional_formatting.add(
        'S2:S100',
        CellIsRule(operator='containsText', formula=['"High"'], fill=PatternFill(start_color='D4EDDA', fill_type='solid'))
    )
    ws.conditional_formatting.add(
        'S2:S100',
        CellIsRule(operator='containsText', formula=['"Medium"'], fill=PatternFill(start_color='FFF3CD', fill_type='solid'))
    )
    ws.conditional_formatting.add(
        'S2:S100',
        CellIsRule(operator='containsText', formula=['"Low"'], fill=PatternFill(start_color='F8D7DA', fill_type='solid'))
    )

    # Demo booked highlight (Column L)
    ws.conditional_formatting.add(
        'L2:L100',
        CellIsRule(operator='greaterThan', formula=['0'], fill=PatternFill(start_color='34A853', fill_type='solid'), font=Font(color='FFFFFF', bold=True))
    )

    # Adjust column widths
    column_widths = {
        'A': 10, 'B': 12, 'C': 12, 'D': 20, 'E': 12,
        'F': 12, 'G': 8, 'H': 10, 'I': 8, 'J': 12,
        'K': 12, 'L': 12, 'M': 35, 'N': 12, 'O': 12,
        'P': 12, 'Q': 12, 'R': 12, 'S': 12, 'T': 15
    }
    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width

    # Freeze header row
    ws.freeze_panes = 'A2'

    # Add data validation dropdowns
    from openpyxl.worksheet.datavalidation import DataValidation

    # Vertical dropdown (Column C)
    dv_vertical = DataValidation(type="list", formula1='"Electrical,HVAC,Plumbing,Energy,Multi-Vertical"', allow_blank=False)
    ws.add_data_validation(dv_vertical)
    dv_vertical.add('C2:C100')

    # Pain Point dropdown (Column D)
    dv_pain = DataValidation(type="list", formula1='"Material Cost Overruns,Labor Burden Blindness,Admin Time Waste,Cash Flow Delays,Job Profitability Opacity"', allow_blank=False)
    ws.add_data_validation(dv_pain)
    dv_pain.add('D2:D100')

    # Post Type dropdown (Column E)
    dv_type = DataValidation(type="list", formula1='"Hand-Raiser,Educational,Case Study,Poll/Survey,Testimonial"', allow_blank=False)
    ws.add_data_validation(dv_type)
    dv_type.add('E2:E100')

def create_dashboard_sheet(wb):
    """TAB 2: Vertical Performance Dashboard"""
    ws = wb.create_sheet("Dashboard", 1)

    # Section 1: Vertical Performance Summary
    ws['A1'] = 'VERTICAL PERFORMANCE SUMMARY'
    ws['A1'].font = Font(bold=True, size=14)

    headers = ['Vertical', 'Total Posts', 'Avg Engage%', 'Total DMs', 'Videos Sent', 'Demos Booked']
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=2, column=col_num, value=header)
        cell.font = Font(bold=True)
        cell.fill = PatternFill(start_color="4A90E2", end_color="4A90E2", fill_type="solid")
        cell.font = Font(bold=True, color="FFFFFF")

    verticals = ['Electrical', 'HVAC', 'Plumbing', 'TOTAL']
    for row_num, vertical in enumerate(verticals, 3):
        ws.cell(row=row_num, column=1, value=vertical)

    # Add formulas for Electrical (Row 3)
    ws['B3'] = '=COUNTIF(\'Post Performance Tracker\'!C:C,"Electrical")'
    ws['C3'] = '=IFERROR(AVERAGEIF(\'Post Performance Tracker\'!C:C,"Electrical",\'Post Performance Tracker\'!O:O),0)'
    ws['C3'].number_format = '0.0"%"'
    ws['D3'] = '=SUMIF(\'Post Performance Tracker\'!C:C,"Electrical",\'Post Performance Tracker\'!J:J)'
    ws['E3'] = '=SUMIF(\'Post Performance Tracker\'!C:C,"Electrical",\'Post Performance Tracker\'!K:K)'
    ws['F3'] = '=SUMIF(\'Post Performance Tracker\'!C:C,"Electrical",\'Post Performance Tracker\'!L:L)'

    # Add formulas for HVAC (Row 4)
    ws['B4'] = '=COUNTIF(\'Post Performance Tracker\'!C:C,"HVAC")'
    ws['C4'] = '=IFERROR(AVERAGEIF(\'Post Performance Tracker\'!C:C,"HVAC",\'Post Performance Tracker\'!O:O),0)'
    ws['C4'].number_format = '0.0"%"'
    ws['D4'] = '=SUMIF(\'Post Performance Tracker\'!C:C,"HVAC",\'Post Performance Tracker\'!J:J)'
    ws['E4'] = '=SUMIF(\'Post Performance Tracker\'!C:C,"HVAC",\'Post Performance Tracker\'!K:K)'
    ws['F4'] = '=SUMIF(\'Post Performance Tracker\'!C:C,"HVAC",\'Post Performance Tracker\'!L:L)'

    # Add formulas for Plumbing (Row 5)
    ws['B5'] = '=COUNTIF(\'Post Performance Tracker\'!C:C,"Plumbing")'
    ws['C5'] = '=IFERROR(AVERAGEIF(\'Post Performance Tracker\'!C:C,"Plumbing",\'Post Performance Tracker\'!O:O),0)'
    ws['C5'].number_format = '0.0"%"'
    ws['D5'] = '=SUMIF(\'Post Performance Tracker\'!C:C,"Plumbing",\'Post Performance Tracker\'!J:J)'
    ws['E5'] = '=SUMIF(\'Post Performance Tracker\'!C:C,"Plumbing",\'Post Performance Tracker\'!K:K)'
    ws['F5'] = '=SUMIF(\'Post Performance Tracker\'!C:C,"Plumbing",\'Post Performance Tracker\'!L:L)'

    # Add TOTAL row formulas (Row 6)
    ws['B6'] = '=SUM(B3:B5)'
    ws['C6'] = '=AVERAGE(C3:C5)'
    ws['C6'].number_format = '0.0"%"'
    ws['D6'] = '=SUM(D3:D5)'
    ws['E6'] = '=SUM(E3:E5)'
    ws['F6'] = '=SUM(F3:F5)'

    # Bold TOTAL row
    for col in range(1, 7):
        ws.cell(row=6, column=col).font = Font(bold=True)

    # Section 2: Pain Point Performance
    ws['A9'] = 'PAIN POINT PERFORMANCE'
    ws['A9'].font = Font(bold=True, size=14)

    pain_headers = ['Pain Point', 'Posts Count', 'Avg Engage%', 'Demos']
    for col_num, header in enumerate(pain_headers, 1):
        cell = ws.cell(row=10, column=col_num, value=header)
        cell.font = Font(bold=True)
        cell.fill = PatternFill(start_color="4A90E2", end_color="4A90E2", fill_type="solid")
        cell.font = Font(bold=True, color="FFFFFF")

    pain_points = ['Material Cost Overruns', 'Labor Burden Blindness', 'Admin Time Waste']
    for row_num, pain in enumerate(pain_points, 11):
        ws.cell(row=row_num, column=1, value=pain)
        ws[f'B{row_num}'] = f'=COUNTIF(\'Post Performance Tracker\'!D:D,"{pain}")'
        ws[f'C{row_num}'] = f'=IFERROR(AVERAGEIF(\'Post Performance Tracker\'!D:D,"{pain}",\'Post Performance Tracker\'!O:O),0)'
        ws[f'C{row_num}'].number_format = '0.0"%"'
        ws[f'D{row_num}'] = f'=SUMIF(\'Post Performance Tracker\'!D:D,"{pain}",\'Post Performance Tracker\'!L:L)'

    # Section 3: Weekly Trends
    ws['A16'] = 'WEEKLY TRENDS'
    ws['A16'].font = Font(bold=True, size=14)

    trend_headers = ['Week', 'Posts Published', 'Total DMs', 'Demos Booked']
    for col_num, header in enumerate(trend_headers, 1):
        cell = ws.cell(row=17, column=col_num, value=header)
        cell.font = Font(bold=True)
        cell.fill = PatternFill(start_color="4A90E2", end_color="4A90E2", fill_type="solid")
        cell.font = Font(bold=True, color="FFFFFF")

    weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
    for row_num, week in enumerate(weeks, 18):
        ws.cell(row=row_num, column=1, value=week)
        # Formulas would need specific date ranges - placeholder zeros for now
        ws.cell(row=row_num, column=2, value=0)
        ws.cell(row=row_num, column=3, value=0)
        ws.cell(row=row_num, column=4, value=0)

    # Section 4: Conversion Funnel
    ws['A23'] = 'CONVERSION FUNNEL'
    ws['A23'].font = Font(bold=True, size=14)

    funnel_stages = [
        ('Total Impressions', '=SUM(\'Post Performance Tracker\'!F:F)'),
        ('Total Engagement', '=SUM(\'Post Performance Tracker\'!N:N)'),
        ('DMs Received', '=SUM(\'Post Performance Tracker\'!J:J)'),
        ('Videos Sent', '=SUM(\'Post Performance Tracker\'!K:K)'),
        ('Demos Booked', '=SUM(\'Post Performance Tracker\'!L:L)')
    ]

    ws['A24'] = 'Stage'
    ws['B24'] = 'Count'
    ws['A24'].font = Font(bold=True)
    ws['B24'].font = Font(bold=True)

    for row_num, (stage, formula) in enumerate(funnel_stages, 25):
        ws.cell(row=row_num, column=1, value=stage)
        ws.cell(row=row_num, column=2, value=formula)

    # Adjust column widths
    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 15
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 15

def create_response_tracker_sheet(wb):
    """TAB 3: Engagement Response Tracker"""
    ws = wb.create_sheet("Response Tracker", 2)

    # Define headers
    headers = [
        'Prospect', 'Vertical', 'Post ID', 'Engage Type', 'Date Engaged',
        'Video Sent', 'Demo Date', 'Status', 'Days→Video', 'Days→Demo',
        'Speed Grade', 'Stage'
    ]

    # Write headers (Row 1)
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num, value=header)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="4A90E2", end_color="4A90E2", fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # Sample data
    sample_prospects = [
        ['John Smith', 'Electrical', 'EC-001', 'Comment', datetime(2025, 1, 13),
         datetime(2025, 1, 13), datetime(2025, 1, 18), 'Demo Booked'],
        ['Mike Johnson', 'HVAC', 'HV-001', 'DM', datetime(2025, 1, 15),
         datetime(2025, 1, 15), datetime(2025, 1, 20), 'Demo Booked'],
        ['Sarah Williams', 'Plumbing', 'PL-001', 'Comment', datetime(2025, 1, 17),
         datetime(2025, 1, 18), None, 'Video Sent'],
        ['Dave Martinez', 'Electrical', 'EC-001', 'DM', datetime(2025, 1, 13),
         None, None, 'Engaged']
    ]

    # Write sample data
    for row_num, row_data in enumerate(sample_prospects, 2):
        for col_num, value in enumerate(row_data, 1):
            ws.cell(row=row_num, column=col_num, value=value)

    # Add formulas for calculated columns
    for row in range(2, 6):  # Rows 2-5
        # Column I: Days→Video (Video Sent - Date Engaged)
        ws[f'I{row}'] = f'=IF(F{row}="","",F{row}-E{row})'

        # Column J: Days→Demo (Demo Date - Date Engaged)
        ws[f'J{row}'] = f'=IF(G{row}="","",G{row}-E{row})'

        # Column K: Speed Grade (based on Days→Video)
        ws[f'K{row}'] = f'=IF(I{row}="","",IF(I{row}<=1,"🟢 Fast",IF(I{row}<=3,"🟡 OK","🔴 Slow")))'

        # Column L: Pipeline Stage
        ws[f'L{row}'] = f'=IF(H{row}="Demo Booked","Stage 3: Demo",IF(F{row}<>"","Stage 2: Video Sent",IF(E{row}<>"","Stage 1: Engaged","")))'

    # Apply conditional formatting
    # Overdue video responses (Column I > 2 days)
    ws.conditional_formatting.add(
        'I2:I100',
        CellIsRule(operator='greaterThan', formula=['2'], fill=PatternFill(start_color='EA4335', fill_type='solid'), font=Font(color='FFFFFF', bold=True))
    )

    # Pipeline stage coloring (Column L)
    ws.conditional_formatting.add(
        'L2:L100',
        CellIsRule(operator='containsText', formula=['"Stage 3"'], fill=PatternFill(start_color='34A853', fill_type='solid'))
    )
    ws.conditional_formatting.add(
        'L2:L100',
        CellIsRule(operator='containsText', formula=['"Stage 2"'], fill=PatternFill(start_color='FBBC04', fill_type='solid'))
    )
    ws.conditional_formatting.add(
        'L2:L100',
        CellIsRule(operator='containsText', formula=['"Stage 1"'], fill=PatternFill(start_color='4A90E2', fill_type='solid'))
    )

    # Adjust column widths
    column_widths = {
        'A': 18, 'B': 12, 'C': 10, 'D': 12, 'E': 14,
        'F': 14, 'G': 14, 'H': 15, 'I': 12, 'J': 12,
        'K': 15, 'L': 18
    }
    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width

    # Freeze header row
    ws.freeze_panes = 'A2'

if __name__ == "__main__":
    print("🚀 Building LinkedIn Hand-Raiser Engagement Tracker...")
    create_tracker_workbook()
    print("\n✅ Complete! Open the file to start tracking.")
