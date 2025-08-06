import requests
import json

url = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEVS/current/index.json"

def fetch_aws_pricing_data():
    """Fetch pricing data from AWS API"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def extract_pricing_info(data):
    """Extract Location, InstanceType, SubscriptionModel, RegionCode, and price per unit"""
    pricing_info = []
    
    if not data or 'products' not in data or 'terms' not in data:
        print("Invalid data structure")
        return pricing_info
    
    products = data['products']
    terms = data['terms'].get('OnDemand', {})
    
    for sku, product in products.items():
        if 'attributes' not in product:
            continue
            
        attributes = product['attributes']
        
        # Extract basic info from product attributes
        location = attributes.get('location', '')
        instance_type = attributes.get('instanceType', '')
        subscription_model = attributes.get('subscriptionModel', '')
        region_code = attributes.get('regionCode', '')
        
        # Get pricing information from terms
        price_per_unit = None
        if sku in terms:
            term_entries = terms[sku]
            for term_key, term_data in term_entries.items():
                if 'priceDimensions' in term_data:
                    price_dimensions = term_data['priceDimensions']
                    for price_key, price_data in price_dimensions.items():
                        if 'pricePerUnit' in price_data and 'USD' in price_data['pricePerUnit']:
                            price_per_unit = price_data['pricePerUnit']['USD']
                            break
                    if price_per_unit:
                        break
        
        if location and instance_type and subscription_model and price_per_unit:
            pricing_info.append({
                'Location': location,
                'InstanceType': instance_type,
                'SubscriptionModel': subscription_model,
                'RegionCode': region_code,
                'PricePerUnit': price_per_unit
            })
    
    return pricing_info

def save_to_json(data, filename='aws_evs_pricing.json'):
    """Save extracted data to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving file: {e}")

def main():
    print("Fetching AWS EVS pricing data...")
    
    # Fetch data from AWS API
    raw_data = fetch_aws_pricing_data()
    if not raw_data:
        print("Failed to fetch data from AWS API")
        return
    
    # Extract required information
    pricing_info = extract_pricing_info(raw_data)
    
    if not pricing_info:
        print("No pricing information found")
        return
    
    print(f"Found {len(pricing_info)} pricing entries")
    
    # Save to JSON file
    save_to_json(pricing_info)
    
    # Print first few entries as preview
    print("\nPreview of extracted data:")
    for i, entry in enumerate(pricing_info[:3]):
        print(f"{i+1}. {entry}")

if __name__ == "__main__":
    main()

