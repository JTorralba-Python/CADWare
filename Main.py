#!/usr/bin/env python

import os
from Tkinter import *
import ttk
import tkFont

import random
import string

def Clear():

    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class _Geometry(object):

    def __init__(self, X, Y):

        self.X = X
        self.Y = Y
        self.XY = str(X) + 'x' + str(Y)
        self.Menu_Y = 24
        self.Status_Y = 24
        self.Canvas_Y = Y - self.Menu_Y - self.Status_Y

class _Mock(object):

    def __init__(self, Rows, Columns, Slave):

        self.Header = []
        self.Data = []

        Rows = Rows + 1

        for Row_Index in range(Rows):

            Record = []

            if Row_Index is 0:
                Value = 'id'
            else:
                Value = Row_Index

            Record.append(Value)

            for Column_Index in range(Columns):

                if Column_Index is not 0:
                    if Row_Index is not 0:
                        if (Column_Index is 1) and (Slave is True):
                            Value = random.randint(int(Sample_Size * .05) , int(Sample_Size * .95))
                        else:
                            if (Column_Index is not (Columns - 1)) and (Column_Index % 3 is not 0):
                                Value = Random(5, 25)
                            else:
                                Value = round(random.uniform(100, 1000),2)
                    else:
                        if (Column_Index is 1) and (Slave is True):
                            Value = 'key'
                        else:
                            Value = 'field' + str(Column_Index + 1)

                    Record.append(Value)

            if Row_Index is 0:
                self.Header = Record
            else:
                self.Data.append(tuple(Record))

class _Frame(object):

    def __init__(self, X, Y, Fill, Expand, Color):

        self.X = X
        self.Y = Y
        self.Fill = Fill
        self.Expand = Expand
        self.Color = Color

        ttk.Style().configure(Color + 'Background.TFrame', background = Color)

        self.Frame = ttk.Frame(width = X, height = Y, style = Color + 'Background.TFrame', relief = FLAT)
        self.Frame.pack(fill = Fill, expand = Expand)

class _Tree(object):

    def __init__(self, Frame, Frame_Y, Header, Data, Upper):

        self.Header = Header
        self.Data = Data
        self.Upper = Upper

        SBH = Scrollbar(Frame, orient = HORIZONTAL)
        SBH.pack(side = BOTTOM, fill = X)

        SBV = Scrollbar(Frame, orient = VERTICAL)
        SBV.pack(side = RIGHT, fill = Y)

        Max_Tree_Rows = int(round(Frame_Y / Font_LineSpace))

        ttk.Style().configure("Treeview.Heading",
            foreground = 'Black',
            #font = ('', 12)
            )

        self.Tree = ttk.Treeview(Frame, columns = self.Header, show = 'headings', height = Max_Tree_Rows, xscrollcommand = SBH.set, yscrollcommand = SBV.set)
        self.Tree.bind("<Button-3>", self._Right)
        self.Tree.pack(expand = TRUE, fill = BOTH, side = LEFT)

        SBH.config(command = self.Tree.xview)
        SBV.config(command = self.Tree.yview)

        for Column in self.Header:

            self.Tree.heading(Column, text = Column.upper(), command = lambda Column = Column: Sort(self.Tree, Column, 0))

            # Adjust the column's width to the header string.
            self.Tree.column(Column, width = tkFont.Font().measure(Column.title()) + 8)

        self.Tree.tag_configure('Odd', background = 'LightBlue')
        self.Tree.tag_configure('Even', background = 'White')

        self._Insert()

    def _Insert(self):

        Row_Index = 'I000'

        for Row in self.Data:

            if self.Upper is True:
                Row_Upper = []

                for Value in Row:
                    if type(Value) is str:
                        Row_Upper.append(str(Value).upper())
                    else:
                        Row_Upper.append(Value)

                Row = tuple(Row_Upper)

            Row_Index = self.Tree.insert('', 'end', values=Row, tags=(Parity(Row_Index),))

            # Adjust column's width to fit each cell value.
            for Column_Index, Value in enumerate(Row):
                Column_X = tkFont.Font().measure(Value) + 8
                if self.Tree.column(self.Header[Column_Index], width=None) < Column_X:
                    self.Tree.column(self.Header[Column_Index], width=Column_X)

    def _Right(self, event):

        Region = self.Tree.identify_region(event.x, event.y)

        if Region == 'heading':
            Column_Index = int(self.Tree.identify_column(event.x)[1:]) - 1
            Data = sorted(self.Data, key=lambda x: (Numeric(x[Column_Index])))
            self.Data = Data
            Data = None
            self.Tree.delete(*self.Tree.get_children())
            self._Insert()

        if Region == 'cell':
            Row_Index = self.Tree.identify_row(event.y)
            #print(Row_Index)
            self.Tree.selection_remove(Row_Index)
            if len(self.Tree.selection()) == 0:
                #print('EMPTY')
                pass
            else:
                #print('REFRESH')
                pass

def Random(Min_Length, Max_Length):

    Value = String(random.randint(Min_Length, Max_Length))

    Letter = String(1)
    Value = Value.replace(Letter, Letter.upper())

    Letter = String(1)
    Value = Value.replace(Letter, str(random.randint(0, 9)))

    return Value

def String(Length):

    return ''.join(random.choice(string.lowercase) for I in range(Length))

def Parity(String):

    if String [-1:] in '02468ACE':
        return 'Even'
    else:
        return 'Odd'

def Sort(Tree, Column, Direction):

    # Fetch values to sort.
    Data = [(Numeric(Tree.set(Child, Column)), Child) for Child in Tree.get_children('')]

    # Sort data in place.
    Data.sort(reverse = Direction)

    for Index, Item in enumerate(Data):
        Tree.move(Item[1], '', Index)
        Tree.item(Item[1], tags = (Parity(str(Index))))

    # Switch header so it will sort in the opposite direction.
    Tree.heading(Column, command = lambda Column = Column: Sort(Tree, Column, int(not Direction)))

    # Remove selections.
    #Selection = Tree.selection()
    #for Row_Index in Selection:
        #Tree.focus(Row_Index)
        # Tree.selection_remove(Row_Index)
        # pass

    Focus = Tree.focus()
    print(Focus)
    Tree.see(Focus)

def Numeric(String):

    try:
        return float(String)
    except ValueError:
        return String.lower()

def Main():

    global Font_LineSpace
    global Sample_Size

    Geometry = _Geometry(1024, 768)

    root = Tk()
    root.title("CADWare 1.0")
    root.geometry(Geometry.XY)

    # If minimum size is set, and will disable OS sticky edge.
    #root.minsize(Geometry.X, Geometry.Y)
    #root.resizable(0,0)

    Font = tkFont.Font(root = root, family = 'Helvetica', size = 14)
    Font_LineSpace = Font.metrics('linespace')

    Menu = _Frame(Geometry.X, Geometry.Menu_Y, BOTH, FALSE, 'LightGray')
    Canvas = _Frame(Geometry.X, Geometry.Canvas_Y, BOTH, TRUE, 'LightBlue')
    Status = _Frame(Geometry.X, Geometry.Status_Y, BOTH, FALSE, 'LightGreen')

    Pane_Data = PanedWindow(Canvas.Frame, orient = VERTICAL, background = 'LightBlue', showhandle = FALSE, handlepad = 0, handlesize = 0, sashwidth = 2, opaqueresize = 0)
    Pane_Data.pack(side = LEFT, fill = BOTH, expand = TRUE)

    Master_Y = int(round(Canvas.Y * .50))
    Slave_Y = int(Canvas.Y - Master_Y)

    Master = _Frame(Canvas.X, Master_Y, BOTH, TRUE, 'Red')
    Slave = _Frame(Canvas.X, Slave_Y, BOTH, FALSE, 'Pink')

    Pane_Data.add(Master.Frame)
    Pane_Data.add(Slave.Frame)

    Sample_Size = 100

    Master_Sample = _Mock(Sample_Size, 5, False)
    Slave_Sample = _Mock(Sample_Size * 5, 4, True)

    Master = _Tree(Master.Frame, Master.Y, Master_Sample.Header, Master_Sample.Data, False)
    Slave = _Tree(Slave.Frame, Slave.Y, Slave_Sample.Header, Slave_Sample.Data, True)

    root.mainloop()

if __name__ == '__main__':
    Clear()
    Main()