import re

with open("frontend/src/pages/UploadReport.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# The second prediction block starts at:
#                     {/* Prediction Dashboard */}
#                     {predictionResult?.success && (

# It has the exact same content. Let's find all occurrences of 'Prediction Dashboard'
parts = content.split("{/* Prediction Dashboard */}")
if len(parts) > 2:
    # There are at least two prediction dashboards.
    # Keep up to the first one and its content, but skip the second one.
    
    # But wait, there's Risk Intelligence Dashboard in between them!
    # Let's find Risk Intelligence Dashboard
    risk_parts = content.split("{/* Risk Intelligence Dashboard */}")
    
    # We want:
    # Top -> Prediction 1 -> Risk 1 -> End
    # Instead of:
    # Top -> Prediction 1 -> Risk 1 -> Prediction 2 -> End
    
    # Let's just find the exact string to remove.
    # The duplicate block starts at '{/* Prediction Dashboard */}' (the second one)
    # and goes until the end of its div.
    
    # A safer way: I will just use regex to find the second "{/* Prediction Dashboard */}" and everything up to the end.
    pass

# Actually, I can just strip the end of the file and rewrite it correctly.
# The end of the file has:
#                     {/* Risk Intelligence Dashboard */}
# ... risk dashboard content ...
#                       </div>
#                     )}
# ... duplicated prediction dashboard ...

# Let's find the end of Risk Intelligence Dashboard
risk_idx = content.find("{/* Risk Intelligence Dashboard */}")
if risk_idx != -1:
    # Find the next "{/* Prediction Dashboard */}" after risk_idx
    pred2_idx = content.find("{/* Prediction Dashboard */}", risk_idx)
    if pred2_idx != -1:
        # We found the duplicate prediction dashboard.
        # We should slice the string up to pred2_idx and then close the React brackets properly.
        cleaned_content = content[:pred2_idx]
        
        # Now close the brackets. 
        # What brackets are open before pred2_idx?
        # Let's see:
        # <div className="max-w-6xl ...">
        #   {analyzeResult?.success && (
        #     <div ...>
        #       {scanResult && (
        #         <div mt-6>
        #           {gapResult?.success && (
        #             <div mt-8>
        #               ...
        #               Risk Dashboard closes here with:
        #                       </div>
        #                     )}
        # 
        # So after Risk closes, we are inside `gapResult?.success && (` 's div.
        # We need to close:
        # 1. `gapResult` div -> `</div>`
        # 2. `gapResult` conditional -> `)}`
        # 3. `scanResult` div -> `</div>`
        # 4. `scanResult` conditional -> `)}`
        # 5. `analyzeResult` div -> `</div>`
        # 6. `analyzeResult` conditional -> `)}`
        # 7. main wrapper div -> `</div>`
        
        closing_tags = """
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
"""
        # Let's just count open/close braces from the top to be 100% sure.
        pass

# The safest way to fix the TSX is to rewrite the file using an AST parser, or simply re-download it from the codebase if we have an original copy. 
# But we don't. Let's just write a script that counts '{' vs '}', '<div' vs '</div', and '(' vs ')'
