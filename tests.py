import pytest
import os
from pathlib import Path
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from config import MAX


class TestGetFilesInfo:
    """Test suite for the get_files_info function using the calculator package."""
    
    @pytest.fixture
    def calculator_dir(self):
        """Return the path to the calculator directory."""
        return str(Path(__file__).parent / "calculator")
    
    def test_calculator_current_directory(self, calculator_dir):
        """Test listing files in the calculator directory (.)"""
        result = self.run_get_files_info_test(
            calculator_dir, ".", "\n=== Test: Calculator Current Directory ==="
        )
        assert "Result for current directory:" in result
        assert "main.py" in result
        assert "tests.py" in result
        assert "pkg" in result
        assert "file_size=" in result
        assert "is_dir=" in result
    
    def test_calculator_pkg_subdirectory(self, calculator_dir):
        """Test listing files in the pkg subdirectory."""
        result = self.run_get_files_info_test(
            calculator_dir, "pkg", "\n=== Test: Calculator pkg Subdirectory ==="
        )
        assert "Result for 'pkg' directory:" in result
        assert "calculator.py" in result
        assert "render.py" in result
        assert "file_size=" in result
        assert "is_dir=" in result
    
    def test_path_traversal_to_bin(self, calculator_dir):
        """Test security: prevent accessing /bin from calculator directory."""
        result = self.run_get_files_info_test(
            calculator_dir, "/bin", "\n=== Test: Path Traversal to /bin ==="
        )
        assert "Error: Cannot list" in result
        assert "outside the permitted working directory" in result
    
    def test_path_traversal_parent(self, calculator_dir):
        """Test security: prevent accessing parent directory."""
        result = self.run_get_files_info_test(
            calculator_dir,
            "../",
            "\n=== Test: Path Traversal to Parent Directory ===",
        )
        assert "Error: Cannot list" in result
        assert "outside the permitted working directory" in result
    
    def test_nonexistent_directory(self, calculator_dir):
        """Test error handling for non-existent directory."""
        result = self.run_get_files_info_test(
            calculator_dir, "nonexistent", "\n=== Test: Non-existent Directory ==="
        )
        assert "Error: Directory 'nonexistent' does not exist" in result
    
    def test_file_not_directory(self, calculator_dir):
        """Test error handling when path points to a file, not a directory."""
        result = self.run_get_files_info_test(
            calculator_dir, "main.py", "\n=== Test: File (Not Directory) ==="
        )
        assert "Error: 'main.py' is not a directory" in result
    
    def test_file_sizes_reported(self, calculator_dir):
        """Test that file sizes are reported correctly."""
        result = self.run_get_files_info_test(
            calculator_dir, ".", "\n=== Test: File Sizes ==="
        )
        assert "main.py" in result
        assert "file_size=" in result
        assert "bytes" in result
        # Verify that main.py line contains file_size
        assert "main.py: file_size=" in result
    
    def test_main_py_has_positive_size(self, calculator_dir):
        """Test that main.py has a positive file size."""
        result = self.run_get_files_info_test(
            calculator_dir, ".", "\n=== Test: main.py Has Positive Size ==="
        )
        main_py_line = self._extract_line_containing(result, "main.py")
        size = self._extract_file_size(main_py_line)
        print(f"Extracted size: {size} bytes")
        assert size > 0
    
    def test_pkg_is_directory(self, calculator_dir):
        """Test that pkg is correctly identified as a directory."""
        result = self.run_get_files_info_test(
            calculator_dir, ".", "\n=== Test: pkg is Directory ==="
        )
        pkg_line = self._extract_line_containing(result, "pkg")
        assert "is_dir=True" in pkg_line
    
    def test_main_py_is_not_directory(self, calculator_dir):
        """Test that main.py is correctly identified as not a directory."""
        result = get_files_info(calculator_dir, ".")
        main_py_line = self._extract_line_containing(result, "main.py")
        assert "is_dir=False" in main_py_line
    
    def test_tests_py_is_not_directory(self, calculator_dir):
        """Test that tests.py is correctly identified as not a directory."""
        result = get_files_info(calculator_dir, ".")
        tests_py_line = self._extract_line_containing(result, "tests.py")
        assert "is_dir=False" in tests_py_line
    
    # Helper methods
    def _extract_line_containing(self, text, search_term):
        """Extract the line containing the search term."""
        lines = text.split("\n")
        matching_lines = [line for line in lines if search_term in line and "file_size=" in line]
        assert matching_lines, f"No line found containing '{search_term}'"
        return matching_lines[0]
    
    def _extract_file_size(self, line):
        """Extract file size as integer from a line."""
        size_part = line.split("file_size=")[1].split(" ")[0]
        return int(size_part)

    def run_get_files_info_test(self, calculator_dir, arg1, arg2):
        return get_files_info(calculator_dir, arg1)


def _print_test_result(header: str, result: str):
    """Helper to print test headers and results consistently."""
    print("\n" + header)
    print(result)
    print("=" * 40)


class TestGetFileContent:
        """Tests for get_file_content using the calculator package."""

        @pytest.fixture
        def calculator_dir(self):
            return str(Path(__file__).parent / "calculator")

        def test_read_small_file(self, calculator_dir):
            # Read an existing small file (main.py)
            path = os.path.join(calculator_dir, "main.py")
            result = get_file_content(calculator_dir, path)
            assert isinstance(result, str)
            assert "def" in result or "import" in result or len(result) > 0

        def test_read_long_file_truncated(self, calculator_dir):
            # Read the long file which should be truncated at MAX
            path = os.path.join(calculator_dir, "long.txt")
            result = get_file_content(calculator_dir, path)
            assert isinstance(result, str)
            # Should include truncation marker when file is longer than MAX
            if os.path.getsize(path) > MAX:
                assert "truncated" in result or "[...]" in result
            # Ensure returned content length is at most MAX plus marker
            assert len(result) <= MAX + 200

        def test_path_traversal_outside(self, calculator_dir):
            # Attempt to read /bin/ls should be denied
            outside = "/bin/ls"
            result = get_file_content(calculator_dir, outside)
            assert "Error: Cannot read" in result
            assert "outside the permitted working directory" in result

        def test_nonexistent_file(self, calculator_dir):
            path = os.path.join(calculator_dir, "does_not_exist.txt")
            result = get_file_content(calculator_dir, path)
            assert "Error: File not found" in result or "is not a regular file" in result

        def test_read_directory_instead_of_file(self, calculator_dir):
            # Passing a directory path should report not a regular file
            result = get_file_content(calculator_dir, calculator_dir)
            assert "Error: File not found" in result or "is not a regular file" in result

        def test_read_pkg_calculator(self, calculator_dir):
            # Read the calculator module inside pkg
            path = os.path.join(calculator_dir, "pkg", "calculator.py")
            result = get_file_content(calculator_dir, path)
            assert isinstance(result, str)
            assert "class Calculator" in result
            assert "def evaluate" in result or "def _evaluate_infix" in result


class TestWriteFile:
    """Tests for the write_file function."""

    @pytest.fixture
    def calculator_dir(self):
        return str(Path(__file__).parent / "calculator")

    def test_write_lorem(self, calculator_dir):
        p = os.path.join(calculator_dir, "lorem.txt")
        content = "wait, this isn't lorem ipsum"
        res = write_file(calculator_dir, p, content)
        _print_test_result("=== Test: write_file to lorem.txt ===", res)
        assert res.startswith("Successfully wrote to")
        # verify file content
        with open(p, "r") as f:
            assert f.read() == content

    def test_write_pkg_morelorem(self, calculator_dir):
        p = os.path.join(calculator_dir, "pkg", "morelorem.txt")
        content = "lorem ipsum dolor sit amet"
        res = write_file(calculator_dir, p, content)
        _print_test_result("=== Test: write_file to pkg/morelorem.txt ===", res)
        assert res.startswith("Successfully wrote to")
        # verify file content
        with open(p, "r") as f:
            assert f.read() == content

    def test_write_tmp_denied(self, calculator_dir):
        p = "/tmp/temp.txt"
        res = write_file(calculator_dir, p, "this should not be allowed")
        _print_test_result("=== Test: write_file to /tmp/temp.txt ===", res)
        assert "outside the permitted working directory" in res

if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
