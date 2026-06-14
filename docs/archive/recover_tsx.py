import re

content = open("temp.tsx", encoding="utf-8").read()

# The file got duplicated sections at the bottom. We need to truncate everything after the Risk Dashboard's </tbody>
# and then append the correct closing tags.
# Wait, Test Dashboard and Prediction Dashboard should come AFTER Gap Dashboard, but they are currently inside Gap Dashboard?
# No, let's see where Test Dashboard starts.
# It starts at: "{/* Test Generation Results */}"
# Let's find all occurrences of Test Generation Results
tests = content.split("{/* Test Generation Results */}")
print(f"Found {len(tests)-1} Test Generation Results")

predictions = content.split("{/* Prediction Dashboard */}")
print(f"Found {len(predictions)-1} Prediction Dashboards")

risks = content.split("{/* Risk Intelligence Dashboard */}")
print(f"Found {len(risks)-1} Risk Intelligence Dashboards")

# Let's rebuild the bottom of the file correctly.
# The correct order inside `gapResult?.success && (` was:
# 1. Gap Metrics
# 2. Gap Table
# Wait! Are Test, Prediction, and Risk supposed to be INSIDE `gapResult?.success`?
# YES, because they rely on the AST/Gap data flow in the UI. Or maybe they are just sequentially after it?
# Let's check where the original closing tags were.
# Actually, I'll just restore from the transcript!
import os
import json

transcript_path = "C:/Users/asus/.gemini/antigravity/brain/a466503e-1cf1-48b8-a78c-5ca5dbf462e6/.system_generated/logs/transcript.jsonl"
if os.path.exists(transcript_path):
    # Search backwards for UploadReport.tsx
    best_content = None
    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                step = json.loads(line)
                if step.get("type") == "PLANNER_RESPONSE":
                    for tc in step.get("tool_calls", []):
                        if tc.get("function") == "default_api:write_to_file":
                            args = tc.get("arguments", {})
                            if args.get("TargetFile", "").endswith("UploadReport.tsx"):
                                best_content = args.get("CodeContent")
                        elif tc.get("function") == "default_api:replace_file_content":
                            # We might not have the full file here, just patches.
                            pass
            except:
                pass
    if best_content:
        open("recovered.tsx", "w", encoding="utf-8").write(best_content)
        print("Recovered from write_to_file!")
    else:
        print("Could not find full write_to_file in transcript.")
