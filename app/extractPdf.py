import PyPDF2

def extractText(filepath):
    pdf_file = open(filepath, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    page_content = ''
    for i in range(number_of_pages):
        page = read_pdf.getPage(i)
        page_content += page.extractText()
    # print(page_content)
    # return page_content.encode('utf-8')
    return page_content

# for test
# text = extractText("static/presentation_pdf.pdf")
# print(text)