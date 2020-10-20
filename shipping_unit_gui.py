import sys
import csv
import ezgmail
import PySimpleGUI as sg
from Shipments import Shipment


def save_new_shipment():
    sg.change_look_and_feel("DarkBlue")

    layout = [
        [sg.Text("Please enter the shipment details")],
        [sg.Text("Client", size=(15, 1)), sg.InputText(key="Client")],
        [sg.Text("Width", size=(15, 1)), sg.InputText(key="Width")],
        [sg.Text("Length", size=(15, 1)), sg.InputText(key="Length")],
        [sg.Text("Height", size=(15, 1)), sg.InputText(key="Height")],
        [sg.Text("Gross Weight", size=(15, 1)), sg.InputText(key="Gross Weight")],
        [sg.Text("Purpose", size=(15, 1)), sg.InputText(key="Purpose")],
        [sg.Submit(), sg.Cancel()],
    ]

    window = sg.Window("Shipment Details", layout)
    event, values = window.read()

    if event is None:
        sys.exit()

    new_shipment = Shipment(
        values["Client"],
        values["Width"],
        values["Length"],
        values["Height"],
        values["Gross Weight"],
        values["Purpose"],
    )

    return new_shipment.add_shipment()


def view_shipments():
    result = Shipment.fetch_all_records()
    result = [list(x) for x in result]
    headings = [
        "Client",
        "Width",
        "Length",
        "Height",
        "Gross Weight",
        "Purpose",
        "On-hand",
        "Create Date",
        "Release Status",
        "HAWB",
        "MAWB",
    ]

    sg.change_look_and_feel("DarkBlue")

    layout = [
        [
            sg.Table(
                values=result,
                headings=headings,
                key="table",
                auto_size_columns=True,
                background_color="grey",
                alternating_row_color="DarkBlue",
                tooltip="Select a shipment. Hold CTRL to select multiple.",
            )
        ],
        [
            sg.Cancel(),
            sg.Button("Release", key="release"),
            sg.Button("Delete", key="delete"),
        ],
    ]

    window = sg.Window("Shipments", layout, resizable=True)
    event, values = window.read()

    window.close()

    if event is None:
        sys.exit()

    if event == "release":
        if values["table"]:
            units = []
            for i in values["table"]:
                units.append(Shipment(*result[i]))
            on_hands = [units[i].on_hand_number for i in range(len(units))]

            layout_confirm = [
                [
                    sg.Text(
                        f"Please confirm you want to\
                 release the following shipments: {on_hands}"
                    )
                ],
                [sg.Button("Yes", key="yes")],
                [sg.Button("No", key="no")],
            ]

            win = sg.Window("Confirm", layout_confirm)
            ev2, _ = win.read()
            if ev2 == "yes":
                release_selected_shipments(units)
                return print(f"Shipments {on_hands} released!")
            else:
                return view_shipments()

    if event == "delete":
        if values["table"]:
            units = []
            for i in values["table"]:
                units.append(Shipment(*result[i]))
            on_hands = [units[i].on_hand_number for i in range(len(units))]

            layout_confirm = [
                [
                    sg.Text(
                        f"Please confirm you want to\
                 delete the following shipments: {on_hands}"
                    )
                ],
                [sg.Button("Yes", key="yes")],
                [sg.Button("No", key="no")],
            ]

            win3 = sg.Window("Confirm", layout_confirm)
            ev3, _ = win3.read()
            if ev3 == "yes":
                delete_selected_shipments(units)
                return print(f"Shipments {on_hands} deleted!")
            else:
                return view_shipments()


def release_selected_shipments(values):
    for unit in values:
        unit.release_shipment()
    return print(f"Shipments {values} released")


def update_a_shipment(onhand):
    unit = Shipment.find_one_record(onhand)
    layout = [
        [sg.Text(f"Shipment: {unit.on_hand_number}", font=("Comic", 25))],
        [
            sg.Text("Client:", font=("Comic", 15)),
            sg.InputText(f"{unit.client}", key="client"),
        ],
        [
            sg.Text("Width:", font=("Comic", 15)),
            sg.InputText(f"{unit.width}", key="width"),
        ],
        [
            sg.Text("Length:", font=("Comic", 15)),
            sg.InputText(f"{unit.length}", key="length"),
        ],
        [
            sg.Text("Height:", font=("Comic", 15)),
            sg.InputText(f"{unit.height}", key="height"),
        ],
        [
            sg.Text("Gross Weight:", font=("Comic", 15)),
            sg.InputText(f"{unit.gross_weight}", key="gw"),
        ],
        [
            sg.Text("Purpose:", font=("Comic", 15)),
            sg.InputText(f"{unit.purpose}", key="purpose"),
        ],
        [sg.Text(f"Create Date: {unit.create_date}", font=("Comic", 15))],
        [sg.Text(f"Release Date: {unit.release_date}", font=("Comic", 15))],
        [sg.Button("Update", key="update"), sg.Cancel()],
    ]

    sg.change_look_and_feel("DarkBlue")

    window = sg.Window(
        f"Update Shipment: {unit.on_hand_number}", layout, resizable=True
    )
    event, values = window.read()
    window.close()

    if event == "update":
        unit.update_shipment(*values.values())
        return f"Shipment {unit.on_hand_number} updated!"


def delete_selected_shipments(values):
    for unit in values:
        unit.delete_shipment()
    return None


def lookup_a_shipment(onhand):
    unit = Shipment.find_one_record(onhand)
    layout = [
        [sg.Text(f"Shipment: {unit.on_hand_number}", font=("Comic", 25))],
        [sg.Text(f"Client: {unit.client}", font=("Comic", 15))],
        [sg.Text(f"Dimensions: {unit.volume_weight()} kg/vol", font=("Comic", 15))],
        [sg.Text(f"Gross Weight: {unit.lbs_to_kg()} kg", font=("Comic", 15))],
        [sg.Text(f"Purpose: {unit.purpose}", font=("Comic", 15))],
        [sg.Text(f"Create Date: {unit.create_date}", font=("Comic", 15))],
        [sg.Text(f"Release Date: {unit.release_date}", font=("Comic", 15))],
        [sg.Button("Update", key="update"), sg.Button("Release", key="release")],
        [sg.Button("View Shipments", key="view")],
    ]

    sg.change_look_and_feel("DarkBlue")

    window = sg.Window(f"Shipment {unit.on_hand_number}", layout, resizable=True)
    event, _ = window.read()

    window.close()

    if event == "update":
        return update_a_shipment(unit.on_hand_number)
    elif event == "release":
        return unit.release_shipment()
    elif event == "view":
        return view_shipments()


def export_to_csv():
    layout = [
        [sg.CalendarButton("from date", key="from")],
        [sg.CalendarButton("to date", key="to")],
        [sg.Cancel("Cancel"), sg.Submit("Submit")],
    ]

    window = sg.Window("Select Dates", layout, resizable=True)
    _, values = window.read()
    from_date = values["from"]
    to_date = values["to"]
    window.close()

    if not (from_date and to_date):
        sys.exit()
    else:
        from_date = values["from"].strftime("%Y-%m-%d")
        to_date = values["to"].strftime("%Y-%m-%d")

    results = Shipment.fetch_all_records_in_date(from_date, to_date)

    with open(f"{from_date} to {to_date} consol.csv", "w", newline="") as csvfile:
        r = csv.writer(csvfile, delimiter=",")
        headings = [
            "Client",
            "Width",
            "Length",
            "Height",
            "Gross Weight",
            "Purpose",
            "On-hand",
            "Create Date",
            "Release Status",
            "HAWB",
            "MAWB",
        ]
        r.writerow(headings)
        for i in range(len(results)):
            r.writerow(results[i])


def consolidation():
    result = Shipment.view_all_units_inhouse()
    result = [list(x) for x in result]
    headings = [
        "Client",
        "Width",
        "Length",
        "Height",
        "Gross Weight",
        "Purpose",
        "On-hand",
        "Create Date",
        "Release Status",
        "HAWB",
        "MAWB",
    ]

    sg.change_look_and_feel("DarkBlue")

    layout = [
        [
            sg.Table(
                values=result,
                headings=headings,
                key="table",
                auto_size_columns=True,
                alternating_row_color="gray",
            )
        ],
        [sg.Text("Enter MAWB"), sg.InputText("MAWB", key="mawb")],
        [sg.Text("Enter HAWB"), sg.InputText("HAWB", key="hawb")],
        [
            sg.Cancel(),
            sg.Button("Consol", key="consol"),
            sg.Button("Delete", key="delete"),
        ],
    ]

    window = sg.Window("Shipments", layout, resizable=True)
    event, values = window.read()

    window.close()

    if event is None:
        view_shipments()
    if event == "consol":
        for unit in result:
            shipping_unit = Shipment(*unit)
            shipping_unit.release_shipment(values["mawb"], values["hawb"])
    # assign on-hands a MAWB number (or consol date),
    # total weight and shipping unit count.
    # send email to respective parties.


def report():
    # need to flesh out
    layout = [
        [sg.CalendarButton("from date", key="from")],
        [sg.CalendarButton("to date", key="to")],
        [sg.Cancel("Cancel"), sg.Submit("Submit")],
    ]

    window = sg.Window("Select Dates", layout, resizable=True)
    event, values = window.read()
    from_date = values["from"]
    to_date = values["to"]
    window.close()

    if not (from_date and to_date):
        sys.exit()
    else:
        from_date = values["from"].strftime("%Y-%m-%d")
        to_date = values["to"].strftime("%Y-%m-%d")

    results = Shipment.fetch_all_records_in_date(from_date, to_date)

    ezgmail.init()
    ezgmail.send("lpennicott3@gmail.com", "Shipping Unit Program!", str(results[0]))

