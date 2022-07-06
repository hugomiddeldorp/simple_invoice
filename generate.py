import json
import datetime
from weasyprint import HTML, CSS
from jinja2 import Template


def selectClient():
    with open("clients.json", "r") as f:
        clients = json.load(f)

    i = 0
    print('\nCLIENTS:')
    for client in clients['clients']:
        print(str(i) + ".", client['firstName'], client['lastName'])
        i += 1
    print()

    while True:
        selection = input("Client Number: ")
        if selection and 0 <= int(selection) <= len(clients["clients"]):
            break

    client = clients["clients"][int(selection)]
    print(client["companyName"])
    return client


def enterDescription():
    entries = []
    i = 1
    while True:
        description = input("Item {}: ".format(str(i)))
        if description == "":
            break
        else:
            i += 1
            entries.append(description)

    return entries


def enterAmount(entries):
    amount_list = []
    for i in range(0, entries):
        amount = float(input("Number of Hours Worked: "))
        amount_list.append(amount)

    return amount_list


def makeTable(entries, amounts, client):
    html = ""

    for i in range(0, len(entries)):
        total = "{:.2f}".format(client["rate"] * amounts[i])
        html += """<tr>
          <td>
          {} 
          </td>
          <td>
           $ {}
          </td>
          <td>
          {}
          </td>
          <td>
           ${}
          </td>
         </tr>""".format(entries[i], client["rate"], amounts[i], total)

    return html


def getTotal(amounts, client):
    total = 0.0

    for amount in amounts:
        total += client["rate"] * amount

    return "{:.2f}".format(total)


def updateHTML(client, entries, amounts):
    print("Writing HTML...")
    with open("conf.json") as f:
        config = json.load(f)
    with open("template.html") as file:
        template = Template(file.read())


    total = getTotal(amounts, client)
    table = makeTable(entries, amounts, client)
    date = datetime.datetime.now()
    full_invoice_number = date.strftime("%Y%m%d") + str(config["invoice_number"])

    with open("invoice.html", 'w') as save_file:
        save_file.write(template.render(client=client,
            config=config,
            invoice_number=full_invoice_number,
            table=table,
            total=total,
            date=date.strftime("%d %B")))

    return full_invoice_number


def generatePDF(invoice_number):
    print("Generating PDF...")
    fn = "inv/" + invoice_number + ".pdf"
    HTML('invoice.html').write_pdf(fn, stylesheets=[CSS('style.css')])

    return fn


def changeInvoiceNumber():
    with open("conf.json", "r+") as f:
        config = json.load(f)
        config["invoice_number"] += 1
        f.seek(0)
        json.dump(config, f, indent=4)


def main():
    client = selectClient()
    entries = enterDescription()
    amounts = enterAmount(len(entries))
    
    invoice_number = updateHTML(client, entries, amounts)
    changeInvoiceNumber()
    
    generatePDF(invoice_number)


if __name__ == "__main__":
    main()
