# AGENTS.md — dlopezcuadrado (GitHub profile)

`README.md` is rendered as the GitHub profile page for `dlopezcuadrado`. `LINKEDIN_IMPROVEMENTS.md` holds the drafted LinkedIn profile copy.

## Editing the profile

Everything you read on the profile is plain text in `README.md`; only the activity card is generated.

- **Hero**: the centred name, role line and link badges at the top.
- **Career**: a Mermaid `timeline` block that GitHub draws. One line per step, `Period : Title` followed by `: Team` lines. Keep colons out of the text.
- **Side projects**: a two-column HTML table. Each cell is one project, in this shape, blank lines included:

  ```
  <td width="50%" valign="top">

  **🏠 [Name](https://url)**<br>
  One sentence on what it does.<br>
  <sub>Stack · Stack · Stack</sub>

  </td>
  ```

  Add projects two per `<tr>`. Only list projects that are David's own and public or live; check `isFork` before listing a repo.
- **Stack**: a Markdown table, one row per area.
- **Activity**: `assets/activity-light.svg` and `assets/activity-dark.svg`, shown through a `<picture>` that follows the viewer's GitHub theme. `.github/workflows/activity-card.yml` regenerates both daily from `.github/scripts/activity_card.py`; never edit the SVGs by hand.

Wording: describe AI in general (agents, LLM integrations), never a single tool, and never imply AI does most of the work.

## Backlog

Work is tracked in GitHub Issues: **[dlopezcuadrado/dlopezcuadrado](https://github.com/dlopezcuadrado/dlopezcuadrado/issues)**. This repo has no TODO or roadmap file, and none should be added - anything that needs doing is a GitHub issue.

- **Pick work** from the repo's open issues, highest priority first (`priority: urgent` → `high` → `medium` → `low`). Skip issues labelled `blocked`: they wait on something only the owner can do, described in the issue.
- **Start**: add the `in progress` label (`gh issue edit <n> --add-label "in progress"`). Work directly on `main` - no feature branches.
- **Commits** cite the issue number: `fix(#7): add rollback to the deploy script`. GitHub then links the commit to the issue. The commit that finishes the issue also says `Closes #7` in its body.
- **Finish**: the issue closes when that commit lands on `main` (otherwise `gh issue close <n>`). Git history is the record of what happened - no "done" lists in files.
- **Found something new?** Open an issue in this repo (`gh issue create`) with a label (`bug`, `feature`, `improvement`, plus a `priority:` label; add `blocked` plus what's needed if it depends on the owner) instead of a TODO in a file.
- **Old Linear IDs** (`DLO-123`) in commits and docs come from the retired Linear workspace. Open issues were moved here with their old ID in the body: `gh issue list --search DLO-123 --state all`.
- **No GitHub access** in this session (`gh` not signed in)? Say so and ask - don't recreate a backlog file.
