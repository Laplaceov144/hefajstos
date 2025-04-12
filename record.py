from selenium import webdriver
import json
import sys

def start_recording(url):
    # Load JavaScript from external file
    with open('event_recorder.js', 'r') as file:
        js_script = file.read()
    
    # Set up WebDriver
    driver = webdriver.Chrome()
    
    # Open the target URL
    driver.get(url)  # Replace with your actual URL
    
    # Inject the loaded JavaScript to intercept clicks
    driver.execute_script(js_script)
    
    try:
        print("Recording started. Perform actions in the browser.")
        input("Press Enter to stop recording...")  # Wait for user to finish interaction
        
        # Fetch recorded events from the browser
        recorded_js_events = driver.execute_script("return getRecordedEvents();")
        recorded_events = json.loads(recorded_js_events)
        
        # Save events to a JSON file
        with open('recorded_elements.json', 'w') as f:
            json.dump(recorded_events, f, indent=4)
        print("Recording complete. Events saved to 'recorded_elements.json'.")
    
    finally:

        # Transform the list of characters into a list of concatenated text expressions
        fetched_chars = []
        with open('recorded_elements.json', 'r') as f:
            actions = json.load(f)
            non_char_keys = ['Tab', 'CapsLock', 'Shift', 'Control', 'Alt', 'Meta', 'ArrowLeft', 'ArrowDown'
                'ArrowRight', 'ArrowUp', 'Backspace']
            for action in actions:
                if action['event'] == 'keypress' and action.get("key") not in non_char_keys:
                    single_char = action.get("key")
                    fetched_chars.append(single_char)
                elif action.get("key") == 'Backspace': 
                    fetched_chars.pop()
                else:
                    fetched_chars.append('~')
        text_values = []
        tmp_string = ''
        for char in fetched_chars:
            if char != '~':
                tmp_string += char
            else:
                if tmp_string != '':
                    text_values.append(tmp_string)
                tmp_string = ''
            print("Extracted text value: " + tmp_string)

        # Save the text values into a file        
        with open('text_values.txt', 'w') as tf:
            for item in text_values:
                tf.write(item + '\n')

        # Close the browser once the recording is done
        driver.quit()

if __name__ == "__main__":
    url = sys.argv[1]
    start_recording(url)
