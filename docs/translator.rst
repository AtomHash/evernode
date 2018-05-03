.. _translator:

Translator
==============

This section will cover the basics of EverNode language translations.

Language translations are key to support internationalization. EverNode makes translations
easy with its built in Translator class. 


Translator Class
----------------

The Translator class uses a an index from the Content-Language HTTP header. If Content-Language is
not set the DEFAULT_LANGUAGE set in your config.json will be used. The Translator class defaults
to parse language packs from the root resoucres/lang folder.

| **Translator Class**
| class: :class:`evernode.classes.Translator`

::

    from evernode.classes import Translator

    translator = Translator()


What are Language Packs?
------------------------

Language Packs are files that end in :code:`.lang` that contain valid json. These files can be parsed
to translate certain messages from different languages.

**Root Folder:**
Let's create a file called hello-world.lang.

English Example(resources/lang/en)::

    {
        "message": "Hello World"
    }

French Example(resources/lang/fr)::

    {
        "message": "Bonjour le monde"
    }

**Module Folder:**
Let's create a file called hello-world.lang.

English Example(modules/<module-name>/resources/lang/en)::

    {
        "message": "Hello World"
    }

French Example(modules/<module-name>/resources/lang/fr)::

    {
        "message": "Bonjour le monde"
    }

You just created your first Language Pack. Now how do you use it? Simple.

How to use a Language Pack?
---------------------------

**Root Folder:**
Init the Translator app::

    from evernode.classes import Translator

    translator = Translator()
    print(translator.trans('hello-world.message'))

Output::

    # Content-language: en
    output: 'Hello World'

    # Content-language: fr
    output: 'Bonjour le monde'

**Module Folder:**
Init the Translator app::

    from evernode.classes import Translator

    translator = Translator(module_name='<module-name>')
    print(translator.trans('hello-world.message'))

Output::

    # Content-language: en
    output: 'Hello World'

    # Content-language: fr
    output: 'Bonjour le monde'

What Language is Used?
----------------------

EverNode will choose the index set in Content-Language. If the Content-Language(HTTP header) is :code:`fr`,
lang/fr is used. If Content-Language is not set, your :code:`DEFAULT_LANGUAGE` index is used. EverNode's default
config uses :code:`en`, lang/en will be used. Content-Language should use an ISO 639-1 code but can be anything.