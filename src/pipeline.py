import os
import json
from detect_score     import run_on_all_frames as run_ocr
from detect_explosion import run_on_all_frames as run_explosion
from fusion           import run_fusion
from generate_higlights import generate_highlights

FRAMES_DIR  = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\frames\match_02"
VIDEO_PATH  = r"C:\Users\sankr\Videos\IVP\IVP_Project\data\raw\rlcs_match_02.mp4"
OUTPUT_JSON = r"C:\Users\sankr\Videos\IVP\IVP_Project\outputs\match_02_highlights.json"
OUTPUT_CLIPS= r"C:\Users\sankr\Videos\IVP\IVP_Project\outputs\clips_match_02"

def main():
    print("=" * 55)
    print("   ROCKET LEAGUE HIGHLIGHT DETECTION PIPELINE")
    print("=" * 55)

    # Step 1 — OCR score detection
    print("\n[1/4] Running scoreboard OCR detector...")
    print("-" * 55)
    goal_events = run_ocr(FRAMES_DIR)
    print(f"OCR detected {len(goal_events)} goal events")

    # Step 2 — Explosion detection
    print("\n[2/4] Running explosion detector...")
    print("-" * 55)
    _, explosion_events = run_explosion(FRAMES_DIR)
    print(f"Explosion detector found {len(explosion_events)} events")

    # Step 3 — Fusion
    print("\n[3/4] Running signal fusion...")
    print("-" * 55)
    results = run_fusion(goal_events, explosion_events, OUTPUT_JSON)

    total = (
        len(results["premium"]) +
        len(results["feature"]) +
        len(results["standard"])
    )
    print(f"\nFusion Summary:")
    print(f"  Premium  highlights (goal explosions) : {len(results['premium'])}")
    print(f"  Feature  highlights (demolitions)     : {len(results['feature'])}")
    print(f"  Standard highlights (OCR only goals)  : {len(results['standard'])}")
    print(f"  Total                                 : {total}")

    # Step 4 — Clip generation
    print("\n[4/4] Generating highlight clips...")
    print("-" * 55)
    generate_highlights(OUTPUT_JSON, VIDEO_PATH, OUTPUT_CLIPS)

    print("\n" + "=" * 55)
    print("PIPELINE COMPLETE")
    print(f"Highlights JSON : {OUTPUT_JSON}")
    print(f"Clips folder    : {OUTPUT_CLIPS}")
    print("=" * 55)

if __name__ == "__main__":
    main()