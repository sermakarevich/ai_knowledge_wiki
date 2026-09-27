> [[index|Wiki]] | [[summary|Summary]]
# Agentflow — In Plain Language

## What is this about?

Think of a busy kitchen making a big dinner from one recipe card.
One cook writes the plan for the night.
Then the head cook copies the same small job many times and hands
one copy to each cook, so all cooks work side by side at the same time.
Each cook works in a small corner of the kitchen that belongs only
to them, so they do not bump into each other.

When the cooks finish, a helper gathers all their dishes and combines
them into a few shared bowls, and then into one final plate.
Before the plate goes out, one trusted cook tastes it.
If the taste is wrong, the dish goes back for fixing, again and again,
until the taste is right or the kitchen decides to stop trying.
Every move is written down in a log book, so anyone can later see
who did what and what happened.

That kitchen is what this system is.
It is a way to write down a big job with smart helpers,
split it into many small jobs that run at the same time,
bring the answers back together, check the answers,
and repeat the weak parts until they are good enough.

## Why does it matter?

Big jobs with smart helpers get messy fast.
People lose track of who was asked to do what.
Two helpers may change the same file at the same time.
A bad answer may slip through because nobody checked it.
A job that fails may stop everything, or run forever in a loop.

This system fixes that mess in a simple way.
It gives you one clear recipe card for the whole job.
It keeps each helper in its own work area.
It limits how many helpers work at once, so the kitchen is not crowded.
It checks each answer with a clear pass-or-fail taste test.
It sends bad work back for another try, but only for a set number of tries.
And it saves all outputs and notes, so you can replay what happened.

## How does it work?

1. Write a recipe card with a name and shared settings, such as where
   the work happens, how many helpers may work at once, and how many
   repeat tries are allowed.

2. List the small jobs in order, such as first make a plan,
   then build it, then check it, then write a short summary.

3. Draw lines between jobs to show what must finish first.
   A later job waits until the jobs before it are done.

4. For heavy work, take one job card and copy it many times.
   Each copy gets a number and its own small work corner,
   plus its own slice of the work, like pages 1 to 10 for copy 1.

5. Let all copies run at the same time, up to the limit you set.
   If the limit is three, only three copies cook at once
   and the rest wait for a free spot.

6. After the copies finish, combine their answers.
   You can combine in small groups, such as 16 copies into 8 short reports,
   or group by topic, such as one combined report per town or per book.

7. Let later jobs read earlier answers through fill-in blanks.
   For example, the build job can say, here is the plan from the first job,
   now please build it, and the plan text is pasted in by itself.

8. Give each checking job a clear pass rule, such as the answer must hold
   the words looks good, or a certain file must exist and not be empty.

9. If a check fails, send the work back one step for fixing.
   The fixer sees the last review notes and tries again.
   This taste-and-fix loop runs until the check passes.

10. If work keeps failing, try the same small job a few times with short
    rests in between, getting longer after each miss.

11. Stop the loop after the max number of tries you set.
    Skipped work stays skipped if the job before it did not finish well.

12. Save everything as you go: what ran, what passed, what failed,
    the final words from each job, and a line-by-line event list.
    You can open these files later to see the full story.

## Where can this be used?

Use it when one big writing or coding job should be split into many
small tries, such as reading many files, trying many fixes,
or testing many ideas at once and then picking the best parts.

Use it when answers must be checked before they move on,
such as write a draft, let another helper review it,
fix the problems, and only then share the final text.

Use it when many helpers must not clash,
such as each helper owns one folder, writes notes in a shared place
with care, and all work is gathered into one clean handoff report.

Use it when you want a clear record,
such as what each helper said, how many tries it took,
and where the final answer came from.

## Conclusions & takeaways

Big helper jobs work best with a clear recipe, small owned work areas,
limited side-by-side work, simple combine steps, and honest taste tests.
Split wide when there is lots to cover, bring answers together early,
and loop back only where the check says more work is needed.
Set a firm stop count so loops always end.
Keep every output and event, because the log is how you learn
what helped, what failed, and what to change next time.
Start small with plan, build, check, and summary,
then grow to many copies and group combines once the small shape works.

## Jargon decoder

| Term | What it means in plain words |
| --- | --- |
| DAG | A job map with no endless loops, where each step waits for the steps before it |
| fanout | Copying one job card into many copies that run side by side |
| merge/reducer | A helper step that gathers many answers and combines them into fewer reports |
| node | One single small job or step on the recipe card |
| LGTM | Short for looks good to me, a pass word that means the check is happy |
| harness | The outer frame that starts helpers, feeds them jobs, and collects answers |
| SSH | A safe locked door for running work on another computer far away |
| EC2 | Rented computers from a cloud company that you can turn on and off |
| ECS | A cloud helper that runs many small boxed-up jobs for you |
| Jinja template | A fill-in-blank note where names in curly marks get replaced with real answers |
| concurrency | How many helpers are allowed to work at the very same time |
| success_criteria | The pass rules a job must meet, like holding certain words or making a file |
