import re
import string

# class takes relativeFilename constructor
class Note:
  def __init__(self, relativeFilename):
    self.relativeFilename = relativeFilename
    self.text = None
    self.hashtags = set()

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
      tag = tag.rstrip(''.join(punctuation_set))
      tag = tag.lower()
      self.hashtags.add(tag)

    return hashtags
