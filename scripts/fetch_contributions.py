# scripts/fetch_contributions.py
import json
import requests
from bs4 import BeautifulSoup

def main():
    username = "Sandeep-al"
    url = f"https://github.com/users/{username}/contributions"
    
    print(f"⏳ Fetching contributions for {username}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch contributions. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    days = soup.find_all('td', class_='ContributionCalendar-day')
    
    contrib_data = []
    
    for day in days:
        date = day.get('data-date')
        level = day.get('data-level', '0')
        
        # Pull text description to grab exact count (e.g., "5 contributions on...")
        sr_text = day.find('span', class_='sr-only')
        count = 0
        if sr_text:
            text = sr_text.text.lower()
            if 'no contributions' not in text:
                try:
                    count = int(text.split()[0])
                except ValueError:
                    count = 0
                    
        if date:
            contrib_data.append({
                "date": date,
                "level": int(level),
                "count": count
            })
            
    # Save raw data to json
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(contrib_data, f, indent=2)
        
    print("✅ Raw contribution metrics saved to 'data/contributions.json'!")

if __name__ == "__main__":
    main()