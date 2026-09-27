> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Advanced structure

**In one sentence:** Instructions, Choice options, Score levels, and Noul criteria all accept JSON structure (string, object, array, or null), letting labeled keys, supporting data, and examples carry meaning the model actually uses.

## Key points

- System One models are trained to understand structure: every `instructions` field and every Choice option, Score level, and Noul `true`/`false` description is an `EntryType` accepting `string`, `object`, `array`, or `null`.
- Structure when it helps clarity (multi-part questions read better as labeled JSON keys) or when the question needs supporting data (a schema, taxonomy, or database row can be passed as JSON instead of serialized into a string template).
- One shared `field` object shape can drive all three primitives at once: the invoice example uses the same field-description pattern for a Noul verifying a value, a Choice picking among candidates, and two Scores placing values on scales.
- Choice options accept rubric objects (`what` / `not_for` / `examples`) that sharpen boundaries — e.g. billing vs orders vs account — and whole taxonomy subtrees as values, so the model sees what lives under a branch before committing to it.
- Walking a deep taxonomy means asking one Choice per level with the current node's children as options, using `probabilities` to decide whether to explore both branches, trimming oversized subtrees, and optionally beam-searching the best K paths.
- Score levels accept objects like `{summary, signals}` (PR-focus example) and `{what, examples}` mirroring the Score page's finding that matching examples concentrate probability on one level.
- Noul's optional `criteria` accepts structured `true`/`false` objects (`what` plus `examples` on each side), as in the credential-request check that inspects `message` for a request to send the credential itself rather than reset it.

---

## Core claim

Two verbatim claims open the source:

> "Instructions, Choice options, Score levels, and Noul criteria all accept JSON structure."

> "System One models are trained to understand structure."

## Where structure is allowed

"Every one of these fields is an [`EntryType`](/sdk/javascript/api/type-aliases/EntryType)."

| Field | Applies to | Accepted shape |
|---|---|---|
| `instructions` | Choice, Score, Noul | `string`, `object`, `array`, or `null` |
| `criteria` values (option descriptions) | Choice | `string`, `object`, `array`, or `null` |
| `criteria` entries (level descriptions) | Score | `string`, `object`, `array`, or `null` |
| `criteria.true` and `criteria.false` | Noul | `string`, `object`, `array`, or `null` |

## When to structure a question

- "**When it helps with clarity.** When a question has multiple parts, putting them in the form of JSON helps with clarity because the keys are labeled."
- "**When question needs supporting data.** A schema, a taxonomy, or a database row is already JSON. Use the JSON entirely or pass in the relevant subfields instead of serializing them into a string template."

## Structured instructions

"One `field` object describes the field being checked, and each question refers to it by key. The same shape drives a Noul that verifies a value, a Choice that picks one from candidates, and two Scores that place a value on a scale."

Reference request: state `{source_text: 'Invoice #4471 issued March 3, 2026 to Beaver Dam Logistics for $12,840.00, net 30.'}`, model `jev-latest`, four questions sharing the `field` + `question` shape:

| Question | Type | Field | Question text |
|---|---|---|---|
| `invoice_number_is_correct` | noul | `{name: invoice_number, type: string, description: 'The identifier printed on the invoice.'}` + `extracted_value: '4471'` | 'Does `extracted_value` match the `field` as it appears in `source_text`?' |
| `customer_name` | choice | `{name: customer_name, type: string, description: 'The organization the invoice was issued to.'}` | 'Which option is the value of `field` in `source_text`?' (options: 'Beaver Logistics', 'Dam Logistics', 'Beaver Dam Logistics', 'Beaver', 'Dam', all null) |
| `amount_due` | score | `{name: amount_due, type: number, unit: USD, description: 'The total the invoice asks to be paid.'}` | 'How large is the `field` value in `source_text`?' (levels: Under $1,000 / $1,000–$10,000 / $10,000–$100,000 / $100,000–$1,000,000 / Over $1,000,000) |
| `payment_terms` | score | `{name: payment_terms, type: integer, unit: days, description: 'Days allowed for payment, from terms such as "net 30".'}` | 'How many days does the `field` in `source_text` allow for payment?' (levels: Due on receipt / Net 10 / Net 30 / Net 60 / Net 90) |

"In code, you could loop over the potential records and build one of these questions per field, all sent in a single call. The [SDE cascade cookbook](/cookbooks/sde_cascade) does something similar to this."

Arrays work too — "Use one when the instruction is a list of things to check or to compare":

```json
"instructions": {
  "question": "Does the claimed sender identity conflict with the sending domain?",
  "compare": ["ticket.sender.display_name", "ticket.sender.email"],
  "focus": "Compare the named organization with the email domain."
}
```

## Structured Choice options

"A Choice option description can be a structured object as well."

### JSON rubric for boundary clarification

Reference: state `'I ordered the standing desk two weeks ago and tracking still says label created. Was I even charged?'`, instructions `{question: 'Which team should handle this message?', focus: "Classify the customer's primary request, not every topic mentioned."}`, criteria `billing` (`what`: 'Charges, invoices, refunds, or subscriptions'; `not_for`: 'Order tracking or account access'; `examples`: ['I was charged twice', 'Where is my refund?']), `orders` (status/delivery/cancellation/returns; not charges or account access), `account` (login/password/profile/security; not charges or delivery). "The example tells the model what each option does and does *not* cover. It sharpens the boundary between options."

### Walking a taxonomy

"To classify into a deep taxonomy, ask one Choice per level and walk the tree in code. At each step the options are the children of the current node, and each option's value is the child's tree. Doing so lets the model see what lives under a branch before committing to it, which matters when the item belongs to a leaf whose name is not obvious from the branch name alone."

Reference: state `"32oz plastic bottle with a flip straw lid. Fits most bike cages."`, first question picks a top-level department with subtree values (`Sporting Goods` → Cycling/Fitness/Outdoor with leaf lists; `Home & Kitchen` → Drinkware/Cookware; `Baby & Toddler` leaf list). "The bottle plausibly fits under two departments. Showing the subtrees lets the model see that both `Sporting Goods > Cycling > Bike Bottles & Cages` and `Home & Kitchen > Drinkware > Water Bottles` exist, and weigh the listing's emphasis on bike cages against everyday drinkware. The `probabilities` on this answer tell you whether the split is close enough to explore both branches."

"Once a department is chosen, ask the next Choice with that department's children as the options and their subtrees as the values, and repeat until you reach a leaf. In code this could be a loop over a nested dict, where each question's `criteria` is simply the current node." The Hierarchical Classification cookbook "shows an example of a similar walk of the tree, including a beam search that keeps several candidate paths alive when the probabilities are close." Caveat: "Subtrees can get large. If a branch is too large, trim the value to its direct children and a sample of leaves."

## Structured Score levels

"Each entry in a Score `criteria` array can be an object." Reference: state `'Fixed the null check in the payment handler. Also refactored the retry loop while I was in there, and bumped the SDK version since the old one had that timeout bug.'`, instructions `{question: 'How focused is this pull request description on a single change?', note: 'Judge the number of independent changes, not the size of any one change.'}`, three levels with `{summary, signals}` — 'One change, clearly stated' / 'One main change plus a small related tweak' / 'Several independent changes bundled together', each with two signal strings (e.g. 'A single fix or feature', 'Nothing described as "also" or "while I was in there"').

## Structured Noul criteria

"Noul `criteria` is optional, and when the yes/no boundary is subtle, structured `true` and `false` descriptions let you pin it down with a definition and examples on each side." Reference: state `{sender: {display_name: 'Beaver Dam Builders Ltd.', email: 'donotreply@payroll.example'}, message: 'Your Q3 bonus is ready. Reply with your login password so we can verify your identity and release the funds.'}`, question `requests_credentials` with instructions `{question: 'Does the `message` ask the recipient to disclose a sensitive credential?', inspect: 'message', focus: 'Look for a request to send the credential itself, not a request to change or reset it.'}` and criteria `true` (`what`: 'Asks the recipient to reply with, type, or send a password, PIN, one-time code, or other security sensitive answer'; `examples`: ['Reply with your password', 'Send us the 6-digit code you just received']) vs `false` (`what`: 'No sensitive credential is requested'; `examples`: ['Reset your password from the settings page', 'Your statement is ready']).

**Covers:** https://docs.typesafe.ai/primitives/advanced-structure
