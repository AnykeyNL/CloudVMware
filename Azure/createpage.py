import json

currencies = ["USD", "EUR", "GBP"]

# Load data from data.json
with open('data.json', 'r') as file:
    data = json.load(file)

# Update the page title and subtitle, and enhance the styling for a modern look
# Escape curly braces in the CSS section
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Azure AVS</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 20px;
        }}
        h1 {{
            text-align: center;
            color: #0052cc;
        }}
        h2 {{
            text-align: center;
            color: #666;
            margin-top: -10px;
        }}
        table {{
            width: 90%;
            border-collapse: collapse;
            margin: 20px auto;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: center;
            vertical-align: top;
        }}
        th {{
            background-color: #0052cc;
            color: white;
        }}
        .available {{
            background-color: #e0f7fa;
            color: #00796b;
        }}
        .unavailable {{
            background-color: #f0f0f0;
            color: #999;
        }}
    </style>
</head>
<body>
    <h1>Azure AVS</h1>
    <h2>Price per Node per Month</h2>
    <table>
        <tr>
            <th>Location</th>
            <th>AV36</th>
            <th>AV36 VCF BYOL</th>
            <th>AV36P</th>
            <th>AV36P VCF BYOL</th>
            <th>AV48</th>
            <th>AV48 VCF BYOL</th>
            <th>AV52</th>
            <th>AV52 VCF BYOL</th>
            <th>AV64</th>
            <th>AV64 VCF BYOL</th>
        </tr>
        {rows}
    </table>
</body>
</html>
'''

# Update the table row generation to handle the new data.json format
rows = ''
# Sort the terms within each cell in the specified order
order = {"hourly": 0, "1 Year": 1, "3 Years": 2, "5 Years": 3}
# Define a mapping of currency codes to symbols
currency_symbols = {
    "USD": "$",
    "EUR": "&euro;",
    "GBP": "&pound;"
}

# Iterate over each currency to create a separate HTML page
for currency in currencies:
    # Load data from the corresponding JSON file
    with open(f'data_{currency}.json', 'r') as file:
        data = json.load(file)

    # Generate the HTML content as before
    rows = ''
    for location in sorted(data.keys()):
        skus = data[location]
        row = f'<tr><td>{location}</td>'
        for sku in ["AV36", "AV36 VCF BYOL", "AV36P", "AV36P VCF BYOL", "AV48", "AV48 VCF BYOL", "AV52", "AV52 VCF BYOL", "AV64", "AV64 VCF BYOL"]: 
            available_terms = [term for term in skus if term[0] == sku]
            available_terms.sort(key=lambda x: order.get(x[1], 4))
            if available_terms:
                adjusted_terms = []
                for term in available_terms:
                    commitment = term[1]
                    price = term[2]
                    if commitment == "hourly":
                        price *= 730
                    elif commitment == "1 Year":
                        price /= 12
                    elif commitment == "3 Years":
                        price /= 36
                    elif commitment == "5 Years":
                        price /= 60
                    adjusted_terms.append((commitment, price))
                # Use the correct currency symbol
                symbol = currency_symbols.get(currency, '$')
                cell_content = f'<b>{sku}</b><br><font size="-2">{location.split("<br>")[1]}</font><br>' + '<br>'.join([f'{term[0]}: {symbol}{int(term[1]):,}' for term in adjusted_terms])
                row += f'<td class="available">{cell_content}</td>'
            else:
                row += f'<td class="unavailable">Not Available</td>'
        row += '</tr>'
        rows += row

    # Add links to all currency pages below the subtitle
    links = ' | '.join([f'<a href="index_{cur}.html">{cur}</a>' for cur in currencies])

    # Write the HTML to a currency-specific file
    with open(f'index_{currency}.html', 'w') as file:
        file.write(html_template.format(rows=rows).replace('</h2>', f'</h2><div style="text-align: center;">{links}</div>'))

    print(f"HTML page created as index_{currency}.html")
