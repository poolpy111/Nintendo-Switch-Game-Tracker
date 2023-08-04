import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext

def extract_data():
    global items
    res = requests.get('https://rutracker.net/forum/tracker.php', params=params, cookies=cookies, headers=headers)
    html = BeautifulSoup(res.text, 'html.parser')

    for row in html.find_all('tr', class_='tCenter hl-tr'):
        title_div = row.find('div', class_='wbr t-title')
        seed_number_tag = row.find('b', class_='seedmed')

        if title_div:
            title_link = title_div.find('a', class_='med tLink tt-text ts-text hl-tags bold')
            seed_number = seed_number_tag.text if seed_number_tag else None

            if title_link:
                title_text = title_link.text.replace('[Nintendo Switch]', '').strip()
                href_url = "https://rutracker.net/forum/" + title_link['href']
                items.append((title_text, int(seed_number), href_url))

    display_items(items)

def display_items(item_list):
    result_text.delete(1.0, tk.END)
    for item in item_list:
        title, seed, url = item
        result_text.insert(tk.END, f"Title: {title}\nSeed Number: {seed}\nURL: {url}\n")
        result_text.insert(tk.END, "-" * 50 + "\n")

def sort_items():
    global sorted_asc, items
    items = sorted(items, key=lambda x: x[1], reverse=sorted_asc)
    sorted_asc = not sorted_asc
    display_items(items)

# Configuration for request
cookies = {
    'bb_session': '0-43744445-IS1q12Gz0MOrPyBNV8FW',
}

headers = {
    'authority': 'rutracker.net',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0',
}

params = {
    'rid': '8994327',
}

# GUI Configuration
root = tk.Tk()
root.title("Title and Seed Extractor")

items = []
sorted_asc = True

result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
result_text.pack(padx=10, pady=10)

sort_button = tk.Button(root, text="Sort", command=sort_items, font=("Arial", 12), bg="#4caf50", fg="white", padx=10, pady=5)
sort_button.pack()

extract_data()  # Call the function directly to run on startup

root.mainloop()
