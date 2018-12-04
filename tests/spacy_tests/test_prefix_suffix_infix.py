# coding: utf-8
"""Test that tokenizer prefixes, suffixes and infixes are handled correctly."""


from __future__ import unicode_literals

import pytest
import spacy

@pytest.mark.parametrize('text', ["(can)"])
def test_tokenizer_splits_no_special(combined_rule_tokenizer_fixture, text):
    tokens = combined_rule_tokenizer_fixture(text)
    assert len(tokens) == 3


@pytest.mark.parametrize('text', ["can't"])
def test_tokenizer_splits_no_punct(combined_rule_tokenizer_fixture, text):
    tokens = combined_rule_tokenizer_fixture(text)
    assert len(tokens) == 2


@pytest.mark.parametrize('text', ["(can't"])
def test_tokenizer_splits_prefix_punct(combined_rule_tokenizer_fixture, text):
    tokens = combined_rule_tokenizer_fixture(text)
    assert len(tokens) == 3


@pytest.mark.parametrize('text', ["can't)"])
def test_tokenizer_splits_suffix_punct(combined_rule_tokenizer_fixture, text):
    tokens = combined_rule_tokenizer_fixture(text)
    assert len(tokens) == 3


@pytest.mark.parametrize('text', ["(can't)"])
def test_tokenizer_splits_even_wrap(combined_rule_tokenizer_fixture, text):
    tokens = combined_rule_tokenizer_fixture(text)
    assert len(tokens) == 4


@pytest.mark.parametrize('text', ["(can't?)"])
def test_tokenizer_splits_uneven_wrap(combined_rule_tokenizer_fixture, text):
    tokens = combined_rule_tokenizer_fixture(text)
    assert len(tokens) == 5


@pytest.mark.parametrize('text,length', [("U.S.", 1), ("us.", 2), ("(U.S.", 2)])
def test_tokenizer_splits_prefix_interact(combined_rule_tokenizer_fixture, text, length):
    tokens = combined_rule_tokenizer_fixture(text)
    assert len(tokens) == length


@pytest.mark.parametrize('text', ["U.S.)"])
def test_tokenizer_splits_suffix_interact(combined_rule_tokenizer_fixture, text):
    tokens = combined_rule_tokenizer_fixture(text)
    assert len(tokens) == 2


@pytest.mark.parametrize('text', ["(U.S.)"])
def test_tokenizer_splits_even_wrap_interact(combined_rule_tokenizer_fixture, text):
    tokens = combined_rule_tokenizer_fixture(text)
    assert len(tokens) == 3


@pytest.mark.parametrize('text', ["(U.S.?)"])
def test_tokenizer_splits_uneven_wrap_interact(combined_rule_tokenizer_fixture, text):
    tokens = combined_rule_tokenizer_fixture(text)
    assert len(tokens) == 4


@pytest.mark.parametrize('text', ["best-known"])
def test_tokenizer_splits_hyphens(combined_rule_tokenizer_fixture, text):
    tokens = combined_rule_tokenizer_fixture(text)
    assert len(tokens) == 1 # CHANGED FROM 3 TO 1


@pytest.mark.parametrize('text', ["0.1-13.5", "0.0-0.1", "103.27-300"])
def test_tokenizer_splits_numeric_range(combined_rule_tokenizer_fixture, text):
    tokens = combined_rule_tokenizer_fixture(text)
    assert len(tokens) == 3


@pytest.mark.parametrize('text', ["best.Known", "Hello.World"])
def test_tokenizer_splits_period_infix(combined_rule_tokenizer_fixture, text):
    tokens = combined_rule_tokenizer_fixture(text)
    assert len(tokens) == 3


@pytest.mark.parametrize('text', ["Hello,world", "one,two"])
def test_tokenizer_splits_comma_infix(combined_rule_tokenizer_fixture, text):
    tokens = combined_rule_tokenizer_fixture(text)
    assert len(tokens) == 3
    assert tokens[0].text == text.split(",")[0]
    assert tokens[1].text == ","
    assert tokens[2].text == text.split(",")[1]


@pytest.mark.parametrize('text', ["best...Known", "best...known"])
def test_tokenizer_splits_ellipsis_infix(combined_rule_tokenizer_fixture, text):
    tokens = combined_rule_tokenizer_fixture(text)
    assert len(tokens) == 3


def test_tokenizer_splits_double_hyphen_infix(combined_rule_tokenizer_fixture):
    tokens = combined_rule_tokenizer_fixture("No decent--let alone well-bred--people.")
    assert tokens[0].text == "No"
    assert tokens[1].text == "decent"
    assert tokens[2].text == "--"
    assert tokens[3].text == "let"
    assert tokens[4].text == "alone"
    assert tokens[5].text == "well-bred" # CHANGED
    # assert tokens[6].text == "-"
    # assert tokens[7].text == "bred"
    assert tokens[6].text == "--"
    assert tokens[7].text == "people"


@pytest.mark.xfail
def test_tokenizer_splits_period_abbr(combined_rule_tokenizer_fixture):
    text = "Today is Tuesday.Mr."
    tokens = combined_rule_tokenizer_fixture(text)
    assert len(tokens) == 5
    assert tokens[0].text == "Today"
    assert tokens[1].text == "is"
    assert tokens[2].text == "Tuesday"
    assert tokens[3].text == "."
    assert tokens[4].text == "Mr."


@pytest.mark.xfail
def test_tokenizer_splits_em_dash_infix(combined_rule_tokenizer_fixture):
    # Re Issue #225
    tokens = combined_rule_tokenizer_fixture("""Will this road take me to Puddleton?\u2014No, """
                          """you'll have to walk there.\u2014Ariel.""")
    assert tokens[6].text == "Puddleton"
    assert tokens[7].text == "?"
    assert tokens[8].text == "\u2014"