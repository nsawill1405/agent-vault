---
name: parallel-agents
description: "Use at the start of any task with more than one independent part. Split the work into parallel subagents with distinct roles (explorer, implementer, reviewer, tester) and coordinate their results."
triggers:
  - user
  - model
allowed-tools:
  - read
  - grep
  - glob
  - exec
---
# Parallel agents

William wants agents to split tasks and work in parallel with different roles, to get code written quickly. See [[Workflow Preferences]]. Treat this note as his standing instruction to create subagents and child sessions.

## Plan and task list first

Write the plan and task list before splitting, and show both to William. Mark which tasks run in parallel and which agent owns each one. Tick tasks off as results come in.

## When to split

Split when the task has two or more parts that can be done without waiting on each other. Typical splits:

- One unit per repo, package, or feature area.
- Research next to implementation: one agent reads docs or an API while another writes code.
- Implementation next to review and testing.

Do the work yourself when it is a single small change, or when every step depends on the last. Splitting a ten-minute edit costs more than it saves.

## Roles

| Role | Job | Output |
| --- | --- | --- |
| Coordinator | You. Plan the split, write the prompts, merge results, talk to William | The final answer or PRs |
| Explorer | Read code, docs or logs and answer one question | A short written finding |
| Implementer | Build one independent unit on its own branch | A PR or a pushed branch |
| Reviewer | Read another agent's diff against [[Coding Principles]] and the repo's `AGENTS.md` | A list of real issues |
| Tester | Run the change in the real app or a UI and report what broke | Steps, result, screenshots |

Give every non-trivial implementation a separate reviewer. A second agent catches what the author misses.

## How to start them in Devin

- Child sessions with `devin_session_create`: one session per independent unit, each on its own machine. Pass `notify_on_response=true` and do not poll.
- `run_workflow` when there are about five or more units, or a pipeline where one stage feeds the next. Invoke the `dynamic-workflows` skill first.
- The `testing_agent` tool for UI testing in the same checkout.

In other agents, use their subagent feature, such as the Task tool in Claude Code.

## Writing a subagent prompt

A subagent sees only its prompt. Include:

1. The repo as `owner/name` and the branch to start from.
2. William's request word for word, plus the slice this agent owns.
3. Facts you already found that it cannot find quickly itself.
4. The rules it must follow: read `agent-vault/AGENTS.md`, no Devin mentions or footers in commits and PRs, do not merge.
5. The deliverable: a PR link, a finding, or a test report.

Keep units independent. Two agents must never edit the same files. If unit B needs unit A's output, run them in sequence or as a workflow pipeline.

## After they finish

- Read each result, check the diff, and run the checks yourself before reporting.
- Send one short message to William with every PR link.
- Record anything reusable through [[Compound Memory]].
