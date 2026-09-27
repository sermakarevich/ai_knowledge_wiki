[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Purposes, Benefits, Limitations and Challenges (RQ2.2–RQ2.3)
**In one sentence:** Users report 15 limitations topped by IDE-integration difficulty (114, 28.1%) and access difficulty (69, 17.0%), plus code-generation limits, poor quality, and privacy concerns, and respond with 29 expected features led by support for more IDEs (32, 28.8%) and shortcut customization (12, 10.8%).
## Key points
- Table 5 lists 15 limitations and challenges (RQ2.2); the top two are difficulty of integration (114, 28.1%) and difficulty of accessing Copilot (69, 17.0%).
- Integration difficulty means plug-ins stop working after Copilot installation, shortcut-setting conflicts, no support for some editors, plus server instability, no proxy support, and region access restrictions blocking access.
- Code-generation constraints include too few solutions ("multiple solution is too little", GitHub #37304) and a ~1000-character response limit (GitHub #15122), reported by 48 users (11.8%).
- Poor generated-code quality was reported by 36 users (8.9%), with quotes "GitHub Copilot suggest solutions that don't work" (SO #73701039) and quality that "becomes unacceptable" as files get larger (GitHub #9282).
- Code-privacy threat was reported by 29 users (7.1%), who worried Copilot may use their code information without permission.
- Unfriendly user experience (25, 6.2%) contrasts with the benefit-tail quote that Copilot is "a lot more fun to use and does not annoy me like some other AI systems" (GitHub #7254), whose other products are unnamed.
- Difficulty of subscription (22, 5.4%) increased significantly versus previous work [9], attributed in the chunk to free-plan restrictions, e.g. "so looks like people with a free plan are stuck on a rate-limit for now with no way out" (GitHub #43893).
- Table 6 lists 29 expected features (RQ2.3), led by integration with more IDEs (32, 28.8%), shortcut customization (12, 10.8%), and suggestions only when requested (8, 7.2%) because always-on suggestions are interruptive.
---
## Benefit tail: comparison with other products
One practitioner said Copilot is "a lot more fun to use and does not annoy me like some other AI systems" (GitHub #7254), without providing the names of the other products.

## RQ2.2: What are the limitations & challenges of using GitHub Copilot?
Table 5 lists 15 limitations and challenges of using Copilot. Most developers pointed out the difficulty of integration between Copilot and IDEs or other plug-ins: after Copilot was installed, certain plug-ins did not work and Copilot may conflict with some shortcut settings of the editors, and Copilot cannot be successfully integrated with some IDEs as it does not support these editors yet. Due to server instability, no support for proxies, and access restriction of some regions, developers may have difficulties accessing Copilot. The suggested code sometimes offers few solutions, "which are not enough for users, which brings limitation to code generation", e.g. "multiple solution is too little" (GitHub #37304). Practitioners complained about poor quality of generated code, e.g. "GitHub Copilot suggest solutions that don't work" (SO #73701039), and quality that "becomes unacceptable" when code files became larger (GitHub #9282). Developers worried about code privacy threat, i.e. Copilot may use their code information without permission. Contrary to developers who said Copilot gave a better user experience than other AI-assisted programming tools, some practitioners reported an unfriendly user experience. Compared with previous work [9], difficulty of subscription increases significantly, possibly caused by restrictions for free users, e.g. "so looks like people with a free plan are stuck on a rate-limit for now with no way out" (GitHub #43893).

| Limitation & Challenge | Example | Count | % |
|---|---|---:|---:|
| Difficulty of integration | Copilot only works with VSCode, VSCodium is not supported at the moment (GitHub #14837) | 114 | 28.1% |
| Difficulty of accessing Copilot | I cannot connect to the GitHub account and the Copilot server in VSCode, also cannot use the Copilot plugin (SO #74398521) | 69 | 17.0% |
| Limitation to code generation | Copilot is limited to around 1000 characters in the response (GitHub #15122) | 48 | 11.8% |
| Poor quality of generated code | Github Copilot suggest solutions that don't work (SO #73701039) | 36 | 8.9% |
| Code privacy threat | Copilot does collect personal data so just take precaution when working in private repos (GitHub #7163) | 29 | 7.1% |
| Unfriendly user experience | I had the same problem today, an amazing tool with poor user experience (GitHub #8468) | 25 | 6.2% |
| Difficulty of subscription | My copilot subscription suddenly stopped. Tried log out and in. Never have reply on support ticket over 10 days (GitHub #36190) | 22 | 5.4% |
| High pricing | it is obvious that no one in South America will pay that price, it is too expensive (GitHub #24594) | 14 | 3.4% |
| Lack of customization | My question is about setting up shortcuts in Visual Studio Code VSCode for GitHub Copilot Labs. (SO #73564811) | 13 | 3.2% |
| Difficulty of understanding the generated code | I really do not understand this enough, and have no idea half of what this code does honestly. It was written by Copilot. (SO #72282605) | 12 | 3.0% |
| Hard to configure | Keep getting "Your Copilot experience is not fully configured, complete your setup" in Visual Studio 2022 (GitHub #19556) | 10 | 2.5% |
| No edition for organizations | Currently, Copilot is only available for individual user accounts and organizations aren't able to purchase/manage Copilot for their members just yet (GitHub #32775) | 8 | 2.0% |
| Show loading | I am not sure what is causing this but while editing files within Visual Studio, I am periodically locking up with the following dialog showing (SO #73682137) | 3 | 0.7% |
| Challenge of not providing outdated suggestions | making sure that the tool does not provide outdated suggestions would still be a challenge (SO #72554382) | 2 | 0.5% |
| Need of basic programming knowledge | It is useless if you do not understand the programming language or the task you want to do (GitHub #35850) | 1 | 0.2% |

## RQ2.3: What are the expected features of users about GitHub Copilot? (partial, as present in chunk)
Table 6 presents 29 features users expected. The most mentioned is integration with more IDEs (28.8%); given the dominant RQ2.2 limitation is difficulty of integration, the chunk calls this reasonable. 10.8% wanted customization of shortcuts for suggestions, e.g. "Github CoPilot should give us an option to assign a custom key instead of a [TAB] or should change to something like [SHIFT + TAB] instead of TAB" (GitHub #7036). Eight users (7.2%) expected suggestions when requested, not all the time, because always-on suggestions were interruptive, e.g. "Is it possible to not have GitHub Copilot automatically suggest code, instead only showing its suggestions when using the 'trigger inline suggestion' shortcut?" (SO #76147937). Seven developers each expected a team version and proxy access support. Five wanted customization of the format of generated code, to "configure suggestion appearance" (GitHub #7234) so suggestions are "more distinguishable with normal code" and "improve the accessibility" (GitHub #7628). Few wanted to "accept one line of several" of suggested code (SO #75183662), i.e. accept only the needed part of suggestions. Four hoped Copilot could be compatible with other code generation tools like ReSharper.

| Expected Feature | Count | % |
|---|---:|---:|
| Can be integrated with more IDEs | 32 | 28.8% |
| Allow customization of shortcuts for suggestions | 12 | 10.8% |
| Give suggestions when requested | 8 | 7.2% |
| A team version | 7 | 6.3% |
| Support access proxies | 7 | 6.3% |
| Allow customization of the format of generated code | 5 | 4.5% |
| Accept the needed part of the suggestions | 4 | 3.6% |
| Compatible with other code generation tools | 4 | 3.6% |
| Allow setting filters for suggestions | 3 | 2.7% |
| Allow self-signed certificates | 3 | 2.7% |
| Can be used with more development frameworks | 2 | 1.8% |
| Ability to turn off data collection | 2 | 1.8% |
| Suggestions in IDE UI can be configured | 2 | 1.8% |
| Code explanation | 2 | 1.8% |
| Free for certain type of users | 2 | 1.8% |
| Provide more suggestions at a time | 2 | 1.8% |
| Provide more complete suggestions | 2 | 1.8% |
| Ability to draw UML digrams [sic, as in chunk] | 1 | 0.9% |
| Enable a dialog to accept or deny suggestions | 1 | 0.9% |
| A version for CLI (Command-Line Interface) | 1 | 0.9% |
| A on-premises version | 1 | 0.9% |
| Ability to select the training sources for suggestions | 1 | 0.9% |
| Can be used in remote servers | 1 | 0.9% |
| Provide a getting started guide | 1 | 0.9% |
| Provide a security rating for generated code | 1 | 0.9% |
| Remind users when it has no suggestions | 1 | 0.9% |
| Show acceptance rate of suggestions | 1 | 0.9% |
| View the code-related data shared by Copilot | 1 | 0.9% |
| Disable notification sounds of suggestions | 1 | 0.9% |

**Covers:** RQ2.2–RQ2.3 results in chunk 06 (benefit-tail quote, Table 5 limitations/challenges, Table 6 expected features); plan slug 06-the-other-products-out-there-it.
