"""

            ASSUMPTIONS:
            -------------

            1) First line of the PDF is Name
            2) Second line must have a "|"(pipe  delimited  to extract the Email and Address
            3) Every Section must be followed by a UNDERLINE, which is of length 203
                ex
                    Education
                    ___________________________

            RUNNING THE PROGRAM:
            --------------------
            python PdfParser.py "C:\Interview\input\Interview_sample_data.pdf" "output.json"

            On successfull running, a JSON will be  created in the mention location. When the PDF does not
            adhere to the ASSUMPTION # 3 , JSON will  not be created.



"""
import argparse
import os
import sys
import fitz
import re
import json

class PDFParser(object):
    def __init__(self, inputFile, outputFile):
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.keyvalue = {}


    def load_pdf(self):
        """
            Returns a list of string ,by replacing the
            empty spaces, zero width white spaces

            """
        doc = fitz.open(self.inputFile)
        contents = []
        for page in doc:
            contents = page.getText().split("\n")

        return  self._format_pdf_content(contents)

    def _format_pdf_content(self,contents):

        removespaces = [ele.strip() for ele in contents if ele.strip() != '']
        cleaned = [ele.replace('\u200b','') for ele in removespaces]
        return cleaned

    def parse_pdf(self,formattedcontent):

        """
                    Parse and Extract the Name, Address ,Email
                    Sections and Create a dictionary

        """

        self.keyvalue["name"] = formattedcontent[0].strip()

        if "|" in formattedcontent[1]:
            self.keyvalue["address"] = formattedcontent[1].split("|")[0] + formattedcontent[2]
            email = formattedcontent[1].split("|")[1].strip()
            self.keyvalue["email"] = self._validate_email(email)
        else:
            self.keyvalue["address"] = None
            self.keyvalue["email"] = None


        underlineMarker = "_" * 203
        totalLines = len(formattedcontent)
        firstUnderLineFlag = False
        for currLine, value in enumerate(formattedcontent):
            nextLine = currLine + 1
            if value == underlineMarker.strip():
                firstUnderLineFlag = True
                key = formattedcontent[currLine - 1]
                self.keyvalue.setdefault(key, '')
                continue

            if firstUnderLineFlag:
                if nextLine <= totalLines - 1 and formattedcontent[nextLine] != underlineMarker.strip():
                    self.keyvalue[key] += value
                if currLine == totalLines -1 :
                    self.keyvalue[key] += value

        if not firstUnderLineFlag:
            print("This program can parse only PDF, only if the  SECTION HEADING is followed by a UNDERLINE")
            sys.exit()

                    

   

    def _validate_email(self,email):
        emailRE = re.compile(r"""^([a-z0-9_\.-]+)@([a-z0-9]+)\.([a-z]+)$""")
        match = emailRE.fullmatch(email)
        if match:
            try:
                return email
            except IndexError:
                return None

    def  save_json(self):
        outputfile = self.outputFile
        with open(outputfile, "w", encoding="utf-8") as  fp:
            json.dump(self.keyvalue, fp, ensure_ascii=False)

    def start_parsing(self):

        formattedContent = self.load_pdf()

        self.parse_pdf(formattedContent)

        self.save_json()





if __name__ == '__main__':

    argParser = argparse.ArgumentParser(description='Extract the content from given PDF to JSON ')
    argParser.add_argument('pdfpath', type=str, help='Input file path')
    argParser.add_argument('jsonpath', type=str, help='Output file path')

    args = argParser.parse_args()
    input_file = args.pdfpath
    output_file = args.jsonpath

    if not os.path.exists(input_file):
        print('Given PDF is not present in {}. Mention the correct location!!!!!'.format(input_file))
        sys.exit()


    #check the file format
    name,fileFormat = os.path.splitext(input_file)
    if fileFormat != ".pdf":
        print("Given file is not PDF . This application works only for PDF ")
        sys.exit()

    name, fileFormat = os.path.splitext(output_file)
    if fileFormat != ".json":
        print("Given  output file is not JSON . This application works only for JSON ")
        sys.exit()


    parser = PDFParser(input_file,output_file)
    parser.start_parsing()

    print("Parsing of PDF is completed ------  Converted to JSON -----File name is {}".format(output_file))