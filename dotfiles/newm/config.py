## Copyright (C) 2020-2026 Aditya Shakya <adi1090x@gmail.com>
##
## NEWM Config for Archcraft (Improved with Theme Support)

from __future__ import annotations
from typing import Callable, Any
import os, logging, random, glob, subprocess, shlex

from newm.layout import Layout
from pywm import (
    PYWM_MOD_LOGO,
    PYWM_MOD_ALT,

    PYWM_TRANSFORM_90,
    PYWM_TRANSFORM_180,
    PYWM_TRANSFORM_270,
    PYWM_TRANSFORM_FLIPPED,
    PYWM_TRANSFORM_FLIPPED_90,
    PYWM_TRANSFORM_FLIPPED_180,
    PYWM_TRANSFORM_FLIPPED_270,
)

logger = logging.getLogger("newm.config")

## Theme ──────────────────────────────────────────────────────────────
theme = {
    "gtk_theme": "Nordic",
    "icon_theme": "Qogir-Dark",
    "cursor_theme": "Pear-Dark",
    "cursor_size": 16,
    "font": "Inter 9",

    "focus_color": "#FFFFFFFF",
    "ssd_color": "#000000FF",

    "wallpapers": "~/.config/newm/wallpapers/*.jpg",
    "default_wallpaper": "~/.config/newm/wallpapers/wallpaper-1.jpg",
}

## Helpers ─────────────────────────────────────────────────────────────
def run(cmd: str):
    """Run shell command safely in background."""
    try:
        subprocess.Popen(shlex.split(cmd))
    except Exception as e:
        logger.error(f"Failed: {cmd} -> {e}")

## Centralize scripts ─────────────────────────────────────────────────
scripts_dir = os.path.expanduser("~/.config/newm/scripts")
def sc(name: str): return os.path.join(scripts_dir, name)

scripts = {
    "terminal": sc("terminal"),
    "kitty": sc("kitty"),
    "colorpicker": sc("colorpicker"),
    "wlogout": sc("wlogout"),
    "screenshot": sc("screenshot"),
    "brightness": sc("brightness"),
    "volume": sc("volume"),
    "rofi": {
        "launcher": sc("rofi_launcher"),
        "music_mpd": sc("rofi_mpd"),
        "music_spotify": sc("rofi_spotify"),
        "bluetooth": sc("rofi_bluetooth"),
        "network": sc("rofi_network"),
        "powermenu": sc("rofi_powermenu"),
        "runner": sc("rofi_runner"),
        "screenshot": sc("rofi_screenshot"),
        "asroot": sc("rofi_asroot"),
    },
    "wofi": {
        "menu": sc("wofi_menu"),
        "powermenu": sc("wofi_powermenu"),
    }
}

## Startup ─────────────────────────────────────────────────────────────
def on_startup():
    init_service = (
        "systemctl --user import-environment DISPLAY WAYLAND_DISPLAY XDG_CURRENT_DESKTOP",
        "dbus-update-activation-environment --systemd DISPLAY WAYLAND_DISPLAY XDG_CURRENT_DESKTOP",
        "thunar --daemon",
        "nm-applet --indicator",
        "/usr/lib/xfce-polkit/xfce-polkit",
        sc("notifications"),
        sc("gtkthemes"),
        "mpd",
    )
    for service in init_service: run(service)
    logger.info("Startup complete")

## Reconfigure ────────────────────────────────────────────────────────
def on_reconfigure():
    run("notify-send -h string:x-canonical-private-synchronous:sys-notify -u low -i ~/.config/newm/mako/icons/desktop.png NEWM \"Configuration Reloaded\"")
    gnome_schema = 'org.gnome.desktop.interface'
    gnome_peripheral = 'org.gnome.desktop.peripherals'
    wm_service_extra_config = (
        f"gsettings set {gnome_schema} gtk-theme '{theme['gtk_theme']}'",
        f"gsettings set {gnome_schema} icon-theme '{theme['icon_theme']}'",
        f"gsettings set {gnome_schema} cursor-theme '{theme['cursor_theme']}'",
        f"gsettings set {gnome_schema} font-name '{theme['font']}'",
        f"gsettings set {gnome_peripheral}.keyboard repeat-interval 30",
        f"gsettings set {gnome_peripheral}.keyboard delay 500",
        f"gsettings set {gnome_peripheral}.mouse natural-scroll false",
        f"gsettings set {gnome_peripheral}.mouse speed 0.0",
        f"gsettings set {gnome_peripheral}.mouse accel-profile 'default'",
        f"gsettings set {gnome_peripheral}.touchpad natural-scroll false",
        f"gsettings set {gnome_peripheral}.touchpad speed 0.0",
        "gsettings set org.gnome.desktop.wm.preferences button-layout :",
    )
    for config in wm_service_extra_config: run(config)
    logger.info("Configuration reloaded")

## Wallpaper ───────────────────────────────────────────────────────────
##-- Apply random wallpaper on each startup and config reload
wp_files = glob.glob(os.path.expanduser(theme["wallpapers"]))
if not wp_files: wp_files = [os.path.expanduser(theme["default_wallpaper"])]
background = {
    #'path': os.environ['HOME'] + '/.config/newm/wallpapers/wallpaper-1.jpg',  # fixed example
    'path': random.choice(wp_files),
    'time_scale': 0.01,
    'anim': True,
}

## Output / Monitors ──────────────────────────────────────────────────
outputs = [
	##-- Default (All Monitors), Mode: 1920x1080, Scale: 0.67
    { 'name': '*', 'scale': 0.67, 'width': 1920, 'height': 1080,
      'mHz': 60, 'pos_x': 0, 'pos_y': 0 , 'anim': True },

	##-- Laptop Display, Mode: 1920x1080, Scale: 1
    #{ 'name': 'eDP-1', 'scale': 1.0, 'width': 1920, 'height': 1080,
    #  'mHz': 60, 'pos_x': 0, 'pos_y': 0 , 'anim': True },

	##-- External Monitor, Mode: 1920x1080, Scale: 1.5, Position: Right of Laptop
    #{ 'name': 'HDMI-A-1', 'scale': 1.5, 'width': 1920, 'height': 1080,
    #  'mHz': 60, 'pos_x': 1920, 'pos_y': 0 , 'anim': True },
]

## General Settings ───────────────────────────────────────────────────
corner_radius = 15
anim_time = 0.05
blend_time = 0.1
pywm = {
    'xkb_model': "",
    'xkb_layout': "",
    'xkb_variant': "",
    'xkb_options': "",
    'enable_xwayland': True,
    'xcursor_theme': theme["cursor_theme"],
    'xcursor_size': theme["cursor_size"],
    'tap_to_click': True,
    'natural_scroll': False,
    'focus_follows_mouse': True,
    'contstrain_popups_to_toplevel': True,
    'encourage_csd': False,
    'texture_shaders': 'basic',
    'renderer_mode': 'pywm',
}

## App Rules ──────────────────────────────────────────────────────────
def app_rules(view):
    # External blur toggle file
    blur_state_file = os.path.expanduser("~/.config/newm/waybar/.blur_state")
    blur_enabled = True
    try:
        with open(blur_state_file, "r") as f:
            blur_enabled = f.read().strip().lower() == "on"
    except FileNotFoundError:
        blur_enabled = True  # default to ON if file missing

    # Blur intensity values
    blur_settings = {"radius": 12, "passes": 6} if blur_enabled else {"radius": 0, "passes": 0}

    float_apps = {
        "io.calamares.calamares","Yad","yad","nm-connection-editor","org.pulseaudio.pavucontrol",
        "xfce-polkit","kvantummanager","qt5ct","qt6ct","feh","viewnior","Gpicview",
        "gimp","MPlayer","VirtualBox Manager","qemu","Qemu-system-x86_64"
    }
    blur_apps = {"Alacritty","kitty","rofi","Rofi","mako","google-chrome","Google-chrome","qutebrowser","org.qutebrowser.qutebrowser"}
    float_blur_apps = {"wofi","wlogout","alacritty-float","kitty-float"}

    if view.app_id in {"google-chrome", "Google-chrome", "Alacritty", "kitty", "qutebrowser", "org.qutebrowser.qutebrowser"}:
        return {"blur": blur_settings, "opacity": 0.65, "corner_radius": 15}

    if view.app_id in float_apps:
        return {"float": True}
    if (view.app_id in blur_apps or view.title == "rofi") and blur_enabled:
        return {"blur": blur_settings, "opacity": 0.70}
    if view.app_id in float_blur_apps:
        return {"float": True, "blur": blur_settings if blur_enabled else None, "opacity": 0.70}

    return None

## View ───────────────────────────────────────────────────────────────
view = {
    'corner_radius': 15,
    'padding': 8,
    'fullscreen_padding': 0,
    'send_fullscreen': True,
    'accept_fullscreen': True,
    'floating_min_size': False,
    'debug_scaling': True,
    'border_ws_switch': 100,
    'rules': app_rules,
    'ssd': {
		'enabled': False,
		'color': theme["ssd_color"],
		'width': 2,
    },
}

interpolation = {'size_adjustment': 0.5}

## Focus ──────────────────────────────────────────────────────────────
focus = {
    'enabled': False,
    'color': theme["focus_color"],
    'distance': 4,
    'width': 0,
    'animate_on_change': False,
    'anim_time': 0.05,
}

## Panels ─────────────────────────────────────────────────────────────
panels = {
    'bar': {
		'cmd': sc("statusbar"),
		'visible_fullscreen': False,
		'visible_normal': True,
    },
    'lock': {
        'cmd': 'alacritty -e newm-panel-basic lock',
        'w': 0.5,
        'h': 0.5,
        'corner_radius': 60,
    },
    'launcher': {
        'cmd': 'alacritty -e newm-panel-basic launcher',
        'w': 0.4,
        'h': 0.4,
        'corner_radius': 20,
    },
	'top_bar': {
		'native': { 'enabled': False,'height': 38,'font': 'Inter','texts': lambda: [""] }
	},
}

## Power Saving ───────────────────────────────────────────────────────
energy = {
    'idle_callback': lambda event: "idle",
    'idle_times': [120, 300, 600],
    'suspend_command': "loginctl lock-session && systemctl suspend",
}

## Key Bindings ───────────────────────────────────────────────────────
def key_bindings(layout: Layout) -> list[tuple[str, Callable[[], Any]]]:
    return [
		# -- Terminal : Alacritty
        ("L-Return", lambda: run(scripts["terminal"])),
        ("L-S-Return", lambda: run(f"{scripts['terminal']} -f")),
        ("L-A-Return", lambda: run(f"{scripts['terminal']} -s")),

		# -- Terminal : kitty
        #("L-Return", lambda: run(f"{scripts['kitty']}")),
        #("L-S-Return", lambda: run(f"{scripts['kitty']} -f")),
        #("L-A-Return", lambda: run(f"{scripts['kitty']} -F")),

		# -- Applications
        ("L-f", lambda: run("thunar")),
        ("L-e", lambda: run("geany")),
        ("L-w", lambda: run("firefox")),
        ("L-g", lambda: run("qutebrowser")),
        ("L-C", lambda: run("google-chrome-stable --force-dark-mode --enable-features=WebUIDarkMode")),

		# -- Rofi
        ("A-F1", lambda: run(scripts["rofi"]["launcher"])),
        ("A-F2", lambda: run(scripts["rofi"]["runner"])),
        ("L-d", lambda: run(scripts["rofi"]["launcher"])),
        ("L-S-d", lambda: run(scripts["rofi"]["launcher"])),
        #("L-m", lambda: run(scripts["rofi"]["music_mpd"])),
        ("L-m", lambda: run(scripts["rofi"]["music_spotify"])),
        ("L-b", lambda: run(scripts["rofi"]["bluetooth"])),
        ("L-n", lambda: run(scripts["rofi"]["network"])),
        ("L-x", lambda: run(scripts["rofi"]["powermenu"])),
        ("L-r", lambda: run(scripts["rofi"]["asroot"])),
        ("L-s", lambda: run(f"{scripts['screenshot']} --area")),

		# -- Wofi
        #("L-d", lambda: run(scripts["wofi"]["menu"])),
        #("A-F1", lambda: run(scripts["wofi"]["menu"])),
        #("L-x", lambda: run(scripts["wofi"]["powermenu"])),

		# -- Misc
        #("L-n", lambda: run("nm-connection-editor")),
        ("L-p", lambda: run(scripts["colorpicker"])),
        #("L-x", lambda: run(scripts["wlogout"])),

		# -- Focus / Scale (Mouse wheel style)
        ("C-Left", lambda: layout.move(-1, 0)),
        ("C-Right", lambda: layout.move(1, 0)),
        ("C-Up", lambda: layout.basic_scale(1)),
        ("C-Down", lambda: layout.basic_scale(-1)),
        ("L-Tab", lambda: layout.move(1, 0)),
        ("L-S-Tab", lambda: layout.move(-1, 0)),
        ("L-tab", lambda: layout.move(1, 0)),
        ("L-S-tab", lambda: layout.move(-1, 0)),
        ("L-A-Left", lambda: layout.move(-1, 0)),
        ("L-A-Down", lambda: layout.move(0, 1)),
        ("L-A-Up", lambda: layout.move(0, -1)),
        ("L-A-Right", lambda: layout.move(1, 0)),
        ("L-a", lambda: layout.move_in_stack(1)),
        ("L-space", lambda: layout.toggle_fullscreen()),
        ("L-S-space", lambda: layout.toggle_focused_view_floating()),

		# -- Scale
        ("L-equal", lambda: layout.basic_scale(1)),
        ("L-minus", lambda: layout.basic_scale(-1)),

		# -- Move
        ("L-S-Left", lambda: layout.move_focused_view(-1, 0)),
        ("L-S-Down", lambda: layout.move_focused_view(0, 1)),
        ("L-S-Up", lambda: layout.move_focused_view(0, -1)),
        ("L-S-Right", lambda: layout.move_focused_view(1, 0)),

		# -- Resize
        ("L-Left", lambda: layout.resize_focused_view(-1, 0)),
        ("L-Down", lambda: layout.resize_focused_view(0, 1)),
        ("L-Up", lambda: layout.resize_focused_view(0, -1)),
        ("L-Right", lambda: layout.resize_focused_view(1, 0)),
        ("L-C-Left", lambda: layout.resize_focused_view(-1, 0)),
        ("L-C-Down", lambda: layout.resize_focused_view(0, 1)),
        ("L-C-Up", lambda: layout.resize_focused_view(0, -1)),
        ("L-C-Right", lambda: layout.resize_focused_view(1, 0)),

		# -- Newm Misc
        ("L-", lambda: layout.toggle_overview(only_active_workspace=True)),
        ("L-q", lambda: layout.close_focused_view()),
        ("L-c", lambda: layout.close_focused_view()),
        ("L-A-c", lambda: layout.update_config()),
        ("L-Q", lambda: layout.terminate()),  # Do not delete this.
        ("C-A-Delete", lambda: layout.terminate()),
        ("C-A-l", lambda: layout.ensure_locked(dim=True)),

		# -- Function Keys
        ("XF86MonBrightnessUp", lambda: run(f"{scripts['brightness']} --inc")),
        ("XF86MonBrightnessDown", lambda: run(f"{scripts['brightness']} --dec")),
        ("XF86AudioRaiseVolume", lambda: run(f"{scripts['volume']} --inc")),
        ("XF86AudioLowerVolume", lambda: run(f"{scripts['volume']} --dec")),
        ("XF86AudioMute", lambda: run(f"{scripts['volume']} --toggle")),
        ("XF86AudioMicMute", lambda: run(f"{scripts['volume']} --toggle-mic")),

        ("Print", lambda: run(f"{scripts['screenshot']} --area")),
        ("A-Print", lambda: run(f"{scripts['screenshot']} --in5")),
        ("S-Print", lambda: run(f"{scripts['screenshot']} --in10")),
        ("L-Print", lambda: run(f"{scripts['screenshot']} --area")),
        ("L-S-s", lambda: run(f"{scripts['screenshot']} --area")),
        ("L-S-o", lambda: run(f"{scripts['screenshot']} --ocr")),
    ]

## Gestures ──────────────────────────────────────────────────────────
gesture_bindings = {
    'launcher': (None, "swipe-5"),
    'move_resize': ("L", "move-1", "swipe-2"),
    'swipe': (None, "swipe-3"),
    'swipe_to_zoom': (None, "swipe-4"),
}

gestures = {
    'lp_freq': 30.,
    'lp_inertia': 0.1,
    'two_finger_min_dist': 0.1,
    'validate_threshold': 0.02,

    'c': {
		'enabled': True,
		'scale_px': 800,
    },

    'dbus': {
		'enabled': True,
    },

    'pyevdev': {
		'enabled': False,
		'two_finger_min_dist': 0.1,
		'validate_threshold': 0.02,
    },
}

swipe = {
    'gesture_factor': 3,
    'grid_m': 1,
    'grid_ovr': 0.01,
    'lock_dist': 0.01,
}

swipe_zoom = {
    'gesture_factor': 3,
    'grid_m': 1,
    'grid_ovr': 0.01,
    'hyst': 0.01,
}

grid = {
    'min_dist': .05,
    'throw_ps': [2, 10],
    'time_scale': 0.05,
}

resize = {
    'grid_m': 3,
    'grid_ovr': 0.01,
    'hyst': 0.01,
}

move = {
    'grid_m': 3,
    'grid_ovr': 0.01,
}

move_resize = {
    'gesture_factor': 2
}

## EOF ───────────────────────────────────────────────────────────────
