# Started - 23/11/2020
# Completed - 09/12/2020
# @author : OMAR REHAN MOMIN

from tkinter import *
from tkinter import ttk
from PIL     import ImageTk, Image
import sqlite3 as s

root = Tk()

root.title( 'bday bday bday !!!' )
root.iconbitmap( 'cake_icon.ico' )

bg_color     = 'snow'
root[ 'bg' ] = bg_color


#  MAIN-LABEL------------------------------------------------------------------------------
heading_image = ImageTk.PhotoImage( Image.open( 'kake.ico' ))

birthday_label = Label( root, text = 'Birthdays', bg = bg_color, fg = 'lightcoral', font = ( 'forte', 45 ))
birthday_label.pack( fill = BOTH, expand = True )

birthday_label[ 'compound' ] = LEFT
birthday_label[ 'image'    ] = heading_image


#  STYLING-WIDGETS-------------------------------------------------------------------------
style = ttk.Style()

style.theme_create( 'tabs_and_treeview', settings = {
    "." : {
        "configure" : {
            "background" : bg_color,
            "font" : 'crystal' }
        },
    "TNotebook" : {
        "configure" : {
            "background" : bg_color,
            "tabmargins" : [ 2, 5, 0, 0 ] }
        },
    "TNotebook.Tab" : {
        "configure" : {
            "background" : 'lightpink',
            "padding" : [ 4, 2 ], 
            "font" : [ "consolas", 11 ] },
        "map" : {
            "foreground" : [ ( "selected", 'black') ],
            "background" : [ ( "selected", bg_color ) ],
            "expand" : [ ( "selected", [ 1, 1, 1, 0 ] ) ] }
        },
    "Treeview" : {
        "configure" : {
            "background" : "lightpink",
            "foreground" : "black",
            "font" : [ "crystal", 12 ],
            "rowheight"  : 20,
            "fieldbackground" : "lightpink" },
        "map" : {
            "background" : [ ( "selected", "crimson" ) ] },
        "layout" : [
            ( "Treeview.treearea", { "sticky" : "nswe" } ) ]
        },
    "Treeview.Heading" : {
        "configure" : {
            "background" : "mistyrose",
            "foreground" : "black",
            "font" : [ "crystal", 12 ] }
        }
    } )
 
style.theme_use( 'tabs_and_treeview' )


#  CONNECTING-AND-CREATING-SQLITE-DATABASE-------------------------------------------------
conn = s.connect( 'birthdays.db' )
c    = conn.cursor()

'''c.execute('drop table if exists birthday')'''
c.execute(' create table if not exists birthday (name text, date integer, month text)')


#  FUNCTIONS-------------------------------------------------------------------------------
def search() :
    conn = s.connect( 'birthdays.db' )
    c    = conn.cursor()

    c.execute( ' select * from birthday where name like ? or month like ?',
               ( f'{search_entry.get()}%', f'{search_entry.get()}%', ) )

    for items in tree.get_children() :
        tree.delete( items )
    
    records = c.fetchall()
    for rec in records :
        tree.insert( parent = '', index = 'end', text = '',
                     values = ( rec[ 0 ], rec[ 1 ], rec[ 2 ] ))

    search_entry.delete( 0, END )
    
    conn.commit()
    conn.close()
    

def record_add() :
    conn = s.connect( 'birthdays.db' )
    c    = conn.cursor()

    c.execute('insert into birthday values( :name, :date, :month)',
              { 'name'  : enter_name. get(),
                'date'  : enter_date. get(),
                'month' : enter_month.get() } )

    for items in tree.get_children() :
        tree.delete( items )

    tree.insert( parent = '', index = 'end', text = '',
                     values = ( enter_name.get(), enter_date.get(), enter_month.get() ))
        
    clear_edit_tab()
    
    conn.commit()
    conn.close()

def record_select() :
    clear_edit_tab()

    selected = tree.focus()
    values   = tree.item( selected, 'values')

    enter_name. insert( 0, values[ 0 ] )
    enter_date. insert( 0, values[ 1 ] )
    enter_month.insert( 0, values[ 2 ] )

def record_remove() :
    conn = s.connect( 'birthdays.db' )
    c    = conn.cursor()
    
    c.execute('delete from birthday where name = ?', ( enter_name.get(), ))

    for record in tree.selection() :
        tree.delete( record )

    clear_edit_tab()
 
    conn.commit()
    conn.close()
    
def record_update():
    conn = s.connect( 'birthdays.db' )
    c    = conn.cursor()
    
    c.execute('update birthday set date = ?, month = ? where name = ?',
              ( enter_date.get(), enter_month.get(), enter_name.get(), ))
    
    selected = tree.focus()
    tree.item( selected, text = '', values = ( enter_name.get(), enter_date.get(), enter_month.get() ))

    clear_edit_tab()
    
    conn.commit()
    conn.close()
    
def clear_edit_tab() :
    enter_name. delete( 0, END )
    enter_date. delete( 0, END )
    enter_month.delete( 0, END )


#  SETTING-UP-TREEVIEW---------------------------------------------------------------------
treeframe = Frame( root, width = 200, height = 100, bg = bg_color )
treeframe.pack( pady = 10 )

scroll = Scrollbar( treeframe )
scroll.pack( side = RIGHT, fill = Y )

tree = ttk.Treeview( treeframe, yscrollcommand = scroll.set ) 
tree.pack( pady = 20 )

scroll.config( command = tree.yview )

tree[ 'columns' ] = ( 'name', 'date', 'month' )

tree.column( '#0',    width = 0,   stretch = NO ) 
tree.column( 'name',  width = 140 ) 
tree.column( 'date',  width = 100, anchor = CENTER ) 
tree.column( 'month', width = 140, anchor = W ) 

tree.heading( '#0',    text = '',      anchor = W )
tree.heading( 'name',  text = 'Name',  anchor = W )
tree.heading( 'date',  text = 'Date',  anchor = CENTER )
tree.heading( 'month', text = 'Month', anchor = W )


#  TABS------------------------------------------------------------------------------------
tabs = ttk.Notebook( root )
tabs.pack( fill = BOTH, expand = True )

tab1 = Frame( tabs, width = 200, height = 100, bg = bg_color )
tab2 = Frame( tabs, width = 200, height = 100, bg = bg_color )

tab1.pack( fill = 'both', expand = True )
tab2.pack( fill = 'both', expand = True )

tabs.add( tab1, text = 'Search' ) 
tabs.add( tab2, text = 'Edit'   ) 


#  WIDGETS-TAB1----------------------------------------------------------------------------
search_label = Label ( tab1, text = 'Search Name / Month', bg = bg_color, fg = 'black', font = ( 'consolas', 11 ))
search_entry = Entry ( tab1, bg = 'lightpink', font = ( 'consolas', 11 ) )
search_enter = Button( tab1, text = 'Enter' , bg = bg_color, fg = 'black', font = ( 'consolas', 11 ), command = search )

search_label.grid( row = 1, column = 0, pady = 15, padx = 20 )
search_entry.grid( row = 1, column = 1, pady = 15 )
search_enter.grid( row = 1, column = 2, pady = 15, padx = 20 )


#  WIDGETS-TAB2----------------------------------------------------------------------------
select_button = Button( tab2, text = 'Select Record', bg = bg_color, fg = 'black',
            font = ( 'consolas', 11 ), command = record_select )

add_name_label  = Label( tab2, text = 'Name',  bg = bg_color, fg = 'black', font = ( 'consolas', 12 ) )
add_date_label  = Label( tab2, text = 'Date',  bg = bg_color, fg = 'black', font = ( 'consolas', 12 ) )
add_month_label = Label( tab2, text = 'Month', bg = bg_color, fg = 'black', font = ( 'consolas', 12 ) )

enter_name  = Entry( tab2, bg = 'lightpink', font = ( 'consolas', 11 ) )
enter_date  = Entry( tab2, bg = 'lightpink', font = ( 'consolas', 11 ) )
enter_month = Entry( tab2, bg = 'lightpink', font = ( 'consolas', 11 ) )

add_button    = Button( tab2, text = 'Add', bg = bg_color, fg = 'black',
            font = ( 'consolas', 11 ) , command = record_add    )
update_button = Button( tab2, text = 'Update Date/Month', bg = bg_color, fg = 'black',
            font = ( 'consolas', 11 ) , command = record_update )
remove_button = Button( tab2, text = 'Remove Selected', bg = bg_color, fg = 'black',
            font = ( 'consolas', 11 ) , command = record_remove )

select_button.grid( row = 0, column = 1, pady = 15)

add_name_label. grid( row = 1, column = 0, padx = ( 20, 0 ), pady = 5 )
add_date_label. grid( row = 1, column = 1, pady = 5 )
add_month_label.grid( row = 1, column = 2, padx = ( 0, 20 ), pady = 5 )

enter_name. grid( row = 2, column = 0, padx = ( 20, 0 ) )
enter_date. grid( row = 2, column = 1 )
enter_month.grid( row = 2, column = 2, padx = ( 0, 20 ) )

add_button.   grid( row = 3, column = 0, pady = 15 )
update_button.grid( row = 3, column = 1, pady = 15 )
remove_button.grid( row = 3, column = 2, pady = 15 )


#----------------------------------------X--X--X------------------------------------------#
conn.commit()
conn.close()

root.mainloop()
