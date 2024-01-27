import re
import string

# class takes relativeFilename constructor
class Note:
  def __init__(self, relativeFilename):
    self.relativeFilename = relativeFilename
    self.text = None
    self.date = None
    self.time = None
    self.year = None
    self.first = None
    self.second = None
    self.specials = set()
    self.hashtags = set()
    self.name = self.relativeFilename.split('/')[-1].split('.')[0]

  def load(self, text):
    self.text = text

  def scanHashtags(self):
    self.hashtags = set()
    hashtag_pattern = re.compile(r'\B\#[^\s#]+')
    # Find all matches in the text
    hashtags = hashtag_pattern.findall(self.text)
    # normalize
    punctuation_set = set(string.punctuation)
    for tag in hashtags:
      # normalize the tag
      tag = tag[1:]
      tag = tag.rstrip(''.join(punctuation_set))
      tag = tag.lower()
      # special case?
      dateTime = self.isDateTime(tag)
      if (dateTime):
        self.date = dateTime[0]
        self.time = dateTime[1]
        if not self.year:
          self.year = self.date[:4]
      else:
        special = self.isSpecial(tag)
        if (special):
          self.specials.add(tag)
        else:
          if (not self.first):
            self.first = tag
          elif (not self.second):
            self.second = tag
          self.hashtags.add(tag)

    return hashtags

  def isDateTime(self, tag):
    # if the tag start with an isodate, then try to extract the
    # date and time.
    # pattern:
    #   date [time]
    #   where date can be: 2024, 2024-01, 2024-01-01
    iso_date_pattern = re.compile(r'^(\d{4}(-\d{2}(-\d{2})*)*)(?:[T_](\d{2}[:-]\d{2}[:-]\d{2}))?')
    match = iso_date_pattern.match(tag)
    if match:
      date = match.group(1)
      time = match.group(4) if match.group(4) else None
      return date, time
    return None

  def isSpecial(self, tag):
    # return the special tag, if it's special
    if (tag == 'special'):
      return tag
    return None


# some testing functions
def main():
  note=Note('')
  note.load('')
  print(note.dateTime('2023-12-30_14-29-55'))
  print(note.dateTime('2024-01-07_09-49-16'))
  print(note.dateTime('2024-01-07T09-49-16'))
  print(note.dateTime('2024-01-07T09:49:16'))
  print(note.dateTime('2024-01-07'))
  print(note.dateTime('2024-01-07'))
  print(note.dateTime('f2024'))
  print(note.dateTime('2023'))
  print(note.dateTime('2022year'))
  print(note.dateTime('2022-12'))


if __name__ == "__main__":
  main()
