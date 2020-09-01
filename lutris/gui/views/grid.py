"""Grid view for the main window"""
# pylint: disable=no-member
from gi.repository import Gtk

from lutris.gui.views import COL_ICON, COL_NAME
from lutris.gui.views.base import GameView
from lutris.gui.widgets.cellrenderers import GridViewCellRendererText


class GameGridView(Gtk.IconView, GameView):
    __gsignals__ = GameView.__gsignals__

    min_width = 110  # Minimum width for a cell

    def __init__(self, store):
        self.game_store = store
        self.model = self.game_store.store
        super().__init__(model=self.game_store.store)
        GameView.__init__(self)

        self.image_size = store.image_size
        self.service = None
        self.set_column_spacing(1)
        self.set_pixbuf_column(COL_ICON)
        self.set_item_padding(1)
        self.cell_width = (max(store.image_size[0], self.min_width))
        self.cell_renderer = GridViewCellRendererText(self.cell_width)
        self.pack_end(self.cell_renderer, False)
        self.add_attribute(self.cell_renderer, "markup", COL_NAME)

        self.connect_signals()
        self.connect("item-activated", self.on_item_activated)
        self.connect("selection-changed", self.on_selection_changed)
        store.connect("icons-changed", self.on_icons_changed)

    def select(self):
        self.select_path(self.current_path)

    def get_selected_item(self):
        """Return the currently selected game's id."""
        selection = self.get_selected_items()
        if not selection:
            return
        self.current_path = selection[0]
        return self.get_model().get_iter(self.current_path)

    def set_selected_game(self, game_id):
        """Select a game referenced by its ID in the view"""
        row = self.game_store.get_row_by_id(game_id, filtered=True)
        if row:
            self.select_path(row.path)

    def on_item_activated(self, _view, _path):
        """Handles double clicks"""
        selected_item = self.get_selected_item()
        if selected_item:
            self.selected_game = self.get_selected_game(selected_item)
        else:
            self.selected_game = None
        self.emit("game-activated", self.selected_game)

    def on_selection_changed(self, _view):
        """Handles selection changes"""
        selected_item = self.get_selected_item()
        if selected_item:
            self.selected_game = self.get_selected_game(selected_item)
        else:
            self.selected_game = None
        self.emit("game-selected", self.selected_game)

    def on_icons_changed(self, store):
        cell_width = max(store.image_size[0], self.min_width)
        self.set_item_width(cell_width)
        self.cell_renderer.props.width = cell_width
        self.queue_draw()
