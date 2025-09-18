from duplicate import calculate_discount

def test_negative_amounts():
    result = calculate_discount(-100, "regular")
    assert result == -95.00  # -100 - (-100 * 0.05) = -95
    
    result = calculate_discount(-1000, "regular")
    assert result == -950.00 
    