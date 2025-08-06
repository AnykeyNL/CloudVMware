import json

# Load data from aws_evs_pricing.json
with open('aws_evs_pricing.json', 'r') as file:
    data = json.load(file)

# HTML template with modern styling
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS EVS Pricing</title>
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
            color: #ff9900;
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
            background-color: #ff9900;
            color: white;
        }}
        .region-code {{
            font-size: 0.8em;
            color: #666;
            font-style: italic;
        }}
        .price {{
            font-weight: bold;
            color: #ff9900;
        }}
        .subscription-model {{
            font-size: 0.9em;
            color: #555;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        tr:hover {{
            background-color: #f0f0f0;
        }}
        .navigation {{
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}
        .navigation h3 {{
            color: #333;
            margin: 0 0 15px 0;
            font-size: 1.2em;
        }}
        .navigation a {{
            color: #ff9900;
            text-decoration: none;
            padding: 5px 10px;
            margin: 0 5px;
            border-radius: 4px;
            transition: background-color 0.2s;
        }}
        .navigation a:hover {{
            background-color: #ff9900;
            color: white;
        }}
        .nav-section {{
            margin: 10px 0;
        }}
        .nav-section strong {{
            color: #333;
            margin-right: 10px;
        }}
    </style>
</head>
<body>
    <h1>AWS Elastic VMware Service (EVS)</h1>
    <h2>Pricing per Node per Month</h2>
    
    <div class="navigation">
        <h3>Navigation</h3>
        <div class="nav-section">
            <strong>AWS:</strong> 
            <a href="aws_evs_pricing.html">EVS Pricing</a>
        </div>
        <div class="nav-section">
            <strong>Azure:</strong> 
            <a href="../Azure/index.html">AVS (USD)</a> | 
            <a href="../Azure/index_EUR.html">AVS (EUR)</a> | 
            <a href="../Azure/index_GBP.html">AVS (GBP)</a>
        </div>
    </div>
    
    <table>
        <tr>
            <th>Location</th>
            <th>Region Code</th>
            <th>Instance Type</th>
            <th>Subscription Model</th>
            <th>Price per Month (USD)</th>
        </tr>
        {rows}
    </table>
</body>
</html>
'''

# Generate table rows
rows = ''
for entry in data:
    location = entry['Location']
    region_code = entry['RegionCode']
    instance_type = entry['InstanceType']
    subscription_model = entry['SubscriptionModel']
    price_per_unit = entry['PricePerUnit']
    
    # Calculate monthly price based on 730 hours
    monthly_price = float(price_per_unit) * 730
    
    # Format the price to show as currency
    price_formatted = f"${monthly_price:,.2f}"
    
    row = f'''
        <tr>
            <td>{location}</td>
            <td class="region-code">{region_code}</td>
            <td>{instance_type}</td>
            <td class="subscription-model">{subscription_model}</td>
            <td class="price">{price_formatted}</td>
        </tr>
    '''
    rows += row

# Write the HTML file
with open('aws_evs_pricing.html', 'w') as file:
    file.write(html_template.format(rows=rows))

print("HTML page created as aws_evs_pricing.html") 