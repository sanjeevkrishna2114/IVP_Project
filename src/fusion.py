import json
import os

# Window settings
BEFORE_SEC = 5
AFTER_SEC  = 5
DEMO_WINDOW = 5  # seconds between explosion and OCR goal to classify as goal explosion

def load_ocr_goals(goal_events):
    return [g["timestamp_sec"] for g in goal_events]

def classify_explosions(explosion_events, ocr_goal_timestamps):
    premium   = []
    feature   = []

    for exp in explosion_events:
        exp_sec = int(exp["frame"].replace("frame_", "").replace(".jpg", ""))

        nearby_goal = any(
            abs(exp_sec - goal_sec) <= DEMO_WINDOW
            for goal_sec in ocr_goal_timestamps
        )

        if nearby_goal:
            premium.append({
                "type":          "GOAL_EXPLOSION",
                "frame":         exp["frame"],
                "timestamp_sec": exp_sec,
                "clip_start":    max(0, exp_sec - BEFORE_SEC),
                "clip_end":      exp_sec + AFTER_SEC,
                "label":         "Premium highlight — goal explosion detected"
            })
        else:
            feature.append({
                "type":          "DEMOLITION",
                "frame":         exp["frame"],
                "timestamp_sec": exp_sec,
                "clip_start":    max(0, exp_sec - BEFORE_SEC),
                "clip_end":      exp_sec + AFTER_SEC,
                "label":         "Feature highlight — demolition detected"
            })

    return premium, feature

def classify_ocr_goals(goal_events, explosion_events):
    standard = []

    explosion_secs = [
        int(e["frame"].replace("frame_", "").replace(".jpg", ""))
        for e in explosion_events
    ]

    for goal in goal_events:
        goal_sec = goal["timestamp_sec"]

        nearby_explosion = any(
            abs(goal_sec - exp_sec) <= DEMO_WINDOW
            for exp_sec in explosion_secs
        )

        if not nearby_explosion:
            standard.append({
                "type":          "STANDARD_GOAL",
                "frame":         goal["frame"],
                "timestamp_sec": goal_sec,
                "clip_start":    max(0, goal_sec - BEFORE_SEC),
                "clip_end":      goal_sec + AFTER_SEC,
                "team":          goal["team"],
                "orange_score":  goal["orange_score"],
                "blue_score":    goal["blue_score"],
                "game":          goal["game"],
                "label":         f"Standard highlight — {goal['team']} goal, no explosion detected"
            })

    return standard

def merge_overlapping_clips(highlights):
    if not highlights:
        return []

    sorted_clips = sorted(highlights, key=lambda x: x["clip_start"])
    merged = [sorted_clips[0].copy()]

    for current in sorted_clips[1:]:
        last = merged[-1]
        if current["clip_start"] <= last["clip_end"]:
            last["clip_end"] = max(last["clip_end"], current["clip_end"])
            last["label"]    = last["label"] + " + merged"
        else:
            merged.append(current.copy())

    return merged

def run_fusion(goal_events, explosion_events, output_path=None):
    ocr_goal_timestamps = load_ocr_goals(goal_events)

    premium, feature   = classify_explosions(explosion_events, ocr_goal_timestamps)
    standard           = classify_ocr_goals(goal_events, explosion_events)

    all_highlights = premium + feature + standard

    # Merge overlapping clips within each category
    premium_merged  = merge_overlapping_clips(premium)
    feature_merged  = merge_overlapping_clips(feature)
    standard_merged = merge_overlapping_clips(standard)

    print("=" * 50)
    print(f"FUSION RESULTS")
    print("=" * 50)
    print(f"Premium  highlights (goal explosions) : {len(premium_merged)}")
    print(f"Feature  highlights (demolitions)     : {len(feature_merged)}")
    print(f"Standard highlights (OCR only goals)  : {len(standard_merged)}")
    print("=" * 50)

    print("\nPREMIUM HIGHLIGHTS")
    print("-" * 50)
    for h in premium_merged:
        print(f"  frame: {h['frame']} | {h['clip_start']}s → {h['clip_end']}s | {h['label']}")

    print("\nFEATURE HIGHLIGHTS (DEMOLITIONS)")
    print("-" * 50)
    for h in feature_merged:
        print(f"  frame: {h['frame']} | {h['clip_start']}s → {h['clip_end']}s | {h['label']}")

    print("\nSTANDARD HIGHLIGHTS")
    print("-" * 50)
    for h in standard_merged:
        print(f"  frame: {h['frame']} | {h['clip_start']}s → {h['clip_end']}s | {h['label']}")

    results = {
        "premium":  premium_merged,
        "feature":  feature_merged,
        "standard": standard_merged
    }

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nSaved results to {output_path}")

    return results

if __name__ == "__main__":
    from detect_score     import run_on_all_frames as run_ocr
    from detect_explosion import run_on_all_frames as run_explosion

    FRAMES_DIR  = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\frames\match_01"
    OUTPUT_PATH = r"C:\Users\sankr\Videos\IVP\IVP_Project\outputs\match_01_highlights.json"

    print("Step 1 — Running OCR score detector...")
    print("-" * 50)
    goal_events = run_ocr(FRAMES_DIR)

    print("\nStep 2 — Running explosion detector...")
    print("-" * 50)
    _, explosion_events = run_explosion(FRAMES_DIR)

    print("\nStep 3 — Running fusion...")
    print("-" * 50)
    results = run_fusion(goal_events, explosion_events, OUTPUT_PATH)