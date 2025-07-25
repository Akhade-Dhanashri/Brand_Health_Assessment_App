import os
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
)
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from PIL import Image as PILImage
from twilio.rest import Client

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

# --- PDF Generator ---
def generate_pdf(form_data, filename="Brand_Health_Report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CenterTitle", alignment=TA_CENTER, fontSize=18, textColor=EX_BLUE, spaceAfter=20))
    styles.add(ParagraphStyle(name="SectionHeader", fontSize=14, textColor=EX_LIGHT_BLUE, spaceAfter=10))

    # --- Logo ---
    logo_path = "Logo-exmatters.png"
    if os.path.exists(logo_path):
        try:
            pil_logo = PILImage.open(logo_path)
            orig_w, orig_h = pil_logo.size
            max_w = 150
            scale = max_w / orig_w
            new_w, new_h = max_w, orig_h * scale

            logo = Image(logo_path, width=new_w, height=new_h)
            logo.hAlign = 'RIGHT'
            story.append(logo)
        except Exception as e:
            print("⚠️ Logo error:", e)

    # --- Title ---
    story.append(Paragraph("Brand Health Assessment Report", styles["CenterTitle"]))

    # --- Info Block ---
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    story.append(Paragraph(f"<b>Name:</b> {form_data['name']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Email:</b> {form_data['email']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Company:</b> {form_data['company']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Contact:</b> {form_data['contact']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Date:</b> {today}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # --- Score Calculation ---
    section_scores = {}
    total_score = 0

    for section, questions in question_sections.items():
        score = sum(form_data["responses"].get(q, 0) for q in questions)
        section_scores[section] = score
        total_score += score

    percentage = round((total_score / 60) * 100)

    # --- Summary Table ---
    story.append(Paragraph("Brand Health Summary", styles["SectionHeader"]))
    summary_data = [["Section", "Score (out of 15)"]]
    for section, score in section_scores.items():
        summary_data.append([section, str(score)])
    summary_data.append(["Overall Score", f"{total_score} / 60"])
    summary_data.append(["Brand Health %", f"{percentage}%"])

    table = Table(summary_data, colWidths=[300, 200])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), EX_BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -2), EX_GRAY),
        ("BACKGROUND", (0, -2), (-1, -1), EX_TEAL),
        ("TEXTCOLOR", (0, -2), (-1, -1), colors.white),
    ]))
    story.append(table)
    story.append(Spacer(1, 20))

    # --- Bar Chart with Rotated X-Axis Labels ---
    drawing = Drawing(450, 240)
    bar = VerticalBarChart()
    bar.x = 60
    bar.y = 50
    bar.height = 150
    bar.width = 330
    bar.data = [[section_scores[k] for k in section_scores]]
    bar.categoryAxis.categoryNames = list(section_scores.keys())
    bar.categoryAxis.labels.angle = 45
    bar.categoryAxis.labels.dy = -15
    bar.categoryAxis.labels.fontSize = 8
    bar.bars[0].fillColor = EX_LIGHT_BLUE
    bar.valueAxis.valueMin = 0
    bar.valueAxis.valueMax = 15
    bar.valueAxis.valueStep = 5
    drawing.add(bar)

    story.append(Paragraph("Category-wise Scores (Bar Graph)", styles["SectionHeader"]))
    story.append(drawing)
    story.append(Spacer(1, 20))

    # --- Section-wise Feedback ---
    story.append(Paragraph("Section-wise Feedback", styles["SectionHeader"]))
    for section, score in section_scores.items():
        if score <= 5:
            feedback = f"{section}: Needs significant improvement. Focus on clarifying and strengthening your {section.lower()}."
        elif score <= 10:
            feedback = f"{section}: Some clarity exists, but more refinement and differentiation is needed in your {section.lower()}."
        else:
            feedback = f"{section}: Performing well. Keep up the good work and continue optimizing your {section.lower()}."
        story.append(Paragraph(feedback, styles["Normal"]))
        story.append(Spacer(1, 6))

    doc.build(story)
    return filename

# --- Email Sender ---
def send_report_via_email(to_email, filename):
    from_email = "dhanashri.a@exmatters.com"
    app_password = "uund rklj hmdp ijcx"  # replace with secure App Password

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = "Your Brand Health Assessment Report"

    body = "Dear User,\n\nPlease find attached your Brand Health Assessment Report.\n\nBest regards,\nExmatters Team"
    msg.attach(MIMEText(body, "plain"))

    with open(filename, "rb") as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(filename))
        part['Content-Disposition'] = f'attachment; filename="{filename}"'
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_email, app_password)
            server.send_message(msg)
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Email send failed: {e}")

# --- WhatsApp Sender ---
def send_report_to_whatsapp(to_number, media_url):
    account_sid = "your_twilio_sid"
    auth_token = "your_twilio_auth_token"
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            from_="whatsapp:+14155238886",
            to=f"whatsapp:{to_number}",
            body="📄 Here is your Brand Health Report from Exmatters!",
            media_url=[media_url]
        )
        print(f"✅ WhatsApp sent to {to_number}")
    except Exception as e:
        print(f"❌ WhatsApp send failed: {e}")

# --- Final Handler ---
def generate_and_send_report(form_data, public_pdf_url):
    pdf = generate_pdf(form_data)
    send_report_via_email(form_data["email"], pdf)
    send_report_via_email("dhanashri.a@exmatters.com", pdf)
    send_report_to_whatsapp(form_data["contact"], public_pdf_url)
