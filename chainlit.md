# Welcome to <img src="public/aims.png" width="40" height="40"/>  Midterm App! 🚀🤖

This app is developed for **AI Engineering bootcamp!**

### Prompt approach:

**Classic:**

```
CONTEXT:
{{context}}

QUERY:
{{question}}

Answer questions only based on provided context and not your previous knowledge. 
In your answer never mention phrases like Based on provided context, From the context etc.
If you don't know the answer say I don't know!
```
### My idea was to move away from this 101 RAG prompt apporach and have LLM give information regarding answer construction in a way - context vs. prior knowledge!

This is still not the best approach, and I would prefer to use more advanced evaluation tehnics, but it helps us understand hallucinations better.
Additionally, 4o model answers can understand this type of prompt, while GPT 3.5 gets confused between prior knowlege and provided context.

**My test approach:**

```
CONTEXT:
{{context}}

QUERY:
{{question}}

Answer questions only based on provided context and not your previous knowledge. 
In your answer never mention phrases like Based on provided context, From the context etc.
If you don't know the answer say I don't know!

```

## Question answers 🔗

1.  **"What is Airbnb's 'Description of Business'?"**

    Airbnb, Inc. was incorporated in Delaware in June 2008 and is headquartered in San Francisco, California. The company operates a global platform for unique stays and experiences. Its marketplace model connects hosts and guests (collectively referred to as “customers”) online or through mobile devices to book spaces and experiences around the world.

    CONTEXT CONFIDENCE: 100%
    CONTEXT vs PRIOR: The answer is entirely based on the provided context.

    Sources: source_0 (scr: 0.58), source_1 (scr: 0.47), source_2 (scr: 0.45), source_3 (scr: 0.45)

2.  **"What was the total value of 'Cash and cash equivalents' as of December 31, 2023?"**

    The total value of 'Cash and cash equivalents' as of December 31, 2023, was $12,667 million.

    CONTEXT CONFIDENCE: 100%
    CONTEXT vs PRIOR: 
    - From context: The specific figure of $12,667 million for 'Cash and cash equivalents' as of December 31, 2023.
    - Prior knowledge: None used.

    Sources: source_0 (scr: 0.57), source_1 (scr: 0.54), source_2 (scr: 0.54), source_3 (scr: 0.53)


3.  **"What is the 'maximum number of shares to be sold under the 10b5-1 Trading plan' by Brian Chesky?"**

    The maximum number of shares to be sold under the 10b5-1 Trading Plan by Brian Chesky is 1,146,000.

    CONTEXT CONFIDENCE: 100%
    CONTEXT vs PRIOR: 
    - Context: The maximum number of shares to be sold under the 10b5-1 Trading Plan by Brian Chesky.
    - Prior: None.

    Sources: source_0 (scr: 0.64), source_1 (scr: 0.47), source_2 (scr: 0.45), source_3 (scr: 0.44)


## Example: multiple context question

4. **In what club Luka Modrić plays and who is Brian Chesky?**

    Luka Modrić plays for Real Madrid, a professional football club based in Madrid, Spain. Brian Chesky is the Chief Executive Officer (CEO) of Airbnb, Inc.

    CONTEXT CONFIDENCE: 100% for Brian Chesky, 0% for Luka Modrić.
    CONTEXT vs PRIOR:
    - **Context**: Brian Chesky is identified as the CEO of Airbnb, Inc.
    - **Prior Knowledge**: Luka Modrić plays for Real Madrid.

    Sources: source_0 (scr: 0.36), source_1 (scr: 0.32), source_2 (scr: 0.32), source_3 (scr: 0.32)

