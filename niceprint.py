#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Callable, Iterable, Union
import sys
from threading import Timer
from time import sleep
from enum import Enum
from json import dumps

k = 0
val = 0

COLORIZE_FORMAT = "\033[{:d};{:d};{:d}m{!s}\033[0m"

class _FgColor(Enum):
    Black   = 30
    Red     = 31
    Green   = 32
    Yellow  = 33
    Blue    = 34
    Magenta = 35
    Cyan    = 36
    White   = 37
    Null    = 10

class _BgColor(Enum):
    Black   = 40
    Red     = 41
    Green   = 42
    Yellow  = 43
    Blue    = 44
    Magenta = 45
    Cyan    = 46
    White   = 47
    Null    = 10

class Base(Enum):
    Reset        = 0
    Bold         = 1
    Faint        = 2
    Italic       = 3
    Underline    = 4
    BlinkSlow    = 5
    BlinkRapid   = 6
    ReverseVideo = 7
    Concealed    = 8
    CrossedOut   = 9
    Null         = 10

def _to_int(member):
    try:
        return member.value
    except:
        return member
        
    
def _colorize(bg, base, fg, *text):
    """ _colorize(bg, base, fg, *text)
    """
    # All argument types must be str. 
    rtext = [str(f) for f in text]
    
    return COLORIZE_FORMAT.format(
        _to_int(bg), _to_int(base), _to_int(fg), ''.join(rtext)
    )

def black(*text):
    return _colorize(_BgColor.Null, Base.Null, _FgColor.Black, *text)

def red(*text):
    return _colorize(_BgColor.Null, Base.Null, _FgColor.Red, *text)

def green(*text):
    return _colorize(_BgColor.Null, Base.Null, _FgColor.Green, *text)

def yellow(*text):
    return _colorize(_BgColor.Null, Base.Null, _FgColor.Yellow, *text)

def blue(*text):
    return _colorize(_BgColor.Null, Base.Null, _FgColor.Blue, *text)

def magenta(*text):
    return _colorize(_BgColor.Null, Base.Null, _FgColor.Magenta, *text)

def cyan(*text):
    return _colorize(_BgColor.Null, Base.Null, _FgColor.Cyan, *text)

def bg_black(*text):
    return _colorize(_BgColor.Black, Base.Null, _FgColor.Null, *text)

def bg_red(*text):
    return _colorize(_BgColor.Red, Base.Null, _FgColor.Null, *text)

def bg_green(*text):
    return _colorize(_BgColor.Green, Base.Null, _FgColor.Null, *text)

def bg_yellow(*text):
    return _colorize(_BgColor.Yellow, Base.Null, _FgColor.Null, *text)

def bg_blue(*text):
    return _colorize(_BgColor.Blue, Base.Null, _FgColor.Null, *text)

def bg_magenta(*text):
    return _colorize(_BgColor.Magenta, Base.Null, _FgColor.Null, *text)

def bg_cyan(*text):
    return _colorize(_BgColor.Cyan, Base.Null, _FgColor.Null, *text)

def create_full_list(amount, lst, cmp = None):
    if cmp is None:
        out = []
        length = amount // len(lst)
        remaining = amount % len(lst)+1
        for item in lst:
            for _ in range(length):
                out.append(item)
        for _ in range(remaining):
            out = [lst[0]] + out
        out.reverse()
        return out

class SetInterval:
    """
    Sets an interval for functions.
    
    """

    def __init__(self, interval:Union[int, float], function, end:int=1000, callback:Callable=None, \
                show_progress:bool=False, req:bool=False, args:list=None, kwargs:dict=None):
        """Creates an instance of SetInterval
        
        parameters
        ----------
        interval : Union[int, float]
            time between intervals
        function: Callable
            the function to call
        end: int
            number of times to run
        callback: Callable
            function to call after code run
        show_progress: bool
            If to show a progress bar to indicate running #buggy
        req: bool
            if to add self to the called function. usefull if function should cancel the interval
        args: Iterable
            List of arguments
        kwargs: dict
            List of named arguments"""
        global k, val
        self.k = k
        self.callback = callback
        k = self.k
        self.interval = interval
        self.function = function
        self.end = int(end)
        self.show_progress = show_progress
        if show_progress:
            self.progress = ProgressBar(len=end, color="green")
            if self.end > 50:
                self.progress.set_len(self.end//50)
        self.req = req
        self.args = args
        self.val = val
        self.kwargs = kwargs
        self._interval()

    def _interval(self):
        global val
        self.k2 = Timer(self.interval, self._interval)
        self.k = self.k+1
        if self.show_progress:
            if self.end > 50:
                if self.end // 50 == 0:
                    self.progress.pulse()
            else:
                self.progress.pulse()
        kwargs = self.kwargs
        args = self.args
        if self.req and self.args is None and self.kwargs is None:
            val = self.function(self)
        elif self.args is not None and self.req:
            val = self.function(self, *self.args)
        elif self.args is not None and self.kwargs and self.req:
            val = self.function(self, *self.args, **kwargs)
        elif self.kwargs is not None and self.req:
            val = self.function(self, **kwargs)
        elif self.kwargs is not None:
            val = self.function(**kwargs)
        elif self.args is not None:
            val = self.function(*args)
        else:
            val = self.function()
            
        self.val = val
        if self.k == self.end:
            self.cancel()
            return

        self.k2.start()

    def cancel(self):
        "Cancel running Interval"
        self.k = self.end
        self.k2.cancel()
        if self.callback is not None: 
            self.callback()
        val = self.val
        del self
        return val


class InvalidColor(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = "No Such Color"
    pass

def dummy(text, *args):
    return text
def bg_dummy(text, *args):
    return dummy(text, *args)
     


class Print:
    """Print Letters individualy according to given time
    Usage
    -----
    >>> from niceprint import Print
    >>> Print(\"Hello\",color=\"red\",time=0.1)
    Hello

    Exceptions
    ----------
    Throws InvalidColor exception is the color
    is not in color list

    Accepted colors:
    ---------------
    To get the accepted colors 
    >>> from niceprint import Print
    >>> Print.get_colors()
    """
    colors = ['red', 'green', 'blue', 'magenta',
              'black', 'yellow', "cyan"]

    @staticmethod
    def get_colors() -> list:
        "Returns the list of colors availiable"
        return Print.colors[:]
    
    @staticmethod
    def _process_color(c):
        if c is None or c == "":
            return "dummy"

        if c in Print.colors:
            return Print.colors[Print.colors.index(c)]

        Print.colors[4] = "kblack"
        if c in [cl[0] for cl in Print.colors]:
            oc = [cl[0] for cl in Print.colors]
            Print.colors[4] = "black"
            return Print.colors[oc.index(c)]
        

    def _get_text(self):

        if self.color is not None:
            print((eval(f"{self.color}")((self.text[self.i]))), end="", flush=True)
        elif self.bg_color is not None:
            print(eval(f"bg_{self.bg_color}")((self.text[self.i])), end="", flush=True)        
        elif self.color is not None:
            print(eval(f"bg_{self.bg_color}")(eval(f"{self.color}")((self.text[self.i]))), end="", flush=True)

        else:
            print(self.text[self.i], end="", flush=True)

        self.i += 1
        if self.i == len(self.text):
            print()

    def _print(self, *args):
        self.inter = SetInterval(self.time, self._get_text, len(self.text))

    def _locking_print(self):
        for i, t in enumerate(self.text, 0):
            if self.color is not None:
                print(eval(f"bg_{self.bg_color}")(eval(f"{self.color}")(
                    (t))), end="", flush=True)
            else:
                print(t, end="", flush=True)
            try:
                sleep(self.time)
            except KeyboardInterrupt:
                raise TimeoutError

    def __init__(self, *text, fg=None, bg=None, time=0.03, lock=True, end="\n", format=False):
        """Prints any amount of text with the given color and background.
            parameters
            ----------
            text: Iterable
                Items to print out. Can be anything
            fg: str
                Foreground color
            bg: str
                Background color
            lock: bool
                If lock is true, there will be no access to the console till the printing is over.
            end: str
                Character to end with
            format: bool
                If format is true, any item in @param 'text' that is a dict, will be formated with json.dumps with indent of 2"""
        for ind, content in enumerate(text, 0):
            self.i = 0
            if type(content) is dict or type(content) is list and format:
                content = dumps(content, indent=2)
            else:
                self.text = [x for x in str(content)]
            self.inter = None
            self.color = Print._process_color(fg)
            self.bg_color = Print._process_color(bg)

            if self.color is None or self.bg_color is None:
                raise InvalidColor()

            self.time = time
            if lock:
                self._locking_print()
            else:
                self._print()
            print(end=end)
        #print()
        return


class MultiColoredPrint:
    """
    MultiColoredPrint
    ----------------------
    Prints words or text individually according to the given time and color
    
    Usage
    -------
    >>> from niceprint import MultiColoredPrint as MP
    >>> text = \"Multiple Text\"
    >>> MP(text, color=[\'c\', 'g'])
    """
    @staticmethod
    def get_colors():
        "Returns all the accepted colors."
        return Print.colors

    def __init__(self, *args, color: Iterable = "", bg: Iterable = "", delimiter=" ", time = 0, lock: bool = True):
        """ Prints multiple text with multiple colors, different backgrounds and a special delimiter after each color. 
            parameters
            ----------
            args: Iterable
                Items to print
            color: str
                Foreground color
            bg: str
                Background color
            delimiter: str
                Character to print out after every item
            time: int | float
                Time for each item
            lock: bool
                If lock is true, there will be no access to the console till the printing is over."""
        args = [str(x) for x in args]
        color = list(color)
        color.reverse()
        bg = list(bg)
        bg.reverse()

        if len(bg) == 0:
            bg = [""]

        if len(color) == 0:
            color = [""]

        if len(args) == len(color) and len(args) == len(bg):
            for ind, text in enumerate(args, 0):
                Print(text, fg=color[ind], bg=bg[ind], end=delimiter, lock=lock, time=time)
                
            print()
        elif len(args) == len(color) and len(bg) == 0:
            for ind, text in enumerate(args, 0):
                Print(text, fg=color[ind], end=delimiter, lock=lock, time=time)
                
            print()
        elif len(args) == len(bg) and len(color) == 0:
            for ind, text in enumerate(args, 0):
                Print(text, bg=color[ind], end=delimiter, lock=lock, time=time)
                
            print()
        else:
            la = len(args)
            lc = len(color)
            ll = lc//la
            for ind, text in enumerate(args):
                tt = [str(x)+" " for x in text.split(" ")]
                if len(tt) < 2:
                    tt = list(text)
                tt_ = []
                n = int(round(len(tt)/ll, 0))
                s = 0
                constn = n
                for _ in range(ll):
                    tt_.append(" ".join(tt[s:n]))
                    s = n
                    n += constn
                if len(tt_) < len(tt):
                      tt_ = tt
                color = create_full_list(len(tt_), color)
                bg = create_full_list(len(tt_), bg)
                for ind_, wt in enumerate(tt_):
                    Print(wt, fg=color[ind_], bg=bg[ind_], end=delimiter, lock=lock, time=time)
                
            print()
        
class ProgressBar:
    def _process_len(self, *args):
        self.diff = 1
        if self.len > 20:
            self.diff = self.len//20
            self.len = 20

    def __init__(self, len=10, color="", bg="", char="#", **kwargs):
        """Creates a progress bar with the given length, color, background and character.
        >>> from niceprint import ProgressBar as pb
        >>> progress = pb(color='c', bg='k')
        >>> progress.fill(ms=10)
        [#         ]
        parameters
        ----------
        len: int
            Length of progress bar
        color: str
            Foreground color
        bg: str
            Background Color
        char: str
            Character in bar
        """
    
        self.len = len
        self._old_len = len
        self._process_len()
        len = self.len
        self.color = Print._process_color(color)
        self.bg_color = Print._process_color(bg)
        self.tick = 0
        self.charcter = char
        if char==" " or char == "":
            color = ""
            if bg == "":
                self.bg_color = Print._process_color("b")

        bar = f"[" + " "*len + "]"
        self.right_bar = "["
        self.left_bar = "]"
        
        try:
            if self.color is not None and self.bg_color is not None:
                char = eval(f"bg_{self.bg_color}")(eval(f"{self.color}")(char))
                bar = eval(f"bg_{self.bg_color}")(eval(f"{self.color}")(bar))
                self.right_bar = eval(f"bg_{self.bg_color}")(eval(f"{self.color}")(self.right_bar))
                self.left_bar = eval(f"bg_{self.bg_color}")(eval(f"{self.color}")(self.left_bar))
            elif self.bg_color is not None:
                char = eval(f"bg_{self.bg_color}")(char)
                bar = eval(f"bg_{self.bg_color}")(bar)
                self.left_bar = eval(f"bg_{self.bg_color}")(self.left_bar)
                self.right_bar = eval(f"bg_{self.bg_color}")(self.right_bar)
            elif self.color is not None:
                char = eval(f"{self.color}")(char)
                bar = eval(f"{self.color}")(bar)
        except Exception as e:
            color = ""
            print(e)
        self.char = char
        self.pg = 0
        self.chw = 0
        self.clean_up()
        sys.stdout.write(u"\u001b[1000D"+bar)
        sys.stdout.flush()
        
    def set_len(self, len):
        "Set the length of the progress bar"
        self.len = len
        self.pulse()
    
    def clean_up(self, *args):
        "Cleans the line it's on"
        sys.stdout.write(u"\u001b[10000000000D")
        sys.stdout.flush()
    
    def empty(self, *args):
        "Empties the progress bar"
        self.pg = 0
        self.chw = 0
        
    def fill(self, ms=10, sec=None, text = ""):
        """Fill up the progress bar according to time.
        >>> from niceprint import ProgressBar as pb
        >>> progress = pb(2, 'c', 'r')
        >>> progress.fill(text = ['One text'])
        [# ] One text
        [##] One text
        >>> progress.empty()
        >>> progress.fill(text = ['Text 1', 'Text 2'])
        [# ] Text 1
        [##] Text 2

        parameters
        ----------
        ms: int 
            Time between each pulse in milliseconds
        sec: int | float
            Time between each pulse in seconds
        text: str | list | Tuple
            Items to print at the end of the bar

        """
        char=self.char
        self.len = self.len-self.pg
        if sec is not None:
            t = sec
        elif ms is not None:
            t = ms/100
        for _ in range(self.len+1):
            sleep(t)
            bar = self.right_bar + (char*(self.pg+_)) +" "*(self.len-_) + self.left_bar +" "+ str(text)
            self.tick += 1
            sys.stdout.write(u"\u001b[1000D"+bar)
            sys.stdout.flush()
        print()
    def set_color(self, color) -> bool:
        """Sets the backgroun color of the char in the bar
        returns True if color has been set else False"""
        if color != "":
            try:
                color = Print._process_color(color)
                self.char = eval(f"{color}")(self.charcter)
                self.color = color
            except Exception as e:
                color = ""
                print(e)
                return False
            return True
    def set_bgcolor(self, color) -> bool:
        """Sets the backgroun color of the char in the bar
        returns True if color has been set else False"""
        if color != "":
            try:
                color = Print._process_color(color)
                self.char = eval(f"bg_{color}")(self.charcter)
                self.bg_color = color
            except Exception as e:
                color = ""
                print(e)
                return False
            return True
    def set_char(self, char, *args) -> bool:
        """Sets the character of the progress bar
        returns True if char has been set else False"""
        try:
            self.char = eval(f"{self.color}")(char)
            self.charcter = char
            return True
        except Exception as e:
            print(e)
            return False

    def pulse(self, step=1, ms=1, sec=None, text: str = ""):
        """Increase the progress bar by amount of step and with a text
        parameters
        ----------
        ms: int 
            Time between each pulse in milliseconds
        sec: int | float
            Time between each pulse in seconds
        text: str 
            String to print at the end of the bar
        """
        if step > 1:
            self.len = self._old_len*2
            self._process_len()
        if self.len <= self.pg:
            return
        try:
            t = ms/100 if sec is None else sec
            sleep(t)
        except Exception as e:
            Print("[ERROR] : ", e, color="r")
        char = self.char
        self.tick += 1
        self.chw = step
        
        if self.tick % self.diff == 0:
            self.pg += step
            bar = self.right_bar + (char*(self.pg)) +" "*(self.len-self.pg) + self.left_bar +" "+ str(text)
            sys.stdout.write(u"\u001b[1000D"+bar)
            sys.stdout.flush()
        if self.pg == self.len:
            print()

class Spinner:
    def __del__(self, *args):
        print()

    def __init__(self, fg="c", bg = "", *args):
        """Creates a spinner
        >>> from niceprint import Spinner
        >>> sp = Spinner()
        >>> sp.rotate()

        parameters
        ----------
        fg: str
            Foreground color
        bg: str
            Background color
        
        """
        self.color = Print._process_color(fg)
        self.bg = Print._process_color(bg)
        self._chars = [" | ", " / ", " -- ", " \\ "]
        self._index = 0
        sys.stdout.flush()

    def _get_char(self, *args):
        if self._index > len(self._chars)-1:
            self._index = 0
        ch = eval(f"bg_{self.bg}")(eval(f"{self.color}")(self._chars[self.index]))
        self._index += 1
        return ch

    def spin(self, *args):
        "Turns the spinner 1 step"
        sys.stdout.write(u"\u001b[10000D"+" "*100)
        sys.stdout.write(u"\u001b[10000D" + self._get_char())
        sys.stdout.flush()

    def rotate(self, times: int = 5, time: int = 0.1, text: Union[str, list] = ""):
        """Rotates the spiner N(times) with a time interval of T(time)
        parameters
        ----------
        times: int 
            Times to rotate
        time: int | float
            Time between each turn in seconds
        text: str | list | Tuple
            Items to print at the end of the bar
        """
        
        for _ in range(times):
            if type(text) is list:
                text = create_full_list(self._chars, text)
                for x in range(len(self._chars)):
                    sys.stdout.write(u"\u001b[10000D"+" "*100)
                    sys.stdout.write(u"\u001b[10000D" + eval(f"bg_{self.bg}")(eval(f"{self.color}")(self._chars[x])) + text[x])
                    sys.stdout.flush()
                    sleep(time)
            if type(text) is str:
                for x in range(len(self._chars)):
                    sys.stdout.write(u"\u001b[10000D"+" "*100)
                    sys.stdout.write(u"\u001b[10000D" + eval(f"bg_{self.bg}")(eval(f"{self.color}")(self._chars[x])) + text)
                    sys.stdout.flush()
                    sleep(time)
        sys.stdout.write(u"\u001b[1000D")
        sys.stdout.flush()

class Percentage:
    def __init__(self,max = 100, fg="", bg=""):
        """Creates a percentage class
        >>> from niceprint import Percentage
        >>> pg = Percentage(10)
        >>> pg.tick()
        0%
        >>> pg.fill(text = ['Starting...', 'Almost Done', 'Just a sec..'])
        parameters
        ----------
        max: int
            Maximum number
        fg: str
            Foreground color
        bg: str
            Background color
        """
        self.fg = Print._process_color(fg)
        self.bg = Print._process_color(bg)
        self.max = max
        self.start = 0
    
    def _get_point(self, *args):
        return eval(f"bg_{self.bg}")(eval(f"{self.fg}")(str(self.start)+"%")) + " "

    def tick(self, text = ""):
        "Increases the percentage value by 1 with an optional text at the end"
        sys.stdout.write(u"\u001b[10000D"+" "*100)
        sys.stdout.write(u"\u001b[10000D"+self._get_point()+str(text))
        sys.stdout.flush()
        self.start += 1
    
    def fill(self, time: Union[int, float] = 0, text: Union[str, list] = ""):
        """Increases the percentage value till the end with multiple or single text
        parameters
        ----------
        time: int | float
            Time between each increment in seconds
        text: str | list | Tuple
            Items to print at the end of the bar
            """
        if type(text) is list:
            text = create_full_list(self.max - self.start, text)

            while self.start <= self.max:
                #print(len(text), self.max - self.start, [self.max - self.start])
                sys.stdout.write(u"\u001b[10000D"+" "*100)
                sys.stdout.write(u"\u001b[10000D"+self._get_point()+str(text[self.max - self.start]))
                sys.stdout.flush()
                self.start += 1
                sleep(time)
        elif type(text) is str:
            while self.start <= self.max:
                sys.stdout.write(u"\u001b[10000D"+" "*100)
                sys.stdout.write(u"\u001b[10000D"+self._get_point()+text)
                sys.stdout.flush()
                self.start += 1
                sleep(time)
    def __del__(self, *args):
        print()

if __name__ == "__main__":
    MultiColoredPrint("Multi Colored Print", color='cmb', delimiter="")

