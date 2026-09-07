# Test tasks

Three tasks for comparing a run with the skill against a run without it. Each lists what the output must satisfy. Most statements can be checked by script on the produced `.tex` (diff of the coordinate lines, grep for the style names); the rest need a look at the render.

| Task | Input | Main acceptance points |
|---|---|---|
| Results figure from a CSV | `fixtures/results.csv` | numbers unchanged to the decimal, rows sorted best first, ours blue, compiles, width verdict ok |
| Restyle three foreign figures | `fixtures/plain-bars.tex`, `plain-lines.tex`, `plain-scatter.tex` | all three load `plotfig.sty` and the `paper` style, same fonts and palette, every coordinate unchanged, ours in blue in each, default legend boxes replaced by direct labels or a legend row |
| Move a legend, nothing else | `fixtures/legend-figure.tex` | legend inside the plot at the upper left; data, colours, size, tick labels and the rest of the source unchanged; the reply lists what changed and what stayed |

Prompts and expectations are in `evals.json`, in the format of Anthropic's skill-creator (`skills/skill-creator` in [anthropics/skills](https://github.com/anthropics/skills)), which runs each prompt with and without the skill and grades the expectations.

The three `plain-*.tex` fixtures compile with a bare `pgfplots` install and look the way default pgfplots output looks: Computer Modern, boxed axes, legend boxes. `legend-figure.tex` is the skill's own `grouped-bars` example.

## Running by hand

1. Copy the fixture into a scratch directory, start a Claude Code session there with the skill installed, paste the prompt from `evals.json`, and keep the outputs.
2. Repeat in a session without the skill.
3. Check every expectation. For the data checks, `diff` the coordinate lines of the fixture against the output.

No results are recorded yet. Once the tasks have been run, the outputs and the pass/fail per expectation belong in `tests/results/<date>/`, together with the model used and a note on whether any output was edited by hand.
