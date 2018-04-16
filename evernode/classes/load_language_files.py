"""
    Loads custom Modules into flask in modules folder. Routes use: routes.py
"""
import os
import sys
from ..functions import get_subdirectories
from ..helpers import JsonHelper


class LoadLanguageFiles:
    """ Loads modules and global language files """
    app = None
    module_packs = []

    def __init__(self, app):
        self.app = app
        self.app.config.update(dict(LANGUAGE_PACKS={}))
        self.find_files()

    def __call__(self):
        """ after init parse each language file and save it """
        for module_pack in self.module_packs:
            language_pack = {module_pack['name']: {}}
            current_pack = language_pack[module_pack['name']]
            for language in module_pack['languages']:
                current_pack.update({language: {}})
            for file_pack in module_pack['file_packs']:
                file = file_pack['file']
                data = None
                if os.path.exists(file):
                    data = JsonHelper.from_file(file)
                else:
                    raise FileNotFoundError(file)
                current_pack[file_pack['language']] \
                    .update({file_pack['name']: data})
            self.app.config['LANGUAGE_PACKS'].update(language_pack)

    def __get_modules(self) -> list:
        """  Get the subdirectories of modules folder """
        directory = os.path.join(sys.path[0], 'modules')
        return get_subdirectories(directory)

    def find_files(self):
        """ Gets modules routes.py and converts to module imports """
        modules = self.__get_modules()
        dirs = [dict(
            dir=os.path.join(sys.path[0], 'resources', 'lang'), module="root")]
        for module_name in modules:
            modules_folder = "modules/%s"
            if module_name is not None:
                modules_folder = modules_folder % (module_name.strip('/'))
            else:
                continue
            path = os.path.join(
                sys.path[0], modules_folder, 'resources', 'lang')
            if os.path.exists(path):
                dirs.append(dict(
                    dir=path,
                    module=module_name))
        for dir in dirs:
            module_pack = {
                'name': dir['module'],
                'languages': [],
                'file_packs': []
            }
            for path, subdirs, files in os.walk(dir['dir']):
                for subdir in subdirs:
                    module_pack['languages'].append(subdir)
                for name in files:
                    module_pack['file_packs'].append(dict(
                        file=os.path.join(path, name),
                        name=name.rsplit('.', 1)[0].lower(),
                        language=path.split("lang/", 1)[1].strip()
                    ))
            self.module_packs.append(module_pack)
        for module_pack in self.module_packs:
            module_pack['file_packs'] = \
                list({v['file']: v for v in module_pack['file_packs']}
                     .values())
        if 'DEBUG' in self.app.config and self.app.config['DEBUG']:
            print('--- Loading Language Files ---')
            print("Loaded Dirs: " + str(dirs))
            print("Loaded Module Packs: " + str(self.module_packs))
