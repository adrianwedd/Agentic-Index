import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'Agentic Index'
author = 'OpenAI'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
html_theme = 'sphinx_rtd_theme'

autodoc_typehints = 'description'

