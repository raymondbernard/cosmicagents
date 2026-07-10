from src.main import main


def test_main_prints_expected_message(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Starter Python app is running"
