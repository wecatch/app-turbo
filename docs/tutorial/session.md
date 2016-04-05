Turbo has built-in session support. You can easily to customize session store and control the life cycle of a session.


#### The life cycle of a session

By default, the `BaseBaseHandler` class has a `property` called `session`. When tornado server 
prepares to serve a user request, if you call `self.seesion` by yourself in `prepare` hooks or somewhere else before `on_finish` hooks called, a `session_id` will be added to response headers, default in cookie.