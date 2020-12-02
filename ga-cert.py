from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, landscape
from PyPDF2 import PdfFileWriter, PdfFileReader
import io


fullname = input("Please enter full name: ")

date = datetime.today().strftime('%B %Y')

filename = fullname + ".pdf"

namelength = len(fullname)
namepadding = (32 - namelength) // 2
paddedname = ("   " * (namepadding + 0)) + fullname

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
