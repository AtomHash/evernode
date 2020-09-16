"""
    Loads custom Modules into flask in modules folder. Routes use: routes.py
"""
import os
import sys
from .json import Json


class LoadLanguageFiles:
    """ Loads modules and global language files """
    app = None
    evernode_app = None
    module_packs = []

    def __init__(self, evernode_app):
        self.evernode_app = evernode_app
        self.app = evernode_app.app
        self.module_packs = []
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
                    data = Json.from_file(file)
                else:
                    raise FileNotFoundError(file)
                current_pack[file_pack['language']] \
                    .update({file_pack['name']: data})
            self.app.config['LANGUAGE_PACKS'].update(language_pack)

    def find_files(self):
        """ Gets modules routes.py and converts to module imports """
        modules = self.evernode_app.get_modules()
        root_path = sys.path[0] if self.evernode_app.root_path is None \
            else self.evernode_app.root_path
        dirs = [dict(
            dir=os.path.join(root_path, 'resources', 'lang'), module="root")]
        for module_name in modules:
            modules_folder = 'modules{}%s'.format(os.sep)
            if module_name is not None:
                modules_folder = modules_folder % (module_name.strip(os.sep))
            else:
                continue
            path = os.path.join(
                root_path, modules_folder, 'resources', 'lang')
            if os.path.isdir(path):
                dirs.append(dict(dir=path, module=module_name))
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
                    if name.startswith('.'):
                        # ignore hidden files
                        continue
                    module_pack['file_packs'].append(dict(
                        file=os.path.join(path, name),
                        name=name.rsplit('.', 1)[0].lower(),
                        language=path.split("lang%s" % (os.sep), 1)[1].strip()
                    ))
            self.module_packs.append(module_pack)
        for module_pack in self.module_packs:
            module_pack['file_packs'] = \
                list({v['file']: v for v in module_pack['file_packs']}
                     .values())
        if self.app.config['DEBUG']:
            print('--- Loaded Language Files ---')
            print("Loaded Dirs: " + str(dirs))
            print("Loaded Language Packs: " + str(self.module_packs))
