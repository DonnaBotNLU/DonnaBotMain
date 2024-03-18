import pytest
from Modules.linuxtoolbox import display_menu

def test_display_menu(capsys):
    display_menu()
    captured = capsys.readouterr()
    assert captured.out == "Welcome to Linux Toolbox Menu:\n" \
                           "1. Disk Options\n" \
                           "2. Repair options\n" \
                           "3. Restart Donna AI\n" \
                           "4. Install Donna AI [in progress]\n" \
                           "5. Backup Donna AI\n"


if __name__ == "__main__":
    pytest.main()
