with open('frontend/src/pages/UploadReport.tsx', encoding='utf-8') as f:
    c = f.read()

# Remove the extra </div></div> I injected before the modal
c = c.replace('          </div>\n      </div>\n    </div>\n\n    {/* View Reasons Modal */}', '          </div>\n\n    {/* View Reasons Modal */}')

# Wrap the return value in a React fragment
c = c.replace(
    '  return (\n    <div className="max-w-6xl mx-auto p-6 space-y-8">',
    '  return (\n    <>\n    <div className="max-w-6xl mx-auto p-6 space-y-8">',
    1
)

# Find the modal block and ensure the outer div is closed before it, then close fragment after modal
# The modal is inside the return but outside the outer div.
# The file currently ends:    )}\n\n  );\n}\n
# We need:  ...modal}}\n    </>\n  );\n}\n

c = c.replace('    )}\n\n  );\n}\n', '    )}\n    </>\n  );\n}\n', 1)

with open('frontend/src/pages/UploadReport.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

print('Fixed!')
print('Last 100 chars:', repr(c[-100:]))
