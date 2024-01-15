#!/usr/bin/env python3
import argparse
import sys
import os

class Tree(object):
  class Struct:
    def __str__(self):
      return str(self.__dict__)

  def __init__(self, root, relativeKey = False):
    self.root = root
    self.relativeKey = relativeKey
    if not os.path.isdir(self.root):
      raise OSError("Not a folder: {}".format(self.root))
    self.folders = {} # Map of folder data.
    self.files = {} # Map of file data.
    self.basenames = {}
    self.rootFolderData = self.scan(self.root)

  def scan(self, folder, parentData = None):
    folderData = self.Struct()
    folderData.folderDataList = []
    folderData.fileDataList = []
    folderData.name = folder
    folderData.basename = os.path.basename(folder)
    folderData.depth = 1

    if parentData:
        if parentData.relativeName:
            folderData.relativeName = self.useSlash(
              os.path.join(parentData.relativeName, folderData.basename)
            )
        else:
            folderData.relativeName = folderData.basename
    else:
        folderData.relativeName = ""

    key = folderData.relativeName if self.relativeKey else folder
    self.folders[key] = folderData

    for f in os.listdir(folder):
        filename = self.useSlash(
          os.path.join(folder, f)
        )
        if os.path.isdir(filename):
            data = self.scan(filename, folderData)
        elif os.path.isfile(filename):
            data = self.getFile(filename, folderData)

    if parentData:
        parentData.folderDataList.append(folderData)
        parentData.depth = max(parentData.depth, folderData.depth + 1)

    return folderData

  def getFile(self, filename, parentData):
    # Create a data struct for this file; link it to its parent folder data.
    fileData = self.Struct()
    fileData.name = filename
    fileData.basename = os.path.basename(filename)
    fileData.parentData = parentData
    if parentData and parentData.relativeName:
        fileData.relativeName = self.useSlash(
          os.path.join(parentData.relativeName, fileData.basename)
        )
    else:
        fileData.relativeName = fileData.basename

    self.files[filename] = fileData
    found = False
    for i in range(len(parentData.fileDataList)):
        if parentData.fileDataList[i].name == filename:
            # Replace the parent's entry for this file.
            parentData.fileDataList[i] = fileData
            found = True
            break
    if not found:
        # Add this file to the parent's list.
        parentData.fileDataList.append(fileData)

    return fileData

  def useSlash(self, path):
    return path.replace('\\', '/')




def main():
    root = os.path.dirname(os.path.realpath(__file__));
    root = os.path.dirname(root)

    tree = Tree(root, relativeKey = True)

    print(len(tree.folders))
    print(len(tree.files))
    for key, value in tree.files.items():
      print(f'{key} {value}')

if __name__ == "__main__":
    main()
