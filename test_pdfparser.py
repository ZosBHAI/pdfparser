from PdfParser import *

import unittest
import json

class PDFParserTest(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = PDFParser("input\interview_sample_data.pdf", "output.json")


    def test_validate_email(self):
        self.assertEqual(self.parser._validate_email("burk.lee@gmail.com"),"burk.lee@gmail.com","Valid Mail")

    def test_format_pdf_content(self):
        content = ['Language:\u200b Basic Tagalog (written and verbal)  ']
        self.assertEqual(self.parser._format_pdf_content(content),['Language: Basic Tagalog (written and verbal)'])

    def test_parse_pdf(self):

        print("test_parse_pdf")
        self.parser.parse_pdf(self.parser.load_pdf())
        print(str(self.parser.keyvalue))
        with open(self.parser.outputFile,"r",encoding="utf-8") as fp:
            data = json.load(fp)
        print(str(data))
        self.assertEqual(self.parser.keyvalue,data)




if __name__ == '__main__':
    unittest.main()

