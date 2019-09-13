import tkinter as tk
from tkinter import Frame, Canvas, Scrollbar, Button

inString = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut eu neque ligula. Quisque et mattis mauris. Fusce eget dui vitae magna laoreet suscipit. Aenean magna arcu, vehicula sit amet efficitur egestas, posuere eget ex. Phasellus laoreet dui id lectus elementum, ac ornare enim tempor. Proin sit amet odio in enim sodales porttitor sit amet a lectus. Quisque ac nisl malesuada, tristique velit a, gravida urna. Maecenas turpis quam, laoreet vel libero quis, consequat faucibus turpis. Sed a congue dolor. Vestibulum luctus lorem et odio maximus scelerisque. Aenean vehicula tortor placerat ligula blandit, vitae venenatis dui tempus. Pellentesque tincidunt at eros sed condimentum. In dolor ex, hendrerit sed accumsan sed, dapibus nec ligula. Aliquam non lorem eget turpis feugiat luctus ut ut velit. Suspendisse a purus eget massa sollicitudin volutpat. Sed condimentum, turpis nec fringilla blandit, dolor urna mollis diam, eu scelerisque sem metus eu enim.
Duis ut justo erat. Maecenas quis nibh at erat finibus vulputate. Sed sit amet hendrerit urna, in laoreet nunc. Proin aliquam metus nec porta euismod. Nam vel tellus sed neque rutrum ornare. Etiam venenatis mi fermentum, porta libero quis, blandit lorem. Sed rutrum purus ex, id sollicitudin sem tristique a. In at nunc eu dui vehicula egestas a sed velit. Phasellus eu rutrum felis, a consectetur nisl. Integer mollis, dui ac tincidunt vehicula, arcu justo pulvinar ante, at interdum massa tortor id ante. Sed eu erat lobortis, mollis dolor vel, ultricies nisl. Vivamus ornare, erat consectetur viverra semper, massa purus aliquet ipsum, ut blandit neque lectus quis augue. In quis varius sapien. Donec imperdiet purus sed metus laoreet efficitur. Vivamus dictum, augue id accumsan posuere, lectus est malesuada nibh, id commodo justo felis quis ipsum.
"""

def onscroll(axis, *args):
    global canvasL, canvasR
    print(f'axis: {axis} and args are {[*args]}                           ',
          end='\r')
    if axis == 'y-axis':
        canvasL.yview(*args)
        canvasR.yview(*args)

    else:
        assert False, f"axis {axis} is incorrect, use 'x-axis' or 'y-axis'"



root = tk.Tk( className = "testingPrototype" )

frameL = Frame( root, bg = 'grey' )
frameR = Frame( root, bg = 'blue' )

frameL.grid( row = 0, column = 0 )
frameR.grid( row = 0, column = 1 )

yScroll = tk.Scrollbar( frameR, orient='vertical',
                           command=lambda *args: onscroll('y-axis', *args) )
yScroll.pack( side = 'right', fill = 'y', expand = 'yes')

canvasL = tk.Text(frameR, width=20, height=20, bg="blue",
                     yscrollcommand=yScroll.set)
canvasL.pack(side='right')
canvasR = tk.Text(frameL, width=20, height=20, bg="yellow",
                     yscrollcommand=yScroll.set)
canvasR.pack()

canvasL.insert( tk.INSERT, inString )
canvasR.insert( tk.INSERT, inString )



root.mainloop()
