from acid.session import send

def status_finalizer(msg, *_):
    return ('status' in msg and
            not set(msg['status']).intersection({'eval-error'}))

class BaseHandler(object):

    finalizer = status_finalizer

    def __repr__(self):
        return "<Handler: {}>".format(self.__class__.name)

    @classmethod
    def do_init(cls):
        inst = cls()
        inst.on_init()
        return inst

    def with_matcher(self, matcher):
        self.matcher.update(matcher)

    def __init__(self):
        self.matcher = {}
        self.fwd_handlers = {}

    def configure(self, *args, **kwargs):
        self.nvim = kwargs['nvim']
        self.context = kwargs
        self.on_configure(*args, **kwargs)
        return self

    def new_child_handler(self, handler):
        if handler not in self.fwd_handlers:
            self.fwd_handlers[handler] = self.context['handlers']\
                .get(handler).do_init().configure(**self.context)
        return self.fwd_handlers[handler]


    def pass_to(self, msg, handler):
        handler = self.new_child_handler(handler)
        handler.on_handle(msg)

    def on_init(self):
        pass

    def on_configure(self, *_a, **_k):
        pass

    def on_pre_send(self, *_):
        pass

    def pre_send(self, *args):
        self.on_pre_send(*args)

    def on_pre_handle(self, *_):
        pass

    def pre_handle(self, *args):
        self.on_pre_handle(*args)

    def on_handle(self, *_):
        pass

    def after_finish(self, *_):
        for h in self.fwd_handlers.values():
            h.after_finish(*_)

        self.on_after_finish(*_)

    def on_after_finish(self, *_):
        pass

    def gen_handler(self, stop_handler):
        nvim = self.nvim
        finalizer = self.__class__.finalizer
        on_handle = self.on_handle
        after_finish = self.after_finish

        def handler(msg, wc, key):
            try:
                nvim.async_call(lambda: on_handle(msg, wc, key))
            finally:
                if finalizer(msg, wc, key):
                    stop_handler(wc, key)
                    nvim.async_call(after_finish)

        return handler

class SingletonHandler(BaseHandler):

    instances = {}

    def __repr__(self):
        return "<Handler: {}>".format(self.__class__.name)

    @classmethod
    def do_init(cls):
        if not cls.name in SingletonHandler.instances:
            inst = cls()
            inst.on_init()
            SingletonHandler.instances[cls.name] = inst
        else:
            inst = SingletonHandler.instances[cls.name]
        return inst

    @classmethod
    def deinit(cls):
        del SingletonHandler.instances[cls.name]

class WithFSM(BaseHandler):

    initial_state = "init"

    def __repr__(self):
        return "<FSMHandler: {} on state {}>".format(
            self.__class__.name, self.current_state
        )

    def on_init(self):
        self.current_state = self.initial_state
        self.current_handler_fn = self.handle_init
        return self

    def configure(self, *args, **kwargs):
        super().configure(*args, **kwargs)
        self.session_handler = kwargs['session_handler']
        self.url = kwargs['url']
        return self

    def change_state(self, new_state, payload, *handlers):
        handlers = list(handlers)
        handlers.append(self)
        send(self.session_handler, self.url, handlers, payload)
        self.current_state = new_state
        self.current_handler_fn = getattr(
            self,
            'handle_{}'.format(new_state),
            lambda *args, **kwargs: None
        )

    def on_handle(self, msg, wc, key):
        self.current_handler_fn(msg, wc, key)
