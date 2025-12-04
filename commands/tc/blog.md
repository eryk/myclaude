---
allowed-tools: all
description: "Analyze codebase and generate technical blog posts about interesting aspects"
---

# /tc:blog - Analyze codebase and generate technical blog posts about interesting aspects

## Purpose

Deeply analyze the current codebase to identify interesting technical angles, provide options for the user to choose from, and generate comprehensive technical blog posts (5000+ words) with mermaid diagrams about the selected topic.

## Usage

```
/tc:blog [language]
```

## Arguments

- `language` - Blog post language (default: Chinese). Supported: Chinese, English, Japanese, Korean, Spanish, French, German

## Execution

Use @tech-philosophy-writer as the primary blog writer, output the blog post in ./blog/ directory.

### Analysis Process

**Phase 1: Comprehensive Codebase Analysis**

1. **Initial Codebase Survey**
   - Scan project structure and identify main components
   - Analyze programming languages, frameworks, and technologies used
   - Understand the project's domain and business purpose
   - Identify key architectural patterns and design decisions

2. **Deep Technical Analysis**
   - **Architecture & Design Patterns**: Identify unique architectural decisions, design patterns implementation, microservices design, etc.
   - **Algorithms & Data Structures**: Find interesting algorithms, optimization techniques, custom data structures
   - **Product & Business Logic**: Discover clever product features, business rule implementations, user experience considerations
   - **Performance & Scalability**: Analyze performance optimizations, caching strategies, scalability solutions
   - **Security & Reliability**: Examine security implementations, error handling, resilience patterns
   - **Developer Experience**: Study build systems, testing strategies, development workflows
   - **Innovation & Technology**: Identify cutting-edge technology usage, novel solutions to common problems

3. **Interest Discovery**
   - Look for non-obvious technical solutions
   - Identify creative problem-solving approaches
   - Find examples of excellent engineering practices
   - Discover trade-offs and engineering decisions
   - Locate performance bottlenecks and their solutions
   - Examine error handling and edge case management

**Phase 2: Topic Selection**

Present 5-8 interesting angles to the user with descriptions:

```
Found the following interesting technical angles in your codebase:

1. 🏗️ **Elegant Microservices Architecture**
   - Custom service discovery mechanism with health checking
   - Interesting inter-service communication patterns
   - Graceful degradation strategies

2. ⚡ **High-Performance Data Processing Pipeline**
   - Stream processing with custom buffer management
   - Memory-efficient algorithms for large datasets
   - Clever caching layers and optimization techniques

3. 🔐 **Zero-Trust Security Implementation**
   - Multi-layer authentication and authorization
   - End-to-end encryption with key rotation
   - Runtime security monitoring and threat detection

4. 🧠 **Machine Learning Model Deployment**
   - Real-time inference pipeline architecture
   - Model versioning and A/B testing framework
   - Performance monitoring and drift detection

5. 🎨 **User Experience Innovation**
   - Progressive enhancement strategies
   - Accessibility-first design implementation
   - Performance-optimized frontend architecture

Please choose a number (1-5) for the blog post topic, or type 'more' for additional options.
```

**Phase 3: Blog Generation**

Once user selects a topic:

1. **Deep Dive Analysis**
   - Thoroughly examine the chosen aspect
   - Understand the technical challenges and solutions
   - Identify the engineering principles and trade-offs
   - Research relevant industry context and best practices

2. **Content Structure Planning**
   - Introduction: Problem context and why it matters
   - Technical deep dive: Implementation details and decisions
   - Architecture analysis: Design patterns and principles
   - Code examples: Real implementation snippets
   - Visual diagrams: Mermaid charts for system architecture
   - Lessons learned: Key takeaways and insights
   - Industry relevance: How it applies to broader ecosystem
   - Future considerations: Potential improvements and evolution

3. **Blog Post Generation** (Using @technical-documentation-writer)
   - **Length**: Minimum 5000 words, aim for 6000-8000 words
   - **Language**: Use specified language (default Chinese)
   - **Technical Depth**: Balance accessibility with technical accuracy
   - **Code Examples**: Include relevant, well-commented code snippets
   - **Mermaid Diagrams**: At least 2-3 diagrams showing architecture, flow, or relationships
   - **Structure**: Professional blog format with clear sections and headings

4. **Content Requirements**
   - **Introduction** (800-1000 words): Context, problem statement, why this matters
   - **Technical Background** (1000-1500 words): Foundational concepts and industry context
   - **Implementation Deep Dive** (2000-2500 words): Detailed technical analysis with code
   - **Architecture & Design** (1000-1500 words): System design and patterns with mermaid diagrams
   - **Lessons & Insights** (500-800 words): Key takeaways and engineering wisdom
   - **Future Directions** (300-500 words): Potential improvements and industry trends
   - **Conclusion** (200-400 words): Summary and call to action

5. **Quality Standards**
   - All code examples tested and functional
   - Mermaid diagrams properly formatted and meaningful
   - Technical accuracy verified by domain experts
   - Language fluency appropriate for target audience
   - SEO-friendly headings and structure
   - Engaging narrative that tells a story
   - Practical insights that readers can apply

### Output Deliverables

1. **Analysis Report**: Summary of interesting technical aspects found
2. **Topic Options**: 5-8 curated blog post topics with descriptions
3. **Technical Blog Post**: 5000+ word comprehensive article including:
   - Professional formatting with clear headings
   - Multiple mermaid diagrams
   - Well-commented code examples
   - Technical insights and lessons learned
   - Industry context and best practices
   - Future considerations and recommendations

### Blog Post Format Template

```
# [Compelling Title in Target Language]

## 引言 / Introduction
[Context and problem statement]

## 技术背景 / Technical Background
[Industry context and foundational concepts]

## 深入实现 / Implementation Deep Dive
[Detailed technical analysis with code examples]

```mermaid
[Architecture diagram]
```

## 架构设计 / Architecture & Design

[System design patterns and principles]

```mermaid
[Flow or relationship diagram]
```

## 经验与洞察 / Lessons & Insights

[Key takeaways and engineering wisdom]

## 未来方向 / Future Directions

[Potential improvements and trends]

## 结论 / Conclusion

[Summary and actionable insights]

```

### Success Criteria

- ✅ Comprehensive codebase analysis completed
- ✅ Multiple interesting technical angles identified
- ✅ User successfully selects preferred topic
- ✅ Blog post exceeds 5000 words
- ✅ Contains 2+ meaningful mermaid diagrams
- ✅ Includes practical code examples
- ✅ Written in specified target language
- ✅ Professional quality suitable for publication
- ✅ Technical accuracy verified by domain experts
- ✅ Engaging narrative with clear value proposition
