import pytest

import app.main
from app.main import is_allowed_domain


@pytest.fixture(autouse=True)
def allowed_domains(monkeypatch):
    monkeypatch.setattr(app.main, "ALLOWED_DOMAINS", ["tomadoi.com"])


@pytest.mark.parametrize(
    "url",
    [
        "https://tomadoi.com/a.png",
        "http://tomadoi.com/a.png",
        "https://media.tomadoi.com/a.png",
        "https://a.b.tomadoi.com/a.png",
        "https://TOMADOI.com/a.png",
        "https://tomadoi.com:8443/a.png",
        "https://user@media.tomadoi.com/a.png",
        "https://tomadoi.com/a.png?x=1#frag",
    ],
)
def test_allowed(url):
    assert is_allowed_domain(url) is True


@pytest.mark.parametrize(
    "url",
    [
        # 別ドメイン
        "https://evil.com/a.png",
        "https://nottomadoi.com/a.png",
        "https://tomadoi.com.evil.com/a.png",
        # 許可ドメインがホスト以外の部分にあるだけ
        "https://evil.com/?x=.tomadoi.com",
        "https://evil.com/.tomadoi.com",
        "https://evil.com#.tomadoi.com",
        "https://tomadoi.com@evil.com/a.png",
        # WHATWG では "\" が "/" 扱いになり、実際のホストは evil.com になる
        "https://evil.com\\.tomadoi.com/a.png",
        "https://evil.com\\@a.tomadoi.com/a.png",
        # 空白・制御文字
        "https://tomadoi.com/a b.png",
        "https://tomadoi.com\t/a.png",
        "https://tomadoi.com\n/a.png",
        "https://tomadoi.com\x00/a.png",
        # http/https 以外
        "javascript://tomadoi.com/",
        "ftp://tomadoi.com/a.png",
        "file://tomadoi.com/etc/passwd",
        # ホストなし・不正
        "",
        "tomadoi.com/a.png",
        "https:///a.png",
    ],
)
def test_rejected(url):
    assert is_allowed_domain(url) is False


@pytest.mark.parametrize("domains", [[""], [" "], ["", "  "]])
def test_empty_allowed_domains_match_nothing(monkeypatch, domains):
    # ALLOWED_DOMAINS 未設定時は "".split(",") == [""] になる
    monkeypatch.setattr(app.main, "ALLOWED_DOMAINS", domains)
    assert is_allowed_domain("https://evil.com./a.png") is False
    assert is_allowed_domain("https://tomadoi.com/a.png") is False


def test_allowed_domains_are_normalized(monkeypatch):
    # ALLOWED_DOMAINS=tomadoi.com, Example.ORG のような書き方を許容する
    monkeypatch.setattr(app.main, "ALLOWED_DOMAINS", ["tomadoi.com", " Example.ORG"])
    assert is_allowed_domain("https://cdn.example.org/a.png") is True
