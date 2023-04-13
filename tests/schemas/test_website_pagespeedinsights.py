from typing import Dict

import pytest

from app.schemas.website_pagespeedinsights import (
    ValidateWebPSIStrategyRequired,
    ValidateWebPSIValueOptional,
    ValidateWebPSIValueRequired,
)


# Test ValidateWebPSIStrategyRequired
def test_webpsi_strategy_required_with_valid_input() -> None:
    input_data: Dict[str, str] = {"strategy": "mobile"}
    assert ValidateWebPSIStrategyRequired.validate(input_data)


def test_webpsi_strategy_required_with_missing_strategy() -> None:
    input_data: Dict[str, str] = {}
    with pytest.raises(ValueError):
        ValidateWebPSIStrategyRequired.validate(input_data)


def test_webpsi_strategy_required_with_empty_str_strategy() -> None:
    input_data: Dict[str, str] = {"strategy": ""}
    with pytest.raises(ValueError):
        ValidateWebPSIStrategyRequired.validate(input_data)


def test_webpsi_strategy_required_with_invalid_strategy() -> None:
    input_data: Dict[str, str] = {"strategy": "web"}
    with pytest.raises(ValueError):
        ValidateWebPSIStrategyRequired.validate(input_data)


# Test ValidateWebPSIValueRequired
def test_webpsi_value_required_with_valid_input() -> None:
    input_data: Dict[str, str] = {"ps_value": "123"}
    assert ValidateWebPSIValueRequired.validate(input_data)


def test_webpsi_value_required_with_missing_ps_value() -> None:
    input_data: Dict[str, str] = {}
    with pytest.raises(ValueError):
        ValidateWebPSIValueRequired.validate(input_data)


def test_webpsi_value_required_with_empty_str_ps_value() -> None:
    input_data: Dict[str, str] = {"ps_value": ""}
    with pytest.raises(ValueError):
        ValidateWebPSIValueRequired.validate(input_data)


def test_webpsi_value_required_with_invalid_ps_value() -> None:
    input_data: Dict[str, str] = {"ps_value": "12345"}
    with pytest.raises(ValueError):
        ValidateWebPSIValueRequired.validate(input_data)


# Test ValidateWebPSIValueOptional
def test_webpsi_value_optional_with_valid_input() -> None:
    input_data: Dict[str, str] = {"ps_value": "123"}
    assert ValidateWebPSIValueOptional.validate(input_data)


def test_webpsi_value_optional_with_missing_ps_value() -> None:
    input_data: Dict[str, str] = {}
    assert ValidateWebPSIValueOptional.validate(input_data)


def test_webpsi_value_optional_with_empty_str_ps_value() -> None:
    input_data: Dict[str, str] = {"ps_value": ""}
    assert ValidateWebPSIValueOptional.validate(input_data)


def test_webpsi_value_optional_with_invalid_ps_value() -> None:
    input_data: Dict[str, str] = {"ps_value": "12345"}
    with pytest.raises(ValueError):
        ValidateWebPSIValueOptional.validate(input_data)
