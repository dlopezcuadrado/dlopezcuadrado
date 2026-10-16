# AGENTS.md — dlopezcuadrado (GitHub profile)

`README.md` is rendered as the GitHub profile page for `dlopezcuadrado`. `LINKEDIN_IMPROVEMENTS.md` holds the drafted LinkedIn profile copy.

## Backlog

Work is tracked in GitHub Issues: **[dlopezcuadrado/dlopezcuadrado](https://github.com/dlopezcuadrado/dlopezcuadrado/issues)**. This repo has no TODO or roadmap file, and none should be added - anything that needs doing is a GitHub issue.

- **Pick work** from the repo's open issues, highest priority first (`priority: urgent` → `high` → `medium` → `low`). Skip issues labelled `blocked`: they wait on something only the owner can do, described in the issue.
- **Start**: add the `in progress` label (`gh issue edit <n> --add-label "in progress"`). Work directly on `main` - no feature branches.
- **Commits** cite the issue number: `fix(#7): add rollback to the deploy script`. GitHub then links the commit to the issue. The commit that finishes the issue also says `Closes #7` in its body.
- **Finish**: the issue closes when that commit lands on `main` (otherwise `gh issue close <n>`). Git history is the record of what happened - no "done" lists in files.
- **Found something new?** Open an issue in this repo (`gh issue create`) with a label (`bug`, `feature`, `improvement`, plus a `priority:` label; add `blocked` plus what's needed if it depends on the owner) instead of a TODO in a file.
- **Old Linear IDs** (`DLO-123`) in commits and docs come from the retired Linear workspace. Open issues were moved here with their old ID in the body: `gh issue list --search DLO-123 --state all`.
- **No GitHub access** in this session (`gh` not signed in)? Say so and ask - don't recreate a backlog file.
