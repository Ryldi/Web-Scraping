from pdfminer.high_level import extract_text

class PDF_scraper:
  def text_scraper(path):
    text = extract_text(path)
    return text