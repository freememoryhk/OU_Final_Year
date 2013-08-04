class Formatter:
    def __init__(self,decoratorFormatter=None):
        self.decoratorFormatter = decoratorFormatter;
    def format(self,original):
        return original;
class NumericZeroFormatter(Formatter):
    length=11;
    def format(self,original):
        if self.length < len(str(original)) :
            return str(original);
        else:
            zeroFillToOriginal = str(("0" * (self.length - len(str(original)) )));
            result =  zeroFillToOriginal+str(original);
            return result;
