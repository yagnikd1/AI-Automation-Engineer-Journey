"""
Day 51 — Python Basics and HTTP Foundations
Python Fundamentals + Web Scraping Recovery Program (Days 51–65)

Purpose
-------
This guided program revises core Python syntax while inspecting a real HTTP
response from JSONPlaceholder.

Verified practical input: post ID 1
Verified result: HTTP 200, JSON dictionary received, all syntax checks passed.

Still pending for Days 59–63
--------------------------------
1. Advanced HTTP/request error handling
2. Selective retry mechanisms
3. Production logging
4. Systematic debugging
5. Partial-failure recovery

This program intentionally does not implement those advanced topics.
"""

import requests


# input() always returns a string.
record_id_text = input("Enter a post ID from 1 to 100: ")

# Convert the numeric string to an integer.
record_id = int(record_id_text)

# Build the URL by joining text values.
base_url = "https://jsonplaceholder.typicode.com/posts/"
request_url = base_url + str(record_id)

timeout_seconds = 10

# The program is the client. It sends a GET request to the server.
response = requests.get(request_url, timeout=timeout_seconds)

print("\n--- REQUEST INFORMATION ---")
print(f"Requested URL: {request_url}")
print("HTTP method: GET")
print(f"Timeout: {timeout_seconds} seconds")

print("\n--- RESPONSE INFORMATION ---")
print(f"Status code: {response.status_code}")
print(f"Reason: {response.reason}")
print(f"Content type: {response.headers.get('Content-Type')}")
print(f"Response size: {len(response.content)} bytes")

print("\n--- PYTHON DATA TYPES ---")
print(f"record_id_text: {type(record_id_text)}")
print(f"record_id: {type(record_id)}")
print(f"base_url: {type(base_url)}")
print(f"timeout_seconds: {type(timeout_seconds)}")
print(f"response: {type(response)}")

print("\n--- RESPONSE BODY ---")
print(response.text)

# Convert the JSON response body into a Python dictionary.
# Important: .json() belongs to the response object, not the requests module.
post_data = response.json()

# Extract dictionary values. A missing key returns None.
user_id = post_data.get("userId")
post_id = post_data.get("id")
post_title = post_data.get("title")
post_body = post_data.get("body")
post_category = post_data.get("category")

# Comparisons produce Boolean values.
request_succeeded = response.status_code == 200
correct_post_received = post_id == record_id
body_has_content = len(post_body) > 0

# Membership and logical operators.
content_type = response.headers.get("Content-Type", "")
is_json_response = "application/json" in content_type

valid_response = (
    request_succeeded
    and correct_post_received
    and body_has_content
    and is_json_response
)

# Arithmetic creates new numeric values.
response_size_bytes = len(response.content)
response_size_kilobytes = response_size_bytes / 1024
next_record_id = record_id + 1

# Compound assignment updates the existing value.
inspection_count = 0
inspection_count += 1

print("\n--- CONVERTED JSON DATA ---")
print(f"User ID: {user_id}")
print(f"Post ID: {post_id}")
print(f"Title: {post_title}")
print(f"Missing category: {post_category}")

print("\n--- ADDITIONAL DATA TYPES ---")
print(f"post_data: {type(post_data)}")
print(f"user_id: {type(user_id)}")
print(f"post_title: {type(post_title)}")
print(f"post_category: {type(post_category)}")
print(f"request_succeeded: {type(request_succeeded)}")
print(f"response_size_kilobytes: {type(response_size_kilobytes)}")

print("\n--- OPERATOR RESULTS ---")
print(f"Request succeeded: {request_succeeded}")
print(f"Correct post received: {correct_post_received}")
print(f"Body has content: {body_has_content}")
print(f"JSON response: {is_json_response}")
print(f"Valid response: {valid_response}")
print(f"Category is missing: {post_category is None}")
print(f"Response size: {response_size_kilobytes:.3f} KB")
print(f"Next record ID: {next_record_id}")
print(f"Completed inspections: {inspection_count}")

# Complete arithmetic-operator revision.
title_length = len(post_title)
body_length = len(post_body)
combined_text_length = title_length + body_length
length_difference = body_length - title_length
double_title_length = title_length * 2
whole_kilobytes = response_size_bytes // 1024
remaining_bytes = response_size_bytes % 1024
record_id_squared = record_id**2

# Additional comparison operators.
different_user_and_post_ids = user_id != post_id
record_id_at_least_one = record_id >= 1
record_id_at_most_one_hundred = record_id <= 100

# Additional logical operators.
record_id_in_range = record_id_at_least_one and record_id_at_most_one_hundred
needs_attention = (
    not request_succeeded
    or not is_json_response
    or post_category is None
)

# Membership operators.
title_mentions_architect = "architect" in post_title
title_missing_python = "python" not in post_title

print("\n--- COMPLETE OPERATOR REVISION ---")
print(f"Title length: {title_length}")
print(f"Body length: {body_length}")
print(f"Combined text length: {combined_text_length}")
print(f"Length difference: {length_difference}")
print(f"Double title length: {double_title_length}")
print(f"Whole kilobytes: {whole_kilobytes}")
print(f"Remaining bytes: {remaining_bytes}")
print(f"Record ID squared: {record_id_squared}")
print(f"Different user and post IDs: {different_user_and_post_ids}")
print(f"Record ID is in range: {record_id_in_range}")
print(f"Response needs attention: {needs_attention}")
print(f"Title mentions architect: {title_mentions_architect}")
print(f"Title does not mention Python: {title_missing_python}")

# Reassignment changes the value stored by an existing variable.
response_summary = "Not inspected"
response_summary = "HTTP response inspected successfully"

# Integer division identifies the status-code family.
status_group = response.status_code // 100
is_success_status = status_group == 2
is_client_error_status = status_group == 4
is_server_error_status = status_group == 5

# Headers contain metadata; the body contains the requested content.
header_count = len(response.headers)
body_is_bytes = isinstance(response.content, bytes)
body_text_is_string = isinstance(response.text, str)

print("\n--- HTTP FOUNDATION SUMMARY ---")
print(f"Summary: {response_summary}")
print(f"Status-code group: {status_group}xx")
print(f"Successful status group: {is_success_status}")
print(f"Client-error status group: {is_client_error_status}")
print(f"Server-error status group: {is_server_error_status}")
print(f"Number of response headers: {header_count}")
print(f"response.content contains bytes: {body_is_bytes}")
print(f"response.text contains a string: {body_text_is_string}")

# Explicit type conversions.
record_id_as_float = float(record_id)
status_code_as_text = str(response.status_code)
title_as_boolean = bool(post_title)
category_as_boolean = bool(post_category)

# Remaining comparison and identity operators.
record_id_below_limit = record_id < 101
title_is_available = post_title is not None

# Compound assignment operators.
operator_number = 10
operator_number += 5
after_addition = operator_number
operator_number -= 3
after_subtraction = operator_number
operator_number *= 2
after_multiplication = operator_number
operator_number /= 4
after_division = operator_number

floor_number = 17
floor_number //= 5

remainder_number = 17
remainder_number %= 5

power_number = 3
power_number **= 2

print("\n--- FINAL SYNTAX VERIFICATION ---")
print(f"Record ID as float: {record_id_as_float}")
print(f"Status code as text: {status_code_as_text}")
print(f"Title converted to Boolean: {title_as_boolean}")
print(f"Missing category converted to Boolean: {category_as_boolean}")
print(f"Record ID is below 101: {record_id_below_limit}")
print(f"Title is available: {title_is_available}")
print(f"After += 5: {after_addition}")
print(f"After -= 3: {after_subtraction}")
print(f"After *= 2: {after_multiplication}")
print(f"After /= 4: {after_division}")
print(f"Result of //= 5: {floor_number}")
print(f"Result of %= 5: {remainder_number}")
print(f"Result of **= 2: {power_number}")
