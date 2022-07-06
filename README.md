# Simple Invoice

This is a simple invoicing command line utility written in Python using Jinja2 for the HTML templating and WeasyPrint for the HTML > PDF conversion.
I use this for all of my current invoicing needs.

## How to use

1. Configure your details in conf.json
2. Add clients to clients.json
3. Run the program
4. The items query will repeat until it receives a null entry
5. Your first invoice will have the name YYYYMMDD1.pdf

## Customisation

You can edit the HTML and CSS template to suit your needs.
