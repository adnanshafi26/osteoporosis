from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(data, result, filename="prediction_report.pdf"):

    styles = getSampleStyleSheet()

    report = SimpleDocTemplate(filename)

    content = []

    content.append(Paragraph("Osteoporosis Prediction Medical Report", styles['Title']))
    content.append(Spacer(1, 20))

    content.append(Paragraph(f"Age: {data['age']}", styles['Normal']))
    content.append(Paragraph(f"Gender: {data['gender']}", styles['Normal']))
    content.append(Paragraph(f"BMI: {data['bmi']}", styles['Normal']))
    content.append(Paragraph(f"Bone Density: {data['boneDensity']}", styles['Normal']))
    content.append(Paragraph(f"Calcium Intake: {data['calcium']}", styles['Normal']))
    content.append(Paragraph(f"Vitamin D Level: {data['vitaminD']}", styles['Normal']))

    content.append(Spacer(1, 20))

    content.append(Paragraph(f"Prediction Result: {result}", styles['Heading2']))
    content.append(Spacer(1, 20))

    content.append(Paragraph("Recommendations:", styles['Heading3']))

    content.append(Paragraph("- Maintain healthy BMI (18.5–24.9)", styles['Normal']))
    content.append(Paragraph("- Consume calcium-rich foods", styles['Normal']))
    content.append(Paragraph("- Get adequate sunlight for Vitamin D", styles['Normal']))
    content.append(Paragraph("- Perform regular exercise", styles['Normal']))
    content.append(Paragraph("- Avoid smoking and alcohol", styles['Normal']))

    report.build(content)