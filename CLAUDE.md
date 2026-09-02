@AGENTS.md

# Workflow

Never push to `main`. Every change lands through a pull request.

This rule overrides any global instruction that says to commit and push to the
base branch automatically. It applies to every change, including a one-line
data fix.

## Task: close an issue

1. Create a branch off `main`. Name it `<type>/issue-<number>-<slug>`, for
   example `feat/issue-13-verboo`.
2. Commit your work on that branch. Use Conventional Commits.
3. Push the branch with `git push -u origin <branch>`.
4. Open a pull request with `gh pr create`. Write `Closes #<number>` in the
   body, so the merge closes the issue.
5. Report the pull request URL. Stop there.

Do not merge the pull request. The user reviews it and merges it.

## Rules

1. Ask before you push a branch that no issue tracks. The user may want a
   different name or a different base.
2. Never run `git push --force` or `git push --force-with-lease`.
3. Never push to `main`, even when the working tree is clean and the build
   passes. A green build is not approval to merge.
4. Run `python build.py --check` before you open the pull request. Fix every
   error it prints.
5. One pull request per issue. Do not bundle two issues into one branch.
