'''
@author: Dimitrios Kanellopoulos
@contact: jimmykane9@gmail.com
'''
import os
import re
import logging
import config

import webapp2
import jinja2

from google.appengine.ext import blobstore
from google.appengine.api import files,users,images
from google.appengine.ext.db import ReferencePropertyResolveError
from google.appengine.ext.webapp import blobstore_handlers


class RootPage(webapp2.RequestHandler):

    def get(self):
        jinja_environment = self.jinja_environment
        template = jinja_environment.get_template("/index.html")
        self.response.out.write(template.render({'content': 'OK'}))

    @property
    def jinja_environment(self):
        jinja_environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                os.path.join(os.path.dirname(__file__),
                '../views'
            ))
        )
        return jinja_environment


class UploadFormHandler(webapp2.RequestHandler):

    def get(self):
        image_url = self.request.get('image_url')

        upload_url = blobstore.create_upload_url('/handleblobs/')
        jinja_environment = self.jinja_environment
        template = jinja_environment.get_template("/form.html")
        self.response.out.write(template.render({
            'upload_url': upload_url,
            'image_url': image_url
        }))

    @property
    def jinja_environment(self):
        jinja_environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                os.path.join(os.path.dirname(__file__),
                '../views'
            ))
        )
        return jinja_environment


class UploadBlobsHandler(blobstore_handlers.BlobstoreUploadHandler):

    def post(self):
        try:
            upload = self.get_uploads()[0]
            logging.info(upload)
            url = images.get_serving_url(upload)
            # Do something with it.
        except:
            self.redirect('/uploadform/?error', abort=True)

        self.redirect('/uploadform/?success&image_url=' + url)

