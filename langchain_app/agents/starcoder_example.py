from langchain_app.models.star_coder_http_llm import build_star_coder_llm

llm = build_star_coder_llm()


helo_world = """ 
    # A function that prints hello world
    def print_hello_world():
"""


fill_in_the_middle_input_text = """
    <fim-prefix>
    def print_hello_world():
        <fim-suffix>
        print('Hello world!')
    <fim-middle>
"""

llm._call(helo_world)