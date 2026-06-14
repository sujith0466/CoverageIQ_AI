# CoverageIQ AI - Demo Video Script
**Target Length**: 5-7 minutes
**Format**: Screen recording (Loom/OBS)

## 1. Introduction & Problem Statement (0:00 - 1:00)
- **Visual**: Start on the CoverageIQ AI Landing Page.
- **Script**: "Hello everyone. Welcome to CoverageIQ AI. Traditional code coverage tools tell you *how much* code is covered, but they don't tell you *what* business logic is vulnerable, nor do they help you fix it. CoverageIQ bridges this gap by merging AST-based static analysis with Generative AI to not only find your untested code, but autonomously write the missing tests for you."

## 2. Architecture Overview (1:00 - 1:30)
- **Visual**: Show the Architecture Diagram from the README.
- **Script**: "Our system is built on a decoupled stack: A React/Vite frontend communicates with a FastAPI Python backend. The backend orchestrates PostgreSQL for storage, Python's native `ast` module for local code parsing, and LangChain to interface with Groq and Gemini for instantaneous code generation."

## 3. The Workflow - XML Upload (1:30 - 2:30)
- **Visual**: Switch to the Dashboard. Click "Upload Report".
- **Script**: "Let's see it in action. I'm going to upload a Cobertura XML report for a sample banking application. The system now asks me for the source code directory. By pointing it to my local source tree, our AST Walker dynamically maps the raw Python files, finding functions that the XML report might have missed completely."
- **Action**: Upload `banking_coverage.xml` and submit the local source path.

## 4. Coverage Intelligence & Risk Analysis (2:30 - 4:00)
- **Visual**: The Executive Dashboard loads. Highlight the Coverage Score, Gaps, and Risk table.
- **Script**: "The analysis is complete. Here we see our overall health score. Notice the Risk Engine at work: it hasn't just found untested code, it has graded it. The `transfer_funds` function is marked as HIGH RISK because of its cyclomatic complexity and dependency depth. Engineering teams now know exactly what to prioritize."

## 5. AI Test Generation (4:00 - 5:30)
- **Visual**: Scroll down to the AI Generated Tests section. Open the "View Reasons" governance modal.
- **Script**: "But finding the gap isn't enough. CoverageIQ automatically invoked our LLM pipeline (powered by Groq's Llama 3) to write these `pytest` assertions for `transfer_funds`. It analyzed the AST payload of the untested function and produced syntactically correct tests ready to be committed. We also maintain a strict Governance Trail—if you click 'View Reasons', the system provides an immutable audit log explaining exactly *why* the AI decided to generate a test for this specific function."

## 6. Conclusion & Future Scope (5:30 - 6:00)
- **Visual**: Switch to the GitHub Repository.
- **Script**: "CoverageIQ is fully open-source and containerized. In the future, we plan to integrate this directly into CI/CD pipelines as a GitHub App to automatically comment missing tests on Pull Requests. Thank you for watching!"
