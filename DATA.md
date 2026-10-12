# Data sources, licenses and citations

Raw data never goes on `main`. It lives on the orphan `data` branch (gzipped,
split into <90 MB parts) and is rebuilt locally with
`python3 scripts/restore_data.py`.

| Source | How it gets here | Login? | Redistribution | Cite |
|---|---|---|---|---|
| GSS 1972–2024 cumulative (Release 3), via the `gssr` R package | GitHub Action | No | gssr is MIT-licensed; GSS terms ask for responsible use and citation | Davern, Bautista, Freese, Herd & Morgan, *General Social Survey 1972–2024*, NORC at the University of Chicago; Healy, *gssr* (R package) |
| Voteview members, roll calls, votes | GitHub Action | No | Free public data | Lewis, Poole, Rosenthal, Boche, Rudkin & Sonnet, *Voteview: Congressional Roll-Call Votes Database*, voteview.com |
| CES 2024 Common Content | GitHub Action (Harvard Dataverse API) | No | Check the dataset's license on Dataverse before redistributing (doi:10.7910/DVN/X11EP6) | Schaffner, Ansolabehere & Shih, *Cooperative Election Study Common Content, 2024* |
| CES cumulative 2006–2024 | GitHub Action (Dataverse) | No | Check license (doi:10.7910/DVN/II2DB6) | Kuriwaki, *Cumulative CES Common Content* |
| ANES 2024 Time Series | You download it, then `scripts/push_local_data.sh anes <zip>` | Yes | Terms restrict redistribution: **private repo only** | American National Election Studies, *ANES 2024 Time Series Study* |
| Pew ATP / Typology 2026 microdata | You download it, then `scripts/push_local_data.sh pew <zip>` | Yes | Terms restrict redistribution: **private repo only** | Pew Research Center, *American Trends Panel Wave 183* |

Before publishing anything derived from these, re-read each source's current
terms. Item wordings are reused with attribution; the Political Compass's
items are copyrighted and are not used anywhere in this project.

## Getting the data

**Public sources (GSS, Voteview, CES):** GitHub → Actions → "Fetch public
data" → Run workflow. It also runs monthly. The Action's log lists anything
that failed.

**ANES 2024:**
1. Sign in at electionstudies.org and download the 2024 Time Series CSV zip.
2. Make sure the repo is private (Settings → General → Danger Zone → Change
   visibility), or point the script at a separate private repo with
   `DATA_REMOTE=<remote-name>`.
3. From the repo folder: `scripts/push_local_data.sh anes ~/Downloads/<the zip>`

The script refuses to push to a public repo when the GitHub CLI (`gh`) is
installed, unless you override it with `ALLOW_PUBLIC=1`.
