import PySimpleGUI as sg
import shipping_unit_gui

# Main window to stay active for duration of the program.
# Other options occur in Multi-window.
# Add ability to add comments to shipping units
# another database table for MAWB consols

layout = [
           [
                sg.Text('Shipping Unit Program!',
                    size=(30, 1), font=('Comic', 25))],
           [sg.Text('Please select an option below or search for a shipment',
                    size=(30, 2), font=('Comic', 15))],
           [sg.Text('Search with on-hand number', size=(25, 1)),
            sg.InputText(key='search on-hand')],
            [
                sg.Button('Add Shipment', key='save_new'),
                sg.Button('View Shipments', key='view'),
                sg.Button('Export', key='export'),
                sg.Button('Search', key='search'),
                sg.Button('Consolidation', key='consol'),
                sg.Button('Report', key='report'),
            ],
    [sg.Cancel()]
]

sg.change_look_and_feel('DarkBlue')

window = (sg.Window('Main Menu', layout, resizable=True))
event, values = window.read()

window.close()

if event == 'save_new':
    shipping_unit_gui.save_new_shipment()
elif event == 'view':
    shipping_unit_gui.view_shipments()
elif event == 'search':
    try:
        shipping_unit_gui.lookup_a_shipment(values['search on-hand'])
    except:
        layout2 = [
                    [sg.Text('Shipping Unit not found! Click below to view shipments.')],
                    [sg.Submit()]
                ]
        sg.change_look_and_feel('DarkBlue')

        window2 = (sg.Window('Shipment not found!', layout2))
        event, values = window2.read()
        window2.close()
        shipping_unit_gui.view_shipments()
elif event == 'export':
    shipping_unit_gui.export_to_csv()
elif event == 'report':
    shipping_unit_gui.report()
elif event == 'consol':
    shipping_unit_gui.consolidation()
