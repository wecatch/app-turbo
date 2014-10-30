# -*- coding:utf-8 -*-

# installed app list 
INSTALLED_APPS = (
    'user',
)

#  static file config
#  if application debug is true:
#      static_url is maked by application settings static_path
#  if application debug is false:
#      if cdn is true:
#          static url is cdn
#      if cdn is false:
#          static url is maked by application settings static_path
CDN = {
    'is': False,
    'host': 'http://www.staticfile.org/'
}

# refer to https://www.flickr.com/services/api/
RESPONSE_CODE_MESSAGE = {

}

#language
LANG = 'zh_CN'
