from urllib.parse import quote

class Index:
  def __init__(self, notes):
    self.notes = notes
    self.map = {}

    for note in notes:
      print(note.hashtags)
      for tag in note.hashtags:
        value = note.relativeFilename
        if tag in self.map:
          self.map[tag].append(value)
        else:
          self.map[tag] = [value]

  def toMd(self):
    text = ''

    text +='[readme](./readme.md) | '
    text +='[index](./index.md)'
    text +='\n\n'

    text += '# index'
    text +='\n\n'

    sortedTags = sorted(self.map.keys())
    for tag in sortedTags:
      anchor = quote(tag[1:], safe='')
      text += f'[{tag}](#{anchor}) '

    text += '\n\n'

    for tag in sortedTags:
      label = tag[1:]
      anchor = quote(label, safe='')
      text += f'### {label}'
      if (label != anchor):
        text += f' {{{anchor}}}'
      text += '\n'
      for note in self.map[tag]:
        label = note[:-3]
        link = 'pages/' + note
        text += f'* [{label}]({link})'
        text += '\n'
      text += '\n'

    return text
