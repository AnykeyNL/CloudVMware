import requests
import json

url = "https://prices.azure.com:443/api/retail/prices?api-version=2023-01-01-preview&meterRegion=%27primary%27&$filter=productName eq 'Specialized Compute Azure VMware Solution'"
currencies = ["USD", "EUR", "GBP"]


# Fetch data from the Azure pricing API
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

# Process the data to extract location and SKU information
def process_data(data):
    location_sku_map = {}
    for item in data.get('Items', []):
        location = item.get('location')
        sku_name = item.get('skuName')
        # Set reservationTerm to 'hourly' if it is null
        reservationTerm = item.get('reservationTerm') or 'hourly'
        retailPrice = item.get('retailPrice')
        
        # Ignore any sku_name with the word 'trial'
        if 'trial' in sku_name.lower():
            continue

        # Ignore the location 'global'
        if location.lower() == 'global':
            continue

        # Append armRegionName to the location name, separated by a newline
        armRegionName = item.get('armRegionName')
        location = f'{location}<br>{armRegionName}'

        if location not in location_sku_map:
            location_sku_map[location] = set()
        # Use tuples instead of lists for set elements
        location_sku_map[location].add((sku_name, reservationTerm, retailPrice))
    # Convert sets to lists for JSON serialization
    for location in location_sku_map:
        location_sku_map[location] = list(location_sku_map[location])
    return location_sku_map

# Main function to fetch and process data
def main():
    # Create a separate data.json file for each currency
    for currency in currencies:
        currency_url = url + f"&currencyCode='{currency}'"
        data = fetch_data(currency_url)
        location_sku_map = process_data(data)
        with open(f'data_{currency}.json', 'w') as f:
            json.dump(location_sku_map, f, indent=4)

if __name__ == "__main__":
    main()

