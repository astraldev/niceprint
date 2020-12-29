#!/bin/python3

import color as c
from color import red
import sys
from threading import Timer
from time import sleep
k = 0
val = 0


class SetInterval:
    """
    Set interval 
  @param interval:
    Time to perform function.
    In Seconds
  @param  Function:
    function to perform
  @param  end:
    Time to end interval after
    Defaults to 1000 seconds
  @param lock:
    If to allow execution of other codes 
    """

    def __init__(self, interval, function, end=1000):
        global k
        self.k = k
        k = self.k
        self.interval = interval
        self.function = function
        self.end = end
        self._interval()

    def _interval(self):
        global val
        self.k2 = Timer(self.interval, self._interval)
        self.k = self.k+1
        if self.k == self.end:
            self.cancel()
        val = self.function()
        self.val = val
        self.k2.start()

    def cancel(self):
        self.k = self.end
        self.k2.cancel()
        return


class InvalidColor(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = "No Such Color"
    pass


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
              'black', 'yellow', "cyan", None]

    @staticmethod
    def get_colors():
        return Print.colors[:]

    def _process_color(self, c):
        Print.colors[4] = "kblack"
        if c in Print.colors:
            return Print.colors[Print.colors.index(c)]
        if c in [c[0] for c in Print.colors[:len(Print.colors)-1]]:
            oc = [c[0] for c in Print.colors[:len(Print.colors)-1]]
            Print.colors[4] = "black"
            return Print.colors[oc.index(c)]

    def _get_text(self):

        if self.color is not None:
            print(eval(f"c.{self.color}")(
                (self.text[self.i])), end="", flush=True)
        else:
            print(self.text[self.i], end="", flush=True)

        self.i += 1
        if self.i == len(self.text):
            print()

    def _print(self, *args):
        self.inter = SetInterval(
            self.time, self._get_text, len(self.text))

    def _locking_print(self):
        for i, t in enumerate(self.text, 0):
            if self.color is not None:
                print(eval(f"c.{self.color}")(
                    (t)), end="", flush=True)
            else:
                print(t, end="", flush=True)
            try:
                sleep(self.time)
            except KeyboardInterrupt:
                print("\n", red("[INFO] : Canceled"))
                break

    def __init__(self, *text, color=None, time=0.03, lock=True, end="\n"):
        for ind, content in enumerate(text, 0):
            self.i = 0
            self.text = [x for x in str(content)]
            self.inter = None
            r_e = color not in [c[0]
                                for c in Print.colors[:len(Print.colors)-1]]
            r_e2 = color not in Print.colors
            if r_e is True and r_e2 is True:
                raise InvalidColor(
                    f"{color} Color is not in the list of colors")
            if color == "k":
                self.color = "black"
            else:
                self.color = self._process_color(color)
            self.time = time
            if lock:
                self._locking_print()
            else:
                self._print()
            print(end=end)


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
        return Print.colors
    def __init__(self, *args, color: list = [''], delimeter=" ", time: list = [0.03], lock: bool = True):
        if len(args) == len(color):
            for ind, text in enumerate(args, 0):
                Print(text, color=color[ind], end=delimeter, lock=lock)
            print()
        elif len(args) < len(color):
            la = len(args)
            lc = len(color)
            ll = lc//la
            for ind, text in enumerate(args):
                tt = text.split(" ")
                tt_ = []
                n = int(round(len(tt)/ll, 0))
                s = 0
                constn = n
                for t in range(ll):
                    tt_.append(" ".join(tt[s:n]))
                    s = n
                    temp = n
                    n += constn
                for ind_, wt in enumerate(tt_):
                    Print(wt, color=color[ind_], end=delimeter, lock=lock)
        pass

if __name__ == "__main__":
    MultiColoredPrint(
        """Print Letters individualy according to given time
    Usage
    -------
    >>> from niceprint import Print
    >>> Print(\"Hello\",color=\"red\",time=0.1)
    Hello
    
    Exceptions
    ----------
    Throws InvalidColor exception is the color
    is not in color list

    Accepted colors:
    --------------
    To get the accepted colors 
    >>> from niceprint import Print
    >>> Print.get_colors()
    """, color='mgr')
