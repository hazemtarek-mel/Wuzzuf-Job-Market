import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def scrape_wuzzuf():
    base_url = "https://wuzzuf.net/search/jobs/"
    queries = ["Data Analyst", "Machine Learning"]
    
    # CSS Classes (extracted from inspection)
    # Note: These might change if Wuzzuf redeploys. 
    # Using more generic structure where possible or these specific hashes.
    CARD_CLASS = "css-ghe2tq" 
    TITLE_CLASS = "css-o171kl" # Inside h2
    COMPANY_CLASS = "css-ipsyv7"
    LOCATION_CLASS = "css-16x61xq"
    
    # Headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    all_jobs = []

    for query in queries:
        print(f"Scraping query: {query}")
        for page in range(5): # Limit to 5 pages per query (approx 75 jobs) -> Total 150 jobs
            params = {
                'q': query,
                'a': 'hpb',
                'start': page
            }
            
            try:
                print(f"  Fetching page {page}...")
                response = requests.get(base_url, params=params, headers=headers, timeout=10)
                if response.status_code != 200:
                    print(f"  Failed to retrieve page {page}: {response.status_code}")
                    break
                
                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('div', class_=CARD_CLASS)
                
                if not job_cards:
                    # Fallback: Try finding h2 and parent divs if main class changed
                    h2s = soup.find_all('h2')
                    if h2s:
                        job_cards = [h2.find_parent('div').find_parent('div') for h2 in h2s]
                    else:
                        print("  No jobs found on this page.")
                        break

                print(f"    Found {len(job_cards)} jobs.")
                
                for card in job_cards:
                    try:
                        # Title
                        h2 = card.find('h2')
                        title = h2.text.strip() if h2 else "N/A"
                        
                        # Company
                        company_tag = card.find('a', class_=COMPANY_CLASS)
                        company = company_tag.text.strip().replace(' -', '') if company_tag else "N/A"
                        
                        # Location
                        location_tag = card.find('span', class_=LOCATION_CLASS)
                        location = location_tag.text.strip() if location_tag else "N/A"
                        
                        # Metadata container (Skills, Type, Level)
                        # The generic structure is: Attributes are in 'a' tags or text in the lower divs
                        # Let's extract all text from the bottom container as "Skills/Details"
                        # We can try to parse specific fields if they are consistent
                        
                        # Extracting filters/tags
                        # Usually in div.css-1rhj4yg
                        # It contains: Type (Full time), Level (Entry Level), Experience (x Yrs), Skills...
                        
                        details_container = card.find('div', class_='css-1rhj4yg') # Use the class seen in debug
                        
                        job_type = "Full Time" # Default/Placeholder
                        level = "N/A"
                        years_exp = "N/A"
                        skills = []
                        
                        if details_container:
                            # Extract all text segments or 'a' tags
                            # The first div.css-5jhz9n usually has Type and Remote/Onsite
                            type_div = details_container.find('div', class_='css-5jhz9n')
                            if type_div:
                                types = [t.text.strip() for t in type_div.find_all('span')]
                                if types: job_type = ", ".join(types)
                            
                            # The rest are in the parent div or a sibling div?
                            # In debug: <div> <a ...>Entry Level</a> <span>...</span> </div>
                            # We can just get all 'a' tags in details_container that are NOT in type_div
                            
                            all_links = details_container.find_all('a')
                            for link in all_links:
                                text = link.text.strip()
                                link_parent = link.parent
                                if link_parent == type_div:
                                    continue
                                
                                # Categorize based on common keywords
                                if "Level" in text:
                                    level = text
                                elif "Yrs" in text:
                                    years_exp = text # might be in span?
                                else:
                                    skills.append(text)
                                    
                            # Check text nodes for "Yrs of Exp" if not in 'a'
                            # In debug: <span> · 2 - 3 Yrs of Exp</span>
                            text_content = details_container.get_text(" | ")
                            if "Yrs of Exp" in text_content:
                                import re
                                match = re.search(r'([0-9\+\-\s]+Yrs of Exp)', text_content)
                                if match:
                                    years_exp = match.group(1)

                        all_jobs.append({
                            "Job Title": title,
                            "Company Name": company,
                            "Location": location,
                            "Job Type": job_type,
                            "Level": level,
                            "Years of Experience": years_exp,
                            "Skills": ", ".join(skills),
                            "Country": "Egypt"
                        })
                        
                    except Exception as e:
                        print(f"Error parsing card: {e}")
                        continue
                
                time.sleep(random.uniform(1, 3)) # Polite delay
                
            except Exception as e:
                print(f"Error fetching page: {e}")
                break

    # Save to CSV
    df = pd.DataFrame(all_jobs)
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Save
    import os
    os.makedirs("data", exist_ok=True)
    output_path = "data/wuzzuf_jobs_raw.csv"
    df.to_csv(output_path, index=False)
    print(f"Scraping complete. Saved {len(df)} jobs to {output_path}")

if __name__ == "__main__":
    scrape_wuzzuf()
