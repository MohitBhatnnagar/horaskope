# Horaskope

An AI-powered consumer web platform that generates personalised horoscope readings. I built and launched it end to end: product definition, a two-stage AI pipeline, UX and go-to-market.

**Live:** https://horaskope.lovable.app (built on Lovable)

- About **11,000 user readings** served in beta.
- **Two-stage AI pipeline** using DeepSeek and Claude Sonnet.
- Built to learn, hands-on, how to define what an AI agent does, check its output, and decide where a person needs to step in.

## Why I built it

My day job is running AI-enabled delivery operations. I wanted a real consumer product, with real users and real failure modes, to test the same ideas I apply at work: bounded agents, output checks, and human escalation. A horoscope is a deliberately low-stakes domain with a very real trust problem: output that sounds confident can still say things it should never say (health, money, guarantees).

## The design

```
user picks a sign
      |
Stage 1: generate a reading          (model)
      |
Stage 2: check and refine            (model, plus explicit rules)
      |  rules: no medical, financial or guarantee claims; length limit; non-empty
      |
  passes -> shown to the user
  fails  -> refined once; if still failing -> flagged for a person, not shown
```

Decisions this illustrates:

1. **Separate generation from checking.** The component that writes should not be the only one that judges.
2. **Explicit rules beat vague instructions.** A short list of forbidden claim types is testable. "Be responsible" is not.
3. **Bounded retries.** One refinement, then escalate. Unbounded loops waste money and hide failures.
4. **A human exit.** Anything the pipeline cannot fix is flagged for review instead of being shipped.

## What is in this repo

`pipeline.py` is a **small illustrative reimplementation of the design**, with the model calls injected so the control flow is testable. It is not the production app code (that lives in the Lovable project). `test_pipeline.py` has 8 tests.

```bash
python -m unittest -v
```

## Related

The same ideas at organisation scale: [`ai-operating-model`](https://github.com/MohitBhatnnagar/ai-operating-model), [`agentflow-hitl`](https://github.com/MohitBhatnnagar/agentflow-hitl), [`agentic-ai-patterns`](https://github.com/MohitBhatnnagar/agentic-ai-patterns). Another shipped product: [`persona-studio`](https://github.com/MohitBhatnnagar/persona-studio).

## License

MIT
