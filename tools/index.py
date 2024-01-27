from urllib.parse import quote

class Index:
  def __init__(self, notes):
    self.notes = notes
    self.map = {}

    for note in notes:
      for tag in note.hashtags:
        if tag in self.map:
          self.map[tag].append(note)
        else:
          self.map[tag] = [note]

  def toMd(self):
    text = ''

    text +='[README](README.md) | '
    text +='[index](pageindex.md)'
    text +='\n\n'

    text += '# index'
    text +='\n\n'

    sortedTags = sorted(self.map.keys())
    for tag in sortedTags:
      anchor = quote(tag, safe='')
      text += f'[{tag}](#{anchor}) '

    text += '\n\n'

    for tag in sortedTags:
      label = tag
      anchor = quote(label, safe='')
      text += f'### {label}'
      if (label != anchor):
        text += f' {{{anchor}}}'
      text += '\n'
      for note in self.map[tag]:
        label = note.name
        link = 'pages/' + note.relativeFilename
        text += f'* [{label}]({link})'
        text += self.suffix(note, tag)
        text += '\n'
      text += '\n'

    return text

  def suffix(self, note, tag):
    # Get suffix display text for this note, under this tag
    suffix = ''
    if (note.first):
      otherTag = note.second
      if (note.first != tag):
        otherTag = note.first
      if otherTag:
        suffix += f' [{otherTag}]'

    if note.year:
      suffix += f' [{note.year}]'

    return suffix
