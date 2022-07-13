import inflect
from dateutil import parser
import re


def convert_currency(x):
  """
    Converts currency by ignoring commas and
    seperately reading cents and dollars if there are cents.
      Args:
        x:
          str
      Returns:
        Returns a string.
  """
  if "$" in x:
      x = x.replace(",", "")
      p = inflect.engine()
      if "." in x:
        cents = x.split(".")
        x = (p.number_to_words(cents[0][1:]) + " dollars and "
             + p.number_to_words(cents[1]) + " cents")
      else:
        x = p.number_to_words(x[1:]) + " dollars"
  return x


def convert_date(x):
  """
    Converts date by checking if there is a / or - surrounded by digits,
    rest of dates formats can be solved with regular
    number conversions.
      Args:
        x:
          str
      Returns:
        Returns a string.
  """
  if "/" in x or "-" in x:
    if ((x[x.find("/")-1].isdigit()
        and x[x.find("/")+1].isdigit())
       or (x[x.find("-")-1].isdigit() and x[x.find("-")+1].isdigit())):
      d = parser.parse
      p = inflect.engine()
      z = (d.strftime("%B ")
           + p.number_to_words(p.ordinal(int(d.strftime("%d"))))
           + ", " + p.number_to_words(d.strftime("%Y")))
      return z
  return x


def convert_time(x):
  """
    Converts time by checking if string has colon surorunded by digits
    and can convert for with or without seconds.
      Args:
        x:
          str
      Returns:
        Returns a string.
  """
  if ":" in x:
    if(x[x.find(":")-1].isdigit() and x[x.find(":") - 1].isdigit()):
      d = parser.parse(x)
      p = inflect.engine()
      if x.count(':') == 1:
        return (p.number_to_words(d.strftime("%H"))
                + " hours and " + p.number_to_words(d.strftime("%M"))
                + " minutes")
      if x.count(':') == 2:
        return (p.number_to_words(d.strftime("%H"))
                + " hours " + p.number_to_words(d.strftime("%M"))
                + " minutes and " + p.number_to_words(d.strftime("%S"))
                + " seconds")
  return x


def convert_ordinal(x):
  """
    If some characters are digits and some characters are not,
    checks if the ending of string belongs to ordinals.
    The inflect engine has a function ot convert ordinls.
      Args:
        x:
          str
      Returns:
        Returns a string.
  """
  end_ordinal = ["nd", "rd", "st", "th"]
  if (any(char.isdigit() for char in x)
     and not all(char.isdigit() for char in x)):
    if x[len(x) - 2:] in end_ordinal:
      p = inflect.engine()
      return p.number_to_words(x)
  return x


# code taken from
# https://www.geeksforgeeks.org/python-program-for-converting-roman-numerals-to-decimal-lying-between-1-to-3999/
def value(r):
  """
    Converts roman value into digit.
      Args:
        r:
          char
      Returns:
        Returns digit.
  """
  if (r == 'I'):
    return 1
  if (r == 'V'):
    return 5
  if (r == 'X'):
    return 10
  if (r == 'L'):
    return 50
  if (r == 'C'):
    return 100
  if (r == 'D'):
    return 500
  if (r == 'M'):
    return 1000
  return -1


def convert_roman(x):
  """
    Converts roman numeral into integer and then integer into string.
      Args:
        x:
          str
      Returns:
        Returns a string.
  """
  validRomanNumerals = ["M", "D", "C", "L", "X", "V", "I"]
  for char in x:
    if char not in validRomanNumerals:
      return x
  if len(x) > 1:
    res = 0
    i = 0

    while (i < len(x)):
      s1 = value(x[i])

      if (i + 1 < len(x)):

        # Getting value of symbol s[i + 1]
        s2 = value(x[i + 1])
        # Comparing both values
        if s1 >= s2:
          #   Value of current symbol is greater
          #   or equal to the next symbol
          res = res + s1
          i = i + 1
        else:
          # Value of current symbol is greater
          # or equal to the next symbol
          res = res + s2 - s1
          i = i + 2
      else:
        res = res + s1
        i = i + 1
    p = inflect.engine()
    return p.number_to_words(res)
  return x
# end of taken code


def convert_abbreviation(x):
  """
    Goes through abbreviation.txt and checks if the str is an abbreviation.
    If so, the txt provides the expanded form.
      Args:
        x:
          str
      Returns:
        Returns a string.
  """
  txt_file = open("abbreviation.txt")
  for line in txt_file:
    if line.split(" ")[0] == x:
      x = line.split(" ", 1)[1].strip("\n")
      return x
  return x


def tts_norm(str):
  res = ""
  str = re.sub(' +', ' ', str)
  str = str.replace(",", "")
  str = str.replace("-", " ")
  str = str.replace("(", " ")
  str = str.replace(")", " ")
  str = str.replace("\"", "")
  str = str.replace("\n", " \n")
  str = str.split(" ")
  for x in str:
    if len(x) > 1 and x.count(".") == 1:
      if x[len(x)-2] == "." and x[len(x)-1] == "\n":
        x = x[:len(x)-2] + "\n"
      elif x[len(x)-1] == ".":
        x = x[:len(x)-1]
    if any(char.isdigit() for char in x):
      x = convert_currency(x)
      x = convert_date(x)
      x = convert_time(x)
      x = convert_ordinal(x)
      if(x.isdigit()):
        x = x.replace(",", "")
        p = inflect.engine()
        x = p.number_to_words(x) + " "
    x = convert_roman(x)
    x = convert_abbreviation(x)
    res += x + " "
  res = res.replace(".", "")
  res = res.replace(",", "")
  res = res.replace("-", " ")
  return res.strip(" ")
