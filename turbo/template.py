# -*- coding:utf-8 -*-
from __future__ import absolute_import, print_function

import re
import functools

from turbo.conf import app_config

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    raise ImportError('jinja2 module ImportError')

class Jinja2Environment(Environment):
    """find template location
    
    according to current parent and template relative path to find template path 

    args:
        template current template that needs to locate
        parent which call template with extends or include directive

    return:
        real template path

    example:
        input:
            template ../../base.html
            parent app/app/index.html
        output:
            base.html

        input:
            template header.html
            parent app/app/index.html
        output:
            app/app/header.html 

        input:
            template ../header.html
            parent app/app/index.html
        output:
            app/header.html 

    """

    relative_path = re.compile('(./|../)', re.IGNORECASE)
    relative_dir = re.compile('([^/\s]{1,}/)', re.IGNORECASE)
    real_name = re.compile('([^/\s]{1,}$)')

    def join_path(self, template, parent):
        t_group = self.relative_path.findall(template)
        p_group = self.relative_dir.findall(parent)

        t_group_length = len(t_group)
        template_name = template
        # 
        real_template_path = p_group
        if t_group_length:
            template_name = self.real_name.match(template, template.rfind('/')+1).group()        
            real_template_path = p_group[0:0-t_group_length]

        real_template_path.append(template_name)
        return ''.join(real_template_path)



def turbo_jinja2(func):
    _jinja2_env = Jinja2Environment(loader=FileSystemLoader(app_config.web_application_setting['template_path']), auto_reload=app_config.web_application_setting['debug'])
    @functools.wraps(func)
    def wrapper(self, template_name, **kwargs):
        template = _jinja2_env.get_template(('%s%s')%(self.template_path, template_name))
        return template.render(handler=self, request=self.request, xsrf_form_html=self.xsrf_form_html(),
            context=self.get_context(), **kwargs)

    return wrapper