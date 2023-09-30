import subprocess
from typing import Iterable, Iterator
from plover.oslayer.keyboardcontrol import KeyboardEmulation as OldKeyboardEmulation
from plover import log
try:
    from plover.key_combo import parse_key_combo
except ImportError:
    log.warning('with KeyCombo new interface')
    from plover.key_combo import KeyCombo
    _key_combo = KeyCombo()
    def parse_key_combo(combo_string: str):
        return _key_combo.parse(combo_string)

have_output_plugin = False
try:
    from plover.oslayer import KeyboardEmulationBase
    have_output_plugin = True
except ImportError:
    pass
class Main:
    def __init__(self, engine):
        self._engine = engine
        self._old_keyboard_emulation=None
    def start(self):
        if hasattr(self._engine, "_output"):
            pass
        else:
            if False: # stfu
                log.warning("Output plugin not properly supported!")
            assert self._old_keyboard_emulation is None
            self._old_keyboard_emulation = self._engine._keyboard_emulation
            assert isinstance(self._old_keyboard_emulation, OldKeyboardEmulation)
            self._engine._keyboard_emulation = KeyboardEmulation()
    def stop(self):
        if hasattr(self._engine, "_output"):
            log.warning("stop (while Plover has not quited) not supported -- uninstall the plugin instead")
        else:
            assert self._old_keyboard_emulation is not None
            self._engine._keyboard_emulation = self._old_keyboard_emulation
            self._old_keyboard_emulation = None

# These contain duplicates but whatever
typeable_chars = set([
    0x0031,
0x00B0,
0x00B0,
0x00B9,
0x00AA,
0x00AA,
0x00AA,
0x2081,
0x2081,
0x00AC,
0x0032,
0x00A7,
0x00A7,
0x00B2,
0x00BA,
0x00BA,
0x00BA,
0x2082,
0x2082,
0x2228,
0x0033,
0x2113,
0x2113,
0x00B3,
0x2116,
0x2116,
0x2116,
0x2083,
0x2083,
0x2227,
0x0034,
0x00BB,
0x00BB,
0x203A,
0x2640,
0x2640,
0x22A5,
0x0035,
0x00AB,
0x00AB,
0x2039,
0x00B7,
0x00B7,
0x00B7,
0x2642,
0x2642,
0x2221,
0x0036,
0x0024,
0x0024,
0x00A2,
0x00A3,
0x00A3,
0x00A3,
0x26A5,
0x26A5,
0x2225,
0x0037,
0x20AC,
0x20AC,
0x00A5,
0x00A4,
0x00A4,
0x00A4,
0x03F0,
0x03F0,
0x2192,
0x0038,
0x201E,
0x201E,
0x201A,
0x21E5,
0x21E5,
0x21E5,
0x27E8,
0x27E8,
0x221E,
0x0039,
0x201C,
0x201C,
0x2018,
0x002F,
0x002F,
0x002F,
0x27E9,
0x27E9,
0x221D,
0x0030,
0x201D,
0x201D,
0x2019,
0x002A,
0x002A,
0x002A,
0x2080,
0x2080,
0x2205,
0x002D,
0x2014,
0x2014,
0x002D,
0x002D,
0x002D,
0x2011,
0x2011,
0x254C,
0x0078,
0x0078,
0x0078,
0x0058,
0x0058,
0x2026,
0x03BE,
0x03BE,
0x039E,
0x0076,
0x0076,
0x0076,
0x0056,
0x0056,
0x005F,
0x221A,
0x006C,
0x006C,
0x006C,
0x004C,
0x004C,
0x005B,
0x03BB,
0x03BB,
0x039B,
0x0063,
0x0063,
0x0063,
0x0043,
0x0043,
0x005D,
0x03C7,
0x03C7,
0x2102,
0x0077,
0x0077,
0x0077,
0x0057,
0x0057,
0x005E,
0x03C9,
0x03C9,
0x03A9,
0x006B,
0x006B,
0x006B,
0x004B,
0x004B,
0x0021,
0x00A1,
0x00A1,
0x00A1,
0x03BA,
0x03BA,
0x00D7,
0x0068,
0x0068,
0x0068,
0x0048,
0x0048,
0x003C,
0x0037,
0x0037,
0x0037,
0x03C8,
0x03C8,
0x03A8,
0x0067,
0x0067,
0x0067,
0x0047,
0x0047,
0x003E,
0x0038,
0x0038,
0x0038,
0x03B3,
0x03B3,
0x0393,
0x0066,
0x0066,
0x0066,
0x0046,
0x0046,
0x003D,
0x0039,
0x0039,
0x0039,
0x03C6,
0x03C6,
0x03A6,
0x0071,
0x0071,
0x0071,
0x0051,
0x0051,
0x0026,
0x002B,
0x002B,
0x002B,
0x03D5,
0x03D5,
0x211A,
0x00DF,
0x1E9E,
0x1E9E,
0x1E9E,
0x017F,
0x2212,
0x2212,
0x2212,
0x03C2,
0x03C2,
0x2218,
0x0075,
0x0075,
0x0075,
0x0055,
0x0055,
0x005C,
0x2282,
0x0069,
0x0069,
0x0069,
0x0049,
0x0049,
0x002F,
0x03B9,
0x03B9,
0x222B,
0x0061,
0x0061,
0x0061,
0x0041,
0x0041,
0x007B,
0x03B1,
0x03B1,
0x2200,
0x0065,
0x0065,
0x0065,
0x0045,
0x0045,
0x007D,
0x03B5,
0x03B5,
0x2203,
0x006F,
0x006F,
0x006F,
0x004F,
0x004F,
0x002A,
0x03BF,
0x03BF,
0x2208,
0x0073,
0x0073,
0x0073,
0x0053,
0x0053,
0x003F,
0x00BF,
0x00BF,
0x00BF,
0x03C3,
0x03C3,
0x03A3,
0x006E,
0x006E,
0x006E,
0x004E,
0x004E,
0x0028,
0x0034,
0x0034,
0x0034,
0x03BD,
0x03BD,
0x2115,
0x0072,
0x0072,
0x0072,
0x0052,
0x0052,
0x0029,
0x0035,
0x0035,
0x0035,
0x03C1,
0x03C1,
0x211D,
0x0074,
0x0074,
0x0074,
0x0054,
0x0054,
0x002D,
0x0036,
0x0036,
0x0036,
0x03C4,
0x03C4,
0x2202,
0x0064,
0x0064,
0x0064,
0x0044,
0x0044,
0x003A,
0x002C,
0x002C,
0x002C,
0x03B4,
0x03B4,
0x0394,
0x0079,
0x0079,
0x0079,
0x0059,
0x0059,
0x0040,
0x002E,
0x002E,
0x002E,
0x03C5,
0x03C5,
0x2207,
0x00FC,
0x00FC,
0x00FC,
0x00DC,
0x00DC,
0x0023,
0x222A,
0x00F6,
0x00F6,
0x00F6,
0x00D6,
0x00D6,
0x0024,
0x03F5,
0x03F5,
0x2229,
0x00E4,
0x00E4,
0x00E4,
0x00C4,
0x00C4,
0x007C,
0x03B7,
0x03B7,
0x2135,
0x0070,
0x0070,
0x0070,
0x0050,
0x0050,
0x007E,
0x03C0,
0x03C0,
0x03A0,
0x007A,
0x007A,
0x007A,
0x005A,
0x005A,
0x0060,
0x03B6,
0x03B6,
0x2124,
0x0062,
0x0062,
0x0062,
0x0042,
0x0042,
0x002B,
0x003A,
0x003A,
0x003A,
0x03B2,
0x03B2,
0x21D0,
0x006D,
0x006D,
0x006D,
0x004D,
0x004D,
0x0025,
0x0031,
0x0031,
0x0031,
0x03BC,
0x03BC,
0x21D4,
0x002C,
0x2013,
0x2013,
0x0022,
0x0032,
0x0032,
0x0032,
0x03F1,
0x03F1,
0x21D2,
0x002E,
0x2022,
0x2022,
0x0027,
0x0033,
0x0033,
0x0033,
0x03D1,
0x03D1,
0x21A6,
0x006A,
0x006A,
0x006A,
0x004A,
0x004A,
0x003B,
0x003B,
0x003B,
0x003B,
0x03B8,
0x03B8,
0x0398,
0x0020,
0x0030,
0x0030,
0x0030,
0x02DE,
0x02DE,
0x202F,
0x02C7,
0x02C7,
0x21BB,
0x02D9,
0x02D9,
0x02D9,
0x02DE,
0x02DE,
0x002E,
0x02DA,
0x1FFE,
0x1FFE,
0x00AF,
0x002F,
0x02DD,
0x02DD,
0x02DD,
0x1FBF,
0x1FBF,
0x02D8,
0x003D,
0x2260,
0x2260,
0x2260,
0x2248,
0x2248,
0x2261,
0x002F,
0x002F,
0x002F,
0x00F7,
0x2044,
0x2044,
0x2044,
0x2300,
0x2300,
0x2223,
0x002A,
0x002A,
0x002A,
0x22C5,
0x00D7,
0x00D7,
0x00D7,
0x2299,
0x2299,
0x2297,
0x002D,
0x002D,
0x002D,
0x2212,
0x2216,
0x2216,
0x2216,
0x2296,
0x2296,
0x2238,
0x0037,
0x2714,
0x2714,
0x2195,
0x226A,
0x226A,
0x2308,
0x0038,
0x2718,
0x2718,
0x2191,
0x2229,
0x2229,
0x22C2,
0x0039,
0x2020,
0x2020,
0x226B,
0x226B,
0x2309,
0x0034,
0x2663,
0x2663,
0x2190,
0x2282,
0x2282,
0x2286,
0x0035,
0x20AC,
0x20AC,
0x003A,
0x22B6,
0x22B6,
0x22B7,
0x0036,
0x2023,
0x2023,
0x2192,
0x2283,
0x2283,
0x2287,
0x002B,
0x002B,
0x002B,
0x00B1,
0x2213,
0x2213,
0x2213,
0x2295,
0x2295,
0x2214,
0x0031,
0x2666,
0x2666,
0x2194,
0x2264,
0x2264,
0x230A,
0x0032,
0x2665,
0x2665,
0x2193,
0x222A,
0x222A,
0x22C3,
0x0033,
0x2660,
0x2660,
0x21CC,
0x2265,
0x2265,
0x230B,
0x0030,
0x2423,
0x2423,
0x0025,
0x2030,
0x2030,
0x25A1,
0x002C,
0x002E,
0x002E,
0x002C,
0x2032,
0x2032,
0x2033,
ord('\b')] # for backspace
)

def to_commands(text: Iterable[str]) -> Iterator[str]:
    cur_str = ""
    for c in text:
        if c in typeable_chars:
            cur_str += c
        else:
            if cur_str:
                yield f"type {cur_str}"
                cur_str = ""
            yield "key ctrl+shift+u"
            yield f"type {hex(ord(c))[2:]}"
            yield "key space"
    if cur_str:
        yield f"type {cur_str}"
            

class KeyboardEmulation(*([KeyboardEmulationBase] if have_output_plugin else [])):
    """Emulate keyboard events."""

    @classmethod
    def get_option_info(cls):
        return {}

    def __init__(self, params = None):
        if have_output_plugin:
            KeyboardEmulationBase.__init__(self, params)
        self._ms = None
        self._dotool = subprocess.Popen(["dotool"], stdin = subprocess.PIPE)
    
    def _communicate(self, input):
        self._dotool.communicate(input.encode("UTF-8") + b"\n")

    def start(self):
        start()

    def cancel(self):
        pass

    def set_ms(self, ms):
        if self._ms != ms:
            self._communicate(f"keydelay {ms}")
            self._communicate(f"keyhold {ms}")
            self._communicate(f"typedelay {ms}")
            self._communicate(f"typehold {ms}")
            self._ms = ms

    def _wtype_string(self, s):
        for cmd in to_commands(s):
            self._communicate(cmd)

    def send_string(self, s):
        self._wtype_string(s)

    def send_key_combination(self, combo_string):
        key_events = parse_key_combo(combo_string)
        for (name, press) in key_events:
            if press:
                self._communicate(f"keydown {name}")
            else:
                self._communicate(f"keyup {name}")

    def send_backspaces(self, n):
        self._wtype_string("\b" * n)
