from flask import Flask, render_template

app = Flask(__name__)

# Sample data (in a real app, this would come from your database/API)
last_run = "2025-08-05 09:00:00"
last_status = "Success"
tenders_found = 6
total_tenders = 120

sources = [
    {
        "name": "eProcure Government Tenders",
        "url": "https://eprocure.gov.in/cppp/tenders",
        "selectors": {
            "tender": ".tender-list .tender",
            "title": "h3 a",
            "organization": ".org",
            "publish_date": ".publish-date",
            "close_date": ".close-date",
            "opening_date": ".opening-date"
        }
    }
]

tenders = [
  {
    "close_date": "19-Aug-2025 03:00 PM",
    "opening_date": "19-Aug-2025 03:30 PM",
    "organisation_name": "Central Public Works Department (CPWD)",
    "publish_date": "05-Aug-2025 01:04 PM",
    "tender_name": "19/EE/Srinagar of 2025-26",
    "url": "https://eprocure.gov.in/cppp/tendersfullview/MTI5MTIwNzg=A13h1OGQ2NzAxYTMwZTJhNTIxMGNiNmEwM2EzNmNhYWZhODk=A13h1OGQ2NzAxYTMwZTJhNTIxMGNiNmEwM2EzNmNhYWZhODk=A13h1MTc1NDM3OTU5NQ==A13h1MTkvRUUvU3JpbmFnYXIgb2YgMjAyNS0yNg==A13h1MTIyMjAx"
  },
  {
    "close_date": "19-Aug-2025 04:30 PM",
    "opening_date": "19-Aug-2025 04:30 PM",
    "organisation_name": "Department of Biotechnology",
    "publish_date": "05-Aug-2025 01:00 PM",
    "tender_name": "Supply,Installation and Commisioning of goods",
    "url": "https://eprocure.gov.in/cppp/tendersfullview/MTI5MTIwMjM=A13h1OGQ2NzAxYTMwZTJhNTIxMGNiNmEwM2EzNmNhYWZhODk=A13h1OGQ2NzAxYTMwZTJhNTIxMGNiNmEwM2EzNmNhYWZhODk=A13h1MTc1NDM3OTU5NQ==A13h1UkdDQi9QVVIvNTM3LzI1LzUwNA==A13h1MjAyNV9NU1RfODA3OTY0XzE="
  },
  {
    "close_date": "12-Aug-2025 04:00 PM",
    "opening_date": "12-Aug-2025 04:30 PM",
    "organisation_name": "MOIL Limited",
    "publish_date": "05-Aug-2025 01:00 PM",
    "tender_name": "Operation and General Maintaence of Loaders and Tippers at Gumgaon Mine",
    "url": "https://eprocure.gov.in/cppp/tendersfullview/MTI5MTE5MTg=A13h1OGQ2NzAxYTMwZTJhNTIxMGNiNmEwM2EzNmNhYWZhODk=A13h1OGQ2NzAxYTMwZTJhNTIxMGNiNmEwM2EzNmNhYWZhODk=A13h1MTc1NDM3OTU5NQ==A13h1R3VtL01lY2gvMjAyNS0yNi82MDE=A13h1MjAyNV9NT0lMXzgwNzk1MV8x"
  },
  {
    "close_date": "12-Aug-2025 03:00 PM",
    "opening_date": "12-Aug-2025 03:30 PM",
    "organisation_name": "National Rural Roads Development Agency (NRRDA)",
    "publish_date": "05-Aug-2025 01:00 PM",
    "tender_name": "PMKKKY/01/ET/2025-26-NEEMCHAK BATHANI",
    "url": "https://eprocure.gov.in/cppp/tendersfullview/MTI5MTIwMTA=A13h1OGQ2NzAxYTMwZTJhNTIxMGNiNmEwM2EzNmNhYWZhODk=A13h1OGQ2NzAxYTMwZTJhNTIxMGNiNmEwM2EzNmNhYWZhODk=A13h1MTc1NDM3OTU5NQ==A13h1UE1LS0tZLzAxL0VULzIwMjUtMjYtTkVFTUNIQUsgQkFUSEFOSQ==A13h1MjAyNV9FQ0JJSF8xNDM4MTlfMQ=="
  },
  {
    "close_date": "13-Aug-2025 02:00 PM",
    "opening_date": "13-Aug-2025 03:00 PM",
    "organisation_name": "Union Bank of India",
    "publish_date": "05-Aug-2025 01:00 PM",
    "tender_name": "Tender for Furnishing Work at alternate premises of Tehra Branch under UBI RO Agra",
    "url": "https://eprocure.gov.in/cppp/tendersfullview/MTI5MTIwMTc=A13h1OGQ2NzAxYTMwZTJhNTIxMGNiNmEwM2EzNmNhYWZhODk=A13h1OGQ2NzAxYTMwZTJhNTIxMGNiNmEwM2EzNmNhYWZhODk=A13h1MTc1NDM3OTU5NQ==A13h1VGVocmFGdXJuaXNoaW5nV29yaw==A13h1MjAyNV9VQm9JXzgwNzk1N18x"
  },
  {
    "close_date": "11-Aug-2025 03:00 PM",
    "opening_date": "11-Aug-2025 04:30 PM",
    "organisation_name": "MOIL Limited",
    "publish_date": "05-Aug-2025 01:00 PM",
    "tender_name": "Repairing of body and auto electrical work of the Utility Jeep MH36F 0583.",
    "url": "https://eprocure.gov.in/cppp/tendersfullview/MTI5MTIwMjE=A13h1OGQ2NzAxYTMwZTJhNTIxMGNiNmEwM2EzNmNhYWZhODk=A13h1OGQ2NzAxYTMwZTJhNTIxMGNiNmEwM2EzNmNhYWZhODk=A13h1MTc1NDM3OTU5NQ==A13h1Q0gvTUVDSC8yNS0yNi83Ni0zNTQxNy8xNzk4A13h1MjAyNV9NT0lMXzgwNzk2Ml8x"
  }
]

@app.route('/')
def dashboard():
    return render_template('dashboard.html',
                           last_run=last_run,
                           last_status=last_status,
                           tenders_found=tenders_found,
                           total_tenders=total_tenders,
                           sources=sources,
                           tenders=tenders)

if __name__ == '__main__':
    app.run(debug=True)