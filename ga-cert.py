from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, landscape
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import csv

names = []

with open('names.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        names.append(row)


date = datetime.today().strftime('%B %Y')

for name in names:
    filename = name[0] + ".pdf"

    namelength = len(name[0])
    namepadding = (32 - namelength) // 2
    paddedname = ("   " * (namepadding + 1)) + name[0]

    datelength = len(date)
    datepadding = (32 - datelength) // 2
    paddeddate = ("   " * (datepadding + 1)) + date

    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, landscape(A4))
    can.setFont("Helvetica", 30)
    can.setFillColorRGB((81/256), (92/256), (78/256))
    can.drawString((0) * cm, 12.5 * cm, paddeddate)
    can.setFillColorRGB((141/256), (183/256), (58/256))
    can.drawString((0) * cm, 10 * cm, paddedname)

    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("certificate.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(filename, "wb")
    output.write(outputStream)
    outputStream.close()

    print("{} is printed".format(filename))
