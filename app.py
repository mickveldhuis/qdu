import sys
import webbrowser
import json
import urwid

from services import NewsService

PALETTE = [
    ('body', 'white', 'black'),
    ('footer', 'white', 'black', 'bold'),
    ('header', 'white', 'dark magenta', 'bold'),
    ('container', 'white', 'black'),
    ('button', 'light magenta', 'black')
]

class BaseView(urwid.WidgetWrap):
    def __init__(self, controller):
        self.controller = controller
        super().__init__(self.window())

    def window(self):
        pass

    def quit_program(self):
        raise urwid.ExitMainLoop()

    def on_quit(self, button):
        self.quit_program()

class UpdatesView(BaseView):
    def __init__(self, controller):
        super().__init__(controller)

    def window(self):
        hd = urwid.Columns([
            urwid.Text(u'Quick Daily Updates'),
            urwid.Text(u'[Q/q]: Quit'),
            urwid.Text(u'[↑/↓]: Up/Down')
        ])

        hd = urwid.AttrMap(hd, 'header')

        lb_content = []

        self.walker = urwid.SimpleFocusListWalker(lb_content)
        self.listbox = urwid.ListBox(self.walker)

        view = urwid.Frame(self.listbox, header=hd)

        return view

    def fill_window(self):
        div = urwid.Divider()

        lb_content = [div]
        
        items = self.controller.news_service.get_news()

        for item in items:
            lb_content.append(self._gen_news_item(
                item['title'], item['date'], item['text'], item['url']))

        self.walker[:] = lb_content
        self.listbox.set_focus(1) # Set focus to the first news item
    
    def _gen_news_item(self, title, date, text, url):
        div = urwid.Divider()

        pile = urwid.Pile([
            div,
            urwid.Padding(urwid.Text(text), align='center', width=('relative', 90)),
            div,
            urwid.Padding(urwid.Button(('button', u'Go To Article'), self.to_article, url),
                                  align='center', width=('relative', 90))
        ])

        item = urwid.Padding(urwid.LineBox(pile, title='{} [{}]'.format(title, date)),
                            align='center', width=('relative', 80))

        return item
    
    def to_article(self, button, url):
        webbrowser.open(url, new=2)

class DailyUpdater:
    def __init__(self):
        self.view = UpdatesView(self)
        self.news_service = None

    def main(self, source):
        if not self.is_provider(source):
            print('News source not available, please check the providers.json file!')
            self.terminate()
        
        self.news_service = NewsService(source)

        self.view.fill_window()

        self.loop = urwid.MainLoop(self.view, palette=PALETTE, unhandled_input=self.key_input)
        self.loop.run()

    def key_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        else:
            pass

    def is_provider(self, provider):
        return provider in self._get_providers()

    def _get_providers(self):
        with open('providers.json', 'r') as pf:
            prov = json.load(pf)
        
        return [*prov.keys()]
    
    def terminate(self):
        sys.exit()