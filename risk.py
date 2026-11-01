# ==============================================================================
# CalSymPy (Team 4, Delta-T) — risk.py
#
# Plain-English Summary:
# This module translates raw calculus temperatures into practical risk assessments
# for electronic cooling. In commercial computer engineering (e.g. Intel and AMD
# microprocessors), the silicon junction limit (TjMax) is typically 95°C to 105°C.
# To ensure long-term reliability and avoid thermal throttling, engineers maintain
# a safety margin of at least 15°C below TjMax.
#
# Classification Rules (evaluated after rounding temperature to 1 decimal place):
# - LOW (< 70.0 °C): Safe operating conditions.
# - MODERATE (70.0 °C <= T <= 90.0 °C): Warm operating conditions with reduced margin.
# - HIGH (> 90.0 °C): Dangerously hot, risking thermal shutdown or permanent silicon damage.
#
# Note on Threshold Origins:
# The 70 °C and 90 °C cutoffs are our project's chosen temperature bands, informed by
# published commercial processor junction thermal limits (TjMax ~ 95–105 °C, staying ~15 °C below
# for safe operation). They are engineering design heuristics chosen for this project, NOT an
# official industry or regulatory standard.
#
# Every assessment provides two perspectives:
# 1. A rigorous technical engineering statement citing TjMax margins.
# 2. A plain-English sentence suitable for non-technical stakeholders (e.g. HR or management).
# ==============================================================================


LEVEL_LOW = "LOW"
LEVEL_MODERATE = "MODERATE"
LEVEL_HIGH = "HIGH"

# Plain-English explanations explicitly specified for non-technical readers
PLAIN_ENGLISH_TEXT = {
    LEVEL_LOW: (
        "This component is running at a safe temperature. No action needed right now."
    ),
    LEVEL_MODERATE: (
        "This part is running warmer than ideal. It's not an emergency, but it's "
        "worth adding some cooling soon - cheaper to prevent now than repair later."
    ),
    LEVEL_HIGH: (
        "This part is running dangerously hot. If nothing changes it will likely "
        "slow down or fail, which usually costs more to fix later than to prevent now."
    ),
}

BADGE_TEXT = {
    LEVEL_LOW: "🟢 LOW RISK",
    LEVEL_MODERATE: "🟡 MODERATE RISK",
    LEVEL_HIGH: "🔴 HIGH RISK",
}

EMOJI_ICONS = {
    LEVEL_LOW: "🟢",
    LEVEL_MODERATE: "🟡",
    LEVEL_HIGH: "🔴",
}


def classify_risk(temperature):
    """
    Classify a temperature reading into LOW, MODERATE, or HIGH risk.
    
    Procedure:
    1. Round the temperature to 1 decimal place: T_round = round(temperature, 1).
    2. Check thresholds:
       - T_round < 70.0 -> LOW
       - 70.0 <= T_round <= 90.0 -> MODERATE
       - T_round > 90.0 -> HIGH
       
    Parameters:
        temperature (float): Peak or point temperature in degrees Celsius.
        
    Returns:
        dict: Detailed risk classification including level, badge, plain-English
              explanation, and technical engineering analysis.
    """
    raw_t = float(temperature)
    rounded_t = round(raw_t, 1)

    if rounded_t < 70.0:
        level = LEVEL_LOW
        technical = (
            f"Peak temperature is {rounded_t:.1f} °C, comfortably below the 70.0 °C threshold. "
            "The system operates with generous thermal headroom (>25 °C margin relative to "
            "silicon junction thermal limit TjMax ~95-105 °C). No thermal throttling expected."
        )
    elif rounded_t <= 90.0:
        level = LEVEL_MODERATE
        technical = (
            f"Peak temperature is {rounded_t:.1f} °C (within 70.0–90.0 °C). "
            "Thermal headroom is constricted (~5–25 °C margin below standard TjMax ~95-105 °C). "
            "While functional, prolonged operation at this level accelerates thermal wear."
        )
    else:
        level = LEVEL_HIGH
        technical = (
            f"Peak temperature is {rounded_t:.1f} °C, exceeding the 90.0 °C safety threshold. "
            "Operating dangerously close to or exceeding silicon junction thermal limits (TjMax ~95-105 °C). "
            "Risk of thermal shutdown, silicon degradation, and hardware failure."
        )

    return {
        'raw_temperature': raw_t,
        'rounded_temperature': rounded_t,
        'level': level,
        'badge': BADGE_TEXT[level],
        'emoji': EMOJI_ICONS[level],
        'plain_english': PLAIN_ENGLISH_TEXT[level],
        'technical': technical,
    }
