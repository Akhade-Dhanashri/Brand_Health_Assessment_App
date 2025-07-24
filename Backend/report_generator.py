import os
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics import renderPDF
from datetime import datetime
from email.message import EmailMessage
import smtplib
from twilio.rest import Client


def generate_report(name, email, company, contact, responses):
    # Paths and PDF setup
    filename = f"Brand_Health_Report_{name.replace(' ', '_')}.pdf"
    filepath = os.path.join(tempfile.gettempdir(), filename)
    doc = SimpleDocTemplate(filepath, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Logo
    logo_path = "Logo-exmatters.png"
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=120, height=40)
        logo.hAlign = 'RIGHT'
        elements.append(logo)

    # Title
    elements.append(Paragraph("<b>Brand Health Assessment Report</b>", styles['Title']))
    elements.append(Spacer(1, 12))

    # Info
    elements.append(Paragraph(f"<b>Name:</b> {name}", styles['Normal']))
    elements.append(Paragraph(f"<b>Company:</b> {company}", styles['Normal']))
    elements.append(Paragraph(f"<b>Email:</b> {email}", styles['Normal']))
    elements.append(Paragraph(f"<b>Contact:</b> {contact}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Sections
    sections = {
        "Brand Strategy": list(responses.values())[:3],
        "Brand Alignment": list(responses.values())[3:6],
        "Brand Communication": list(responses.values())[6:9],
        "Brand Execution": list(responses.values())[9:12]
    }

    section_scores = {sec: sum(scores) for sec, scores in sections.items()}
    section_avgs = {sec: round(sum(scores)/len(scores), 2) for sec, scores in sections.items()}
    total_score = sum(section_scores.values())
    percent_score = round((total_score / 60) * 100)

    # Summary Table
    data = [["Section", "Score (out of 15)", "Avg (out of 5)"]]
    for sec in sections:
        data.append([sec, section_scores[sec], section_avgs[sec]])
    data.append(["Total", f"{total_score} / 60", f"{percent_score}%"])

    table = Table(data, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0076A8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER')
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))

    # Feedback function
    def feedback(score):
        if score <= 5:
            return "Needs significant improvement in this area."
        elif score <= 10:
            return "Some clarity exists, but more differentiation and alignment are needed."
        else:
            return "Performing well in this area."

    # Feedback Section
    elements.append(Paragraph("<b>Section-wise Feedback:</b>", styles['Heading2']))
    for sec, score in section_scores.items():
        fb = feedback(score)
        elements.append(Paragraph(f"<b>{sec}:</b> {fb}", styles['Normal']))
        elements.append(Spacer(1, 6))
    elements.append(Spacer(1, 16))

    # Bar chart using reportlab graphics
    drawing = Drawing(400, 200)
    chart = VerticalBarChart()
    chart.x = 50
    chart.y = 30
    chart.height = 125
    chart.width = 300
    chart.data = [list(section_scores.values())]
    chart.categoryAxis.categoryNames = list(section_scores.keys())
    chart.barWidth = 15
    chart.fillColor = colors.HexColor("#0076A8")
    chart.bars[0].fillColor = colors.HexColor("#0076A8")
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 15
    chart.categoryAxis.labels.angle = 20
    chart.categoryAxis.labels.dy = -10

    drawing.add(chart)
    drawing.add(String(150, 180, 'Brand Health Score by Section', fontSize=12, fillColor=colors.black))
    elements.append(drawing)

    # Build PDF
    doc.build(elements)

    # Send email to both recipient and internal address
    send_email(email, filename, filepath)
    send_email("info@exmatters.com", filename, filepath)

    # Send WhatsApp
    send_whatsapp(contact, filename)

    return filename, filepath


def send_email(to_email, filename, filepath):
    email_sender = "info@exmatters.com"
    email_password = "kqjn unjt qgvy cef"

    msg = EmailMessage()
    msg["Subject"] = "📄 Your Brand Health Assessment Report"
    msg["From"] = email_sender
    msg["To"] = to_email
    msg.set_content("Hello,\n\nPlease find attached your Brand Health Assessment Report PDF.\n\nThank you.\n- Exmatters Team")

    with open(filepath, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=filename)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(msg)


def send_whatsapp(phone_number, filename):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_whatsapp = os.getenv("TWILIO_WHATSAPP_NUMBER")

    client = Client(account_sid, auth_token)

    client.messages.create(
        from_=f"whatsapp:{from_whatsapp}",
        to=f"whatsapp:{phone_number}",
        body="Hi! 👋 This is your Brand Health Report from Exmatters. Please check your email for the attached PDF."
    )
