import os
from subprocess import Popen, PIPE
from platform import system

import sublime
import sublime_plugin

if system() == "Windows":
  slash = "\\"
else:
  slash = "/"


# Return various paths to the file.
# Return a number of different file paths for various uses.
# Ex: If a file's full path is /Users/me/git/my.repo/dir/file.php, you will get the following:
#    ['my.repo/dir/file.php', 'my.repo', 'dir/file.php', '/Users/me/git/my.repo', 'file.php']
# --- File with Repo -------- Repo Name - File no Repo ------ Repo location ------ File Name
# If outside of folder structure, returns full path in first subarray.
def getPaths(obj):
  projectFolders = obj.view.window().folders()
  path = obj.view.file_name()

  relativeToFolder = path # If outside of open folder, we'll just give absolute path
  repoName = ''
  relativeToRepo = ''
  pathToRepo = ''
  fileName = os.path.basename(path)

  # In the case that we have multiple folders open, find the one the file is in.
  for folder in projectFolders:
    if folder in path:
      relativeToFolder = path.replace(folder, '')[1:]
      repoName = relativeToFolder[:relativeToFolder.find(slash)]
      relativeToRepo = relativeToFolder[len(repoName)+1:]
      pathToRepo = path[:-len(relativeToRepo)-1]
      break

  return [relativeToFolder, repoName, relativeToRepo, pathToRepo, fileName]


def simpleShellExecute(command, executePath):
  execution = Popen(command, cwd=executePath, stdout=PIPE, stderr=PIPE)
  (results, error) = execution.communicate()

  if len(error) == 0:
    return results.decode('utf-8').strip()
  else:
    return ""



class PushCurrentFileCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    paths = getPaths(self)

    if len(paths[2]) != 0 and len(paths[3]) != 0:
      command = ['/Users/kyleg/bin/push', paths[2]]
      simpleShellExecute(command, paths[3])
      sublime.status_message("Pushed %s from %s" % (paths[2], paths[3]))


  def is_enabled(self):
    return bool(self.view.file_name() and len(self.view.file_name()) > 0)