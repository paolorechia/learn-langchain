from langchain_app.models.llama_http_llm import build_llama_base_llm

output = None
# Now let's test it out!
while True:
    params = {"temperature": 1.3, "max_new_tokens": 1024, "stop": []}
    llm = build_llama_base_llm(parameters=params)
    # Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
    output = llm._call("""
        You are given a list of tasks. Please extend it with new unique tasks:

            1. "Print hello world to the terminal",
            2. "Fetch a Chuck Norris joke from this endpoint https://api.chucknorris.io/jokes/random",
            3. "Parse this HTML page https://api.chucknorris.io/  and find all the API endpoints ",
            4. "Generate 10 unique cat jokes and store them in a CSV file with two columns, punch line and joke finisher",
            5. "Connect to a Postgres database and return the existing databases names. Use the following credentials: \n\nhost localhost\nport 7036\nuser admin\npassword admin", 
            6. List the existing files in the current directory", 
            7. "Find out your existing working directory" ,
            8. "Fix the syntax error of this code snippet:\ndef myfunc():\n\tprint(“hello",
            9. "Find the keys of the JSON payload stored in the variable response_json",
            10. "Extract the key called 'address' from the JSON stored in the variable json_ and store into a variable called address",
            11. "Create a joke about AI bots and save it in a local text file",
            12. "Create an unit test for the following snippet of code:\ndef sum_2(x, y):\n\treturn x + y",
            13. "Create random data and plot it using matplotlib and store the result as a .PNG image",
            14. "Download a CSV file about suicide from the webpage https://catalog.data.gov/dataset/?res_format=CSV and plot a bar chart comparing the suicide numbers of male vs ,female",
            15. "Design a Todo list system. Write the explanation in a file called 'todo_list_system_design.txt'",
            16. Search for the source code called 'example.py' in the directory, inspect the file, write unit tests for it and execute them to make sure everything is correct.",
            17. "Write a data pipeline that ingests data from the Crime Data from 2020 to present from https://catalog.data.gov/dataset/?res_format=CSV. Use the requests and pandas, save the csv to the local disk. Create a directory if necessary, give an appropriate name"
        """)
    with open("generated_tasks.txt", "a") as fp:
        fp.write(output)