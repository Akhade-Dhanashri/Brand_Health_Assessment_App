import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from PIL import Image as PILImage
from twilio.rest import Client

# --- Config ---
SENDER_EMAIL = "dhanashri.a@exmatters.com"
SENDER_PASSWORD = "uund rklj hmdp ijcx"  # Gmail App Password
TWILIO_SID = "YOUR_TWILIO_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+917517364815"  # Default sandbox number

# --- Exmatters Colors ---
EX_BLUE = colors.HexColor("#003366")
EX_LIGHT_BLUE = colors.HexColor("#0072CE")
EX_TEAL = colors.HexColor("#00B2A9")
EX_GRAY = colors.HexColor("#F2F2F2")

# --- Section Questions ---
question_sections = {
    "Brand Strategy": [
        "My company's product or service has a strong and clear point of differentiation from my competitors.",
        "My client and I can summarize my brand in one word/statement.",
        "The value of my product or services is relevant to the current market environment."
    ],
    "Brand Alignment": [
        "There is harmony/linkage between my company's vision, mission, values and strategy.",
        "My employees are brand ambassadors of the company and can articulate how the offering differs from competitors.",
        "I regularly survey my customers on my brand and use their feedback as an input for strategy."
    ],
    "Brand Communication": [
        "My marketing material clearly communicates the company's brand.",
        "Management reinforces the company's brand in all staff meetings and employee interactions.",
        "All departments follow the company's brand guidelines document and prescribed templates."
    ],
    "Brand Execution": [
        "Clients get the same positive brand experience no matter which department or employee they interact with.",
        "My company has a robust mechanism to deliver a brand experience at every stage of the customer journey (attract, engage, and retain).",
        "My clients do not switch between my competitors and me and regularly refer others to my company."
    ]
}

def generate_pdf(form_data, filename="Brand_Health_Report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CenterTitle", alignment=TA_CENTER, fontSize=18, textColor=EX_BLUE, spaceAfter=20))
    styles.add(ParagraphStyle(name="SectionHeader", fontSize=14, textColor=EX_LIGHT_BLUE, spaceAfter=10))

    # Logo
    logo_path = "Logo-exmatters.png"
    if os.path.exists(logo_path):
        try:
            pil_logo = PILImage.open(logo_path)
            orig_w, orig_h = pil_logo.size
            max_w = 150
            scale = max_w / orig_w
            logo = Image(logo_path, width=max_w, height=orig_h * scale)
            logo.hAlign = 'RIGHT'
            story.append(logo)
        except Exception as e:
            print("⚠️ Logo failed:", e)

    # Header
    story.append(Paragraph("Brand Health Assessment Report", styles["CenterTitle"]))
    story.append(Paragraph(f"<b>Name:</b> {form_data['name']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Email:</b> {form_data['email']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Company:</b> {form_data['company']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Contact Number:</b> {form_data['contact_number']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Date:</b> {datetime.datetime.now().strftime('%Y-%m-%d')}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # Scores
    section_scores = {}
    total_score = 0
    for section, questions in question_sections.items():
        score = sum(form_data["responses"].get(q, 0) for q in questions)
        section_scores[section] = score
        total_score += score
    percentage = round((total_score / 60) * 100)

    # Summary Table
    story.append(Paragraph("Brand Health Summary", styles["SectionHeader"]))
    data = [["Section", "Score (out of 15)"]]
    for s, sc in section_scores.items():
        data.append([s, str(sc)])
    data.append(["Overall Score", f"{total_score} / 60"])
    data.append(["Brand Health %", f"{percentage}%"])

    table = Table(data, colWidths=[300, 200])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), EX_BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -2), EX_GRAY),
        ("BACKGROUND", (0, -2), (-1, -1), EX_TEAL),
        ("TEXTCOLOR", (0, -2), (-1, -1), colors.white),
    ]))
    story.append(table)
    story.append(Spacer(1, 20))

    # Bar Chart
    drawing = Drawing(400, 220)
    bar = VerticalBarChart()
    bar.x = 70
    bar.y = 50
    bar.height = 120
    bar.width = 280
    bar.data = [[section_scores[s] for s in section_scores]]
    bar.categoryAxis.categoryNames = list(section_scores.keys())
    bar.categoryAxis.labels.angle = 45
    bar.categoryAxis.labels.boxAnchor = 'ne'
    bar.bars[0].fillColor = EX_LIGHT_BLUE
    bar.valueAxis.valueMin = 0
    bar.valueAxis.valueMax = 15
    bar.valueAxis.valueStep = 5
    drawing.add(bar)
    story.append(Paragraph("Category-wise Scores", styles["SectionHeader"]))
    story.append(drawing)
    story.append(Spacer(1, 20))

    # Feedback
    story.append(Paragraph("Section-wise Feedback", styles["SectionHeader"]))
    for section, score in section_scores.items():
        if score <= 5:
            fb = f"{section}: Needs significant improvement. Clarify and strengthen your {section.lower()}."
        elif 6 <= score <= 10:
            fb = f"{section}: Some clarity exists, but further refinement is needed."
        else:
            fb = f"{section}: Performing well. Keep optimizing your {section.lower()}."
        story.append(Paragraph(fb, styles["Normal"]))
        story.append(Spacer(1, 6))

    doc.build(story)
    return filename

def send_email_with_attachment(to_email, filename):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = "Brand Health Assessment Report"

    body = "Dear User,\n\nPlease find attached your Brand Health Assessment Report.\n\nRegards,\nExmatters Team"
    msg.attach(MIMEText(body, "plain"))

    with open(filename, "rb") as f:
        part = MIMEApplication(f.read(), Name=filename)
        part['Content-Disposition'] = f'attachment; filename="{filename}"'
        msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

def send_whatsapp_message(contact_number, filename):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        to=f"whatsapp:{contact_number}",
        body="Thank you for completing the Brand Health Assessment! Here's your PDF report.",
    )
    with open(filename, "rb") as f:
        client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f"whatsapp:{contact_number}",
            media_url=["https://brand-health-assessment-app-2ij1.vercel.app/" + filename]
        )

def generate_and_send_report(form_data):
    pdf = generate_pdf(form_data)
    send_email_with_attachment(form_data["email"], pdf)
    send_email_with_attachment("dhanashri.a@exmatters.com", pdf)
    send_whatsapp_message(form_data["contact_number"], pdf)
