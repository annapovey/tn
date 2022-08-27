from ast import Str
from contextlib import nullcontext
import inflect
from dateutil import parser
import re
import random

ABBR_PATH = '../tn/abbreviation.txt'

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
      # seperating by period to get list with two elements, dollars and cents
      cents = x.split(".")
      # removing '$' sign from dollars
      x = p.number_to_words(cents[0][1:])
      # checking for singular of plural of dollar and cent
      if cents[0][1:] == "1":
        x += " dollar and "
      else:
        x += " dollars and "
      x += p.number_to_words(cents[1])
      if cents[1] == "01":
        x += " cent"
      else:
        x += " cents"
    else:
      x = p.number_to_words(x[1:])
      if x[1:] == "1":
        x += " dollar"
      else:
        x += " dollars"
  return x


def convert_year(y):
  # randomizing phrasing to immitate spoken english
  y = int(y)
  p = inflect.engine()
  # if second digit is zero
  if ((y - y % 100) / 100) % 10 == 0:
    # if last two digits are zero (ex. 2000 -> two thousand, 1000 -> one thousand)
    if y % 100 == 0:
      y = p.number_to_words(int((y - y % 1000) / 1000)) + " thousand"
    # if last two digits less than ten (ex. 2010 -> two thousand ten, 1008 -> one thousand eight)
    elif y % 100 < 10:
      if random.random() < 0.5:
        y = p.number_to_words(int((y - y % 1000) / 1000)) + " thousand " + p.number_to_words(int(y % 10))
      # other half of the time the number will get normally converted in convert_digit()
    # else last two digits are greater than 10
    else:
      # ex. 2022 -> twenty twenty two, 1011 -> ten eleven
      if random.random() < 0.5:
        y = p.number_to_words(int((y - y % 100) / 100)) + " " + p.number_to_words(y % 100)
      # ex. 2022 -> two thousand twenty two, 1011 -> one thousand eleven
      else:
        y = p.number_to_words(int((y - y % 1000) / 1000)) + " thousand " + p.number_to_words(int(y % 10))
  # four digit numbers not 2000 or 1000
  elif y < 2000 and y >= 1100:
    # if last two digits are zeros (ex. 1900 -> ninetenn hundred, 1200 -> twelve hundred)
    if y % 100 == 0:
      y = p.number_to_words(int(y / 100)) + " hundred"
    # if last two digits less than ten (ex. 1909 -> ninetenn O nine, 1301 -> thirteen O one)
    elif y % 100 < 10:
      y = p.number_to_words(int((y - y % 100) / 100)) + " O " + p.number_to_words(y % 100)
    # else last two digits greater than ten (ex. 1931 -> nineteen thirty one, 1757 -> seventeen fifty seven)
    else:
      y = p.number_to_words(int((y - y % 100) / 100)) + " " + p.number_to_words(y % 100)
  return str(y)


def convert_date(x, phrase=False):
  # parameter phrase was already checked to be a phrase
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
  if (x.count("/") == 2 or x.count("-") == 2) or phrase:
    if ((x[x.find("/") - 1].isdigit()
       and x[x.find("/") + 1].isdigit())
      or (x[x.find("-") - 1].isdigit() and x[x.find("-") + 1].isdigit())) or phrase:
      d = parser.parse(x)
      p = inflect.engine()
      a = random.random()
      #three ways of saying dates
      # ex. October fourth, ---
      if a < 0.33:
        x = (d.strftime("%B ")
           + p.number_to_words(p.ordinal(int(d.strftime("%d"))))
           + ", ")
      # ex. the fourth of October, 
      elif a < 0.66:
        x = "the " + p.number_to_words(p.ordinal(int(d.strftime("%d")))) + " of " + (d.strftime("%B ")
                                               + ", ")
      # ex. the fourth of October in 
      else:
        x = "the " + p.number_to_words(p.ordinal(int(d.strftime("%d")))) + " of " + (d.strftime("%B ")
                                               + "in ")
      # all cases have year at the end
      x += convert_year(d.strftime("%Y"))
      return x
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
    if (x[x.find(":") - 1].isdigit() and x[x.find(":") - 1].isdigit()):
      d = parser.parse(x)
      p = inflect.engine()
      if x.count(':') == 1:
        if d.strftime("%M") == "00":
          return p.number_to_words(d.strftime("%H")) + " o'clock"
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
  validRomanNumerals = ["X", "V", "I"]
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
  txt_file = open(ABBR_PATH) 
  for line in txt_file:
    if line.split(" ")[0] == x:
      x = line.split(" ", 1)[1].strip("\n")
      return x
  return x

def convert_digit(x):
  p = inflect.engine()
  # numbers seperated by a dash not in a date haven't been dealt with
  dash_pattern = re.compile(r'\d+-\d+')
  dash_pattern_matches = reversed(list(dash_pattern.finditer(x)))
  for match in dash_pattern_matches:
    x = x[:match.start()] + p.number_to_words(x[match.start():match.start() + 2]) + " " + p.number_to_words(
      x[match.end() - 2:match.end()]) + x[match.end():]
  x_without_punc = x.replace(",", "")
  x_without_punc = x_without_punc.replace(".", "")
  if (x_without_punc.isdigit()):
    if "." in x:
      # stripping trailing zeros in decimals or trailing '.0' on integers
      x = x.strip("0")
      x = x.strip(".")
    x = x.replace(",", "")
    x = p.number_to_words(x) + " "
  return x

def beginning_punctuation(s):
  # if user doesn't want punctuation, it is removed at the end
  s = re.sub(r';', ' ;', s)
  s = s.replace("(", "( ")
  s = s.replace(")", " )")
  s = s.replace(" \"", "  \" ")
  s = s.replace("/", " / ")
  s = s.replace("\" ", " \"  ")
  s = s.replace("\n", " \n")
  s = s.replace(", ", " , ")
  s = s.replace("!", " !")
  s = re.sub(r'([0-9])-([a-zA-Z])', r'\1 - \2', s)
  s = s.replace("?", " ?")
  s = re.sub(r'([a-zA-Z])]-([a-z][A-Z])', r'\1 - \2', s)
  s = re.sub(r'([a-zA-Z])-([0-9])', r'\1 - \2', s)
  s = re.sub(r'(^|\s)\-(\d)', r' negative \2', s)
  s = re.sub(r'(\$)([0-9\.]+)\s(million|thousand|trillion|hundred|billion)', r'\2 \3 \1 ', s)
  s = re.sub("([a-zA-Z])-([a-zA-Z])", r'\1 - \2', s)
  s = re.sub(r'([0-9]+)x', r'\1 times', s)
  s = re.sub(r'x([0-9]+)', r'times \1', s)
  s = s.replace("%", " percent")
  s = s.replace("$ ", "dollars")
  s = re.sub(r'#([0-9]+)', r'number \1', s)
  s = re.sub(u'\N{DEGREE SIGN}', 'degrees ', s)
  s = re.sub(r'degrees ([0-9]+)', '\1 degrees', s)
  s = re.sub(' +', ' ', s)
  return s

def final_punctuation(res, punctuation):
  # # acronyms are seperated by spaces (ex. NASA -> N A S A)
  res = re.sub(r'([A-Z])([A-Z])', r'\1 \2', res)
  res = re.sub(r'([A-Z])([A-Z])', r'\1 \2', res)
  res = res.replace("  \"  ", "\"")
  res = res.replace(" \" ", "\"")
  res = re.sub(r' +', ' ', res)
  if punctuation:
    res = res.replace(" .", ".")
    res = res.replace(" ,", ",")
    res = res.replace(" - ", "-")
    res = res.replace("( ", "(")
    res = res.replace(" )", ")")
    res = res.replace(" \n", "\n")
    res = res.replace(" :", ":")
    res = res.replace(" !", "!")
    res = res.replace(" ?", "?")
  else:
    res = re.sub(r'[^A-Z^a-z^\n^\']', ' ', res)
  res = re.sub(r' +', ' ', res)
  return res

def date_patterns(s):
  # (ex. 90s -> ninety's, 1760s -> seventeen sixty's)
  p = inflect.engine()
  decade_pattern = re.compile(r'[0-9]{2,4}s')
  decade_pattern_matches = reversed(list(decade_pattern.finditer(s)))
  for match in decade_pattern_matches:
    s = s[:match.start()] + p.number_to_words(int(s[match.start():match.end()-1])) + "'s" + s[match.end():]

  # (ex. (1721) -> seventeen twenty one)
  date_parenthesis_pattern = re.compile(r'\( \d{4} \)')
  date_parenthesis_matches = reversed(list(date_parenthesis_pattern.finditer(s)))
  for match in date_parenthesis_matches:
    s = s[:match.start()] + "( " + convert_year(s[match.start()+2:match.end()-2]) + " )" + s[match.end():]

  # (ex. 2012-2019 -> two thousand twelve to two thousand nineteen, 1931-1987 -> nineteen thirty one to nineteen eighty seven)
  date_range_pattern = re.compile(r'(\d{4})\-(\d{4}[^\-])')
  date_range_matches = reversed(list(date_range_pattern.finditer(s)))
  for match in date_range_matches:
    s = s[:match.start()] + convert_year(s[match.start():match.start() + 4]) + " to " + convert_year(
      s[match.start() + 5:match.start() + 9]) + s[match.end():]

  # (ex. 1980 to 2000 -> ninteen eighty to two thousand)
  date_range_pattern = re.compile(r'(\d{4}) to (\d{4})')
  date_range_matches = reversed(list(date_range_pattern.finditer(s)))
  for match in date_range_matches:
    s = s[:match.start()] + convert_year(s[match.start():match.start() + 4]) + " to " + convert_year(s[match.end()-4:match.end()]) + s[match.end():]

  # (ex. Jan. 13 1981 -> January thirteen nineteen eighty one, November 2 21 -> the second of November in two thousand twenty one)
  s_lower = s.lower()
  date_pattern = re.compile(
    r'(january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sept|sep|october|oct|november|nov|december|dec)\.?\s\d+\,?\s\d+')
  original_len = len(s_lower)
  date_matches = date_pattern.finditer(s_lower)
  for match in date_matches:
    if (original_len - match.end()) == 0:
      s = s[:-(original_len - match.start())] + convert_date(match.group(), True)
    else:
      s = s[:-(original_len - match.start())] + convert_date(match.group(), True) + s[-(
            original_len - match.end()):]

  # (ex. january )
  s_lower = s.lower()
  date_pattern = re.compile(
    r'\d+\s(january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|october|oct|september|sept|sep|november|nov|december|dec)\.?\,?\s\d+')
  original_len = len(s_lower)
  date_matches = date_pattern.finditer(s_lower)
  for match in date_matches:
    if (original_len - match.end()) == 0:
      s = s[:-(original_len - match.start())] + convert_date(match.group(), True)
    else:
      s = s[:-(original_len - match.start())] + convert_date(match.group(), True) + s[-(
            original_len - match.end()):]

  year = re.compile(r'(1|2)[0-9]{3}')
  year_matches = reversed(list(year.finditer(s)))
  for match in year_matches:
    s = s[:match.start()] + convert_year(s[match.start():match.end()])+ s[match.end():]
  
  s_lower = s.lower()
  month_date_pattern = re.compile(r'(january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sept|sep|october|oct|november|nov|december|dec)\.?\s\d+[a-z]{,3}')
  original_len = len(s_lower)
  month_date_matches = month_date_pattern.finditer(s_lower)
  for match in month_date_matches:
    match_text = s[match.start():match.end()].split()
    p = inflect.engine()
    if (original_len - match.end()) == 0:
      s = s[:-(original_len - match.start())] + match_text[0] + " " + p.number_to_words(match_text[1])
    else:
      s = s[:-(original_len - match.start())] + match_text[0] + " " + p.number_to_words(match_text[1]) + s[-(original_len - match.end()):]
  return s

def tts_norm(s, punctuation=False, uppercase=False):
  res = ""
  # if punctuation is being kept, it should be spaced out from regular
  s = beginning_punctuation(s)
  print(s)
  s = date_patterns(s)
  s = re.sub(r'([0-9]+)([a-zA-Z])', r'\1 \2', s)
  s = s.split(" ")
  for x in s: 
    add_period = False
    x = convert_abbreviation(x)
    if len(x) > 1:
      if x[len(x) - 1] == ".":
        if punctuation:
          add_period = True
        x = x[:len(x) - 1]
    if any(char.isdigit() for char in x):
      x = convert_currency(x)
      x = convert_date(x)
      x = convert_time(x)
      x = convert_ordinal(x)
      x = convert_digit(x)
    x = convert_roman(x)
    res += x + " "
    if add_period:
      res += "."
  print(res)
  res = final_punctuation(res, punctuation)
  if uppercase:
    res = res.upper()
  return res.strip(" ")
