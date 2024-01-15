#!/usr/bin/env python3
import argparse
import sys
import os
from tree import Tree
from note import Note
from index import Index

class Celia(object):
  def __init__(self, root):
    self.root = root
    self.notes = []
    self.keys = []

  def run(self):
    self.findNotes()
    self.index = Index(self.notes)
    self.writeIndex()

  def findNotes(self):
    tree = Tree(self.root, relativeKey = True)
    notesFolder = tree.folders['pages']
    self.notesRoot = notesFolder.name
    # find notes on disk
    prefix = len(self.notesRoot)
    for file in [f for f in tree.files if f.startswith(self.notesRoot)]:
      relative = file[prefix+1:]
      self.notes.append(Note(relative))
    # scan notes
    for note in self.notes:
      self.loadNote(note)
      note.scanHashtags()

  def loadNote(self, note):
    filename = self.notesRoot + '/' + note.relativeFilename
    with open(filename, 'r', encoding='utf-8') as file:
      text = file.read()
      note.load(text)

  def writeIndex(self):
    text = self.index.toMd()
    fileName = os.path.join(self.root, '_index.md')
    with open(fileName, 'w') as file:
      file.write(text)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-v", "--verbose", action="store_true", help="be verbose")
  args = parser.parse_args()

  file = os.path.realpath(__file__)
  folder = os.path.dirname(file)
  parent = os.path.dirname(folder)

  celia = Celia(parent)

  celia.run()


if __name__ == "__main__":
  main()
