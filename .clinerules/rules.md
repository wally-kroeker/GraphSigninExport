---
description: Instructions to be always followed.
globs: 
alwaysApply: true
---

<ENVIRONMENT SPECIFICATIONS>
- This project runs in a Windows Subsystem for Linux (WSL) environment using Ubuntu, or on a Linux server via SSH
- All terminal commands MUST be executed using bash shell, NOT PowerShell
- For commands requiring sudo privileges:
  1. DO NOT attempt to execute them directly
  2. Clearly inform the user that the command requires sudo privileges
  3. Provide the exact command for the user to run manually
  4. Request the user to share the command output after execution
  5. Wait for user's response before proceeding

<PYTHON ENVIRONMENT>
- All Python package and environment management MUST use UV (Astral)
- For Python projects:
  1. Use `uv venv` to create virtual environments
  2. Use `uv pip` for package installation and management
  3. Use `requirements.txt` for dependency specifications with exact versions
  4. Always activate the UV-created virtual environment before running Python code
  5. Use `uv pip compile` to generate requirements.txt from pyproject.toml
  6. Never use pip, conda, poetry, or other package managers directly
</PYTHON ENVIRONMENT>
</ENVIRONMENT SPECIFICATIONS>

- Split into multiple responses if one response isn't enough to answer the question.
- Below is the Workflow to follow:

1. UNDERSTAND the REQUIREMENTS (PLAN MODE):
<CLARIFICATION>
- Always ask for clarifications and follow-ups.
- Identify underspecified requirements and ask for detailed information.
- Fully understand all the aspects of the problem and gather details to make it very precise and clear.
- Ask towards all the hypothesis and assumptions needed to be made. Remove all the ambiguities and uncertainties.
- Suggest solutions that I didn't think about—anticipate my needs
- Only after having hundred percent clarity and confidence, proceed for SOLUTION.
</CLARIFICATION>

2. FORMULATING the SOLUTION (PLAN MODE):
<STEP BY STEP REASONING>
<DECOMPOSE>
- Have a meta architecture plan for the solution.
- Break down the problem into key concepts and smaller sub-problems.
</DECOMPOSE>
a. Think about all possible ways to solve the problem.
b. Set up the evaluation criterias and trade-offs to access the merit of the solutions.
c. Find the optimal solution and the criterias making it optimal and the trade-offs involved.
<WEB USE> Can use the web if needed using use_mcp_tool commands, particularly use the search tool from Perplexity. Example:
<use_mcp_tool>
<server_name>perplexity-mcp</server_name>
<tool_name>search</tool_name>
<arguments>
{
  "param1": "value1",
  "param2": "value2"
}
</arguments>
</use_mcp_tool>
</WEB USE>

<MULTI ATTEMPTS>
a. Reason out rigorously about the optimality of the solution.
b. Question every assumption and inference, and support them with comprehensive reasoning.
c. Think of better solutions than the present one Combining the strongest aspects of different solutions.
d. Repeat the process <MULTI ATTEMPTS> refining and integrating different solutions into one until a strong solution is found.
d. Can use <WEB USE> if needed to do research.
</MULTI ATTEMPTS>
</STEP BY STEP REASONING>

3. SOLUTION VALIDATION (PLAN MODE):

<REASONING PRESENTATION>
- Provide the PLAN with as much detail as possible. 
- Break down the solution step-by-step and think every step in through detail with clarity.
- Reason out its optimality w.r.t. other promising solutions.
- Explicitly tell all your assumptions, choices and decisions 
- Explain trade-offs in solutions
- restate my query in your own words if necessary after giving the solution
</REASONING PRESENTATION>
- Before implementing, validate the SOLUTION plan produced by <REASONING PRESENTATION>.

4. IMPLEMENTATION (ACT MODE):
<PROGRAMMING PRINCIPLES>
- algorithm_efficiency: use the most efficient algorithms and data structures
- modularity: write modular code, break complex logic into smaller atomic parts. Whenever possible break into classes, files, directories, modules, functions, etc.
- file_management: break long files into smaller, more manageable files with smaller functions.
- import_statements: prefer importing functions from other files instead of modifying those files directly.
- file_organization: organize files into directories and folders.
- reuse: prefer to reuse existing code instead of writing it from scratch. 
- code_preservation: Preserve What Works. Don't modify working components without necessity.
- systematic_sequence: Complete one step completely before starting another. Keep systematic sequence of functionalities.
- design_patterns: apply appropriate design patterns for maintainability. Plan for future changes, extendable flexible, scalable, and maintainable code.
- proactive_testing: any functionality codes should be accompanied with proper test code as in <TESTING>.
</PROGRAMMING PRINCIPLES>

<SYSTEMATIC CODE PROTOCOL>
[Step: 1]
<ANALYZE CODE>
<DEPENDENCY ANALYSIS>
- Which components will be affected?
- What dependencies exist?
- Is this local or does it affect core logic?
- Which functionalities will be affected and how?
- What cascading effects will this change have?
</DEPENDENCY ANALYSIS>

<TERMINAL EXECUTION>
- All commands MUST be executed in bash shell
- Before executing any command:
  1. Verify it doesn't require sudo privileges
  2. If sudo is needed, follow the sudo protocol in <ENVIRONMENT SPECIFICATIONS>
  3. Use appropriate bash syntax and commands
  4. Avoid PowerShell-specific commands or syntax
- For long-running commands:
  1. Use proper bash background job management (& and nohup when needed)
  2. Provide instructions for checking job status
</TERMINAL EXECUTION>

<FLOW ANALYSIS>
- Before proposing any changes, conduct a complete end-to-end flow analysis of the relevant use case from the entry point (e.g., function call, variable initialization) to the execution of all affected code. 
- Track the flow of data and logic throughout all components involved to understand its full scope.
</FLOW ANALYSIS>
- Document these dependencies thoroughly, including the specific usage of functions or logic in files specified by the rules in .clinerules/memory
</ANALYZE CODE>

[Step: 2]
<PLAN CODE>
- If needed initiate <CLARIFICATION> process.
- Use <STEP BY STEP REASONING> to Outline a detailed plan including component dependencies, architectural considerations before coding. Use <REASONING PRESENTATION> to Explain all code changes, what each part does, and how it affects other areas.
<STRUCTURED PROPOSALS>
- Provide a proposal that specifies: 1) what files, functions, or lines of code are being changed; 2) why the change is necessary (i.e. bug fix, improvement or new feature); 3) all of the directly impacted modules or files; 4) potential side effects; 5) a detailed explanation of any tradeoffs.
</STRUCTURED PROPOSALS> 
</PLAN CODE>

[Step: 3]
<MAKE CHANGES>

1. Document Current State in files specified by by the rules in .clinerules/memory
- What's currently working?
- What's the current error/issue?
- Which files will be affected?

2. Plan Single Logical Change at a Time
<INCREMENTAL ROLLOUTS>
- One logical feature at a time
- But fully resolve this one change by accomodating appropriate changes in other parts of the code.
- Adjust all existing dependencies and issues created by this change.
- architecture_preservation: Ensure that all new code integrates seamlessly with existing project structure and architecture before committing changes. Do not make changes that disrupt existing code organization or files.
</INCREMENTAL ROLLOUTS>

3. Simulation Testing
<SIMULATION ANALYSIS>
- Simulate user interactions and behaviors by performing dry runs, trace calls, or other appropriate methods to rigorously analyze the impact of proposed changes on both expected and edge-case scenarios. 
- Generate feedback on all potential side effects.
</SIMULATION ANALYSIS>
<SIMULATION VALIDATION>
- Do not propose a change unless the simulation passes and verifies that all existing functionality is preserved, and if a simulation breaks, provide fixes immediately before proceeding.
</SIMULATION VALIDATION>
- If Simulation Testing Passes, do the actual implementation.
</MAKE CHANGES>

[Step: 4] Perform <TESTING>.

[Step: 5] LOOP 1-4 and implement all changes
- Incorporate all the changes systematically, one by one.
- Verify the changes and test them one by one.

[Step: 6] Optimize the changed codes
- Optimize the changed codes, after all changes are tested and verified.

</SYSTEMATIC CODE PROTOCOL>

<REFERENCE>
- Reference relevant documentation and best practices
- Use <WEB USE> if needed to refer to documentation or best practices
</REFERENCE>

<TESTING>

<DEPENDENCY BASED TESTING>
Create unit tests for any new functionality. Run all tests from the <ANALYZE CODE> to confirm that existing behavior is still as expected.
</DEPENDENCY BASED TESTING>
<NO BREAKAGE ASSERTION>
After you propose a change, run the tests yourself, and verify that it passes. Do not rely on me to do this, and be certain that my code will not be broken.
</NO BREAKAGE ASSERTION>

1. Write test logic in seperate files than the code implementation for teh functionality to keep the code clean and maintainable

<TEST PLAN>
- Think of sufficiently exhaustive test plans for the functionalities added/updated against the requirements and desired outcomes.
- Define comprehensive test scenarios covering edge cases
- Specify appropriate validation methods for the project's stack
- Suggest monitoring approaches to verify the solution's effectiveness
- Consider potential regressions and how to prevent them
</TEST PLAN>

2. Write test code for ANY added critical functionality ALWAYS. For initial test generation use <DEPENDENCY BASED TESTING> and <NO BREAKAGE ASSERTION>. Then use <TEST PLAN> to write code for extensive testing.
3. Document testing as specified by the rules in .clinerules/memory
</TESTING>

<DEBUGGING>
Below debugging routine is for persistent errors or incomplete fixes. So use this routine only when got stuck.
<DIAGNOSE>
- Gather all error messages, logs, and behavioral symptoms
- Add relevant context from files
- Retrieve relevant project architecture, plan and current working task as specified by the rules in .clinerules/memory 
</DIAGNOSE>

- Whenever you fail with any test result, always add more context using <DIAGNOSE> and debug the issue effectively first, then when you have complete information move towards a fix. 
- Explain your OBSERVATIONS and then give your REASONINGS to explain why this is EXACTLY the issue and not anything else. 
- If you aren't sure, first get more OBSERVATIONS by adding more <DIAGNOSE> context to the issue so you exactly and specifically know what's wrong. Additionally you can seek <CLARIFICATION> if required.
- Understand architecture using <ANALYZE CODE> relevant to the issue.
- Use <STEP BY STEP REASONING> to think of all possible causes like architectural misalignment, design flaw rather than just a bug, etc.
- Look for similar patterns already solved elsewhere in the codebase in  .cursor/rules/error-documentation.mdc and <WEB USE> if needed.
- Present your fix using <REASONING PRESENTATION> for validation.
- Start modifying code to update and fix things using <SYSTEMATIC CODE PROTOCOL> and <TESTING>.

</DEBUGGING>

- When implementing something new, be relentless and implement everything to the letter. Stop only when you're done till successfully testing, not before.

5. IMPROVEMENTS and FURTHER PROGRESSIONS (PLAN MODE):
- S1: Suggest ways to improve code stability or scalability.
- S2: Offer strategies to enhance performance or security.
- S3: Recommend methods for improving readability or maintainability.
- Recommend areas for further investigation
