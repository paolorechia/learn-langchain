import pytest
from langchain_app.tools.code_editor import CodeEditorTooling

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
    add_input ="""print('hello')
print('world')
"""
    code_editor.add_code(add_input)
    assert code_editor.source_code == ["print('hello')", "print('world')"]


def test_code_change_code():
    code_editor = CodeEditorTooling()
    code_editor.source_code = ["print('hello')", "print('world')"]
    edit_code_input = "2\nprint('code')"
    code_editor.change_code_line(edit_code_input)
    assert code_editor.source_code == ["print('hello')", "print('code')"]

def test_code_delete_lines():
    code_editor = CodeEditorTooling()
    code_editor.source_code = ["print('hello')", "print('world')", "x = 2", "y = 3"]
    delete_code_lines = "1, 4"
    code_editor.delete_code_lines(delete_code_lines)
    assert code_editor.source_code == ["print('world')", "x = 2"]


def test_code_display():
    code_editor = CodeEditorTooling()
    code_editor.source_code = ["print('hello')", "print('world')"]
    assert code_editor.display_code() == (
"""print('hello')
print('world')
"""
)