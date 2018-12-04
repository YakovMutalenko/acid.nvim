from acid.handlers import BaseHandler
from acid.nvim.log import info, log_debug, warning, log_error
from acid.zen.ui import build_window


class Handler(BaseHandler):

    name = "Doc"
    priority = 0

    def on_init(self, *_):
        self.doc_buf_nr = None

    def on_configure(self, transform, *args, **kwargs):
        log_debug('Got {} as transform fn', transform)
        self.transform = transform

    def on_handle(self, msg, *_):
        if 'no-info' in msg.get('status', []):
            warning(self.nvim, "No information for symbol")
            return

        try:
            lines = self.transform(msg)
        except Exception as e:
            warning(self.nvim, "Couldn't transform msg into doc.")
            log_error(e)
            return

        no_doc_buffer = self.doc_buf_nr is None
        buf_win_nr = self.nvim.funcs.bufwinnr(self.doc_buf_nr)
        doc_len = len(lines)

        if no_doc_buffer or buf_win_nr == -1:
            cmds = ['file acid://doc',
                    'wincmd p']

            self.doc_buf_nr = build_window(
                self.nvim, close=1, commands=cmds, throwaway=1,
                orientation="leftabove {} split".format(doc_len)
            )
        else:
            self.nvim.command('{} wincmd w | resize {} | wincmd p'.format(
                    buf_win_nr, doc_len
            ))

        log_debug(lines)
        self.nvim.buffers[self.doc_buf_nr][:] = lines
