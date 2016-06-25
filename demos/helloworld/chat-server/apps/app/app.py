#-*- coding:utf-8 -*-

import os.path
import uuid

import tornado.escape
import tornado.web
from tornado import gen

import turbo.log
from turbo.flux import state as turbo_state

from base import BaseHandler

logger = turbo.log.getLogger(__file__)


global_message_buffer = turbo_state.chat.message_buffer


class MainHandler(BaseHandler):
    def get(self):
        self.render("index.html", messages=global_message_buffer.cache)


class MessageNewHandler(BaseHandler):
    def post(self):
        message = {
            "id": str(uuid.uuid4()),
            "body": self.get_argument("body"),
        }
        # to_basestring is necessary for Python 3's json encoder,
        # which doesn't accept byte strings.
        message["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=message))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)
        global_message_buffer.new_messages([message])


class MessageUpdatesHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        cursor = self.get_argument("cursor", None)
        # Save the future returned by wait_for_messages so we can cancel
        # it in wait_for_messages
        self.future = global_message_buffer.wait_for_messages(cursor=cursor)
        messages = yield self.future
        if self.request.connection.stream.closed():
            return
        self.write(dict(messages=messages))

    def on_connection_close(self):
        global_message_buffer.cancel_wait(self.future)

