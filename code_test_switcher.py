import os
import re
import functools
import sublime
import string
import sublime_plugin

class SwitchBetweenCodeAndTest(sublime_plugin.TextCommand):
  def run(self, args):
    opposite_file_names = self.opposite_file_names()
    alternates = self.project_files(opposite_file_names)

    if alternates:
      if len(alternates) == 1:
        self.view.window().open_file(alternates.pop())
      else:
        callback = functools.partial(self.on_selected, alternates)
        self.view.window().show_quick_panel(alternates, callback)
    else:
      sublime.error_message("No file found")

  def opposite_file_names(self):
    file_name = self.view.file_name().split(os.sep)[-1]
    return [
      file_name.replace("-test", "")
    ]

  def on_selected(self, alternates, index):
    if index == -1:
      return

    self.view.window().open_file(alternates[index])

  def walk(self, directory):
    for dir, dirnames, files in os.walk(directory):
      # Skip hidden directories
      if re.search('(^|\/)\.', dir):
        continue
      dirnames[:] = [dirname for dirname in dirnames]
      yield dir, dirnames, files

  def project_files(self, files_matcher):
    directories = self.view.window().folders()
    candidates = []
    for directory in directories:
      for dirname, _, files in self.walk(directory):
        for file in files:
          if file in files_matcher:
            candidates += [os.path.join(dirname, file)]
    return candidates
