import requests
import json
import time

BASE_URLS = {
    'auth': 'http://localhost:8001',
    'listings': 'http://localhost:8002',
    'messaging': 'http://localhost:8003'
}

def test_auth_service():
    print("Testing Authentication Service...")
    
    # Test registration
    user_data = {
        "email": "test@ncsu.edu",
        "username": "testuser",
        "password": "testpass123",
        "full_name": "Test User"
    }
    
    response = requests.post(f"{BASE_URLS['auth']}/v1/auth/register", json=user_data)
    print(f"Register: {response.status_code} - {response.json()}")
    
    # Test login
    login_data = {
        "email": "test@ncsu.edu",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URLS['auth']}/v1/auth/login", json=login_data)
    if response.status_code == 200:
        token = response.json()['access_token']
        print(f"Login successful! Token: {token[:20]}...")
        return token
    else:
        print(f"Login failed: {response.status_code} - {response.json()}")
        return None

def test_listings_service(token):
    print("\nTesting Listings Service...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a listing
    listing_data = {
        "title": "Calculus Textbook",
        "description": "Used calculus textbook in good condition",
        "price": 50.00,
        "category": "textbooks",
        "location": "NCSU Campus"
    }
    
    response = requests.post(f"{BASE_URLS['listings']}/v1/listings/", 
                           json=listing_data, headers=headers)
    print(f"Create Listing: {response.status_code}")
    
    if response.status_code == 200:
        listing_id = response.json()['id']
        print(f"Listing created with ID: {listing_id}")
        
        # Get all listings
        response = requests.get(f"{BASE_URLS['listings']}/v1/listings/")
        print(f"Get Listings: {response.status_code} - Found {len(response.json())} listings")
        
        return listing_id
    
    return None

def test_messaging_service(token, listing_id):
    print("\nTesting Messaging Service...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create conversation (this will fail if trying to message own listing, but that's expected)
    conversation_data = {
        "listing_id": listing_id
    }
    
    response = requests.post(f"{BASE_URLS['messaging']}/v1/conversations/", 
                           json=conversation_data, headers=headers)
    print(f"Create Conversation: {response.status_code}")
    
    # Get conversations
    response = requests.get(f"{BASE_URLS['messaging']}/v1/conversations/", headers=headers)
    print(f"Get Conversations: {response.status_code}")

def main():
    print("Starting API Tests...")
    time.sleep(2)  # Wait for services to be ready
    
    token = test_auth_service()
    if token:
        listing_id = test_listings_service(token)
        if listing_id:
            test_messaging_service(token, listing_id)
    
    print("\nTests completed!")

if __name__ == "__main__":
    main()
