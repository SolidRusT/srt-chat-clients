# Prompt Engineering Overview 🛠️

Original post: [Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)

Explore the art and science of Prompt Engineering, a pivotal technique in optimizing the performance of Large Language Models (LLMs) without altering their weights. This README delves into the strategies, applications, and nuances of prompt engineering, drawing insights from Lilian Weng's detailed exploration.

## Introduction to Prompt Engineering 🌟

Prompt Engineering, or In-Context Prompting, is the empirical science of crafting prompts to guide LLMs towards desired outcomes. It encompasses a range of methods, from zero-shot and few-shot learning to more advanced techniques like Chain-of-Thought (CoT) prompting, each requiring meticulous experimentation to master.

## Basic Prompting Techniques 📚

### Zero-Shot Learning
Directly asking the model to perform a task without prior examples, relying solely on its pre-trained knowledge.

### Few-Shot Learning
Introducing a set of high-quality examples to the model, enhancing its understanding of the task and improving performance.

## Advanced Prompting Strategies 🚀

### Instruction Prompting
Simplifying communication with the model by directly providing detailed task instructions, reducing token usage and enhancing model alignment with human intentions.

### Self-Consistency Sampling
Generating multiple outputs and selecting the best one based on criteria like majority vote or task-specific validation methods.

### Chain-of-Thought (CoT) Prompting
Encouraging the model to generate a sequence of reasoning steps, leading to more accurate answers for complex reasoning tasks.

## Tips for Effective Prompt Engineering ✨

- **Example Selection**: Utilize techniques like $k$-NN clustering and graph-based approaches to choose diverse and representative examples.
- **Example Ordering**: Maintain diversity and relevance in example selection to mitigate biases and improve model performance.
- **Complexity and Consistency**: Opt for prompts that encourage complex reasoning and use consistency checks to refine outputs.

## Augmented Language Models 🧠

Exploring models augmented with external tools and capabilities, such as retrieval systems for accessing up-to-date or domain-specific information, and programming language generation for computational tasks.

## Practical Applications and Case Studies 🏆

- **Retrieval-Augmented Generation**: Enhancing LLMs with the ability to retrieve and incorporate external information into their responses.
- **Programming with LLMs**: Generating code snippets to solve problems, leveraging the model's programming knowledge.
- **External API Integration**: Augmenting LLMs with the ability to make external API calls, expanding their utility and application scope.

## Conclusion and Future Directions 🌈

Prompt Engineering stands at the forefront of LLM research and application, offering a versatile toolkit for enhancing model performance across a wide range of tasks. As the field evolves, so too will the techniques and strategies for effective prompt design, promising exciting advancements in AI and machine learning.

---

### Citation

> Weng, Lilian. (Mar 2023). Prompt Engineering. Lil’Log.
> https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/.

### Useful Resources

- [Calibrate Before Use: Improving Few-shot Performance of Language Models](https://arxiv.org/abs/2102.09690)
- [What Makes Good In-Context Examples for GPT-3?](https://arxiv.org/abs/2101.06804)
- [Chain of thought prompting elicits reasoning in large language models](https://arxiv.org/abs/2201.11903)

### Announcement

Link Reader evolved: discover Browser Pro! Try it for unmatched versatility: [https://chat.openai.com/g/g-BlafpMvzd](https://bit.ly/3OCGngz)
