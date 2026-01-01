# AI & Machine Learning Skills for Claude Code

Skills for machine learning, AI integration, and data science workflows.

---

## LLM Integration Skill

```markdown
---
name: llm-integration
description: Integrate LLMs into applications
---

# LLM Integration

## When to Use
- Adding AI features to apps
- Building chatbots
- Text generation/analysis
- Embedding-based search

## Providers
| Provider | Models | Best For |
|----------|--------|----------|
| **Anthropic** | Claude | Complex reasoning |
| **OpenAI** | GPT-4, GPT-3.5 | General purpose |
| **Cohere** | Command | Enterprise |
| **Google** | Gemini | Multimodal |
| **Mistral** | Mistral, Mixtral | Open weights |

## Integration Pattern
async function callLLM(prompt: string) {
  const response = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    messages: [{ role: 'user', content: prompt }]
  });
  return response.content[0].text;
}

## Best Practices
- Use streaming for long responses
- Implement retry with backoff
- Cache common queries
- Monitor token usage
- Handle rate limits gracefully
```

---

## Prompt Engineering Skill

```markdown
---
name: prompt-engineering
description: Craft effective prompts
---

# Prompt Engineering

## Techniques
| Technique | Use Case |
|-----------|----------|
| **Few-shot** | Examples guide output |
| **Chain-of-thought** | Complex reasoning |
| **Role-playing** | Specific perspectives |
| **Structured output** | JSON/XML responses |

## Best Practices
- Be specific and clear
- Provide context
- Use delimiters for sections
- Ask for reasoning before answer
- Iterate and test

## Example: Structured Output
Analyze the following text and respond in JSON:
{
  "sentiment": "positive|negative|neutral",
  "topics": ["list", "of", "topics"],
  "summary": "one sentence summary"
}

Text: [user input]
```

---

## RAG (Retrieval-Augmented Generation) Skill

```markdown
---
name: rag-implementation
description: Build RAG systems
---

# RAG Implementation

## Architecture
1. **Ingest** - Process and chunk documents
2. **Embed** - Convert to vectors
3. **Store** - Vector database
4. **Retrieve** - Semantic search
5. **Generate** - LLM with context

## Chunking Strategies
- Fixed size (512-1024 tokens)
- Semantic (paragraph/section)
- Recursive (with overlap)
- Document-aware (headers, code blocks)

## Vector Databases
| Database | Best For |
|----------|----------|
| **Pinecone** | Managed, scalable |
| **Weaviate** | Hybrid search |
| **Chroma** | Local development |
| **pgvector** | PostgreSQL integration |
| **Qdrant** | Performance |

## Example Flow
// 1. Embed query
const queryEmbedding = await embed(query);

// 2. Search vectors
const docs = await vectorDB.search(queryEmbedding, k=5);

// 3. Generate with context
const response = await llm.generate({
  prompt: `Context: ${docs.join('\n')}\n\nQuestion: ${query}`
});
```

---

## Model Fine-tuning Skill

```markdown
---
name: model-fine-tuning
description: Fine-tune models for specific tasks
---

# Model Fine-tuning

## When to Fine-tune
- Specific domain knowledge
- Consistent output format
- Improved accuracy on task
- Reduced prompt length

## Approaches
| Method | Data Needed | Cost |
|--------|-------------|------|
| **Prompt tuning** | ~10 examples | Low |
| **LoRA** | ~100 examples | Medium |
| **Full fine-tune** | ~1000+ examples | High |

## Data Preparation
- Clean, high-quality examples
- Diverse coverage
- Consistent format
- Train/validation split

## Tools
- Hugging Face Transformers
- OpenAI fine-tuning API
- Anthropic fine-tuning (enterprise)
- Axolotl (open source)
```

---

## Computer Vision Skill

```markdown
---
name: computer-vision
description: Image analysis and processing
---

# Computer Vision

## Tasks
- Image classification
- Object detection
- Segmentation
- OCR
- Image generation

## Tools & Libraries
| Tool | Use Case |
|------|----------|
| **OpenCV** | Image processing |
| **YOLO** | Object detection |
| **Tesseract** | OCR |
| **CLIP** | Image-text matching |
| **Stable Diffusion** | Generation |

## Multimodal LLMs
- Claude (vision-capable)
- GPT-4V
- Gemini Pro Vision

## Example: Claude Vision
const response = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  messages: [{
    role: 'user',
    content: [
      { type: 'image', source: { type: 'base64', data: imageBase64 } },
      { type: 'text', text: 'What is in this image?' }
    ]
  }]
});
```

---

## ML Pipeline Skill

```markdown
---
name: ml-pipeline
description: Build production ML pipelines
---

# ML Pipeline

## Components
1. **Data Ingestion** - Collect and validate
2. **Preprocessing** - Clean, transform
3. **Feature Engineering** - Create features
4. **Training** - Model training
5. **Evaluation** - Metrics, validation
6. **Deployment** - Serve predictions
7. **Monitoring** - Drift detection

## Tools
| Stage | Tools |
|-------|-------|
| Orchestration | Airflow, Prefect, Dagster |
| Experiment Tracking | MLflow, W&B, Neptune |
| Feature Store | Feast, Tecton |
| Serving | BentoML, Ray Serve, TorchServe |
| Monitoring | Evidently, WhyLabs |

## MLOps Best Practices
- Version data and models
- Automated testing
- CI/CD for models
- A/B testing in production
- Monitor for drift
```

---

## Data Processing Skill

```markdown
---
name: data-processing
description: Process and analyze data
---

# Data Processing

## Python Stack
| Library | Purpose |
|---------|---------|
| **pandas** | DataFrames |
| **polars** | Fast DataFrames |
| **numpy** | Numerical computing |
| **dask** | Parallel computing |
| **pyspark** | Big data |

## Common Operations
- Loading data (CSV, JSON, Parquet)
- Cleaning (missing values, duplicates)
- Transformation (groupby, pivot)
- Aggregation (mean, sum, count)
- Joins and merges

## Example: Pandas
import pandas as pd

# Load and clean
df = pd.read_csv('data.csv')
df = df.dropna(subset=['important_col'])
df['date'] = pd.to_datetime(df['date'])

# Aggregate
result = df.groupby('category').agg({
    'value': ['mean', 'sum', 'count']
}).reset_index()
```

---

## AI Safety Skill

```markdown
---
name: ai-safety
description: Implement AI safety measures
---

# AI Safety

## Considerations
- Input validation
- Output filtering
- Rate limiting
- Content moderation
- Bias mitigation

## Guardrails
- Prompt injection detection
- PII detection and redaction
- Toxicity filtering
- Hallucination detection

## Implementation
// Example: Input validation
const sanitizedInput = validateInput(userInput);
if (containsPromptInjection(sanitizedInput)) {
  throw new Error('Invalid input detected');
}

// Output filtering
const response = await llm.generate(sanitizedInput);
const safeResponse = filterOutput(response);
```

---

## AI/ML Commands

### train.md
```markdown
Train ML model:
1. Load and validate dataset
2. Preprocess data
3. Split train/test
4. Train model
5. Evaluate metrics
6. Save model artifacts
```

### evaluate.md
```markdown
Evaluate model performance:
1. Load test dataset
2. Run predictions
3. Calculate metrics
4. Generate confusion matrix
5. Create evaluation report
```

---

## MCP Servers for AI/ML

| Server | Purpose |
|--------|---------|
| **HuggingFace MCP** | Model hub access |
| **MLflow MCP** | Experiment tracking |
| **OpenAI MCP** | GPT integration |
| **Replicate MCP** | Model hosting |

---

## Resources

- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
- [LangChain](https://langchain.com/)
- [LlamaIndex](https://www.llamaindex.ai/)
- [Hugging Face Course](https://huggingface.co/course)
- [MLOps Guide](https://ml-ops.org/)
- [Papers With Code](https://paperswithcode.com/)
