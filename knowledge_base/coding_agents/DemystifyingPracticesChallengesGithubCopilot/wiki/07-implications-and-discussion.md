> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Implications and Discussion
**In one sentence:** The study derives empirically grounded implications urging use of mainstream IDEs, leveraging Copilot for front-end and ML work, releasing specialized Copilot versions, weighing its double-edged trade-offs, and adding code-explanation and suggestion-customization features to enable effective use.
## Key points
- Mainstream IDEs (VS Code, Visual Studio, IntelliJ IDEA, NeoVim, PyCharm) account for 86.2% of Copilot usage, with smoother installation and easier community solutions on SO/GitHub Discussions.
- Using Copilot with lesser-known IDEs (e.g., Sublime Text) causes integration difficulty because the IDE is not officially supported and few peers can offer fixes, so practitioners are advised to use mainstream IDEs while GitHub should support more IDEs.
- Practitioners most often pair JavaScript with front-end element control and Python with ML tasks (data and image processing), reflecting JavaScript's web-client dominance and Python's rich ML libraries such as OpenCV.
- Needed Copilot variants include a team version, a CLI version, and an on-premises version, alongside existing Copilot Labs (experimenting with new ideas), Copilot X (enhancement with new features), and Copilot Nightly (experimental, less well tested changes).
- Copilot is a double-edged sword: benefits such as useful code generation contradict limitations such as limitation to code generation, requiring trade-offs over integration, user experience, budget, and code privacy.
- Understanding generated code is contested — some praise Copilot's code interpretation while others report difficulty understanding output and request explanation features such as auto-generated code comments in the IDE.
- Users demand suggestion customization: changeable accept-suggestion keybinding (currently only Tab), configurable color/font/format to distinguish their code from suggestions, and partial acceptance (line by line or next word only), plus filters, configurable IDE UI, and selectable training sources.
---
## Integration of Copilot with IDEs
**Covers:** Section 5, implications on IDE integration (RQ1.2, RQ2.2)

Most developers integrate Copilot with mainstream IDEs (Visual Studio Code, Visual Studio, IntelliJ IDEA, NeoVim, PyCharm), and "the percentage of mainstream IDEs used with Copilot by practitioners reaches 86.2%". Causes of integration difficulty: incorrect installation in the chosen IDE, and Copilot not supporting certain IDEs. Mainstream-IDE users "can install it smoothly, and even if problems arise during the installation or use, they can easily find a solution on SO or GitHub Discussions"; unpopular-IDE users "may not be able to install it because the IDEs are not officially supported by Copilot". Recommendation: practitioners should use mainstream IDEs; GitHub should integrate Copilot with more IDEs, matching the most expected feature and the RQ2.2 finding that difficulty of integration is the main limitation.

## Support for Front-end and Machine Learning Development
**Covers:** Section 5, implications on languages and technologies (RQ1.1, RQ1.3, RQ1.4)

Practitioners often write JavaScript and Python with Copilot and use front-end and machine learning related technologies (frameworks, APIs, libraries) to implement "front-end (e.g., front-end element control) and machine learning functions (e.g., data processing and image processing)". Rationale given: "JavaScript is the foundation language of many popular front-end frameworks and most of Websites use JavaScript on the client side" and "Python is the first choice when it comes to the development of machine learning solutions with the help of rich libraries, e.g., OpenCV."

## Different Versions of Copilot
**Covers:** Section 5, implications on Copilot variants (RQ2.3)

From RQ2.3, "different versions of Copilot are needed (i.e., a team version, a version for CLI (Command-Line Interface), and a on-premises version)". Releasing them "would increase the usability and acceptance of Copilot and thus make it available to a wider variety of users". Existing versions: "Copilot Labs [25] is used to experiment with new ideas before taking them into real production, Copilot X [26] provides an enhancement with new features, and Copilot Nightly contains experimental and less well tested changes."

## Potentials and Perils of Using Copilot in Software Development
**Covers:** Section 5, trade-offs discussion (RQ2.1, RQ2.2)

"Trained on billions of lines of code, Copilot can turn natural language prompts into coding suggestions across dozens of programming languages and make developers code faster and easier [4]." RQ2.1/RQ2.2 show "many benefits of using Copilot contradict its limitations and challenges, e.g., useful code generation vs. limitation to code generation". Developers "should consider tool integration, user experience, budget, code privacy, and some other aspects, and make trade-offs between these factors". Verbatim: "using Copilot is like a double-edged sword". If used with appropriate languages/technologies for required functions in developers' IDEs, it "will certainly optimize developers' coding workflow and do what matters most - building software by letting AI do the redundant work"; otherwise it brings "difficulties and restrictions to development, making developers feel frustrated and constrained."

## Understanding the Code Generated by Copilot
**Covers:** Section 5, code-comprehension implications (RQ2.1, RQ2.2, RQ2.3)

Some practitioners cite "powerful code interpretation feature" as a benefit, while others "complained about the difficulty of understanding the generated code by Copilot and called for code explanation feature". Open questions: "why developers have opposing attitude towards understanding the code generated by Copilot and how the generated code by Copilot can be better explained to and understood by developers". Copilot Labs (dependent on Copilot extension) "has the feature to provide explanations of the code generated by Copilot for developers [25]" and "The latest Copilot X also has the code explanation feature [26]", but "we do not know the reason why developers do not use Copilot Labs or Copilot X to interpret Copilot-generated code". Suggestion: "Copilot can provide the features for developers to better understand the generated code directly, such as generating code comments with the generated code in IDEs."

## Users' Customization on Suggestions by Copilot
**Covers:** Section 5, customization implications (RQ2.2, RQ2.3)

Per RQ2.2, lack of customization is a limitation; per RQ2.3, developers call for "customization of shortcuts for suggestions", "customization of the format of generated code", and "accept the needed part of the suggestions". Details: users "can only accept suggestions via the tab key" but want '"an option to change the keybinding for accepting the suggestions" instead (GitHub #6919)'; they find it "hard to distinguish between the code wrote by themselves and the code suggested by Copilot" and "wanted to customize the color, font, and format of Copilot suggestions"; they want to "accept Copilot suggestions line by line or accept only the next word of Copilot suggestions each time" rather than the entire suggestion. Related expected features: "allow setting filters for suggestions, suggestions in IDE UI can be configured, and ability to select the training sources for suggestions". Conclusion: "it is necessary for Copilot to allow customization for suggestions".

## Towards an Effective Use of Copilot
**Covers:** Section 5, future-research directions

Further practices research "can be conducted by questionnaire and interview". Worth exploring: "Under what conditions the challenges of using Copilot will show up as advantages or disadvantages, and how to use Copilot to convert its disadvantages into advantages". Although limitations and challenges were investigated, the study "did not looked in depth at what types of users (e.g., developers, educators, and students) who use Copilot, when and how they use Copilot".
