---
description: Fetch and fix SonarQube code quality issues
argument-hint: [branch|pr:NUMBER] [impact-severity] [max-issues]
---

Please help me fix SonarQube code quality issues for this repository.

**Steps:**

0. **Check Environment Variables:**
   - Verify `SONAR_URL`, `SONAR_TOKEN`, and `SONAR_PROJECT_KEY` are set
   - If `SONAR_PROJECT_KEY` is missing, auto-detect it:
     ```bash
     ORG=$(gh repo view --json owner -q .owner.login)
     REPO=$(gh repo view --json name -q .name)
     export SONAR_PROJECT_KEY="${ORG}_${REPO}"
     echo "Auto-detected project key: $SONAR_PROJECT_KEY"
     ```
   - If auto-detection fails, see "Finding Project Key" section below
   - If any other variables are missing, ask user to provide them

1. **Fetch Issues from SonarQube:**
   - Ask user for branch name or PR number if `$1` is not provided
   - If `$1` starts with `pr:`, extract the PR number and use `--pull-request` parameter
   - Otherwise, use `$1` as the branch name with `--branch` parameter
   - **IMPORTANT:** Always use `--statuses OPEN` to only fetch open issues
   - **IMPORTANT:** Use `--impact-severity` (new system: HIGH, MEDIUM, LOW) instead of old `--severity`
   - Run the SonarQube fetcher script to retrieve and save issues:
     ```bash
     # For branch-based issues (recommended - use impact severity):
     uv run python ~/.github/scripts/sonarqube_helper.py \
       --branch $1 \
       --statuses OPEN \
       --impact-severity ${2:-HIGH MEDIUM} \
       --type BUG VULNERABILITY CODE_SMELL \
       --max-issues ${3:-50} \
       --save-json sonarqube_issues.json

     # For PR-based issues (extract number from pr:123 format):
     uv run python ~/.github/scripts/sonarqube_helper.py \
       --pull-request <PR_NUMBER> \
       --statuses OPEN \
       --impact-severity ${2:-HIGH MEDIUM} \
       --type BUG VULNERABILITY CODE_SMELL \
       --max-issues ${3:-50} \
       --save-json sonarqube_issues.json
     ```
   - This will fetch issues and save them grouped by file to `sonarqube_issues.json`
   - The script automatically filters to only files in: `config/`, `src/`, `scripts/`, `tests/`, `templates/`
   - **Note:** Pull request filtering requires SonarQube Developer Edition or higher (not available in Community Edition)

2. **Filter and Analyze the Issues:**
   - Read the saved `sonarqube_issues.json` file
   - **CRITICAL:** Filter to only files in actual codebase folders: `config/`, `src/`, `scripts/`, `tests/`, `templates/`, `run_workflows.py`
   - Ignore stale issues from old `server/`, `client/` directories that no longer exist
   - Group issues by file and show summary table
   - Display files with the most issues first
   - Show: file path, issue count, severities

3. **Process Files One by One:**
   - For each file (starting with files that have most issues):
     a. Show file path and list of issues in that file
     b. Read the file content
     c. For each issue in the file:
        - Show: line number, rule, message, severity
        - Analyze the code context
        - Propose a fix
     d. Apply all fixes to the file at once
     e. Show a diff of changes
     f. Ask for confirmation before writing (unless --auto-approve)
     g. Write the fixed file

4. **Track Progress:**
   - After each file, show:
     - Files completed: X/Y
     - Issues fixed: N
     - Issues remaining: M
   - Continue until all files processed or user stops

5. **Summary:**
   - Total files processed
   - Total issues fixed
   - Any issues that couldn't be fixed automatically
   - Suggest running tests before committing

**Arguments:**
- `$1`: Branch name OR `pr:NUMBER` (required)
  - Branch examples: `main`, `develop`, `feature/my-feature`
  - PR examples: `pr:123`, `pr:456`
- `$2`: Impact Severity filter (optional) - space-separated, default: `HIGH MEDIUM`
  - **New System (recommended):** `BLOCKER HIGH MEDIUM LOW INFO`
  - Old System (deprecated): `BLOCKER CRITICAL MAJOR MINOR INFO` (use `--severity` instead)
- `$3`: Max issues to fetch (optional) - default: `50`

**Environment Variables Required:**
- `SONAR_URL` - SonarQube server URL (e.g., `https://sonarqube.aurecongroup.digital`)
- `SONAR_TOKEN` - SonarQube authentication token (generate in SonarQube UI under User > My Account > Security)
- `SONAR_PROJECT_KEY` - SonarQube project key (NOT the repo name - see "Finding Project Key" below)

**Finding Your SonarQube Project Key:**

The project key follows this pattern: `{GitHub-Organization}_{repository-name}`

Examples:
- Organization: `Aurecon-Creative-Technologies`, Repo: `aurecon-rfi`
- Project Key: `Aurecon-Creative-Technologies_aurecon-rfi`

If you don't know your project key, you can find/construct it:

1. **Auto-detect from GitHub:**
   ```bash
   # Get current repo info
   ORG=$(gh repo view --json owner -q .owner.login)
   REPO=$(gh repo view --json name -q .name)
   PROJECT_KEY="${ORG}_${REPO}"
   echo "Project Key: $PROJECT_KEY"
   ```

2. **Via SonarQube Web UI:**
   - Go to your project in SonarQube
   - Look at the URL or project overview
   - Format: `Organization_repository-name`

3. **Via API (if you have a branch name):**
   ```bash
   # This will show you which project key has issues on your branch
   curl -s -H "Authorization: Bearer $SONAR_TOKEN" \
     "$SONAR_URL/api/issues/search?branch=YOUR_BRANCH_NAME&ps=1" | \
     python3 -c "import sys, json; data=json.load(sys.stdin); print('Project Key:', data['issues'][0]['project'] if data['issues'] else 'No issues found')"
   ```

4. **Ask the user:**
   - If auto-detection fails, ask: "What is your GitHub organization and repository name?"
   - Construct as: `{org}_{repo}`

**Example usage:**
- `/sonarqube-fix develop` - Fix up to 50 HIGH/MEDIUM issues on develop branch
- `/sonarqube-fix main HIGH` - Fix HIGH impact severity issues on main branch
- `/sonarqube-fix pr:123` - Fix up to 50 HIGH/MEDIUM issues in PR #123
- `/sonarqube-fix feature/abc HIGH 100` - Fix 100 HIGH impact issues on branch
- `/sonarqube-fix pr:456 BLOCKER 10` - Fix 10 blocker issues in PR #456
- `/sonarqube-fix develop HIGH MEDIUM LOW 200` - Fix up to 200 HIGH/MEDIUM/LOW issues

**Notes:**
- **Severity Systems:** SonarQube has two severity systems:
  - **Old:** BLOCKER, CRITICAL, MAJOR, MINOR, INFO (use `--severity`)
  - **New (Impact):** BLOCKER, HIGH, MEDIUM, LOW, INFO (use `--impact-severity`) ← **Use this!**
  - The UI shows the new system, so use `--impact-severity` to match what you see
- **Status Filtering:** Always use `--statuses OPEN` to only fetch currently open issues
- **Codebase Filtering:** The script automatically filters out stale issues from old `server/` and `client/` directories
- Fixes are applied file-by-file to handle all issues in a file together
- Each file gets a complete rewrite with all fixes applied
- You can stop at any time between files
- Always review changes before committing
- **Pull request filtering** is only available in SonarQube Developer Edition and higher (not Community Edition)
- When using PR mode, the PR must have been analyzed by SonarQube (check that the PR has quality gate results)
