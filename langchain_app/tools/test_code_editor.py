import pytest
from langchain_app.tools.code_editor import CodeEditorTooling, CodeEditorAddCodeInput, CodeEditorChangeCodeLineInput, CodeEditorDeleteCodeLinesInput

def test_code_editor_init():
    code_editor = CodeEditorTooling()
    assert code_editor


def test_code_run():
    code_editor = CodeEditorTooling()
    code_editor.source_code = ["print('hello, world')"]
    result = code_editor.run_code()
    succeeded = "Succeeded"
    stdout = b'hello, world\n'
    stderr = b''
    assert result == f"Program {succeeded}\nStdout:{stdout}\nStderr:{stderr}"


def test_code_run_exception():
    code_editor = CodeEditorTooling()
    code_editor.source_code = ["print('hello, world'"]
    result = code_editor.run_code()
    assert "Program Failed" in result
    assert "SyntaxError" in result


def test_code_add_code():
    code_editor = CodeEditorTooling()
    add_input = CodeEditorAddCodeInput(
input_code="""print('hello')
print('world')
"""
)
    code_editor.add_code(add_input)
    assert code_editor.source_code == ["print('hello')", "print('world')"]
