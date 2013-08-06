class FormatUnSuportedError(Exception):
    def __init__(self,requestFormat):
        self.requestFormat = requestFormat;
    def __str__(self):
        return "Request Format {} is not supported currently!".format(self.requestFormat);
class Formats:
    JSON="json";
    XML="xml";
    HTML="html";

