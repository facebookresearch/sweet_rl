"""
Copyright (c) Meta Platforms, Inc. and affiliates.

This source code is licensed under the CC-By-NC license found in the
LICENSE file in the root directory of this source tree.
"""

import os
import re
import time
import traceback

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.service import Service



def replace_urls(text):
    # Regular expression to find the URLs
    pattern = r"https://source\.unsplash\.com/random/(\d+)x(\d+)/\?[\w=]+"

    # Function to replace each match with the new URL format
    def replace_match(match):
        width, height = match.groups()
        return f"https://picsum.photos/id/48/{width}/{height}"

    # Use re.sub to replace all occurrences in the text
    new_text = re.sub(pattern, replace_match, text)

    # Make sure that the new text has id 48 for all images
    # Define the regex pattern to match the URLs
    pattern = r"https://picsum\.photos/(\d+)/(\d+)"

    # Define the replacement pattern
    replacement = r"https://picsum.photos/id/48/\1/\2"

    # Use re.sub to replace all matches in the paragraph
    new_text = re.sub(pattern, replacement, new_text)

    return new_text


def get_driver():
    # Set up Chrome options
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    return driver




def render_full_html(driver, html_snippet, temp_path, env_id=0):

    current_time = time.time()


    html_file_path = os.path.join(temp_path, f"{env_id}_{current_time}.html")
    image_path = os.path.join(temp_path, f"{env_id}_{current_time}.png")
    # Save the HTML snippet to a temporary file
    with open(os.path.join(temp_path, f"{env_id}_{current_time}.html"), "w") as file:
        file.write(html_snippet)
    # imgkit.from_file(html_file_path, image_path)

    try:
        # Open the local HTML file
        driver.get(f"file://{html_file_path}")
        driver.get_full_page_screenshot_as_file(image_path)

        os.remove(html_file_path)
        return image_path
    except Exception as e:
        print(e)
        traceback.print_exc()
        if os.path.exists(html_file_path):
            os.remove(html_file_path)
        return None


import re


def extract_html_snippet(paragraph):
    # Regular expression pattern to match the entire HTML content
    paragraph = replace_urls(paragraph)
    html_pattern = r"<html.*?>.*?</html>"

    # Search for the HTML snippet in the paragraph
    match = re.search(html_pattern, paragraph, re.DOTALL)

    if match:
        return paragraph.replace(match.group(0), "[SEE RENDERED HTML]"), match.group(0)
    else:
        html_pattern = r"<body.*?>.*?</body>"
        match = re.search(html_pattern, paragraph, re.DOTALL)
        if match:
            return paragraph.replace(
                match.group(0), "[SEE RENDERED HTML]"
            ), match.group(0)
        else:
            return paragraph, None
