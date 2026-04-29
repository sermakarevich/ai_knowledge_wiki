"""Sample conversations for the Clio sandbox.

~15 conversations across 6 categories to exercise the clustering pipeline.
Each conversation has short but realistic exchanges.
"""

SAMPLE_CONVERSATIONS = [
    # --- Coding (3) ---
    {
        "messages": [
            {"role": "user", "content": "How do I set up a REST API with Express and handle CORS?"},
            {"role": "assistant", "content": "Install express and cors packages, then configure middleware. Use app.use(cors()) for permissive settings or pass an options object to restrict origins."},
            {"role": "user", "content": "How do I add authentication middleware?"},
            {"role": "assistant", "content": "Create a middleware function that verifies JWT tokens from the Authorization header and attaches the decoded payload to req.user before calling next()."},
        ]
    },
    {
        "messages": [
            {"role": "user", "content": "My Python script crashes with a KeyError when parsing JSON from an API response."},
            {"role": "assistant", "content": "The key might be missing in some responses. Use dict.get() with a default value, or wrap the access in a try/except block to handle missing keys gracefully."},
            {"role": "user", "content": "It also sometimes returns None instead of a dict. How do I guard against that?"},
            {"role": "assistant", "content": "Add a type check before accessing keys: if response_data is not None and isinstance(response_data, dict). You could also use a validation library like pydantic."},
        ]
    },
    {
        "messages": [
            {"role": "user", "content": "Write a SQL query to find the top 10 customers by total order value."},
            {"role": "assistant", "content": "SELECT customer_id, SUM(order_total) AS total_value FROM orders GROUP BY customer_id ORDER BY total_value DESC LIMIT 10;"},
            {"role": "user", "content": "Now join it with the customers table to get their names."},
            {"role": "assistant", "content": "SELECT c.name, SUM(o.order_total) AS total_value FROM orders o JOIN customers c ON o.customer_id = c.id GROUP BY c.name ORDER BY total_value DESC LIMIT 10;"},
        ]
    },
    # --- Writing (3) ---
    {
        "messages": [
            {"role": "user", "content": "Help me write an introduction paragraph for an essay about renewable energy policy."},
            {"role": "assistant", "content": "Here's a draft: As global temperatures rise and fossil fuel reserves dwindle, governments face mounting pressure to transition their energy infrastructure toward sustainable alternatives. This essay examines the effectiveness of current renewable energy policies and proposes reforms to accelerate adoption."},
            {"role": "user", "content": "Can you make it more engaging? Start with a surprising statistic."},
            {"role": "assistant", "content": "In 2023, renewable sources generated more electricity in Europe than fossil fuels for the first time in history -- yet global carbon emissions still reached a record high. This paradox reveals that generating clean energy is only half the battle; the policies governing its deployment determine whether progress translates into impact."},
        ]
    },
    {
        "messages": [
            {"role": "user", "content": "Draft a professional email declining a meeting invitation because of a scheduling conflict."},
            {"role": "assistant", "content": "Subject: Re: Meeting on Thursday\n\nThank you for the invitation. Unfortunately, I have a prior commitment during that time slot. Could we reschedule to later in the week, or would it be possible to share the meeting notes afterward? I'd like to stay in the loop."},
            {"role": "user", "content": "Make it shorter and less formal."},
            {"role": "assistant", "content": "Thanks for the invite! I have a conflict at that time -- could we find another slot, or could someone share notes after? Appreciate it."},
        ]
    },
    {
        "messages": [
            {"role": "user", "content": "I want to write a short story about a lighthouse keeper who discovers something strange in the fog."},
            {"role": "assistant", "content": "The fog rolled in thicker than anything Mara had seen in her twenty years at the lighthouse. When the beam swept across the water, it caught something that shouldn't have been there -- a staircase rising from the waves, carved from pale stone, ascending into the mist."},
            {"role": "user", "content": "Continue the story. What does she do next?"},
            {"role": "assistant", "content": "She trained her binoculars on the staircase. Each step glistened with seawater, and at the edge of visibility, a figure stood motionless on the top step. Mara reached for the radio, then stopped. Whoever -- whatever -- it was, it was looking directly at her."},
        ]
    },
    # --- Research (3) ---
    {
        "messages": [
            {"role": "user", "content": "What are the main approaches to literature review in social science research?"},
            {"role": "assistant", "content": "The main approaches are: (1) narrative review -- a qualitative summary of existing work, (2) systematic review -- following a predefined protocol with explicit inclusion criteria, and (3) meta-analysis -- statistically combining results from multiple studies."},
            {"role": "user", "content": "When should I use a systematic review vs a narrative one?"},
            {"role": "assistant", "content": "Use a systematic review when you need reproducibility and want to minimize bias -- common in health sciences and policy. Narrative reviews work better for exploratory questions or when the literature is too heterogeneous for systematic methods."},
        ]
    },
    {
        "messages": [
            {"role": "user", "content": "How do I handle missing data in a survey dataset?"},
            {"role": "assistant", "content": "Common approaches: listwise deletion (drop incomplete rows), mean/median imputation, multiple imputation (MICE), or model-based methods like EM algorithm. The best choice depends on the missing data mechanism -- MCAR, MAR, or MNAR."},
            {"role": "user", "content": "What's the difference between MAR and MNAR?"},
            {"role": "assistant", "content": "MAR (Missing At Random) means missingness depends on observed variables but not the missing value itself. MNAR (Missing Not At Random) means the probability of being missing depends on the unobserved value -- e.g., high earners not reporting income."},
        ]
    },
    {
        "messages": [
            {"role": "user", "content": "What's the difference between qualitative and quantitative research methodology?"},
            {"role": "assistant", "content": "Quantitative research uses numerical data and statistical analysis to test hypotheses. Qualitative research uses non-numerical data like interviews and observations to explore themes. Mixed methods combine both."},
            {"role": "user", "content": "Can you give me an example of a mixed methods design?"},
            {"role": "assistant", "content": "An explanatory sequential design: first collect survey data (quantitative), analyze it, then conduct follow-up interviews (qualitative) to explain surprising survey results. The qualitative phase deepens understanding of the quantitative findings."},
        ]
    },
    # --- Personal (2) ---
    {
        "messages": [
            {"role": "user", "content": "I'm thinking about switching from engineering to product management. What should I consider?"},
            {"role": "assistant", "content": "Key factors: PM roles focus on strategy, prioritization, and stakeholder management rather than hands-on building. Consider whether you enjoy cross-functional collaboration and ambiguity more than deep technical work."},
            {"role": "user", "content": "How do I build PM experience while still in an engineering role?"},
            {"role": "assistant", "content": "Volunteer to write product specs, run user interviews, or lead sprint planning. Side projects where you own the full product lifecycle also help. Many companies have internal transfer programs."},
        ]
    },
    {
        "messages": [
            {"role": "user", "content": "Help me plan a two-week trip to Japan in autumn."},
            {"role": "assistant", "content": "Autumn in Japan (Oct-Nov) is ideal for foliage. Suggested itinerary: Tokyo (3 days), day trip to Nikko, Hakone (1 day), Kyoto (4 days), Nara day trip, Osaka (2 days), Hiroshima + Miyajima (2 days). Get a 14-day Japan Rail Pass."},
            {"role": "user", "content": "What are the must-see spots in Kyoto for fall foliage?"},
            {"role": "assistant", "content": "Top spots: Tofukuji Temple (famous for maple corridors), Eikando Temple (illuminated night viewing), Arashiyama bamboo grove area, and Kiyomizu-dera. Visit early morning or late afternoon to avoid crowds."},
        ]
    },
    # --- Creative (2) ---
    {
        "messages": [
            {"role": "user", "content": "Create a D&D encounter for a party of four level-5 adventurers in a haunted forest."},
            {"role": "assistant", "content": "The Whispering Hollow: The party enters a clearing where ghostly lights drift between dead trees. A Banshee (CR 4) guards a cursed well. Two Shadow Mastiffs (CR 2 each) patrol the perimeter. The well contains a magic item but triggers a Wight (CR 3) if disturbed."},
            {"role": "user", "content": "Add some environmental hazards and a puzzle element."},
            {"role": "assistant", "content": "The ground is covered in Deathcap Fog (DC 13 CON save or poisoned for 1 minute). Four stone pillars around the well each bear a rune. Players must activate them in the correct order (Arcana DC 15 reveals the sequence). Wrong order summons 1d4 Specters."},
        ]
    },
    {
        "messages": [
            {"role": "user", "content": "Give me a recipe for a spicy Thai-inspired coconut soup."},
            {"role": "assistant", "content": "Tom Kha inspired soup: Saut\u00e9 lemongrass, galangal, and Thai chilies in oil. Add coconut milk and chicken broth. Simmer with mushrooms and chicken or tofu. Finish with lime juice, fish sauce, and fresh cilantro."},
            {"role": "user", "content": "Can you make it vegan and add more vegetables?"},
            {"role": "assistant", "content": "Swap chicken broth for vegetable broth, fish sauce for soy sauce + a pinch of seaweed. Add baby corn, snap peas, bell pepper, and bok choy in the last 5 minutes. Top with crispy shallots and Thai basil."},
        ]
    },
    # --- Education (2) ---
    {
        "messages": [
            {"role": "user", "content": "Explain the chain rule in calculus like I'm a beginner."},
            {"role": "assistant", "content": "The chain rule handles derivatives of nested functions. If you have f(g(x)), the derivative is f'(g(x)) * g'(x). Think of it as peeling layers: differentiate the outer function, keep the inner part, then multiply by the derivative of the inner part."},
            {"role": "user", "content": "Can you walk me through an example with sin(x^2)?"},
            {"role": "assistant", "content": "Outer function: sin(u) where u = x^2. Derivative of sin(u) is cos(u). Derivative of u = x^2 is 2x. Chain rule: cos(x^2) * 2x = 2x*cos(x^2)."},
        ]
    },
    {
        "messages": [
            {"role": "user", "content": "How do I learn to conjugate Spanish verbs in the preterite tense?"},
            {"role": "assistant", "content": "Start with regular -ar verbs: drop -ar, add -\u00e9, -aste, -\u00f3, -amos, -asteis, -aron. Then -er/-ir verbs share endings: -\u00ed, -iste, -i\u00f3, -imos, -isteis, -ieron. Practice with high-frequency verbs like hablar, comer, vivir."},
            {"role": "user", "content": "What about irregular preterite verbs?"},
            {"role": "assistant", "content": "Key irregulars to memorize: ser/ir (fui, fuiste, fue...), hacer (hice, hiciste, hizo...), tener (tuve, tuviste, tuvo...). These share a pattern: irregular stems with unstressed endings (-e, -iste, -o, -imos, -isteis, -ieron)."},
        ]
    },
]
