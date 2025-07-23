import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
)
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from PIL import Image as PILImage
import os
import datetime

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
            print("⚠️ Failed to load logo:", e)

    # --- Title ---
    story.append(Paragraph("Brand Health Assessment Report", styles["CenterTitle"]))

    # --- User Info ---
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    story.append(Paragraph(f"<b>Name:</b> {form_data['name']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Email:</b> {form_data['email']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Company:</b> {form_data['company']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Date:</b> {today}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # --- Scores ---
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

    # --- Bar Chart ---
    drawing = Drawing(400, 200)
    bar = VerticalBarChart()
    bar.x = 50
    bar.y = 30
    bar.height = 120
    bar.width = 300
    bar.data = [[section_scores[k] for k in section_scores]]
    bar.categoryAxis.categoryNames = list(section_scores.keys())
    bar.bars[0].fillColor = EX_LIGHT_BLUE
    bar.valueAxis.valueMin = 0
    bar.valueAxis.valueMax = 15
    bar.valueAxis.valueStep = 5
    drawing.add(bar)

    story.append(Paragraph("Category-wise Scores (Bar Graph)", styles["SectionHeader"]))
    story.append(drawing)
    story.append(Spacer(2, 20))

    # --- Feedback ---
    story.append(Paragraph("Feedback", styles["SectionHeader"]))
    if total_score <= 5:
        feedback_text = "You need to improve and differentiate your brand."
    elif 6 <= total_score <= 10:
        feedback_text = "There is some clarity, but more differentiation is required."
    else:
        feedback_text = "Great brand experience delivery! Focus on sustaining it across the customerjourney."
    story.append(Paragraph(feedback_text, styles["Normal"]))

    doc.build(story)
    return filename

# --- Email Sender ---
def send_report_via_email(to_email, filename):
    from_email = "dhanashri.a@exmatters.com"
    app_password = "uund rklj hmdp ijcx"  # Replace with your App Password

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

# --- Final Callable ---
def generate_and_send_report(form_data):
    pdf = generate_pdf(form_data)
    send_report_via_email(form_data["email"], pdf)
