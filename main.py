import os
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from bs4 import BeautifulSoup
import csv

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting various elements
        data = {
            "Title": soup.title.string if soup.title else "No title found",
            "Headings": [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])],
            "Paragraphs": [p.get_text() for p in soup.find_all('p')]
        }

        # Format the result as a readable string
        result = "\n".join([f"{key}:\n" + "\n".join(items) if isinstance(items, list) else f"{key}:\n{items}" for key, items in data.items()])
        
        return result if result.strip() else 'No data found'
    except Exception as e:
        return f"Error: {e}"

def scrape_single_website():
    url = entry.get()
    result = scrape_website(url)
    display_result(result)

def scrape_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    
    results = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row:
                url = row[0]
                result = scrape_website(url)
                results.append((url, result))
    
    combined_results = "\n\n".join([f"{url}:\n{result}" for url, result in results])
    display_result(combined_results)

def display_result(result):
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, result)
    root.update_idletasks()
    
    # Adjust window size based on content
    result_lines = result.count('\n') + 1
    new_height = min(25, result_lines + 5)
    result_text.config(height=new_height)
    root.geometry(f"800x{new_height*24 + 100}")

def save_results():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(result_text.get("1.0", tk.END))

# Create the main window
root = tk.Tk()
root.title("Web Scraping Interface")
root.geometry("800x600")  # Set default window size
root.resizable(True, True)  # Allow the window to be resizable

# Create and place the input field
entry_label = tk.Label(root, text="Enter website URL:")
entry_label.pack(pady=10)
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Create and place the buttons
single_scrape_button = tk.Button(root, text="Scrape Single Website", command=scrape_single_website, bg="red", fg="white", font=('Helvetica', 12))
single_scrape_button.pack(pady=10)

csv_scrape_button = tk.Button(root, text="Scrape from CSV", command=scrape_csv_file, bg="blue", fg="white", font=('Helvetica', 12))
csv_scrape_button.pack(pady=10)

# Create and place the save button
save_button = tk.Button(root, text="Save Results", command=save_results, bg="green", fg="white", font=('Helvetica', 12))
save_button.pack(pady=10)

# Create and place the text field for results
result_text_label = tk.Label(root, text="Scraped Data:")
result_text_label.pack(pady=10)
result_text = tk.Text(root, height=10, width=80)
result_text.pack(pady=10)

# Run the application
root.mainloop()
