********
Examples
********

Usage 
-----
Before using any of the classes or functions, validate color or check for availiable colors using

.. code-block:: python

   from niceprint import get_availiable_colors, color_is_valid
   # Availiable colors
   print(get_availiable_colors())
   # Validating colors
   # Black short form is 'k'
   print(color_is_valid("k"))
   print(color_is_valid("black"))
   print(color_is_valid("b"))
   print(color_is_valid("blue"))
   print(color_is_valid("r"))
   print(color_is_valid("red"))
   print(color_is_valid("m"))
   print(color_is_valid("magenta"))
   print(color_is_valid("c"))
   print(color_is_valid("cyan"))




Using SetInterval
-----------------

SetInterval is asynchronous. It runs in the background.

.. code-block:: python

  from niceprint import SetInterval
  from time import sleep
  def callback():
    print("This is the call back")

  def hello(interval = None, *args, **kwargs):
    print("Hello ")

    if interval:
      print("Interval has been spoted.")
      # Cancelling the interval
      print("Cancelling")
      interval.cancel()

    if args:
      print("Positional arguments are availiable.", args)
      print()

    if kwargs:
      print("Named arguments are availiable.", kwargs)
      print()

  def hello2(*args, **kwargs):
    print("Hello ")

    if args:
      print("Positional arguments are availiable.", args)
      print()

    if kwargs:
      print("Named arguments are availiable.", kwargs)
      print()

  if __name__ == "__main__":
    # Without any args, kwargs and request
    interval = SetInterval(1, hello, 1)
    interval.begin() 
    sleep(2)

    # With args and no request
    interval = SetInterval(1, hello2, 1, args=[1, 2, 3])
    interval.begin()
    sleep(2)

    # With args and request
    interval = SetInterval(1, hello, 2, req=True, args=[1, 2, 3])
    interval.begin()
    sleep(2)

    #With kwargs and no request
    interval = SetInterval(1, hello2, 2, kwargs={"x":4, "y":5})
    interval.begin()
    sleep(2)

    #With kwargs and request
    interval = SetInterval(1, hello, 2, req=True, kwargs={"x":4, "y":5})
    interval.begin()
    sleep(2)
    
    # With callback
    interval = SetInterval(1, hello, 5, callback=callback)
    interval.begin()
    sleep(5)

Using Print
------------

.. code-block:: python

   from niceprint import Print
   # Plain Print
   Print("This is an example", "Line 2")
   # With foreground color
   Print("This is an example", "Line 2", 4500, fg="g")
   # With background color
   Print("This is an example", "Line 2", {"help": "This is a dict"}, bg="k")
   # With foreground and background color
   Print("This is an example", "Line 2", [0, 1, 2, 3], fg="g", bg="k")
   # Slow printing
   Print("Slowly print me", time=1)
   # Formated output
   items = {
      "a": "This is not not a long string", 
      "b": "Short string"
   }
   Print(items, [0, 1, 2, 3, 4], format=True)

Using MultiColoredPrint
-----------------------

.. code-block:: python

   from niceprint import MultiColoredPrint as mcp
   # NOTE:
   #  `color=["r", "g"]` is the same as color="rg", color=("r", "g")
   #  `bg=["r", "g"]` is the same as bg="rg", bg=("r", "g")
   
   # Plain
   mcp("Plain Text")
   # With red foreground
   mcp("Red Text", color="r")
   mcp("RedText", color="r")
   # With red and green foreground
   mcp("Red Green", bg="rg")
   mcp("Red, Green", color=["r","g"])
   # Without space
   mcp("RedGreen", bg="rg")
   mcp("RedGreen", color=["r","g"])
   # With red background
   mcp("Red BG", bg="r")
   # With red and green background
   mcp("Red BG", bg="rg")
   mcp("Red BG", bg=["r","g"])
   # Without space
   mcp("RedBG", bg="rg")
   mcp("RedBG", bg=["r","g"])

   # With both color and background
   mcp("Red BG", bg=["r","g"], color="bk")
   # Timed 
   mcp("Red BG", time=0.5)
   mcp("Red BG", bg=["r","g"], time=0.4)
   mcp("Red BG", color=["r","g"], time=0.4)
   mcp("Red BG", color=["r","g"], bg=["g", "r"], time=0.4)

Using Spinner
-------------

.. code-block:: python

   from niceprint import Spinner
   from time import sleep

   sp = Spinner()

   # Turn the spinner 1 time
   sp.spin() # without text
   sleep(1)
   sp.spin(0) # with text

   # Rotate the spinner 10 times wit 0.5 seconds delay
   sp.rotate(10, 0.5, "Loading...")

Using ProgressBar
-----------------

.. code-block:: python

   from niceprint import ProgressBar
   pb = ProgressBar(6, color="r", bg="k", char="=")
   # Add 1 character to the bar
   pb.pulse()
   # Fill up the bar with each pulse 50ms after the other
   pb.fill(text = [0, 1, 2, 3, 4], ms=50)

Using Percentage
----------------

.. code-block:: python

   from niceprint import Percentage
   pc = Percentage(fg="r", bg="k")
   # Increment of the percentage
   pc.tick()
   # - With text
   pc.tick("First Tick")
   # Fill up percentage. Increase after 0.6s
   pc.fill(0.6, ["Show before 50", "Show after 50"])

