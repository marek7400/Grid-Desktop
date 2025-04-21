import sys
import os
import math
from PyQt6.QtWidgets import (QApplication, QMainWindow, QSystemTrayIcon, QMenu,
                            QCheckBox, QSlider, QLabel, QVBoxLayout, QHBoxLayout, QWidget,
                            QColorDialog, QLineEdit, QPushButton, QGroupBox, QSpinBox,
                            QComboBox) # Removed QShortcut as global hooks are used
# *** FIX 1: Import QGuiApplication ***
from PyQt6.QtGui import (QIcon, QPainter, QPen, QColor, QKeySequence, QPixmap, QFont, QAction,
                         QGuiApplication) # QAction moved to QtGui, Added QGuiApplication
from PyQt6.QtCore import (Qt, QSize, QPoint, QSettings, pyqtSignal, QTimer,
                          QCoreApplication, QPointF) # Added QCoreApplication for attributes, *** Added QPointF ***

# --- Keyboard import ---
try:
    import keyboard
    HAS_KEYBOARD_LIB = True
except ImportError:
    HAS_KEYBOARD_LIB = False
    # Warning will be printed later based on language
except Exception as e:
    HAS_KEYBOARD_LIB = False
    # Warning will be printed later based on language

# --- QtWinExtras Check (Removed as it's not available in PyQt6) ---
HAS_QTWINEXTRAS = False # Always False for PyQt6

# --- Translation Data (Unchanged) ---
translations = {
    'PL': {
        "warning_keyboard_lib": "OSTRZEŻENIE: Biblioteka 'keyboard' nie jest zainstalowana. Globalne skróty nie działają.",
        "error_import_keyboard": "OSTRZEŻENIE: Błąd importu 'keyboard': {e}",
        "info_qtwin_removed": "INFO: Integracja z paskiem zadań Windows (przyciski miniatur) została usunięta w wersji PyQt6.",
        "info_linux_sudo": "INFO: W Linux globalne skróty mogą wymagać uprawnień 'sudo'.",
        "settings_window_title": "Ustawienia siatki",
        "show_grid_checkbox": "Pokaż siatkę (Ctrl+Alt+F10)",
        "grid_mode_label": "Tryb siatki:",
        "mode_sections": "Podział wg ilości sekcji",
        "mode_cell_size": "Podział wg rozmiaru komórki (px)",
        "sections_group_title": "Ustawienia podziału wg ILOŚCI",
        "rows_group_title": "Wiersze (linie poziome) [Ctrl+Alt+Lewo/Prawo]",
        "count_label": "Ilość:",
        "color_label": "Kolor:",
        "opacity_label": "Przezroczystość:",
        "thickness_label": "Grubość:",
        "cols_group_title": "Kolumny (linie pionowe) [Ctrl+Alt+Góra/Dół]",
        "preset_group_title": "Szybki wybór ilości",
        "columns_label": "Kolumny:",
        "rows_label": "Wiersze:",
        "apply_button": "Zastosuj",
        "cellsize_group_title": "Ustawienia podziału wg ROZMIARU KOMÓRKI",
        "cell_dims_group_title": "Rozmiar komórki (px)",
        "width_label": "Szerokość:",
        "height_label": "Wysokość:",
        "cell_h_style_group_title": "Styl linii poziomych (wierszy)",
        "cell_v_style_group_title": "Styl linii pionowych (kolumn)",
        # *** MODIFIED: Updated shortcut keys in description ***
        "offset_group_title": "Pozycja startowa siatki (Offset) [Ctrl+Alt+[ Ctrl+Alt+] Ctrl+Alt+; Ctrl+Alt+\\ Ctrl+Alt+F11]",
        "offset_x_label": "X:",
        "offset_y_label": "Y:",
        "reset_offset_button": "Resetuj Offset do 0,0 (Ctrl+Alt+F11)", # Added shortcut info
        "dots_group_title": "Kropki w środkach sekcji / komórek (Wspólne)",
        "show_dots_checkbox": "Pokaż kropki (Ctrl+Alt+F12)", # Added shortcut info
        "hide_dots": "Ukryj kropki", # Added for toggle message
        "dot_size_label": "Rozmiar (średnica):",
        "choose_color_sections_h": "Wybierz kolor (Sekcje - Poziome)",
        "choose_color_sections_v": "Wybierz kolor (Sekcje - Pionowe)",
        "choose_color_cells_h": "Wybierz kolor (Komórki - Poziome)",
        "choose_color_cells_v": "Wybierz kolor (Komórki - Pionowe)",
        "choose_color_dots": "Wybierz kolor (Kropki)",
        "info_preset_sections_only": "Info: 'Zastosuj' w szybkim wyborze działa tylko w trybie 'Podział wg ilości sekcji'.",
        "resetting_offset": "Resetowanie offsetu do 0,0",
        "saving_settings_exit": "Zapisywanie ustawień przy wyjściu...",
        "settings_saved": "Ustawienia zapisane.",
        "loading_settings": "Ładowanie ustawień...",
        "app_quit_code": "Aplikacja zakończona z kodem: {exit_code}",
        "tray_show_grid": "Pokaż siatkę (Ctrl+Alt+F10)",
        "tray_settings": "Ustawienia",
        "tray_exit": "Wyjście (Ctrl+Shift+Alt+End)",
        "shortcuts_registered": "Globalne skróty zarejestrowane.",
        "shortcuts_fail": "OSTRZEŻENIE: Nie udało się zarejestrować globalnych skrótów: {e}",
        "shortcuts_warn_no_lib": "OSTRZEŻENIE: Biblioteka 'keyboard' niedostępna, globalne skróty nie działają.",
        "clearing_shortcuts": "Czyszczenie globalnych skrótów klawiszowych...",
        "shortcuts_cleared": "Skróty klawiszowe usunięte.",
        "shortcuts_clear_fail": "Błąd podczas usuwania skrótów klawiszowych: {e}",
        "shortcut_inc_cols": "Skrót: Zwiększ Kolumny (Sekcje) do {new_val}",
        "shortcut_dec_cols": "Skrót: Zmniejsz Kolumny (Sekcje) do {new_val}",
        "shortcut_inc_rows": "Skrót: Zwiększ Wiersze (Sekcje) do {new_val}",
        "shortcut_dec_rows": "Skrót: Zmniejsz Wiersze (Sekcje) do {new_val}",
        "shortcut_inc_x": "Skrót: Zwiększ Offset X do {new_val}",
        "shortcut_dec_x": "Skrót: Zmniejsz Offset X do {new_val}",
        "shortcut_inc_y": "Skrót: Zwiększ Offset Y do {new_val}",
        "shortcut_dec_y": "Skrót: Zmniejsz Offset Y do {new_val}",
        "shortcut_ignored_mode": "Skrót zignorowany: Zmiana działa tylko w trybie 'Sekcje'.",
        # *** ADDED: New shortcut descriptions ***
        "shortcut_reset_offset": "Skrót: Resetuj Offset do 0,0",
        "shortcut_toggle_dots": "Skrót: Przełącz Kropki (Nowy stan: {state})",
        "language_label": "Język:",
        "language_pl": "Polski (PL)",
        "language_en": "English (ENG)",
        "switch_mode_log": "Zmieniono tryb siatki na: {mode_name}"
    },
    'ENG': {
        "warning_keyboard_lib": "WARNING: Library 'keyboard' not installed. Global shortcuts will not work.",
        "error_import_keyboard": "WARNING: Error importing 'keyboard': {e}",
        "info_qtwin_removed": "INFO: Windows taskbar integration (thumbnail buttons) has been removed in the PyQt6 version.",
        "info_linux_sudo": "INFO: On Linux, global shortcuts might require 'sudo' privileges.",
        "settings_window_title": "Grid Settings",
        "show_grid_checkbox": "Show Grid (Ctrl+Alt+F10)",
        "grid_mode_label": "Grid Mode:",
        "mode_sections": "Division by Number of Sections",
        "mode_cell_size": "Division by Cell Size (px)",
        "sections_group_title": "Settings for Division by COUNT",
        "rows_group_title": "Rows (Horizontal Lines) [Ctrl+Alt+Left/Right]",
        "count_label": "Count:",
        "color_label": "Color:",
        "opacity_label": "Opacity:",
        "thickness_label": "Thickness:",
        "cols_group_title": "Columns (Vertical Lines) [Ctrl+Alt+Up/Down]",
        "preset_group_title": "Quick Count Selection",
        "columns_label": "Columns:",
        "rows_label": "Rows:",
        "apply_button": "Apply",
        "cellsize_group_title": "Settings for Division by CELL SIZE",
        "cell_dims_group_title": "Cell Size (px)",
        "width_label": "Width:",
        "height_label": "Height:",
        "cell_h_style_group_title": "Horizontal Line Style (Rows)",
        "cell_v_style_group_title": "Vertical Line Style (Columns)",
        # *** MODIFIED: Updated shortcut keys in description ***
        "offset_group_title": "Grid Start Position (Offset) [Ctrl+Alt+[ Ctrl+Alt+] Ctrl+Alt+; Ctrl+Alt+\\ Ctrl+Alt+F11]",
        "offset_x_label": "X:",
        "offset_y_label": "Y:",
        "reset_offset_button": "Reset Offset to 0,0 (Ctrl+Alt+F11)", # Added shortcut info
        "dots_group_title": "Dots in Section/Cell Centers (Common)",
        "show_dots_checkbox": "Show Dots (Ctrl+Alt+F12)", # Added shortcut info
        "hide_dots": "Hide Dots", # Added for toggle message
        "dot_size_label": "Size (Diameter):",
        "choose_color_sections_h": "Choose Color (Sections - Horizontal)",
        "choose_color_sections_v": "Choose Color (Sections - Vertical)",
        "choose_color_cells_h": "Choose Color (Cells - Horizontal)",
        "choose_color_cells_v": "Choose Color (Cells - Vertical)",
        "choose_color_dots": "Choose Color (Dots)",
        "info_preset_sections_only": "Info: 'Apply' in quick selection only works in 'Division by Number of Sections' mode.",
        "resetting_offset": "Resetting offset to 0,0",
        "saving_settings_exit": "Saving settings on exit...",
        "settings_saved": "Settings saved.",
        "loading_settings": "Loading settings...",
        "app_quit_code": "Application finished with code: {exit_code}",
        "tray_show_grid": "Show Grid (Ctrl+Alt+F10)",
        "tray_settings": "Settings",
        "tray_exit": "Exit (Ctrl+Shift+Alt+End)",
        "shortcuts_registered": "Global hotkeys registered.",
        "shortcuts_fail": "WARNING: Failed to register global hotkeys: {e}",
        "shortcuts_warn_no_lib": "WARNING: 'keyboard' library not available, global hotkeys disabled.",
        "clearing_shortcuts": "Clearing global hotkeys...",
        "shortcuts_cleared": "Hotkeys removed.",
        "shortcuts_clear_fail": "Error removing hotkeys: {e}",
        "shortcut_inc_cols": "Shortcut: Increase Columns (Sections) to {new_val}",
        "shortcut_dec_cols": "Shortcut: Decrease Columns (Sections) to {new_val}",
        "shortcut_inc_rows": "Shortcut: Increase Rows (Sections) to {new_val}",
        "shortcut_dec_rows": "Shortcut: Decrease Rows (Sections) to {new_val}",
        "shortcut_inc_x": "Shortcut: Increase X Offset to {new_val}",
        "shortcut_dec_x": "Shortcut: Decrease X Offset to {new_val}",
        "shortcut_inc_y": "Shortcut: Increase Y Offset to {new_val}",
        "shortcut_dec_y": "Shortcut: Decrease Y Offset to {new_val}",
        "shortcut_ignored_mode": "Shortcut ignored: Change only works in 'Sections' mode.",
        # *** ADDED: New shortcut descriptions ***
        "shortcut_reset_offset": "Shortcut: Reset Offset to 0,0",
        "shortcut_toggle_dots": "Shortcut: Toggle Dots (New state: {state})",
        "language_label": "Language:",
        "language_pl": "Polski (PL)",
        "language_en": "English (ENG)",
        "switch_mode_log": "Switched grid mode to: {mode_name}"
    }
}
current_lang = 'PL' # Default language, will be updated from settings

def tr(key, **kwargs):
    """Translates a key using the current language."""
    lang_dict = translations.get(current_lang, translations['ENG']) # Fallback to English
    base_string = lang_dict.get(key, key) # Return key if not found
    try:
        return base_string.format(**kwargs)
    except KeyError as e:
        print(f"Warning: Missing format key '{e}' for translation key '{key}' in lang '{current_lang}'")
        return base_string # Return the base string even if formatting fails

# --- GridOverlay Class ---
class GridOverlay(QWidget):
    MODE_SECTIONS = 0
    MODE_CELL_SIZE = 1

    def __init__(self, parent=None):
        super(GridOverlay, self).__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)

        # Default values
        self.grid_mode = GridOverlay.MODE_SECTIONS
        self.visible = True
        self.offset_x = 0
        self.offset_y = 0
        self.horizontal_sections = 11
        self.vertical_sections = 11
        self.horizontal_color = QColor(0, 120, 215, 128)
        self.vertical_color = QColor(0, 120, 215, 128)
        self.horizontal_width = 1
        self.vertical_width = 1
        self.cell_width = 50
        self.cell_height = 50
        self.cell_horizontal_color = QColor(215, 120, 0, 128)
        self.cell_vertical_color = QColor(215, 120, 0, 128)
        self.cell_horizontal_width = 1
        self.cell_vertical_width = 1
        self.show_dots = False
        self.dot_size = 4
        self.dot_color = QColor(0, 255, 0, 192)

    def paintEvent(self, event):
        if not self.visible:
            return
        painter = QPainter(self)
        h_width = self.horizontal_width if self.grid_mode == self.MODE_SECTIONS else self.cell_horizontal_width
        v_width = self.vertical_width if self.grid_mode == self.MODE_SECTIONS else self.cell_vertical_width
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, h_width > 1 or v_width > 1)
        painter.save()
        painter.translate(float(self.offset_x), float(self.offset_y))
        draw_width = self.width()
        draw_height = self.height()
        if self.grid_mode == GridOverlay.MODE_SECTIONS:
            self._paint_by_sections(painter, draw_width, draw_height)
        elif self.grid_mode == GridOverlay.MODE_CELL_SIZE:
            self._paint_by_cell_size(painter, draw_width, draw_height)
        if self.show_dots:
            self._paint_dots(painter, draw_width, draw_height)
        painter.restore()

    def _paint_by_sections(self, painter, w, h):
        if self.horizontal_sections <= 0 or self.vertical_sections <= 0: return
        horizontal_spacing = float(w) / self.vertical_sections if self.vertical_sections else 0
        vertical_spacing = float(h) / self.horizontal_sections if self.horizontal_sections else 0
        num_horizontal_lines = max(0, self.horizontal_sections - 1)
        num_vertical_lines = max(0, self.vertical_sections - 1)
        if num_horizontal_lines > 0:
            pen = QPen(self.horizontal_color); pen.setWidth(self.horizontal_width); painter.setPen(pen)
            for i in range(1, num_horizontal_lines + 1): y = int(i * vertical_spacing); painter.drawLine(0, y, w, y)
        if num_vertical_lines > 0:
            pen = QPen(self.vertical_color); pen.setWidth(self.vertical_width); painter.setPen(pen)
            for i in range(1, num_vertical_lines + 1): x = int(i * horizontal_spacing); painter.drawLine(x, 0, x, h)

    # --- MODIFIED: Corrected _paint_by_cell_size ---
    def _paint_by_cell_size(self, painter, w, h):
        if self.cell_width <= 0 or self.cell_height <= 0: return
        start_y_limit = -self.offset_y
        start_x_limit = -self.offset_x

        # Draw horizontal lines
        if self.cell_height > 0:
            pen = QPen(self.cell_horizontal_color)
            pen.setWidth(self.cell_horizontal_width)
            painter.setPen(pen)
            # Calculate the y-coordinate of the first line potentially visible or just above the view
            first_y_index = math.floor(start_y_limit / self.cell_height)
            y = float(first_y_index * self.cell_height)
            # Loop until the line is below the visible area considering offset
            while y < h - self.offset_y:
                iy = int(y) # Convert to integer for drawing
                painter.drawLine(0, iy, w, iy)
                y += self.cell_height
                # Removed the problematic 'if y == ...: break' which caused SyntaxError and was redundant

        # Draw vertical lines
        if self.cell_width > 0:
            pen = QPen(self.cell_vertical_color)
            pen.setWidth(self.cell_vertical_width)
            painter.setPen(pen)
            # Calculate the x-coordinate of the first line potentially visible or just left of the view
            first_x_index = math.floor(start_x_limit / self.cell_width)
            x = float(first_x_index * self.cell_width)
            # Loop until the line is beyond the right edge considering offset
            while x < w - self.offset_x:
                ix = int(x) # Convert to integer for drawing
                painter.drawLine(ix, 0, ix, h)
                x += self.cell_width
                # Removed the problematic 'if x == ...: break' which was redundant
    # --- END MODIFICATION ---

    def _paint_dots(self, painter, w, h):
        painter.setPen(Qt.PenStyle.NoPen); painter.setBrush(self.dot_color); half_dot = self.dot_size / 2.0
        if self.grid_mode == GridOverlay.MODE_SECTIONS:
            if self.horizontal_sections <= 0 or self.vertical_sections <= 0: return
            horizontal_spacing = float(w) / self.vertical_sections if self.vertical_sections else 0
            vertical_spacing = float(h) / self.horizontal_sections if self.horizontal_sections else 0
            for row_idx in range(self.horizontal_sections):
                for col_idx in range(self.vertical_sections):
                    x = (col_idx + 0.5) * horizontal_spacing; y = (row_idx + 0.5) * vertical_spacing
                    painter.drawEllipse(QPointF(x, y), half_dot, half_dot)
        elif self.grid_mode == GridOverlay.MODE_CELL_SIZE:
            if self.cell_width <= 0 or self.cell_height <= 0: return
            start_y_limit = -self.offset_y; start_x_limit = -self.offset_x
            first_y_index = math.floor(start_y_limit / self.cell_height) if self.cell_height else 0
            first_x_index = math.floor(start_x_limit / self.cell_width) if self.cell_width else 0
            first_center_y = (first_y_index + 0.5) * self.cell_height; first_center_x = (first_x_index + 0.5) * self.cell_width
            y = first_center_y
            while y < h - self.offset_y:
                x = first_center_x
                while x < w - self.offset_x:
                    painter.drawEllipse(QPointF(x, y), half_dot, half_dot)
                    if self.cell_width <= 0: break # Prevent infinite loop if somehow cell_width becomes 0 mid-loop
                    x += self.cell_width
                if self.cell_height <= 0: break # Prevent infinite loop if somehow cell_height becomes 0 mid-loop
                y += self.cell_height
                # Check needed if height/width is very small or zero to prevent infinite loop if y/x does not change
                if y == first_center_y and self.cell_height > 0: # Added check > 0 to avoid comparing floats if cell_height is 0
                    break
            # A similar check for x might be needed if cell_width could be problematic


# --- SettingsWindow Class ---
class SettingsWindow(QMainWindow):
    languageChanged = pyqtSignal()

    def __init__(self, grid_overlay):
        super(SettingsWindow, self).__init__()
        self.grid_overlay = grid_overlay
        self.settings = QSettings("GridTool", "ConfigurableGrid")
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self._loading_settings = False
        self.current_language = 'PL'
        self.initUI()
        self.loadSettings()

    def initUI(self):
        self.setMinimumWidth(470)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)

        # Language
        lang_layout = QHBoxLayout(); self.lang_label = QLabel(); lang_layout.addWidget(self.lang_label)
        self.language_combobox = QComboBox(); self.language_combobox.addItem(tr("language_pl"), "PL"); self.language_combobox.addItem(tr("language_en"), "ENG")
        self.language_combobox.currentIndexChanged.connect(self.changeLanguage); lang_layout.addWidget(self.language_combobox); lang_layout.addStretch(); main_layout.addLayout(lang_layout)

        # Visibility
        self.grid_checkbox = QCheckBox(); self.grid_checkbox.setChecked(self.grid_overlay.visible)
        self.grid_checkbox.stateChanged.connect(self.toggleGrid); main_layout.addWidget(self.grid_checkbox)

        # Mode
        mode_layout = QHBoxLayout(); self.mode_label = QLabel(); mode_layout.addWidget(self.mode_label)
        self.mode_combobox = QComboBox(); self.mode_combobox.currentIndexChanged.connect(self._update_mode_ui)
        mode_layout.addWidget(self.mode_combobox); mode_layout.addStretch(); main_layout.addLayout(mode_layout)

        # Sections Group
        self.sections_group = QGroupBox(); sections_layout = QVBoxLayout()
        self.horizontal_group = QGroupBox(); horizontal_layout = QVBoxLayout()
        h_count_layout = QHBoxLayout(); self.h_count_label = QLabel(); h_count_layout.addWidget(self.h_count_label); self.h_slider = QSlider(Qt.Orientation.Horizontal); self.h_slider.setRange(1, 100)
        self.h_slider.valueChanged.connect(self.updateHorizontalSections); h_count_layout.addWidget(self.h_slider); self.h_value = QSpinBox(); self.h_value.setRange(1, 10000)
        self.h_value.valueChanged.connect(self.updateHorizontalSectionsValue); h_count_layout.addWidget(self.h_value); horizontal_layout.addLayout(h_count_layout)
        h_color_layout = QHBoxLayout(); self.h_color_label = QLabel(); h_color_layout.addWidget(self.h_color_label); self.h_color_button = QPushButton(); self.h_color_button.setMinimumSize(QSize(40, 20))
        self.h_color_button.clicked.connect(self.chooseHorizontalColor); h_color_layout.addWidget(self.h_color_button); self.h_opacity_label = QLabel(); h_color_layout.addWidget(self.h_opacity_label)
        self.h_opacity_slider = QSlider(Qt.Orientation.Horizontal); self.h_opacity_slider.setRange(0, 255); self.h_opacity_slider.valueChanged.connect(self.updateHorizontalOpacity); h_color_layout.addWidget(self.h_opacity_slider); horizontal_layout.addLayout(h_color_layout)
        h_width_layout = QHBoxLayout(); self.h_width_label = QLabel(); h_width_layout.addWidget(self.h_width_label); self.h_width_slider = QSlider(Qt.Orientation.Horizontal); self.h_width_slider.setRange(1, 10)
        self.h_width_slider.valueChanged.connect(self.updateHorizontalWidth); h_width_layout.addWidget(self.h_width_slider); self.h_width_value = QSpinBox(); self.h_width_value.setRange(1, 20)
        self.h_width_value.valueChanged.connect(self.updateHorizontalWidthValue); h_width_layout.addWidget(self.h_width_value); horizontal_layout.addLayout(h_width_layout)
        self.horizontal_group.setLayout(horizontal_layout); sections_layout.addWidget(self.horizontal_group)

        self.vertical_group = QGroupBox(); vertical_layout = QVBoxLayout()
        v_count_layout = QHBoxLayout(); self.v_count_label = QLabel(); v_count_layout.addWidget(self.v_count_label); self.v_slider = QSlider(Qt.Orientation.Horizontal); self.v_slider.setRange(1, 100)
        self.v_slider.valueChanged.connect(self.updateVerticalSections); v_count_layout.addWidget(self.v_slider); self.v_value = QSpinBox(); self.v_value.setRange(1, 10000)
        self.v_value.valueChanged.connect(self.updateVerticalSectionsValue); v_count_layout.addWidget(self.v_value); vertical_layout.addLayout(v_count_layout)
        v_color_layout = QHBoxLayout(); self.v_color_label = QLabel(); v_color_layout.addWidget(self.v_color_label); self.v_color_button = QPushButton(); self.v_color_button.setMinimumSize(QSize(40, 20))
        self.v_color_button.clicked.connect(self.chooseVerticalColor); v_color_layout.addWidget(self.v_color_button); self.v_opacity_label = QLabel(); v_color_layout.addWidget(self.v_opacity_label)
        self.v_opacity_slider = QSlider(Qt.Orientation.Horizontal); self.v_opacity_slider.setRange(0, 255); self.v_opacity_slider.valueChanged.connect(self.updateVerticalOpacity); v_color_layout.addWidget(self.v_opacity_slider); vertical_layout.addLayout(v_color_layout)
        v_width_layout = QHBoxLayout(); self.v_width_label = QLabel(); v_width_layout.addWidget(self.v_width_label); self.v_width_slider = QSlider(Qt.Orientation.Horizontal); self.v_width_slider.setRange(1, 10)
        self.v_width_slider.valueChanged.connect(self.updateVerticalWidth); v_width_layout.addWidget(self.v_width_slider); self.v_width_value = QSpinBox(); self.v_width_value.setRange(1, 20)
        self.v_width_value.valueChanged.connect(self.updateVerticalWidthValue); v_width_layout.addWidget(self.v_width_value); vertical_layout.addLayout(v_width_layout)
        self.vertical_group.setLayout(vertical_layout); sections_layout.addWidget(self.vertical_group)

        self.grid_preset_group = QGroupBox(); grid_preset_layout = QHBoxLayout(); self.columns_preset_label = QLabel(); grid_preset_layout.addWidget(self.columns_preset_label)
        self.columns_spinbox = QSpinBox(); self.columns_spinbox.setRange(1, 10000); grid_preset_layout.addWidget(self.columns_spinbox); self.rows_preset_label = QLabel(); grid_preset_layout.addWidget(self.rows_preset_label)
        self.rows_spinbox = QSpinBox(); self.rows_spinbox.setRange(1, 10000); grid_preset_layout.addWidget(self.rows_spinbox)
        self.apply_button = QPushButton(); self.apply_button.clicked.connect(self.applyGridPreset); grid_preset_layout.addWidget(self.apply_button)
        self.grid_preset_group.setLayout(grid_preset_layout); sections_layout.addWidget(self.grid_preset_group)
        self.sections_group.setLayout(sections_layout); main_layout.addWidget(self.sections_group)

        # Cell Size Group
        self.cellsize_group = QGroupBox(); cellsize_layout = QVBoxLayout()
        self.cell_dims_group = QGroupBox(); cell_dims_layout = QHBoxLayout()
        self.cell_width_label = QLabel(); cell_dims_layout.addWidget(self.cell_width_label); self.cell_width_spinbox = QSpinBox(); self.cell_width_spinbox.setRange(1, 5000)
        self.cell_width_spinbox.valueChanged.connect(self._update_cell_width); cell_dims_layout.addWidget(self.cell_width_spinbox); cell_dims_layout.addSpacing(20)
        self.cell_height_label = QLabel(); cell_dims_layout.addWidget(self.cell_height_label); self.cell_height_spinbox = QSpinBox(); self.cell_height_spinbox.setRange(1, 5000)
        self.cell_height_spinbox.valueChanged.connect(self._update_cell_height); cell_dims_layout.addWidget(self.cell_height_spinbox); cell_dims_layout.addStretch()
        self.cell_dims_group.setLayout(cell_dims_layout); cellsize_layout.addWidget(self.cell_dims_group)

        self.cell_h_style_group = QGroupBox(); cell_h_style_layout = QVBoxLayout()
        cell_h_color_layout = QHBoxLayout(); self.cell_h_color_label = QLabel(); cell_h_color_layout.addWidget(self.cell_h_color_label); self.cell_h_color_button = QPushButton(); self.cell_h_color_button.setMinimumSize(QSize(40, 20))
        self.cell_h_color_button.clicked.connect(self.chooseCellHorizontalColor); cell_h_color_layout.addWidget(self.cell_h_color_button); self.cell_h_opacity_label = QLabel(); cell_h_color_layout.addWidget(self.cell_h_opacity_label)
        self.cell_h_opacity_slider = QSlider(Qt.Orientation.Horizontal); self.cell_h_opacity_slider.setRange(0, 255); self.cell_h_opacity_slider.valueChanged.connect(self.updateCellHorizontalOpacity); cell_h_color_layout.addWidget(self.cell_h_opacity_slider); cell_h_style_layout.addLayout(cell_h_color_layout)
        cell_h_width_layout = QHBoxLayout(); self.cell_h_width_label = QLabel(); cell_h_width_layout.addWidget(self.cell_h_width_label); self.cell_h_width_slider = QSlider(Qt.Orientation.Horizontal); self.cell_h_width_slider.setRange(1, 10)
        self.cell_h_width_slider.valueChanged.connect(self.updateCellHorizontalWidth); cell_h_width_layout.addWidget(self.cell_h_width_slider); self.cell_h_width_value = QSpinBox(); self.cell_h_width_value.setRange(1, 20)
        self.cell_h_width_value.valueChanged.connect(self.updateCellHorizontalWidthValue); cell_h_width_layout.addWidget(self.cell_h_width_value); cell_h_style_layout.addLayout(cell_h_width_layout)
        self.cell_h_style_group.setLayout(cell_h_style_layout); cellsize_layout.addWidget(self.cell_h_style_group)

        self.cell_v_style_group = QGroupBox(); cell_v_style_layout = QVBoxLayout()
        cell_v_color_layout = QHBoxLayout(); self.cell_v_color_label = QLabel(); cell_v_color_layout.addWidget(self.cell_v_color_label); self.cell_v_color_button = QPushButton(); self.cell_v_color_button.setMinimumSize(QSize(40, 20))
        self.cell_v_color_button.clicked.connect(self.chooseCellVerticalColor); cell_v_color_layout.addWidget(self.cell_v_color_button); self.cell_v_opacity_label = QLabel(); cell_v_color_layout.addWidget(self.cell_v_opacity_label)
        self.cell_v_opacity_slider = QSlider(Qt.Orientation.Horizontal); self.cell_v_opacity_slider.setRange(0, 255); self.cell_v_opacity_slider.valueChanged.connect(self.updateCellVerticalOpacity); cell_v_color_layout.addWidget(self.cell_v_opacity_slider); cell_v_style_layout.addLayout(cell_v_color_layout)
        cell_v_width_layout = QHBoxLayout(); self.cell_v_width_label = QLabel(); cell_v_width_layout.addWidget(self.cell_v_width_label); self.cell_v_width_slider = QSlider(Qt.Orientation.Horizontal); self.cell_v_width_slider.setRange(1, 10)
        self.cell_v_width_slider.valueChanged.connect(self.updateCellVerticalWidth); cell_v_width_layout.addWidget(self.cell_v_width_slider); self.cell_v_width_value = QSpinBox(); self.cell_v_width_value.setRange(1, 20)
        self.cell_v_width_value.valueChanged.connect(self.updateCellVerticalWidthValue); cell_v_width_layout.addWidget(self.cell_v_width_value); cell_v_style_layout.addLayout(cell_v_width_layout)
        self.cell_v_style_group.setLayout(cell_v_style_layout); cellsize_layout.addWidget(self.cell_v_style_group)
        self.cellsize_group.setLayout(cellsize_layout); main_layout.addWidget(self.cellsize_group)
        self.cellsize_group.setVisible(False)

        # Common Settings (Offset, Dots)
        self.offset_group = QGroupBox(); offset_layout = QVBoxLayout()
        x_offset_layout = QHBoxLayout(); self.x_offset_label = QLabel(); x_offset_layout.addWidget(self.x_offset_label); self.x_offset_slider = QSlider(Qt.Orientation.Horizontal); self.x_offset_slider.setRange(-500, 500)
        self.x_offset_slider.valueChanged.connect(self.updateOffsetX); x_offset_layout.addWidget(self.x_offset_slider); self.x_offset_value = QSpinBox(); self.x_offset_value.setRange(-10000, 10000)
        self.x_offset_value.valueChanged.connect(self.updateOffsetXValue); x_offset_layout.addWidget(self.x_offset_value); offset_layout.addLayout(x_offset_layout)
        y_offset_layout = QHBoxLayout(); self.y_offset_label = QLabel(); y_offset_layout.addWidget(self.y_offset_label); self.y_offset_slider = QSlider(Qt.Orientation.Horizontal); self.y_offset_slider.setRange(-500, 500)
        self.y_offset_slider.valueChanged.connect(self.updateOffsetY); y_offset_layout.addWidget(self.y_offset_slider); self.y_offset_value = QSpinBox(); self.y_offset_value.setRange(-10000, 10000)
        self.y_offset_value.valueChanged.connect(self.updateOffsetYValue); y_offset_layout.addWidget(self.y_offset_value); offset_layout.addLayout(y_offset_layout)
        reset_button_layout = QHBoxLayout(); reset_button_layout.addStretch()
        self.reset_offset_button = QPushButton(); self.reset_offset_button.clicked.connect(self.resetOffsets); reset_button_layout.addWidget(self.reset_offset_button); offset_layout.addLayout(reset_button_layout)
        self.offset_group.setLayout(offset_layout); main_layout.addWidget(self.offset_group)

        self.dots_group = QGroupBox(); dots_layout = QVBoxLayout()
        self.dots_checkbox = QCheckBox(); self.dots_checkbox.stateChanged.connect(self.toggleDots); dots_layout.addWidget(self.dots_checkbox)
        dot_size_layout = QHBoxLayout(); self.dot_size_label = QLabel(); dot_size_layout.addWidget(self.dot_size_label); self.dot_size_slider = QSlider(Qt.Orientation.Horizontal); self.dot_size_slider.setRange(1, 20)
        self.dot_size_slider.valueChanged.connect(self.updateDotSize); dot_size_layout.addWidget(self.dot_size_slider); self.dot_size_value = QSpinBox(); self.dot_size_value.setRange(1, 50)
        self.dot_size_value.valueChanged.connect(self.updateDotSizeValue); dot_size_layout.addWidget(self.dot_size_value); dots_layout.addLayout(dot_size_layout)
        dot_color_layout = QHBoxLayout(); self.dot_color_label = QLabel(); dot_color_layout.addWidget(self.dot_color_label); self.dot_color_button = QPushButton(); self.dot_color_button.setMinimumSize(QSize(40, 20))
        self.dot_color_button.clicked.connect(self.chooseDotColor); dot_color_layout.addWidget(self.dot_color_button); self.dot_opacity_label = QLabel(); dot_color_layout.addWidget(self.dot_opacity_label)
        self.dot_opacity_slider = QSlider(Qt.Orientation.Horizontal); self.dot_opacity_slider.setRange(0, 255); self.dot_opacity_slider.valueChanged.connect(self.updateDotOpacity); dot_color_layout.addWidget(self.dot_opacity_slider); dots_layout.addLayout(dot_color_layout)
        self.dots_group.setLayout(dots_layout); main_layout.addWidget(self.dots_group)

        main_layout.addStretch()
        self.retranslateUi()

    def retranslateUi(self):
        global current_lang; current_lang = self.current_language
        self.setWindowTitle(tr("settings_window_title"))
        self.lang_label.setText(tr("language_label"))
        self.language_combobox.blockSignals(True)
        self.language_combobox.setItemText(0, tr("language_pl")); self.language_combobox.setItemText(1, tr("language_en"))
        lang_index = self.language_combobox.findData(self.current_language); self.language_combobox.setCurrentIndex(lang_index if lang_index != -1 else 0); self.language_combobox.blockSignals(False)
        self.grid_checkbox.setText(tr("show_grid_checkbox")); self.mode_label.setText(tr("grid_mode_label"))
        selected_mode_data = self.mode_combobox.currentData()
        self.mode_combobox.blockSignals(True); self.mode_combobox.clear(); self.mode_combobox.addItem(tr("mode_sections"), GridOverlay.MODE_SECTIONS); self.mode_combobox.addItem(tr("mode_cell_size"), GridOverlay.MODE_CELL_SIZE)
        mode_index = self.mode_combobox.findData(selected_mode_data); self.mode_combobox.setCurrentIndex(mode_index if mode_index != -1 else 0); self.mode_combobox.blockSignals(False)
        self.sections_group.setTitle(tr("sections_group_title")); self.horizontal_group.setTitle(tr("rows_group_title"))
        self.h_count_label.setText(tr("count_label")); self.h_color_label.setText(tr("color_label")); self.h_opacity_label.setText(tr("opacity_label")); self.h_width_label.setText(tr("thickness_label"))
        self.vertical_group.setTitle(tr("cols_group_title")); self.v_count_label.setText(tr("count_label")); self.v_color_label.setText(tr("color_label")); self.v_opacity_label.setText(tr("opacity_label")); self.v_width_label.setText(tr("thickness_label"))
        self.grid_preset_group.setTitle(tr("preset_group_title")); self.columns_preset_label.setText(tr("columns_label")); self.rows_preset_label.setText(tr("rows_label")); self.apply_button.setText(tr("apply_button"))
        self.cellsize_group.setTitle(tr("cellsize_group_title")); self.cell_dims_group.setTitle(tr("cell_dims_group_title"))
        self.cell_width_label.setText(tr("width_label")); self.cell_height_label.setText(tr("height_label"))
        self.cell_h_style_group.setTitle(tr("cell_h_style_group_title")); self.cell_h_color_label.setText(tr("color_label")); self.cell_h_opacity_label.setText(tr("opacity_label")); self.cell_h_width_label.setText(tr("thickness_label"))
        self.cell_v_style_group.setTitle(tr("cell_v_style_group_title")); self.cell_v_color_label.setText(tr("color_label")); self.cell_v_opacity_label.setText(tr("opacity_label")); self.cell_v_width_label.setText(tr("thickness_label"))
        self.offset_group.setTitle(tr("offset_group_title")); self.x_offset_label.setText(tr("offset_x_label")); self.y_offset_label.setText(tr("offset_y_label")); self.reset_offset_button.setText(tr("reset_offset_button"))
        self.dots_group.setTitle(tr("dots_group_title")); self.dots_checkbox.setText(tr("show_dots_checkbox")); self.dot_size_label.setText(tr("dot_size_label")); self.dot_color_label.setText(tr("color_label")); self.dot_opacity_label.setText(tr("opacity_label"))
        self.h_color_dialog_title = tr("choose_color_sections_h"); self.v_color_dialog_title = tr("choose_color_sections_v"); self.cell_h_color_dialog_title = tr("choose_color_cells_h"); self.cell_v_color_dialog_title = tr("choose_color_cells_v"); self.dot_color_dialog_title = tr("choose_color_dots")
        self.languageChanged.emit()

    def changeLanguage(self, index):
        if self._loading_settings: return
        selected_lang = self.language_combobox.itemData(index)
        if selected_lang and selected_lang != self.current_language:
            self.current_language = selected_lang; self.settings.setValue("language", self.current_language); self.retranslateUi()

    def _update_mode_ui(self, index):
        selected_mode = self.mode_combobox.itemData(index)
        if selected_mode is None: return
        self.sections_group.setVisible(selected_mode == GridOverlay.MODE_SECTIONS); self.cellsize_group.setVisible(selected_mode == GridOverlay.MODE_CELL_SIZE)
        if not self._loading_settings:
            self.grid_overlay.grid_mode = selected_mode; mode_name = tr("mode_sections") if selected_mode == GridOverlay.MODE_SECTIONS else tr("mode_cell_size")
            print(tr("switch_mode_log", mode_name=mode_name)); self.grid_overlay.update()

    def toggleGrid(self, state_int):
        checked = (state_int == Qt.CheckState.Checked.value)
        self.grid_overlay.visible = checked; self.grid_overlay.setVisible(checked)
        app = QApplication.instance();
        if hasattr(app, 'tray_show_action'): app.tray_show_action.setChecked(checked)
        if not self._loading_settings: self.settings.setValue("visible", checked)

    def updateHorizontalSections(self, value):
        if not self._loading_settings: self.grid_overlay.horizontal_sections = value; self.grid_overlay.update()
        self.h_value.setValue(value); self.rows_spinbox.setValue(value)
    def updateHorizontalSectionsValue(self, value):
        if not self._loading_settings: self.grid_overlay.horizontal_sections = value; self.grid_overlay.update()
        self.rows_spinbox.setValue(value); self.h_slider.setValue(value) if 1 <= value <= self.h_slider.maximum() else None
    def updateVerticalSections(self, value):
        if not self._loading_settings: self.grid_overlay.vertical_sections = value; self.grid_overlay.update()
        self.v_value.setValue(value); self.columns_spinbox.setValue(value)
    def updateVerticalSectionsValue(self, value):
        if not self._loading_settings: self.grid_overlay.vertical_sections = value; self.grid_overlay.update()
        self.columns_spinbox.setValue(value); self.v_slider.setValue(value) if 1 <= value <= self.v_slider.maximum() else None
    def chooseHorizontalColor(self):
        color = QColorDialog.getColor(self.grid_overlay.horizontal_color, self, self.h_color_dialog_title, options=QColorDialog.ColorDialogOption.ShowAlphaChannel)
        if color.isValid(): self.grid_overlay.horizontal_color = color; self.updateHorizontalColorButton(); self.h_opacity_slider.setValue(color.alpha()); self.grid_overlay.update() # Update slider and button on valid color
    def updateHorizontalOpacity(self, value): color = self.grid_overlay.horizontal_color; color.setAlpha(value); self.grid_overlay.horizontal_color = color; self.updateHorizontalColorButton(); self.grid_overlay.update()
    def updateHorizontalWidth(self, value): self.grid_overlay.horizontal_width = value; self.h_width_value.setValue(value); self.grid_overlay.update()
    def updateHorizontalWidthValue(self, value): self.grid_overlay.horizontal_width = value; self.h_width_slider.setValue(value) if 1 <= value <= self.h_width_slider.maximum() else None; self.grid_overlay.update()
    def chooseVerticalColor(self):
        color = QColorDialog.getColor(self.grid_overlay.vertical_color, self, self.v_color_dialog_title, options=QColorDialog.ColorDialogOption.ShowAlphaChannel)
        if color.isValid(): self.grid_overlay.vertical_color = color; self.updateVerticalColorButton(); self.v_opacity_slider.setValue(color.alpha()); self.grid_overlay.update() # Update slider and button on valid color
    def updateVerticalOpacity(self, value): color = self.grid_overlay.vertical_color; color.setAlpha(value); self.grid_overlay.vertical_color = color; self.updateVerticalColorButton(); self.grid_overlay.update()
    def updateVerticalWidth(self, value): self.grid_overlay.vertical_width = value; self.v_width_value.setValue(value); self.grid_overlay.update()
    def updateVerticalWidthValue(self, value): self.grid_overlay.vertical_width = value; self.v_width_slider.setValue(value) if 1 <= value <= self.v_width_slider.maximum() else None; self.grid_overlay.update()
    def applyGridPreset(self):
        if self.grid_overlay.grid_mode == GridOverlay.MODE_SECTIONS: self.updateVerticalSectionsValue(self.columns_spinbox.value()); self.updateHorizontalSectionsValue(self.rows_spinbox.value())
        else: print(tr("info_preset_sections_only"))

    def _update_cell_width(self, value):
        if not self._loading_settings: self.grid_overlay.cell_width = value; self.grid_overlay.update()
    def _update_cell_height(self, value):
        if not self._loading_settings: self.grid_overlay.cell_height = value; self.grid_overlay.update()
    def chooseCellHorizontalColor(self):
        color = QColorDialog.getColor(self.grid_overlay.cell_horizontal_color, self, self.cell_h_color_dialog_title, options=QColorDialog.ColorDialogOption.ShowAlphaChannel)
        if color.isValid(): self.grid_overlay.cell_horizontal_color = color; self.updateCellHorizontalColorButton(); self.cell_h_opacity_slider.setValue(color.alpha()); self.grid_overlay.update() # Update slider and button
    def updateCellHorizontalOpacity(self, value): color = self.grid_overlay.cell_horizontal_color; color.setAlpha(value); self.grid_overlay.cell_horizontal_color = color; self.updateCellHorizontalColorButton(); self.grid_overlay.update()
    def updateCellHorizontalWidth(self, value): self.grid_overlay.cell_horizontal_width = value; self.cell_h_width_value.setValue(value); self.grid_overlay.update()
    def updateCellHorizontalWidthValue(self, value): self.grid_overlay.cell_horizontal_width = value; self.cell_h_width_slider.setValue(value) if 1 <= value <= self.cell_h_width_slider.maximum() else None; self.grid_overlay.update()
    def chooseCellVerticalColor(self):
        color = QColorDialog.getColor(self.grid_overlay.cell_vertical_color, self, self.cell_v_color_dialog_title, options=QColorDialog.ColorDialogOption.ShowAlphaChannel)
        if color.isValid(): self.grid_overlay.cell_vertical_color = color; self.updateCellVerticalColorButton(); self.cell_v_opacity_slider.setValue(color.alpha()); self.grid_overlay.update() # Update slider and button
    def updateCellVerticalOpacity(self, value): color = self.grid_overlay.cell_vertical_color; color.setAlpha(value); self.grid_overlay.cell_vertical_color = color; self.updateCellVerticalColorButton(); self.grid_overlay.update()
    def updateCellVerticalWidth(self, value): self.grid_overlay.cell_vertical_width = value; self.cell_v_width_value.setValue(value); self.grid_overlay.update()
    def updateCellVerticalWidthValue(self, value): self.grid_overlay.cell_vertical_width = value; self.cell_v_width_slider.setValue(value) if 1 <= value <= self.cell_v_width_slider.maximum() else None; self.grid_overlay.update()

    def updateOffsetX(self, value): self.grid_overlay.offset_x = value; self.x_offset_value.setValue(value); self.grid_overlay.update()
    def updateOffsetXValue(self, value): self.grid_overlay.offset_x = value; self.x_offset_slider.setValue(value) if self.x_offset_slider.minimum() <= value <= self.x_offset_slider.maximum() else None; self.grid_overlay.update()
    def updateOffsetY(self, value): self.grid_overlay.offset_y = value; self.y_offset_value.setValue(value); self.grid_overlay.update()
    def updateOffsetYValue(self, value): self.grid_overlay.offset_y = value; self.y_offset_slider.setValue(value) if self.y_offset_slider.minimum() <= value <= self.y_offset_slider.maximum() else None; self.grid_overlay.update()
    def resetOffsets(self): print(tr("resetting_offset")); self.updateOffsetXValue(0); self.updateOffsetYValue(0)

    def toggleDots(self, state_int):
        checked = (state_int == Qt.CheckState.Checked.value)
        # Update the internal state regardless of loading
        self.grid_overlay.show_dots = checked
        # Only trigger grid redraw if not loading settings
        if not self._loading_settings:
            self.grid_overlay.update()
        # Save setting immediately when toggled by user or shortcut (or on exit)
        # Let's save on exit to avoid too frequent writes.
        # self.settings.setValue("showDots", checked) # Optionally save immediately


    def updateDotSize(self, value): self.grid_overlay.dot_size = value; self.dot_size_value.setValue(value); self.grid_overlay.update()
    def updateDotSizeValue(self, value): self.grid_overlay.dot_size = value; self.dot_size_slider.setValue(value) if 1 <= value <= self.dot_size_slider.maximum() else None; self.grid_overlay.update()
    def chooseDotColor(self):
        color = QColorDialog.getColor(self.grid_overlay.dot_color, self, self.dot_color_dialog_title, options=QColorDialog.ColorDialogOption.ShowAlphaChannel)
        if color.isValid(): self.grid_overlay.dot_color = color; self.updateDotColorButton(); self.dot_opacity_slider.setValue(color.alpha()); self.grid_overlay.update() # Update slider and button
    def updateDotOpacity(self, value): color = self.grid_overlay.dot_color; color.setAlpha(value); self.grid_overlay.dot_color = color; self.updateDotColorButton(); self.grid_overlay.update()

    def updateHorizontalColorButton(self): self.h_color_button.setStyleSheet(f"background-color: {self.grid_overlay.horizontal_color.name(QColor.NameFormat.HexArgb)};")
    def updateVerticalColorButton(self): self.v_color_button.setStyleSheet(f"background-color: {self.grid_overlay.vertical_color.name(QColor.NameFormat.HexArgb)};")
    def updateCellHorizontalColorButton(self): self.cell_h_color_button.setStyleSheet(f"background-color: {self.grid_overlay.cell_horizontal_color.name(QColor.NameFormat.HexArgb)};")
    def updateCellVerticalColorButton(self): self.cell_v_color_button.setStyleSheet(f"background-color: {self.grid_overlay.cell_vertical_color.name(QColor.NameFormat.HexArgb)};")
    def updateDotColorButton(self): self.dot_color_button.setStyleSheet(f"background-color: {self.grid_overlay.dot_color.name(QColor.NameFormat.HexArgb)};")

    def saveSettings(self):
        self.settings.setValue("language", self.current_language)
        self.settings.setValue("gridMode", self.grid_overlay.grid_mode)
        self.settings.setValue("visible", self.grid_overlay.visible)
        self.settings.setValue("horizontalSections", self.grid_overlay.horizontal_sections)
        self.settings.setValue("verticalSections", self.grid_overlay.vertical_sections)
        self.settings.setValue("horizontalColor", self.grid_overlay.horizontal_color.name(QColor.NameFormat.HexArgb))
        self.settings.setValue("verticalColor", self.grid_overlay.vertical_color.name(QColor.NameFormat.HexArgb))
        self.settings.setValue("horizontalWidth", self.grid_overlay.horizontal_width)
        self.settings.setValue("verticalWidth", self.grid_overlay.vertical_width)
        self.settings.setValue("cellWidth", self.grid_overlay.cell_width)
        self.settings.setValue("cellHeight", self.grid_overlay.cell_height)
        self.settings.setValue("cellHorizontalColor", self.grid_overlay.cell_horizontal_color.name(QColor.NameFormat.HexArgb))
        self.settings.setValue("cellVerticalColor", self.grid_overlay.cell_vertical_color.name(QColor.NameFormat.HexArgb))
        self.settings.setValue("cellHorizontalWidth", self.grid_overlay.cell_horizontal_width)
        self.settings.setValue("cellVerticalWidth", self.grid_overlay.cell_vertical_width)
        self.settings.setValue("offsetX", self.grid_overlay.offset_x)
        self.settings.setValue("offsetY", self.grid_overlay.offset_y)
        self.settings.setValue("showDots", self.grid_overlay.show_dots) # Save dot visibility
        self.settings.setValue("dotSize", self.grid_overlay.dot_size)
        self.settings.setValue("dotColor", self.grid_overlay.dot_color.name(QColor.NameFormat.HexArgb))
        self.settings.sync()

    def loadSettings(self):
        print(tr("loading_settings"))
        self._loading_settings = True
        global current_lang
        loaded_lang = self.settings.value("language", "PL", type=str); self.current_language = loaded_lang if loaded_lang in translations else "PL"; current_lang = self.current_language
        self.retranslateUi()

        self.grid_overlay.visible = self.settings.value("visible", True, type=bool); self.grid_checkbox.setChecked(self.grid_overlay.visible)
        loaded_mode = int(self.settings.value("gridMode", GridOverlay.MODE_SECTIONS, type=int)); index = self.mode_combobox.findData(loaded_mode); self.mode_combobox.setCurrentIndex(index if index != -1 else 0); self.grid_overlay.grid_mode = loaded_mode

        h_sections = int(self.settings.value("horizontalSections", 11, type=int)); v_sections = int(self.settings.value("verticalSections", 11, type=int))
        self.grid_overlay.horizontal_sections = max(1, h_sections); self.grid_overlay.vertical_sections = max(1, v_sections)
        self.h_value.setValue(self.grid_overlay.horizontal_sections); self.h_slider.setValue(self.grid_overlay.horizontal_sections) if 1 <= self.grid_overlay.horizontal_sections <= self.h_slider.maximum() else None; self.rows_spinbox.setValue(self.grid_overlay.horizontal_sections)
        self.v_value.setValue(self.grid_overlay.vertical_sections); self.v_slider.setValue(self.grid_overlay.vertical_sections) if 1 <= self.grid_overlay.vertical_sections <= self.v_slider.maximum() else None; self.columns_spinbox.setValue(self.grid_overlay.vertical_sections)

        h_color_default = QColor(0, 120, 215, 128).name(QColor.NameFormat.HexArgb); self.grid_overlay.horizontal_color = QColor(self.settings.value("horizontalColor", h_color_default, type=str)); self.updateHorizontalColorButton(); self.h_opacity_slider.setValue(self.grid_overlay.horizontal_color.alpha())
        v_color_default = QColor(0, 120, 215, 128).name(QColor.NameFormat.HexArgb); self.grid_overlay.vertical_color = QColor(self.settings.value("verticalColor", v_color_default, type=str)); self.updateVerticalColorButton(); self.v_opacity_slider.setValue(self.grid_overlay.vertical_color.alpha())

        self.grid_overlay.horizontal_width = max(1, int(self.settings.value("horizontalWidth", 1, type=int))); self.h_width_value.setValue(self.grid_overlay.horizontal_width); self.h_width_slider.setValue(self.grid_overlay.horizontal_width) if 1 <= self.grid_overlay.horizontal_width <= self.h_width_slider.maximum() else None
        self.grid_overlay.vertical_width = max(1, int(self.settings.value("verticalWidth", 1, type=int))); self.v_width_value.setValue(self.grid_overlay.vertical_width); self.v_width_slider.setValue(self.grid_overlay.vertical_width) if 1 <= self.grid_overlay.vertical_width <= self.v_width_slider.maximum() else None

        self.grid_overlay.cell_width = max(1, int(self.settings.value("cellWidth", 50, type=int))); self.grid_overlay.cell_height = max(1, int(self.settings.value("cellHeight", 50, type=int)))
        self.cell_width_spinbox.setValue(self.grid_overlay.cell_width); self.cell_height_spinbox.setValue(self.grid_overlay.cell_height)

        cell_h_color_default = QColor(215, 120, 0, 128).name(QColor.NameFormat.HexArgb); self.grid_overlay.cell_horizontal_color = QColor(self.settings.value("cellHorizontalColor", cell_h_color_default, type=str)); self.updateCellHorizontalColorButton(); self.cell_h_opacity_slider.setValue(self.grid_overlay.cell_horizontal_color.alpha())
        cell_v_color_default = QColor(215, 120, 0, 128).name(QColor.NameFormat.HexArgb); self.grid_overlay.cell_vertical_color = QColor(self.settings.value("cellVerticalColor", cell_v_color_default, type=str)); self.updateCellVerticalColorButton(); self.cell_v_opacity_slider.setValue(self.grid_overlay.cell_vertical_color.alpha())

        self.grid_overlay.cell_horizontal_width = max(1, int(self.settings.value("cellHorizontalWidth", 1, type=int))); self.cell_h_width_value.setValue(self.grid_overlay.cell_horizontal_width); self.cell_h_width_slider.setValue(self.grid_overlay.cell_horizontal_width) if 1 <= self.grid_overlay.cell_horizontal_width <= self.cell_h_width_slider.maximum() else None
        self.grid_overlay.cell_vertical_width = max(1, int(self.settings.value("cellVerticalWidth", 1, type=int))); self.cell_v_width_value.setValue(self.grid_overlay.cell_vertical_width); self.cell_v_width_slider.setValue(self.grid_overlay.cell_vertical_width) if 1 <= self.grid_overlay.cell_vertical_width <= self.cell_v_width_slider.maximum() else None

        self.grid_overlay.offset_x = int(self.settings.value("offsetX", 0, type=int)); self.grid_overlay.offset_y = int(self.settings.value("offsetY", 0, type=int))
        self.x_offset_value.setValue(self.grid_overlay.offset_x); self.x_offset_slider.setValue(self.grid_overlay.offset_x) if self.x_offset_slider.minimum() <= self.grid_overlay.offset_x <= self.x_offset_slider.maximum() else None
        self.y_offset_value.setValue(self.grid_overlay.offset_y); self.y_offset_slider.setValue(self.grid_overlay.offset_y) if self.y_offset_slider.minimum() <= self.grid_overlay.offset_y <= self.y_offset_slider.maximum() else None

        self.grid_overlay.show_dots = self.settings.value("showDots", False, type=bool); self.dots_checkbox.setChecked(self.grid_overlay.show_dots) # Load dot visibility
        self.grid_overlay.dot_size = max(1, int(self.settings.value("dotSize", 4, type=int)))
        self.dot_size_value.setValue(self.grid_overlay.dot_size); self.dot_size_slider.setValue(self.grid_overlay.dot_size) if 1 <= self.grid_overlay.dot_size <= self.dot_size_slider.maximum() else None

        dot_color_default = QColor(0, 255, 0, 192).name(QColor.NameFormat.HexArgb); self.grid_overlay.dot_color = QColor(self.settings.value("dotColor", dot_color_default, type=str)); self.updateDotColorButton(); self.dot_opacity_slider.setValue(self.grid_overlay.dot_color.alpha())

        self._update_mode_ui(self.mode_combobox.currentIndex())
        self._loading_settings = False
        self.grid_overlay.update()


# --- GridApp Class ---
class GridApp(QApplication):
    toggleGridSignal = pyqtSignal()
    quitSignal = pyqtSignal()
    increaseColsSignal = pyqtSignal()
    decreaseColsSignal = pyqtSignal()
    increaseRowsSignal = pyqtSignal()
    decreaseRowsSignal = pyqtSignal()
    increaseXOffsetSignal = pyqtSignal()
    decreaseXOffsetSignal = pyqtSignal()
    increaseYOffsetSignal = pyqtSignal()
    decreaseYOffsetSignal = pyqtSignal()
    resetOffsetSignal = pyqtSignal()
    toggleDotsSignal = pyqtSignal()

    def __init__(self, argv):
        super(GridApp, self).__init__(argv)
        self.setQuitOnLastWindowClosed(False)
        self.grid_overlay = GridOverlay()
        self.settings_window = SettingsWindow(self.grid_overlay)
        self.settings_window.languageChanged.connect(self.updateLocalizedTexts)

        # Connect signals
        self.toggleGridSignal.connect(self.toggleGridShortcut)
        self.quitSignal.connect(self.quit)
        self.increaseColsSignal.connect(self.increaseColsShortcut)
        self.decreaseColsSignal.connect(self.decreaseColsShortcut)
        self.increaseRowsSignal.connect(self.increaseRowsShortcut)
        self.decreaseRowsSignal.connect(self.decreaseRowsShortcut)
        self.increaseXOffsetSignal.connect(self.increaseXOffsetShortcut)
        self.decreaseXOffsetSignal.connect(self.decreaseXOffsetShortcut)
        self.increaseYOffsetSignal.connect(self.increaseYOffsetShortcut)
        self.decreaseYOffsetSignal.connect(self.decreaseYOffsetShortcut)
        self.resetOffsetSignal.connect(self.resetOffsetShortcut)
        self.toggleDotsSignal.connect(self.toggleDotsShortcut)

        self.tray_icon = QSystemTrayIcon(self)
        self.createTrayIcon()
        if hasattr(self, 'tray_show_action'): self.tray_show_action.setChecked(self.grid_overlay.visible)

        self.registerShortcuts()

        self.updateGridGeometry()
        self.grid_overlay.setVisible(self.grid_overlay.visible)
        self.grid_overlay.show()

        if QGuiApplication.instance():
            QGuiApplication.instance().primaryScreenChanged.connect(self.updateGridGeometry)
            for screen in QGuiApplication.instance().screens():
                screen.geometryChanged.connect(self.updateGridGeometry)
                screen.availableGeometryChanged.connect(self.updateGridGeometry)
        else: print("Warning: Could not get QGuiApplication instance for screen signals.")

        self.aboutToQuit.connect(self.cleanupKeyboardHooks)

    def updateGridGeometry(self, screen_arg=None):
        qapp = QGuiApplication.instance()
        if not qapp: print("Warning: Could not access QGuiApplication instance for screen info."); return
        screen = qapp.primaryScreen()
        if not screen: print("Warning: Could not access primary screen."); return
        screen_geometry = screen.availableGeometry()
        if screen_geometry.isValid() and screen_geometry.width() > 0 and screen_geometry.height() > 0:
            self.grid_overlay.setGeometry(screen_geometry); self.grid_overlay.update()
        else: print(f"Warning: Invalid screen geometry obtained: {screen_geometry}")

    def createTrayIcon(self):
        icon_size = 32; pixmap = QPixmap(icon_size, icon_size); pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap); painter.setPen(QColor("yellow")); font = QFont("Arial", 30, QFont.Weight.Bold); painter.setFont(font)
        fm = painter.fontMetrics(); text_width = fm.horizontalAdvance("#"); text_height = fm.height()
        x = (icon_size - text_width) / 2; y = (icon_size - text_height) / 2 + fm.ascent()
        painter.drawText(QPoint(int(x), int(y)), "#"); painter.end(); icon = QIcon(pixmap)
        self.setWindowIcon(icon); self.tray_icon.setIcon(icon)

        tray_menu = QMenu()
        self.tray_show_action = QAction(tr("tray_show_grid"), self); self.tray_show_action.setCheckable(True)
        self.tray_show_action.setChecked(self.grid_overlay.visible); self.tray_show_action.triggered.connect(self.toggleGridViaMenu); tray_menu.addAction(self.tray_show_action)
        settings_action = QAction(tr("tray_settings"), self); settings_action.triggered.connect(self.showSettings); tray_menu.addAction(settings_action)
        tray_menu.addSeparator()
        quit_action = QAction(tr("tray_exit"), self); quit_action.triggered.connect(self.quit); tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        if not self.tray_icon.isVisible(): self.tray_icon.show()
        self.tray_icon.activated.connect(self.trayIconActivated)

    def updateLocalizedTexts(self):
        self.createTrayIcon()

    def trayIconActivated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger: self.showSettings()

    def toggleGridViaMenu(self, checked):
        self.settings_window.toggleGrid(Qt.CheckState.Checked.value if checked else Qt.CheckState.Unchecked.value)

    def showSettings(self):
        self.settings_window.show(); self.settings_window.raise_(); self.settings_window.activateWindow()

    def registerShortcuts(self):
        if HAS_KEYBOARD_LIB:
            try:
                keyboard.unhook_all() # Unhook previous first

                keyboard.add_hotkey('ctrl+shift+alt+end', lambda: self.quitSignal.emit(), trigger_on_release=False)
                keyboard.add_hotkey('ctrl+alt+f10', lambda: self.toggleGridSignal.emit(), trigger_on_release=False)
                keyboard.add_hotkey('ctrl+alt+up', lambda: self.increaseColsSignal.emit(), trigger_on_release=False)
                keyboard.add_hotkey('ctrl+alt+down', lambda: self.decreaseColsSignal.emit(), trigger_on_release=False)
                keyboard.add_hotkey('ctrl+alt+right', lambda: self.increaseRowsSignal.emit(), trigger_on_release=False)
                keyboard.add_hotkey('ctrl+alt+left', lambda: self.decreaseRowsSignal.emit(), trigger_on_release=False)
                keyboard.add_hotkey('ctrl+alt+;', lambda: self.decreaseXOffsetSignal.emit(), trigger_on_release=False)
                keyboard.add_hotkey('ctrl+alt+\\', lambda: self.increaseXOffsetSignal.emit(), trigger_on_release=False) # Use '\\' for backslash
                keyboard.add_hotkey('ctrl+alt+[', lambda: self.decreaseYOffsetSignal.emit(), trigger_on_release=False)
                keyboard.add_hotkey('ctrl+alt+]', lambda: self.increaseYOffsetSignal.emit(), trigger_on_release=False)
                keyboard.add_hotkey('ctrl+alt+f11', lambda: self.resetOffsetSignal.emit(), trigger_on_release=False)
                keyboard.add_hotkey('ctrl+alt+f12', lambda: self.toggleDotsSignal.emit(), trigger_on_release=False)

                print(tr("shortcuts_registered"))
            except Exception as e:
                print(tr("shortcuts_fail", e=e))
        else:
             pass # Warning handled in main

    def toggleGridShortcut(self):
        current_state = self.grid_overlay.isVisible()
        self.settings_window.toggleGrid(Qt.CheckState.Unchecked.value if current_state else Qt.CheckState.Checked.value)

    # --- Shortcut Handlers ---
    def increaseColsShortcut(self):
        if self.grid_overlay.grid_mode == GridOverlay.MODE_SECTIONS:
            new_val = self.grid_overlay.vertical_sections + 1; print(tr("shortcut_inc_cols", new_val=new_val)); self.settings_window.updateVerticalSectionsValue(new_val)
        else: print(tr("shortcut_ignored_mode"))
    def decreaseColsShortcut(self):
        if self.grid_overlay.grid_mode == GridOverlay.MODE_SECTIONS:
            new_val = max(1, self.grid_overlay.vertical_sections - 1); print(tr("shortcut_dec_cols", new_val=new_val)); self.settings_window.updateVerticalSectionsValue(new_val)
        else: print(tr("shortcut_ignored_mode"))
    def increaseRowsShortcut(self):
        if self.grid_overlay.grid_mode == GridOverlay.MODE_SECTIONS:
            new_val = self.grid_overlay.horizontal_sections + 1; print(tr("shortcut_inc_rows", new_val=new_val)); self.settings_window.updateHorizontalSectionsValue(new_val)
        else: print(tr("shortcut_ignored_mode"))
    def decreaseRowsShortcut(self):
         if self.grid_overlay.grid_mode == GridOverlay.MODE_SECTIONS:
            new_val = max(1, self.grid_overlay.horizontal_sections - 1); print(tr("shortcut_dec_rows", new_val=new_val)); self.settings_window.updateHorizontalSectionsValue(new_val)
         else: print(tr("shortcut_ignored_mode"))
    def increaseXOffsetShortcut(self):
        new_val = self.grid_overlay.offset_x + 1; print(tr("shortcut_inc_x", new_val=new_val)); self.settings_window.updateOffsetXValue(new_val)
    def decreaseXOffsetShortcut(self):
        new_val = self.grid_overlay.offset_x - 1; print(tr("shortcut_dec_x", new_val=new_val)); self.settings_window.updateOffsetXValue(new_val)
    def increaseYOffsetShortcut(self):
        new_val = self.grid_overlay.offset_y + 1; print(tr("shortcut_inc_y", new_val=new_val)); self.settings_window.updateOffsetYValue(new_val)
    def decreaseYOffsetShortcut(self):
        new_val = self.grid_overlay.offset_y - 1; print(tr("shortcut_dec_y", new_val=new_val)); self.settings_window.updateOffsetYValue(new_val)

    def resetOffsetShortcut(self):
        """Handles the Ctrl+Alt+F11 shortcut."""
        print(tr("shortcut_reset_offset"))
        self.settings_window.resetOffsets() # Call the existing reset function

    def toggleDotsShortcut(self):
        """Handles the Ctrl+Alt+F12 shortcut."""
        current_state = self.settings_window.dots_checkbox.isChecked()
        new_state = not current_state
        # Determine the correct translation key for the state message
        state_key = "show_dots_checkbox" if new_state else "hide_dots"
        print(tr("shortcut_toggle_dots", state=tr(state_key)))
        self.settings_window.dots_checkbox.setChecked(new_state)
        # The checkbox stateChanged signal will automatically call settings_window.toggleDots

    def cleanupKeyboardHooks(self):
        if HAS_KEYBOARD_LIB:
            print(tr("clearing_shortcuts"))
            try: keyboard.unhook_all(); print(tr("shortcuts_cleared"))
            except Exception as e: print(tr("shortcuts_clear_fail", e=e))

    def saveAllSettingsOnExit(self):
        print(tr("saving_settings_exit")); self.settings_window.saveSettings(); print(tr("settings_saved"))

    def quit(self):
        self.saveAllSettingsOnExit(); super().quit()

def main():
    temp_settings = QSettings("GridTool", "ConfigurableGrid")
    global current_lang
    loaded_lang = temp_settings.value("language", "PL", type=str); current_lang = loaded_lang if loaded_lang in translations else "PL"; del temp_settings

    app = GridApp(sys.argv)

    if not HAS_KEYBOARD_LIB : print(f"\n*** {tr('warning_keyboard_lib')} ***\n")
    elif sys.platform == 'linux':
         if HAS_KEYBOARD_LIB and hasattr(os, 'geteuid') and os.geteuid() != 0: # Check if geteuid exists (not on Windows)
              print(f"\n*** {tr('info_linux_sudo')} ***\n")
    elif sys.platform == 'win32': print(f"\n*** {tr('info_qtwin_removed')} ***\n")

    exit_code = app.exec(); print(tr("app_quit_code", exit_code=exit_code)); sys.exit(exit_code)

if __name__ == "__main__":
    main()