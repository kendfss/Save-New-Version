import sublime
import sublime_plugin
import os

def namespacer(path:str, sep:str='_', start:int=2) -> str:
    """
    Returns a unique version of a given string by appending an integer

    example:
        tree:
            /folder
                /file.ext
                /file_2.ext

        >>> nameSpacer('file', sep='-', start=2)
        >>> nameSpacer('file', sep='_', start=2)
        file_3.ext
        >>> nameSpacer('file', sep='_', start=0)
        file_0.ext
    """
    id = start
    oldPath = path[:]
    while os.path.exists(path): ##for general use
        newPath = list(os.path.splitext(path))
        if sep in newPath[0]:
            if newPath[0].split(sep)[-1].isnumeric():
                # print('case1a')
                id = newPath[0].split(sep)[-1]
                newPath[0] = newPath[0].replace(
                        '{}{}'.format(sep, id), 
                        '{}{}'.format(sep, str(int(id)+1))
                    )
                path = ''.join(newPath)
            else:
                # print('case1b')
                newPath[0] += '{}{}'.format(sep, id)
                path = ''.join(newPath)
                id += 1
        else:
            # print('case2')
            newPath[0] += '{}{}'.format(sep, id)
            path = ''.join(newPath)
            id += 1
    return path

def scrape(path):
    with open(path, 'r') as fob:
        return fob.read()

class SaveNewVersionCommand(sublime_plugin.WindowCommand):
    def run(self):

        old_name = self.window.active_view().file_name()
        new_name = namespacer(old_name)
        
        text = scrape(old_name)
        
        with open(new_name, 'w') as fob:
            fob.write(text)

        self.window.run_command('close_file')
        self.window.run_command('open_file', {"file": new_name})