import sys
import json

# Final role prediction logic using all 50 questions

def predict_role(answers):
    roles = ["IGL", "Entry Fragger", "Support", "Freestyle", "Fragger", "Sniper"]
    scores = {role: 0 for role in roles}

    # Role-based keyword mapping (simple scoring logic)
    keyword_map = {
        "IGL": ["call", "lead", "rotate", "guide", "decision", "plan", "entry", "control", "command"],
        "Entry Fragger": ["push", "entry", "first knock", "aggressive", "rush", "initiate", "hot drop"],
        "Support": ["revive", "share", "support", "assist", "heal", "backup", "follow"],
        "Freestyle": ["flank", "independent", "solo", "adaptive", "freestyle", "random"],
        "Fragger": ["frag", "kill", "fight", "tdm", "arena", "gun skill"],
        "Sniper": ["snipe", "scout", "peek", "hold", "long-range"]
    }

    # Custom index-based weighting for sliders
    slider_weights = {
        3: {"IGL": 1},
        6: {"IGL": 1},
        7: {"IGL": 1},
        # These can be extended with more question IDs and mappings if needed
    }

    for idx, response in answers.items():
        if isinstance(response, str):
            lowered = response.lower()
            for role, keywords in keyword_map.items():
                for kw in keywords:
                    if kw in lowered:
                        scores[role] += 1
        elif isinstance(response, int):
            # Slider question scoring (custom per slider)
            if idx + 1 in slider_weights:
                for role, weight in slider_weights[idx + 1].items():
                    scores[role] += weight * response

    # Return role with highest score
    best_role = max(scores, key=scores.get)
    return best_role
