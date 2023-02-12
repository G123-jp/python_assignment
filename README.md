# Take-Home Assignment

The goal of this take-home assignment is to evaluate your abilities to design a API in Python.

You should first fork this repository, and then share the url of your forked repository via email to HR.

**Please do not submit any pull requests to this repository.**

## Problem Statement:

Develop a program that parses the input JSON file and converts the Unix timestamps into human-readable format. The program should output the opening and closing hours of a store for each day of the week.

Input:

- A JSON file consisting of days of the week as keys and corresponding opening hours as values.
- Each day of the week is represented as a string (e.g. "Monday").
- The value for each day of the week is an array of objects that represent the opening hours. Each object consists of two keys:
    - type: A string indicating whether the time represents an opening or closing time.
    - value: A Unix timestamp representing the opening or closing time.

Output:

- The program should output the opening and closing hours for each day of the week in human-readable format (e.g. "9:00 AM" or "10:30 PM").
- The output should be in the format:
```
[Day of Week]:
    [Opening Time] - [Closing Time]
```

## Requirements:

- The program should be written in Python 3.
- The program should use the datetime module to convert the Unix timestamps to human-readable format.
- The program should handle errors, such as missing keys or invalid timestamps, and output a meaningful error message.
- The program should be well-documented and easy to understand, with clear and concise code and comments.
- The program should be tested with multiple input JSON files to ensure its correctness, a sample input JSON file has been provided.
 - The program should be submitted as a single Python file, along with a brief write-up explaining how to run the program and any assumptions made during development.
- You are free to use any frameworks and libraries you like, but should include a brief explanation of why you chose the frameworks and libraries you used.
- The program should include error handling to handle cases where the API returns an error or the data is not in the correct format.

## Example:
Input
```
{
    "Monday": [
        { "type": "open", "value": 32400 },
        { "type": "close", "value": 64800 }
    ],
    "Tuesday": [
        { "type": "open", "value": 36000 },
        { "type": "close", "value": 72000 }
    ],
    ...
}
```
Output
```
{
    "Monday": "9:00 AM - 6:00 PM",
    "Tuesday": "10:00 AM - 8:00 PM"
    ...
}
```

A detailed sample input and output has been provided in the project root folder.

## Submission:

Please submit the following:

- The Python source code of your solution.
- A brief explanation of your design choices and trade-offs, as well as any challenges you faced while implementing the program, and please also describe how to test your code in local.
- Include test file covers all edge cases you can think of.
- A requirements.txt file which contains your dependency libraries.
- A Dockerfile which can be used to run your API in local environment is a plus.
- A Swagger API documentation is a plus.

## Evaluation Criteria:

Your solution will be evaluated based on the following criteria:

- Correctness: Does the program produce the correct results?
- Code quality: Is the code well-structured, easy to read, and maintainable?
- Design: Does the program make good use of functions, data structures, and libraries?
- Error handling: Does the program handle errors and unexpected input appropriately?
- Documentation: Is the code adequately documented, with clear explanations of the algorithms and data structures used?

## Additional Notes:

You have 7 days to complete this assignment and submit your solution.
