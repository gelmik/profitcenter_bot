import easyocr

reader = easyocr.Reader(['en'])
print(reader.readtext("mail_images/12215966065661472234.png", detail=2))