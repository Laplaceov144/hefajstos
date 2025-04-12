import csv
import json
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By

def replay_actions(csv_file, url):
    # Load recorded actions
    with open('recorded_elements.json', 'r') as f:
        actions = json.load(f)
    
    # Read CSV data
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)
    
    if not rows:
        print("The CSV file is empty.")
        return
    
    # Initialize WebDriver once at the start
    driver = webdriver.Chrome()
    
    # Go to desired URL
    driver.get(url)

    def perform_actions_with_text(row):
        previous_time = actions[0]['time'] if actions else None

        # Extract unique CSS selectors that should correspond to respective text values
        unique_keypress_elements = {item['element'] for item in actions if item['event'] == 'keypress'}
        input_mappings = {element: index for index, element in enumerate(unique_keypress_elements)}

        for action in actions:
            # Calculate delay
            if previous_time is not None:
                delay = (action['time'] - previous_time) / 1000.0
                time.sleep(max(delay, 0))
            
            previous_time = action['time']
            
            try:
                element = driver.find_element(By.CSS_SELECTOR, action['element'])
                
                if action['event'] == 'click':
                    element.click()
                    print(f"Clicked on: {action['element']} with text: '{action['text']}'")
                
                elif action['event'] == 'keypress' and "input" in action['element']:
                    column_index = input_mappings.get(action['element'])
                    if column_index is not None and column_index < len(row):
                        element.clear()
                        print("Extracted cell value: " + str(row[column_index]))
                        element.send_keys(row[column_index])
                        print(f"Typed value from CSV in element: {action['element']}")
                
                elif action['event'] == 'change' and element.tag_name.lower() == 'select':
                    select_options = element.find_elements(By.TAG_NAME, 'option')
                    for option in select_options:
                        if option.get_attribute('value') == action['selectedValue']:
                            option.click()
                            print(f"Changed select element: {action['element']} to value: {action['selectedValue']}")
                            break
            
            except Exception as e:
                print(f"Error interacting with element: {action['element']}. Exception: {e}")

    # Process each row in the CSV
    for row in rows[1:]:
        perform_actions_with_text(row)
        print("Form submitted for current row.")
        # You may need to add logic here to reset the form or navigate back to initial state if necessary.

    # Close the browser after all iterations
    driver.quit()

if __name__ == "__main__":
    url = sys.argv[1]
    csv_file = 'text_values.csv'  # Path to your CSV file
    replay_actions(csv_file, url)
