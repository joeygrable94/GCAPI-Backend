from typing import Dict

import pytest

from app.db.validators import (
    ValidateSchemaPerformanceValueOptional,
    ValidateSchemaPerformanceValueRequired,
    ValidateSchemaStrategyRequired,
)


# Test ValidateSchemaStrategyRequired
def test_webpsi_strategy_required_with_valid_input() -> None:
    input_data: Dict[str, str] = {"strategy": "mobile"}
    assert ValidateSchemaStrategyRequired.model_validate(input_data)


def test_webpsi_strategy_required_with_missing_strategy() -> None:
    input_data: Dict[str, str] = {}
    with pytest.raises(ValueError):
        ValidateSchemaStrategyRequired.model_validate(input_data)


def test_webpsi_strategy_required_with_empty_str_strategy() -> None:
    input_data: Dict[str, str] = {"strategy": ""}
    with pytest.raises(ValueError):
        ValidateSchemaStrategyRequired.model_validate(input_data)


def test_webpsi_strategy_required_with_invalid_strategy() -> None:
    input_data: Dict[str, str] = {"strategy": "web"}
    with pytest.raises(ValueError):
        ValidateSchemaStrategyRequired.model_validate(input_data)


# Test ValidateSchemaPerformanceValueRequired
def test_webpsi_value_required_with_valid_input() -> None:
    input_data: Dict[str, str] = {"ps_value": "123"}
    assert ValidateSchemaPerformanceValueRequired.model_validate(input_data)


def test_webpsi_value_required_with_missing_ps_value() -> None:
    input_data: Dict[str, str] = {}
    with pytest.raises(ValueError):
        ValidateSchemaPerformanceValueRequired.model_validate(input_data)


def test_webpsi_value_required_with_empty_str_ps_value() -> None:
    input_data: Dict[str, str] = {"ps_value": ""}
    with pytest.raises(ValueError):
        ValidateSchemaPerformanceValueRequired.model_validate(input_data)


def test_webpsi_value_required_with_invalid_ps_value() -> None:
    input_data: Dict[str, str] = {"ps_value": "12345"}
    with pytest.raises(ValueError):
        ValidateSchemaPerformanceValueRequired.model_validate(input_data)


# Test ValidateSchemaPerformanceValueOptional
def test_webpsi_value_optional_with_valid_input() -> None:
    input_data: Dict[str, str] = {"ps_value": "123"}
    assert ValidateSchemaPerformanceValueOptional.model_validate(input_data)


def test_webpsi_value_optional_with_missing_ps_value() -> None:
    input_data: Dict[str, str] = {}
    assert ValidateSchemaPerformanceValueOptional.model_validate(input_data)


def test_webpsi_value_optional_with_empty_str_ps_value() -> None:
    input_data: Dict[str, str] = {"ps_value": ""}
    assert ValidateSchemaPerformanceValueOptional.model_validate(input_data)


def test_webpsi_value_optional_with_invalid_ps_value() -> None:
    input_data: Dict[str, str] = {"ps_value": "12345"}
    with pytest.raises(ValueError):
        ValidateSchemaPerformanceValueOptional.model_validate(input_data)
